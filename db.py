import binascii
try:
	import ipaddress
except ImportError:
	import ipaddr as ipaddress

from sqlalchemy import create_engine, Column, Integer, Boolean, String, Datetime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref, sessionmaker

import sqlalchemy.ext.declarative
Base = sqlalchemy.ext.declarative.declarative_base()

def db_init(*args, **kwargs):
	engine = create_engine(*args, **kwargs)
	Base.metadata.create_all(engine)
	return sessionmaker(bind=engine)()

class Role(Base):
	__tablename__ = "role"
	id = Column(Integer, primary_key=True)
	email = Column(String(100), unique=True)
	name = Column(String(50), unique=True)
	create_date = Column(Datetime, nullable=False)
	
	password = relationship("Password", cascade="all,delete-orphan", backref="role")

class Password(Base):
	__tablename__ = "password"
	id = Column(Integer, primary_key=True)
	role_id = Column(Integer, ForeignKey("Role.id"))
	key = Column(String(12), nullable=False)
	create_date = Column(Datetime, nullable=False)
	status = Column(Integer, nullable=False) # 0:off, 1:on, 2:out

class RoleLink(Base):
	__tablename__ = "role_link"
	__table_args__ = (UniqueConstraint("up_role_id","up_role_pass","down_role_id","down_role_pass"),)
	up_role_id = Column(Integer, ForeignKey("Role.id"))
	up_role_pass = Column(Integer, ForeignKey("Password.key"))
	down_role_id = Column(Integer, ForeignKey("Role.id"))
	down_role_pass = Column(Integer, ForeignKey("Password.key"))

class RoleFollow(Base):
	__tablename__ = "role_follow"
	__table_args__ = (UniqueConstraint("up_role_id","up_role_pass","down_role_id","down_role_pass"),)
	up_role_id = Column(Integer, ForeignKey("Role.id"))
	up_role_pass = Column(Integer, ForeignKey("Password.key"))
	down_role_id = Column(Integer, ForeignKey("Role.id"))
	down_role_pass = Column(Integer, ForeignKey("Password.key"))

class RoleBlock(Base):
	__tablename__ = "role_block"
	__table_args__ = (UniqueConstraint("up_role_id","up_role_pass","down_role_id","block_role_pass"),)
	up_role_id = Column(Integer, ForeignKey("Role.id"))
	up_role_pass = Column(Integer, ForeignKey("Password.key"))
	block_role_id = Column(Integer, ForeignKey("Role.id"))

class Group(Base):
	__tablename__ = "group"
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)
	creater = Column(Integer, ForeignKey("Role.id"))
	create_date = Column(Datetime, nullable=False)

class GroupLink(Base):
	__tablename__ = "group_link"
	__table_args__ = (UniqueConstraint("up_group_id", "down_group_id"),)
	up_group_id = Column(Integer, ForeignKey("Group.id"))
	down_group_id = Column(Integer, ForeignKey("Group.id"))

class GroupManager(Base):
	__tablename__ = "group_manager"
	__table_args__ = (UniqueConstraint("group_id", "manager_id", "manager_pass"),)
	group_id = Column(Integer, ForeignKey("Group.id"))
	manager_id = Coumn(Integer, ForeignKey("Role.id"))
	manager_pass = Column(Integer, ForeignKey("Password.key"))

class GroupJoiner(Base):
	__tablename__ = "group_joiner"
	__table_args__ = (UniqueConstraint("group_id", "joiner_id", "joiner_pass"),)
	group_id = Column(Integer, ForeignKey("Group.id"))
	joiner_id = Coumn(Integer, ForeignKey("Role.id"))
	joiner_pass = Column(Integer, ForeignKey("Password.key"))

class Permission(Base):
	'''
	bootstrap network has both mac or network_user_name to be null, and that 
	row must be the only row in this table.
	'''
	__tablename__ = "permission"
	__table_args__ = (UniqueConstraint("network_id","device_id","user_id"),)
	id = Column(Integer, primary_key=True)
	network_id = Column(Integer, ForeignKey("network.id"), nullable=False)
	device_id = Column(Integer, ForeignKey("device.id")) # None means ANY
	user_id = Column(Integer, ForeignKey("user.id")) # None means ANY
	
	def is_bootstrap(self):
		return self.device_id == None and self.user_id == None

class DatapathContainer(Base):
	__tablename__ = "datapath_container"
	id = Column(Integer, primary_key=True)
	ip_address = Column(String, unique=True, nullable=False) # IPv4 or IPv6 address of the openflow switch housing
	# binascii.b2a_hex(ipaddress.IPNetwork(ip_address).packed).
	# This column was introduced to reduce the cost of IP address matching.
	# The meaning of content itself is the same with ip_address, so theoretically, this column is not required.
	ip_address_hex = Column(String, unique=True, nullable=False)
	name = Column(String) # hostname
	type = Column(String) # this setting determines how to submit custom commands that is out of scope of openflow.
	
	datapaths = relationship("Datapath", cascade="all,delete-orphan")
	vlan_static = relationship("VlanStatic", cascade="all,delete-orphan", backref="container")
	
	@staticmethod
	def find_by_ip_address(session, ip_address):
		candidates = []
		candidates.append(binascii.b2a_hex(ipaddress.IPNetwork(ip_address).packed))
		if ip_address.find(".") > 0:
			if ip_address.startswith("::ffff:"):
				candidates.append(binascii.b2a_hex(ipaddress.IPNetwork(ip_address[len("::ffff:"):]).packed))
			elif ip_address.startswith("::ffff:0:"):
				candidates.append(binascii.b2a_hex(ipaddress.IPNetwork(ip_address[len("::ffff:0:"):]).packed))
			
			if ip_address.find(":") < 0:
				candidates.append(binascii.b2a_hex(ipaddress.IPNetwork("::ffff:"+ip_address).packed))
				candidates.append(binascii.b2a_hex(ipaddress.IPNetwork("::ffff:0:"+ip_address).packed))
		
		return session.query(DatapathContainer).filter(
			DatapathContainer.ip_address_hex.in_(candidates)).first()

class Datapath(Base):
	__tablename__ = "datapath"
	id = Column(Integer, primary_key=True)
	datapath_hex = Column(String(16)) # openflow switch datapath_id in hex. Note this is nullable, meaning Datapath may be specified only by datapath_container
	uplink = Column(String, nullable=False) # uplink port name or number on the datapath.
	container_id = Column(Integer, ForeignKey("datapath_container.id")) # Note this is nullable, cascading does not happen on NULL

class VlanStatic(Base):
	'''
	if you want to map a specific vlan to some network, then create an entry in this table.
	'''
	__tablename__ = "vlan_static"
	__table_args__ = (UniqueConstraint("datapath_hex","container_id","network_id"), UniqueConstraint("datapath_hex","container_id","vlan"))
	id = Column(Integer, primary_key=True)
	datapath_hex = Column(String(16))
	container_id = Column(Integer, ForeignKey("datapath_container.id"))
	network_id = Column(Integer, ForeignKey("network.id"), nullable=False)
	vlan = Column(Integer, nullable=False)

class Config(Base):
	__tablename__ = "config"
	name = Column(String, primary_key=True)
	value = Column(String)


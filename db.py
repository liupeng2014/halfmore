import binascii
try:
	import ipaddress
except ImportError:
	import ipaddr as ipaddress

from sqlalchemy import create_engine, func, Column, Integer, Boolean, String, Datetime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref, sessionmaker

import sqlalchemy.ext.declarative
Base = sqlalchemy.ext.declarative.declarative_base()

def db_init(*args, **kwargs):
	engine = create_engine(*args, **kwargs)
	Base.metadata.create_all(engine)
	return sessionmaker(bind=engine)()

class Role(Base):
	__tablename__ = "role"
	__table_args__ = (UniqueConstraint("name","email"),)
	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False, unique=True)
	email = Column(String(100), nullable=False)
	create_date = Column(Datetime, default=func.now())
	
	password = relationship("Password", cascade="all,delete-orphan")

class Password(Base):
	__tablename__ = "password"
	__table_args__ = (UniqueConstraint("role_id","key",)
	role_id = Column(Integer, ForeignKey("Role.id"))
	key = Column(String(20), nullable=False)
	create_date = Column(Datetime, default=func.now())
	status = Column(Integer, nullable=False) # login status. 0:off, 1:on, 2:out

class Profile(Base):
	__tablename__ = "profile"
	__table_args__ = (UniqueConstraint("role_id","role_pass"),)
	role_id = Column(Integer, ForeignKey("Role.id"))
	role_pass = Column(Integer, ForeignKey("Password.key"))
	gender = Column(Boolean)
	locate = Column(String(100))

# RoleLink is for one person.
class RoleLink(Base):
	__tablename__ = "role_link"
	__table_args__ = (UniqueConstraint("up_role_id","up_role_pass","down_role_id","down_role_pass"),)
	up_role_id = Column(Integer, ForeignKey("Role.id"))
	up_role_pass = Column(Integer, ForeignKey("Password.key"))
	down_role_id = Column(Integer, ForeignKey("Role.id"))
	down_role_pass = Column(Integer, ForeignKey("Password.key"))

# RoleFollow if for two persons.
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
	open_status = Column(Integer, nullable=False) # 0:all, 1:can search, 2:private
	creater_id = Column(Integer, ForeignKey("Role.id"))
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

class Input(Base):
	__tablename__ = "input"
	id = Column(Integer, primary_key=True)
	# 0:one action, 1:long text, 2:short text, 3: comment, 4:pic, 5:video, 6:sound, 7:plan
	type = Column(Integer, nullable=False)
	create_id = Column(Integer, ForeignKey("Role.id"))
	create_pass = Column(Integer, ForeignKey("Password.key"))
	create_date = Column(Datetime, nullable=False)
	group_id = Column(Integer, ForeignKey("Group.id"))

class message(Base):
	__tablename__ = "message"
	id = Column(Integer, primary_key=True)


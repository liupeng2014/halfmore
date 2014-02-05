import binascii

from sqlalchemy import create_engine, func, Column, Integer, Boolean, String, DateTime, ForeignKey, UniqueConstraint
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
	create_date = Column(DateTime, default=func.now())
	
	password = relationship("Password", cascade="all,delete-orphan", backref="role")

class Password(Base):
	__tablename__ = "password"
	__table_args__ = (UniqueConstraint("rid","key"),)
	id = Column(Integer, primary_key=True)
	rid = Column(Integer, ForeignKey("role.id"))
	key = Column(String(20), nullable=False)
	create_date = Column(DateTime, default=func.now())
	status = Column(Integer, nullable=False, default=0) # login status. 0:off, 1:on, 2:out
	open_flag = Column(Integer, nullable=False, default=0) # 0:all, 1:secret, 2:friend, 3:group

class Profile(Base):
	__tablename__ = "profile"
	id = Column(Integer, primary_key=True)
	rp = Column(Integer, ForeignKey("password.id"))
	gender = Column(Integer)
	locate = Column(String(100))

# RoleLink is for one person.
class RoleLink(Base):
	__tablename__ = "role_link"
	__table_args__ = (UniqueConstraint("up_rp", "dn_rp"),)
	id = Column(Integer, primary_key=True)
	up_rp = Column(Integer, ForeignKey("password.id"))
	dn_rp = Column(Integer, ForeignKey("password.id"))

# RoleFollow if for two persons.
class RoleFollow(Base):
	__tablename__ = "role_follow"
	__table_args__ = (UniqueConstraint("center_role", "follow_rp"),)
	id = Column(Integer, primary_key=True)
	center_role = Column(Integer, ForeignKey("role.id"))
	follow_rp = Column(Integer, ForeignKey("password.id"))

class RoleBlock(Base):
	__tablename__ = "role_block"
	__table_args__ = (UniqueConstraint("rp", "block_role"),)
	id = Column(Integer, primary_key=True)
	rp = Column(Integer, ForeignKey("password.id"))
	block_role = Column(Integer, ForeignKey("role.id"))

class Group(Base):
	__tablename__ = "group"
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)
	open_status = Column(Integer, nullable=False) # 0:all, 1:can search, 2:private
	creater_id = Column(Integer, ForeignKey("role.id"))
	create_date = Column(DateTime, default=func.now())

class GroupLink(Base):
	__tablename__ = "group_link"
	__table_args__ = (UniqueConstraint("up_group_id", "down_group_id"),)
	id = Column(Integer, primary_key=True)
	up_group_id = Column(Integer, ForeignKey("group.id"))
	down_group_id = Column(Integer, ForeignKey("group.id"))

class GroupManager(Base):
	__tablename__ = "group_manager"
	__table_args__ = (UniqueConstraint("group_id", "manager_id", "manager_pass"),)
	id = Column(Integer, primary_key=True)
	group_id = Column(Integer, ForeignKey("group.id"))
	manager_id = Column(Integer, ForeignKey("role.id"))
	manager_pass = Column(Integer, ForeignKey("password.key"))

class GroupJoiner(Base):
	__tablename__ = "group_joiner"
	__table_args__ = (UniqueConstraint("group_id", "joiner_id", "joiner_pass"),)
	id = Column(Integer, primary_key=True)
	group_id = Column(Integer, ForeignKey("group.id"))
	joiner_id = Column(Integer, ForeignKey("role.id"))
	joiner_pass = Column(Integer, ForeignKey("password.key"))

class Input(Base):
	__tablename__ = "input"
	id = Column(Integer, primary_key=True)
	# 0:one action, 1:long text, 2:short text, 3: comment, 4:pic, 5:video, 6:sound, 7:plan
	type = Column(Integer, nullable=False)
	create_id = Column(Integer, ForeignKey("role.id"))
	create_pass = Column(Integer, ForeignKey("password.key"))
	create_date = Column(DateTime, default=func.now())
	group_id = Column(Integer, ForeignKey("group.id"))

class Message(Base):
	__tablename__ = "message"
	id = Column(Integer, primary_key=True)
	text = Column(String(100))


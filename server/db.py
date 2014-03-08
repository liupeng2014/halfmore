# coding: utf-8

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
	__tablename__ = 'role'
	__table_args__ = (UniqueConstraint('name','email'),)
	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False, unique=True)
	create_time = Column(DateTime, default=func.now())
	modify_time = Column(DateTime, default=func.now())
	
	password = relationship('Password', cascade='all,delete-orphan', backref='role')

class RolePassword(Base):
	__tablename__ = 'role_password'
	__table_args__ = (UniqueConstraint('rid','key'),)
	id = Column(Integer, primary_key=True)
	rid = Column(Integer, ForeignKey('role.id'))
	key = Column(String(20), nullable=False)
	create_time = Column(DateTime, default=func.now())
	modify_time = Column(DateTime, default=func.now())

	login = relationship('Login', cascade='all,delete-orphan')
	profile = relationship('Login', uselist=False, cascade='all,delete-orphan')

class Login(Base):
	__tablename__ = 'login'
	id = Column(Integer, primary_key=True)
	rp = Column(Integer, ForeignKey('role_password.id'))
	status = Column(Integer, nullable=False, default=0) # login status. 0:off, 1:on, 2:out
	update_time = Column(DateTime, default=func.now())	

class Profile(Base):
	__tablename__ = 'profile'
	id = Column(Integer, primary_key=True)
	rp = Column(Integer, ForeignKey('role_password.id'))
	email = Column(String(100), nullable=False)
	open_flag = Column(Integer, nullable=False, default=0) # 0:all, 1:secret, 2:friend, 3:group
	gender = Column(Integer)
	location = Column(String(100))
	update_time = Column(DateTime, default=func.now())

# RoleLink is for one person.
# rp is center, and roles are linked to rp.
class RoleLink(Base):
	__tablename__ = 'role_link'
	__table_args__ = (UniqueConstraint('rp', 'role'),)
	id = Column(Integer, primary_key=True)
	rp = Column(Integer, ForeignKey('role_password.id'))
	role = Column(Integer, ForeignKey('role.id'))

# RoleFollow if for two persons.
# role is up, and rp follows role.
class RoleFollow(Base):
	__tablename__ = 'role_follow'
	__table_args__ = (UniqueConstraint('role', 'rp'),)
	id = Column(Integer, primary_key=True)
	role = Column(Integer, ForeignKey('role.id'))
	rp = Column(Integer, ForeignKey('role_password.id'))

class RoleBlock(Base):
	__tablename__ = 'role_block'
	__table_args__ = (UniqueConstraint('rp', 'block_role'),)
	id = Column(Integer, primary_key=True)
	role = Column(Integer, ForeignKey('role.id'))
	blocked_role = Column(Integer, ForeignKey('role.id'))

class Group(Base):
	__tablename__ = 'group'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)
	open_status = Column(Integer, nullable=False) # 0:all, 1:can search, 2:private
	creater_id = Column(Integer, ForeignKey('role.id'))
	create_time = Column(DateTime, default=func.now())
	update_time = Column(DateTime, default=func.now())

class GroupLink(Base):
	__tablename__ = 'group_link'
	__table_args__ = (UniqueConstraint('up_group_id', 'down_group_id'),)
	id = Column(Integer, primary_key=True)
	up_group_id = Column(Integer, ForeignKey('group.id'))
	down_group_id = Column(Integer, ForeignKey('group.id'))

class GroupManager(Base):
	__tablename__ = 'group_manager'
	__table_args__ = (UniqueConstraint('group_id', 'manager_id', 'manager_pass'),)
	id = Column(Integer, primary_key=True)
	group_id = Column(Integer, ForeignKey('group.id'))
	manager_rp = Column(Integer, ForeignKey('role_password.id'))

class GroupJoiner(Base):
	__tablename__ = 'group_joiner'
	__table_args__ = (UniqueConstraint('group_id', 'joiner_id', 'joiner_pass'),)
	id = Column(Integer, primary_key=True)
	group_id = Column(Integer, ForeignKey('group.id'))
	joiner_rp = Column(Integer, ForeignKey('role_password.id'))

class Input(Base):
	__tablename__ = 'input'
	id = Column(Integer, primary_key=True)
	# 0:one action, 1:long text, 2:short text, 3: comment, 4:pic, 5:video, 6:sound, 7:plan
	type = Column(Integer, nullable=False)
	create_id = Column(Integer, ForeignKey('role.id'))
	create_pass = Column(Integer, ForeignKey('password.key'))
	create_date = Column(DateTime, default=func.now())
	group_id = Column(Integer, ForeignKey('group.id'))

class Message(Base):
	__tablename__ = 'message'
	id = Column(Integer, primary_key=True)
	text = Column(String(100))


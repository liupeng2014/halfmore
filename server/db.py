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
	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False, unique=True)
	create_time = Column(DateTime, default=func.now())
	modify_time = Column(DateTime, default=func.now())
	
	rp = relationship('RolePass', cascade='all,delete-orphan', backref='role')
	rl = relationship('RoleLink', cascade='all,delete-orphan', backref='role')
	rf = relationship('RoleFollow', cascade='all,delete-orphan', backref='role')

class RolePass(Base):
	__tablename__ = 'role_pass'
	__table_args__ = (UniqueConstraint('rid','key'),)
	id = Column(Integer, primary_key=True)
	rid = Column(Integer, ForeignKey('role.id'))
	key = Column(String(20), nullable=False)
	create_time = Column(DateTime, default=func.now())
	modify_time = Column(DateTime, default=func.now())

	login = relationship('Login', cascade='all,delete-orphan')
	profile = relationship('Login', uselist=False, cascade='all,delete-orphan')
	group = relationship('Group', cascade='all,delete-orphan')
	gm = relationship('GroupManager', cascade='all,delete-orphan')
	gj = relationship('GroupJoiner', cascade='all,delete-orphan')

class Login(Base):
	__tablename__ = 'login'
	id = Column(Integer, primary_key=True)
	rp = Column(Integer, ForeignKey('role_pass.id'))
	status = Column(Integer, nullable=False, default=0) # login status. 0:off, 1:on, 2:out
	update_time = Column(DateTime, default=func.now())	

class Profile(Base):
	__tablename__ = 'profile'
	id = Column(Integer, primary_key=True)
	rp = Column(Integer, ForeignKey('role_pass.id'))
	email = Column(String(100), nullable=False)
	open_flag = Column(Integer, nullable=False, default=0) # 0:all, 1:group, 2:self
	gender = Column(Integer, default=2) # 0:woman, 1:man, 2:secret
	location = Column(String(100))
	update_time = Column(DateTime, default=func.now())

# RoleLink is for one person.
# rp is center, and roles are linked to rp.
class RoleLink(Base):
	__tablename__ = 'role_link'
	__table_args__ = (UniqueConstraint('rp', 'linked_role'),)
	id = Column(Integer, primary_key=True)
	rp = Column(Integer, ForeignKey('role_pass.id'))
	linked_role = Column(Integer, ForeignKey('role.id'))

# RoleFollow if for two persons.
# role is up, and rp follows role.
class RoleFollow(Base):
	__tablename__ = 'role_follow'
	__table_args__ = (UniqueConstraint('up_role', 'down_rp'),)
	id = Column(Integer, primary_key=True)
	up_role = Column(Integer, ForeignKey('role.id'))
	down_rp = Column(Integer, ForeignKey('role_pass.id'))

class RoleBlock(Base):
	__tablename__ = 'role_block'
	__table_args__ = (UniqueConstraint('blocker_role_id', 'blocked_role_id'),)
	id = Column(Integer, primary_key=True)
	blocker_role_id = Column(Integer, ForeignKey('role.id'))
	blocked_role_id = Column(Integer, ForeignKey('role.id'))

	blocker_role = relationship('Role', foreign_keys=[blocker_role_id])
	blocked_role = relationship('Role', foreign_keys=[blocked_role_id])

class Group(Base):
	__tablename__ = 'group'
	id = Column(Integer, primary_key=True)
	name = Column(String(50), unique=True, nullable=False)
	open_status = Column(Integer, nullable=False, default=0) # 0:all, 1:can search, 2:private
	creater_rp = Column(Integer, ForeignKey('role_pass.id'))
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
	__table_args__ = (UniqueConstraint('group_id', 'manager_rp'),)
	id = Column(Integer, primary_key=True)
	group_id = Column(Integer, ForeignKey('group.id'))
	manager_rp = Column(Integer, ForeignKey('role_pass.id'))

class GroupJoiner(Base):
	__tablename__ = 'group_joiner'
	__table_args__ = (UniqueConstraint('group_id', 'joiner_rp'),)
	id = Column(Integer, primary_key=True)
	group_id = Column(Integer, ForeignKey('group.id'))
	joiner_rp = Column(Integer, ForeignKey('role_pass.id'))

class Input(Base):
	__tablename__ = 'input'
	id = Column(Integer, primary_key=True)
	# 0:short_message, 1:long_message, 2: comment, 3:schedule, 4:trade
	type = Column(Integer, nullable=False)
	create_rp = Column(Integer, ForeignKey('role_pass.id'), nullable=False)
	group_id = Column(Integer, ForeignKey('group.id'))
	create_time = Column(DateTime, default=func.now())
	update_time = Column(DateTime, default=func.now())

	short_message = relationship('ShortMessage', cascade='all,delete-orphan')
	long_message = relationship('LongMessage', cascade='all,delete-orphan')

class Media(Base):
	__tablename__ = 'media'
	id = Column(Integer, primary_key=True)
	# 0:text 1:pic 2:video 3:audio
	type = Column(Integer, nullable=False)

class ShortMessage(Base):
	__tablename__ = 'short_message'
	id = Column(Integer, primary_key=True)
	input_id = Column(Integer, ForeignKey('input.id'))
	text = Column(String(200))
	create_rp = Column(Integer, ForeignKey('role_pass.id'), nullable=False)
	group_id = Column(Integer, ForeignKey('group.id'))
	create_time = Column(DateTime, default=func.now())
	update_time = Column(DateTime, default=func.now())

class LongMessage(Base):
	__tablename__ = 'long_message'
	id = Column(Integer, primary_key=True)
	input_id = Column(Integer, ForeignKey('input.id'))
	title = Column(String(100))
	text = Column(String(2000))
	create_rp = Column(Integer, ForeignKey('role_pass.id'), nullable=False)
	group_id = Column(Integer, ForeignKey('group.id'))
	create_time = Column(DateTime, default=func.now())
	update_time = Column(DateTime, default=func.now())

class Comment(Base):
	__tablename__ = 'comment'
	id = Column(Integer, primary_key=True)
	input_id = Column(Integer, ForeignKey('input.id'))
	parent_id = Column(Integer, ForeignKey('input.id'), nullable=False)
	text = Column(String(2000))
	create_rp = Column(Integer, ForeignKey('role_pass.id'), nullable=False)
	group_id = Column(Integer, ForeignKey('group.id'))
	create_time = Column(DateTime, default=func.now())
	update_time = Column(DateTime, default=func.now())

	input = relationship('Input', foreign_keys=[input_id])
	parent = relationship('Input', foreign_keys=[parent_id])

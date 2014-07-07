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

def dump_datetime(value):
	if value is None:
		return None
	return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class Account(Base):
	__tablename__ = 'account'
	id = Column(Integer, primary_key=True)
	name = Column(String(20), nullable=False, unique=True)
	key = Column(String(64), nullable=False)
	email = Column(String(200), nullable=False)
	open = Column(Integer, nullable=False, default=0) 
	# open description
	# 0:open, 1:read, 2:self, 3:shut
	# open: show OK, write OK, follow OK, apply OK, 
	# read: show OK, write OK, follow OK, apply NG,
	# self: show NG, write OK, follow NG, apply NG,
	# shut: show NG, write NG, follow NG, apply NG,
	drive = Column(Integer, default=0) # drive value
	location = Column(String(400))
	update_time = Column(DateTime, default=func.now())
	create_time = Column(DateTime, default=func.now())
	modify_time = Column(DateTime, default=func.now())

	role = relationship('Role', cascade='all,delete-orphan', backref='role')
	af = relationship('AccountFollow', cascade='all,delete-orphan')

	@property
	def serialize(self):
		return {
			'id': str(self.id),
			'name': self.name,
			'key': self.key,
			'email': self.email,
			'open': str(self.open),
			'drive': str(self.open),
			'location': self.location,
			'update_time': dump_datetime(self.update_time),
			'create_time': dump_datetime(self.create_time),
			'modify_time': dump_datetime(self.modify_time)
		}

class Role(Base):
	__tablename__ = 'role'
	__table_args__ = (UniqueConstraint('account','name'),)
	id = Column(Integer, primary_key=True)
	account = Column(Integer, ForeignKey('account.id'))
	name = Column(String(20), nullable=False, unique=True)
	key = Column(String(64), nullable=False)
	is_manager = Column(Boolean, default=False)
	area = Column(Integer, nullable=False, default=0) # 0:all, 1:account, 2:self, 3:shut
	status = Column(Integer, nullable=False, default=0) # login status. 0:off, 1:on, 2:out
	email = Column(String(200), nullable=False)
	gender = Column(Integer, default=0) # 0:secret, 1:woman, 2:man, 3:none
	drive = Column(Integer, default=0) # drive value
	location = Column(String(400))
	last_login = Column(DateTime)
	last_logout = Column(DateTime)
	create_time = Column(DateTime, default=func.now())
	update_time = Column(DateTime, default=func.now())

	rl = relationship('RoleLink', cascade='all,delete-orphan')
	rf = relationship('RoleFollow', cascade='all,delete-orphan')
	rb = relationship('RoleBlock', cascade='all,delete-orphan')
	af = relationship('AccountFollow', cascade='all,delete-orphan')
	input = relationship('Input', cascade='all,delete-orphan')

	@property
	def serialize(self):
	    return {
	    	'id': str(self.id),
	    	'account': str(self.rid),
	    	'name': self.name,
	    	'key': self.key,
	    	'is_manager': str(self.is_manager),
	    	'area': self.area,
	    	'status': str(self.status),
			'email': self.email,
	    	'gender': str(self.gender),
	    	'drive': str(self.gender),
			'location': self.location,
	    	'last_login': dump_datetime(self.last_login),
	    	'last_logout': dump_datetime(self.last_logout),
	    	'create_time': dump_datetime(self.create_time),
	    	'update_time': dump_datetime(self.update_time)
	    }
	
# RoleLink is for one person.
class RoleLink(Base):
	__tablename__ = 'role_link'
	__table_args__ = (UniqueConstraint('role', 'linker'),)
	id = Column(Integer, primary_key=True)
	role = Column(Integer, ForeignKey('role.id'))
	linker = Column(Integer, ForeignKey('role.id'))

# RoleFollow is for two persons.
class RoleFollow(Base):
	__tablename__ = 'role_follow'
	__table_args__ = (UniqueConstraint('role', 'follower'),)
	id = Column(Integer, primary_key=True)
	role = Column(Integer, ForeignKey('role.id'))
	follower = Column(Integer, ForeignKey('role.id'))

class RoleBlock(Base):
	__tablename__ = 'role_block'
	__table_args__ = (UniqueConstraint('role', 'blocked'),)
	id = Column(Integer, primary_key=True)
	role = Column(Integer, ForeignKey('role.id'))
	blocked = Column(Integer, ForeignKey('role.id'))

class AccountFollow(Base):
	__tablename__ = 'account_follow'
	__table_args__ = (UniqueConstraint('account', 'follower'),)
	id = Column(Integer, primary_key=True)
	account = Column(Integer, ForeignKey('account.id'))
	follower = Column(Integer, ForeignKey('role.id'))

class Input(Base):
	__tablename__ = 'input'
	id = Column(Integer, primary_key=True)
	# 0:short_message, 1:long_message, 2: comment, 3:event
	type = Column(Integer, nullable=False)
	mark = Column(Integer, default=0) # good mark
	owner = Column(Integer, ForeignKey('role.id'), nullable=False)
	create_time = Column(DateTime, default=func.now(), nullable=False)
	update_time = Column(DateTime, nullable=True)

	short_message = relationship('ShortMessage', cascade='all,delete-orphan')
	long_message = relationship('LongMessage', cascade='all,delete-orphan')
	comment = relationship('Comment', cascade='all,delete-orphan')

class ShortMessage(Base):
	__tablename__ = 'short_message'
	id = Column(Integer, primary_key=True)
	input = Column(Integer, ForeignKey('input.id'))
	text = Column(String(200), nullable=False)

class LongMessage(Base):
	__tablename__ = 'long_message'
	id = Column(Integer, primary_key=True)
	input = Column(Integer, ForeignKey('input.id'))
	title = Column(String(100), nullable=False)
	text = Column(String(2000), nullable=False)

class Comment(Base):
	__tablename__ = 'comment'
	id = Column(Integer, primary_key=True)
	input = Column(Integer, ForeignKey('input.id'), nullable=False)
	top = Column(Integer, ForeignKey('input.id'), nullable=False)
	parent = Column(Integer, ForeignKey('input.id'), nullable=False)
	text = Column(String(400), nullable=False)

class Event(Base):
	__tablename__ = 'event'
	id = Column(Integer, primary_key=True)
	input = Column(Integer, ForeignKey('input.id'), nullable=False)
	title = Column(String(20), nullable=False, unique=True)
	text = Column(String(200), nullable=False)
	open = Column(Integer, nullable=False, default=0) # 0:all, 1:account, 2:self, 3:shut, 4:other
	range = Column(String(500), nullable=True) # for open=4 add account or role
	location = Column(String(400))
	start_time = Column(DateTime, default=func.now(), nullable=False)
	close_time = Column(DateTime, nullable=True)
	repeat = Column(Integer, default=0) # 0:no, 1:day, 2:week, 3:month, 4:year, 5:minute
	interval = Column(Integer, default=0) # for repeat=5 add minutes
	create_time = Column(DateTime, default=func.now(), nullable=False)
	update_time = Column(DateTime, nullable=True)

class Channel(Base):
	__tablename__ = 'channel'
	id = Column(Integer, primary_key=True)
	input = Column(Integer, ForeignKey('input.id'), nullable=False)
	title = Column(String(20), nullable=False, unique=True)
	text = Column(String(200), nullable=False)
	open = Column(Integer, nullable=False, default=0) # 0:all, 1:account, 2:self, 3:shut, 4:other
	range = Column(String(500), nullable=True) # for open=4 add account or role
	create_time = Column(DateTime, default=func.now(), nullable=False)
	update_time = Column(DateTime, nullable=True)

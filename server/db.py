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

class Activity(Base):
	__tablename__ = 'activity'
	id = Column(Integer, primary_key=True)
	name = Column(String(20), nullable=False, unique=True)
	create_time = Column(DateTime, default=func.now())
	modify_time = Column(DateTime, default=func.now())

	role = relationship('Role', cascade='all,delete-orphan', backref='role')

	@property
	def serialize(self):
		return {
			'id': str(self.id),
			'name': self.name,
			'create_time': dump_datetime(self.create_time)
		}

class Role(Base):
	__tablename__ = 'role'
	__table_args__ = (UniqueConstraint('actid','name'),)
	id = Column(Integer, primary_key=True)
	act_id = Column(Integer, ForeignKey('activity.id'))
	name = Column(String(20), nullable=False, unique=True)
	key = Column(String(64), nullable=False)
	email = Column(String(200), nullable=False)
	open = Column(Integer, nullable=False, default=0)
	# open description
	# 0:open, 1:activity, 2:self, 3:shut
	# open: write OK, show for all, be followed OK
	# activity: write OK, show for same activity, be followed by same activity member
	# self: write OK, show for self, be followed NG
	# shut: write NG, show NG, be followed NG
	status = Column(Integer, nullable=False, default=0) # login status. 0:off, 1:on, 2:out
	gender = Column(Integer, default=0) # 0:secret, 1:woman, 2:man, 3:none
	location = Column(String(400))
	last_login = Column(DateTime)
	last_logout = Column(DateTime)
	create_time = Column(DateTime, default=func.now())
	modify_time = Column(DateTime, default=func.now())

	rl = relationship('RoleLink', cascade='all,delete-orphan')
	rf = relationship('RoleFollow', cascade='all,delete-orphan')
	rb = relationship('RoleBlock', cascade='all,delete-orphan')
	input = relationship('Input', cascade='all,delete-orphan')

	@property
	def serialize(self):
	    return {
	    	'id': str(self.id),
	    	'activity': str(self.actid),
	    	'name': self.name,
	    	'key': self.key,
	    	'open': str(self.open),
	    	'status': str(self.status),
			'email': self.email,
	    	'gender': str(self.gender),
			'location': self.location,
	    	'last_login': dump_datetime(self.last_login),
	    	'last_logout': dump_datetime(self.last_logout),
	    	'create_time': dump_datetime(self.create_time),
	    	'update_time': dump_datetime(self.update_time)
	    }

class ActivityFollow(Base):
	__tablename__ = 'activity_follow'
	__table_args__ = (UniqueConstraint('follower', 'activity'),)
	id = Column(Integer, primary_key=True)
	follower = Column(Integer, ForeignKey('role.id'))
	activity = Column(Integer, ForeignKey('activity.id'))

class ActivityBlock(Base):
	__tablename__ = 'activity_block'
	__table_args__ = (UniqueConstraint('blocker', 'activity'),)
	id = Column(Integer, primary_key=True)
	blocker = Column(Integer, ForeignKey('role.id'))
	activity = Column(Integer, ForeignKey('activity.id'))

class RoleFollow(Base):
	__tablename__ = 'role_follow'
	__table_args__ = (UniqueConstraint('follower', 'role'),)
	id = Column(Integer, primary_key=True)
	follower = Column(Integer, ForeignKey('role.id'))
	role = Column(Integer, ForeignKey('role.id'))

class RoleBlock(Base):
	__tablename__ = 'role_block'
	__table_args__ = (UniqueConstraint('blocker', 'role'),)
	id = Column(Integer, primary_key=True)
	blocker = Column(Integer, ForeignKey('role.id'))
	role = Column(Integer, ForeignKey('role.id'))

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

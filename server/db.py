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

# For Act
class Act(Base):
	__tablename__ = 'act'
	id = Column(Integer, primary_key=True)
	name = Column(String(20), nullable=False, unique=True)
	create_time = Column(DateTime, default=func.now())
	modify_time = Column(DateTime, default=func.now())

	role = relationship('Role', cascade='all,delete-orphan', backref='role')
	af = relationship('ActFollow', cascade='all,delete-orphan')
	ab = relationship('ActBlock', cascade='all,delete-orphan')

	@property
	def serialize(self):
		return {
			'id': str(self.id),
			'name': self.name,
			'create_time': dump_datetime(self.create_time),
			'modify_time': dump_datetime(self.modify_time)
		}

# For Role
class Role(Base):
	__tablename__ = 'role'
	__table_args__ = (UniqueConstraint('act_id','name'),)
	id = Column(Integer, primary_key=True)
	act_id = Column(Integer, ForeignKey('act.id'))
	name = Column(String(20), nullable=False)
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
	gender = Column(Integer, default=0) # 0:secret, 1:female, 2:male, 3:none
	location = Column(String(400))
	last_login = Column(DateTime)
	last_logout = Column(DateTime)
	create_time = Column(DateTime, default=func.now())
	modify_time = Column(DateTime, default=func.now())

	rf = relationship('RoleFollow', cascade='all,delete-orphan', foreign_keys = 'RoleFollow.follower')
	rfd = relationship('RoleFollow', cascade='all,delete-orphan', foreign_keys = 'RoleFollow.followed')
	rb = relationship('RoleBlock', cascade='all,delete-orphan', foreign_keys = 'RoleBlock.blocker')
	rbd = relationship('RoleBlock', cascade='all,delete-orphan', foreign_keys = 'RoleBlock.blocked')

	@property
	def serialize(self):
	    return {
	    	'id': str(self.id),
	    	'act_id': str(self.act_id),
	    	'name': self.name,
	    	'key': self.key,
			'email': self.email,
	    	'open': str(self.open),
	    	'status': str(self.status),
	    	'gender': str(self.gender),
			'location': self.location,
	    	'last_login': dump_datetime(self.last_login),
	    	'last_logout': dump_datetime(self.last_logout),
	    	'create_time': dump_datetime(self.create_time),
	    	'modify_time': dump_datetime(self.modify_time)
	    }

class ActFollow(Base):
	__tablename__ = 'act_follow'
	__table_args__ = (UniqueConstraint('follower', 'act'),)
	id = Column(Integer, primary_key=True)
	follower = Column(Integer, ForeignKey('role.id'))
	act = Column(Integer, ForeignKey('act.id'))

class ActBlock(Base):
	__tablename__ = 'act_block'
	__table_args__ = (UniqueConstraint('blocker', 'act'),)
	id = Column(Integer, primary_key=True)
	blocker = Column(Integer, ForeignKey('role.id'))
	act = Column(Integer, ForeignKey('act.id'))

class RoleFollow(Base):
	__tablename__ = 'role_follow'
	__table_args__ = (UniqueConstraint('follower', 'followed'),)
	id = Column(Integer, primary_key=True)
	follower = Column(Integer, ForeignKey('role.id'))
	followed = Column(Integer, ForeignKey('role.id'))

class RoleBlock(Base):
	__tablename__ = 'role_block'
	__table_args__ = (UniqueConstraint('blocker', 'blocked'),)
	id = Column(Integer, primary_key=True)
	blocker = Column(Integer, ForeignKey('role.id'))
	blocked = Column(Integer, ForeignKey('role.id'))

# For Input
class ShortMessage(Base):
	__tablename__ = 'short_message'
	id = Column(Integer, primary_key=True)
	text = Column(String(200), nullable=False)
	owner = Column(Integer, ForeignKey('role.id'), nullable=False)
	create_time = Column(DateTime, default=func.now(), nullable=False)
	update_time = Column(DateTime, nullable=True)

	comment = relationship('Comment', cascade='all,delete-orphan')

class LongMessage(Base):
	__tablename__ = 'long_message'
	id = Column(Integer, primary_key=True)
	title = Column(String(100), nullable=False)
	text = Column(String(2000), nullable=False)
	owner = Column(Integer, ForeignKey('role.id'), nullable=False)
	create_time = Column(DateTime, default=func.now(), nullable=False)
	update_time = Column(DateTime, nullable=True)

	comment = relationship('Comment', cascade='all,delete-orphan')

class Comment(Base):
	__tablename__ = 'comment'
	id = Column(Integer, primary_key=True)
	short_id = Column(Integer, ForeignKey('short_message.id'), nullable=True)
	long_id = Column(Integer, ForeignKey('long_message.id'), nullable=True)
	parent = Column(Integer, nullable=True)
	text = Column(String(400), nullable=False)
	owner = Column(Integer, ForeignKey('role.id'), nullable=False)
	create_time = Column(DateTime, default=func.now(), nullable=False)
	update_time = Column(DateTime, nullable=True)

class Event(Base):
	__tablename__ = 'event'
	id = Column(Integer, primary_key=True)
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
	owner = Column(Integer, ForeignKey('role.id'), nullable=False)
	create_time = Column(DateTime, default=func.now(), nullable=False)
	update_time = Column(DateTime, nullable=True)

class Channel(Base):
	__tablename__ = 'channel'
	id = Column(Integer, primary_key=True)
	title = Column(String(20), nullable=False, unique=True)
	text = Column(String(200), nullable=False)
	open = Column(Integer, nullable=False, default=0) # 0:all, 1:account, 2:self, 3:shut, 4:other
	range = Column(String(500), nullable=True) # for open=4 add account or role
	create_time = Column(DateTime, default=func.now(), nullable=False)
	update_time = Column(DateTime, nullable=True)
	owner = Column(Integer, ForeignKey('role.id'), nullable=False)
	create_time = Column(DateTime, default=func.now(), nullable=False)
	update_time = Column(DateTime, nullable=True)

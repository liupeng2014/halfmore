# coding: utf-8

import sha, datetime
from sqlalchemy import exc

from server import db, dbsession, logger

'''
r1: hmown
r1p1: public
r1p2: group
r1p3: private
r2: hmwork
r2p1: public
r2p2: group
r2p3: private
r2p1 <- r1
r2p2 <- r1
r3: friend1
r3p1: friend1
r1 <- r3p1
r3 <- r1p1
r4: friend2
r4p1: friend2
'''
def db_insert_default(session):
		r1 = register_role(name='hmown', email='hmown@gmail.com', gender=1, location='Tokyo,Japan')
		if not r1:
			logger.info('%s', "DB_INIT:role=hmown register failed.")
			return False

		r1p1 = register_rp(role_id=r1.id, key='public', open_flag=0)
		if not r1p1:
			logger.info('%s', "DB_INIT:hmown p1 register failed.")
			return False

		r1p2 = register_rp(role_id=r1.id, key='group', open_flag=1)
		if not r1p2 :
			logger.info('%s', "DB_INIT:hmown p2 register failed.")
			return False

		r1p3 = register_rp(role_id=r1.id, key='private', open_flag=2)
		if not r1p3 :
			logger.info('%s', "DB_INIT:hmown p3 register failed.")
			return False

		r2 = register_role(name='hmwork', email='hmwork@gmail.com', gender=1, location='Tiba,Japan')
		if not r2 :
			logger.info('%s', "DB_INIT:role=hmwork register failed.")
			return False

		r2p1 = register_rp(role_id=r2.id, key='public', open_flag=0)
		if not r2p1 :
			logger.info('%s', "DB_INIT:hmwork p1 register failed.")
			return False

		r2p2 = register_rp(role_id=r2.id, key='group', open_flag=1)
		if not r2p2 :
			logger.info('%s', "DB_INIT:hmwork p2 register failed.")
			return False

		r2p3 = register_rp(role_id=r2.id, key='private', open_flag=2)
		if not r2p3 :
			logger.info('%s', "DB_INIT:hmwork p3 register failed.")
			return False

		rl211 = register_rolelink(rp_id=r2p1.id, role_id=r1.id)
		if not rl211 :
			logger.info('%s', "DB_INIT:rl211 register failed.")
			return False

		rl231 = register_rolelink(rp_id=r2p3.id, role_id=r1.id)
		if not rl231 :
			logger.info('%s', "DB_INIT:rl231 register failed.")
			return False

		r3 = register_role(name='friend1', email='friend1@gmail.com', gender=1, location='Osaka,Japan')
		if not r3 :
			logger.info('%s', "DB_INIT:role=friend1 register failed.")
			return False

		r3p1 = register_rp(role_id=r3.id, key='friend1', open_flag=0)
		if not r3p1 :
			logger.info('%s', "DB_INIT:friend1 p1 register failed.")
			return False

		rf131 = register_rolefollow(rp_id=r3p1.id, role_id=r1.id)
		if not rf131 :
			logger.info('%s', "DB_INIT:rf131 register failed.")
			return False

		rf311 = register_rolefollow(rp_id=r1p1.id, role_id=r3.id)
		if not rf311 :
			logger.info('%s', "DB_INIT:rf311 register failed.")
			return False

		r4 = register_role(name='friend2', email='friend2@gmail.com', gender=0, location='Yokohama,Japan')
		if not r4 :
			logger.info('%s', "DB_INIT:role=friend2 register failed.")
			return False

		r4p1 = register_rp(role_id=r4.id, key='friend2', open_flag=0)
		if not r4p1 :
			logger.info('%s', "DB_INIT:friend2 p1 register failed.")
			return False

		rf141 = register_rolefollow(rp_id=r4p1.id, role_id=r1.id)
		if not rf141 :
			logger.info('%s', "DB_INIT:rf141 register failed.")
			return False

		rb214 = register_roleblock(rp_id=r2p1.id, role_id=r4.id)
		if not rb214 :
			logger.info('%s', "DB_INIT:rb214 register failed.")
			return False

		g1 = register_group(name='hmcollege', open_status=0, creater_rp=r1p1.id)
		if not g1 :
			logger.info('%s', "DB_INIT:g1 register failed.")
			return False

		gm111 = register_groupmanager(group_id=g1.id, manager_rp=r1p1.id)
		if not gm111 :
			logger.info('%s', "DB_INIT:gm111 register failed.")
			return False

		gm121 = register_groupmanager(group_id=g1.id, manager_rp=r2p1.id)
		if not gm121 :
			logger.info('%s', "DB_INIT:gm121 register failed.")
			return False

		gj131 = register_groupjoiner(group_id=g1.id, joiner_rp=r3p1.id)
		if not gj131 :
			logger.info('%s', "DB_INIT:gj131 register failed.")
			return False

		g2 = register_group(name='hmcompany', open_status=0, creater_rp=r1p1.id)
		if not g2 :
			logger.info('%s', "DB_INIT:g2 register failed.")
			return False

		gm211 = register_groupmanager(group_id=g2.id, manager_rp=r1p1.id)
		if not gm211 :
			logger.info('%s', "DB_INIT:gm211 register failed.")
			return False

		gj231 = register_groupjoiner(group_id=g2.id, joiner_rp=r3p1.id)
		if not gj231:
			logger.info('%s', "DB_INIT:gj231 register failed.")
			return False

		gj241 = register_groupjoiner(group_id=g2.id, joiner_rp=r4p1.id)
		if not gj241:
			logger.info('%s', "DB_INIT:gj241 register failed.")
			return False

def get_role_by_rp(rp_id=None):
	return dbsession.query(db.Role)\
			.filter(db.RolePass.id == rp_id)\
			.filter(db.Role.id == db.RolePass.rid)\
			.first()

def get_role_by_id(role_id=None):
	return dbsession.query(db.Role)\
			.filter(db.Role.id == role_id)\
			.first()

def get_role_by_name(name=None):
	return dbsession.query(db.Role)\
			.filter(db.Role.name == name)\
			.first()

def register_role(*args, **kwargs):
	role = db.Role()
	role.name = kwargs.get('name')
	role.email = kwargs.get('email')
	role.gender = kwargs.get('gender')
	role.location = kwargs.get('location')
	try:
		dbsession.add(role)
		dbsession.commit()
		return role
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def update_role(*args, **kwargs):
	role = get_role(kwargs.get('role_id'))
	if role is None:
		return False

	role.name = kwargs.get('name', role.name)
	role.email = kwargs.get('email', role.email)
	role.gender = kwargs.get('gender', role.gender)
	role.location = kwargs.get('location', role.location)
	role.modify_time = datetime.now()
	try:
		dbsession.commit()
		return role
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_role(role_id=None):
	role = get_role(role_id)
	if role is None:
		return False

	try:
		dbsession.delete(role)
		dbsession.commit()
		return role
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def get_rp(*args, **kwargs):
	if kwargs.get('rp_id'):
		return dbsession.query(db.RolePass)\
			.filter(db.RolePass.id == kwargs['rp_id'])\
			.first()
	elif kwargs.get('role_name') and kwargs.get('key'):
		return dbsession.query(db.RolePass)\
			.filter(db.Role.name == kwargs['role_name'])\
			.filter(db.RolePass.key == sha.new(kwargs['key']).hexdigest())\
			.first()

def register_rp(*args, **kwargs):
	rp = db.RolePass()
	rp.rid = kwargs.get('role_id')
	rp.key = sha.new(kwargs.get('key')).hexdigest()
	rp.open_flag = kwargs.get('open_flag')
	try:
		dbsession.add(rp)
		dbsession.commit()
		return rp
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def update_rp(*args, **kwargs):
	rp = get_rp(**kwargs)
	if rp is None:
		return False

	if kwargs.get('key'):
		rp.key = sha.new(kwargs.get('key')).hexdigest()
	if kwargs.get('open_flag'):
		rp.open_flag = kwargs.get('open_flag')
	rp.modify_time = datetime.now()
	try:
		dbsession.commit()
		return rp
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_rp(rp_id=None):
	rp = get_role(rp_id)
	if rp is None:
		return False

	try:
		dbsession.delete(rp)
		dbsession.commit()
		return rp
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

"""
def get_login(rp_id=None):
	return dbsession.query(db.Login)\
		.filter(db.Login.rp == rp_id)\
		.order_by(db.Login.update_time)\
		.first()

def register_login(*args, **kwargs):
	login = db.Login()
	login.rp = kwargs.get('rp_id')
	login.status = kwargs.get('status')
	login.update_time = datetime.now()
	try:
		dbsession.add(login)
		dbsession.commit()
		return login
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_all_login(rp_id=None):
	try:
		dbsession.query(db.Login)\
		.filter(db.Login.rp==rp_id)\
		.delete()
		dbsession.commit()
		return True
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def get_profile(rp_id=None):
	return dbsession.query(db.Profile)\
		.filter(db.Profile.rp == rp_id)\
		.first()

def register_profile(*args, **kwargs):
	profile = db.Profile()
	profile.rp = kwargs.get('rp_id')
	try:
		dbsession.add(profile)
		dbsession.commit()
		return profile
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def update_profile(*args, **kwargs):
	profile = get_rp(kwargs.get('rp_id'))
	if profile is None:
		return False

	profile.email = kwargs.get('email', profile.email)
	profile.open_flag = kwargs.get('open_flag', profile.open_flag)
	profile.gender = kwargs.get('gender', profile.gender)
	profile.location = kwargs.get('location', profile.location)
	profile.update_time = datetime.now()
	try:
		dbsession.commit()
		return profile
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_profile(rp_id=None):
	profile = get_profile(rp_id)
	if profile is None:
		return False

	try:
		dbsession.delete(profile)
		dbsession.commit()
		return rp
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False
"""

def get_rolelink(*args, **kwargs):
	if kwargs.get('role_id'):
		return dbsession.query(db.RoleLink)\
				.filter(db.RoleLink.rp == kwargs.get('rp_id'))\
				.filter(db.RoleLink.linked_role == kwargs.get('role_id'))\
				.first()
	else:
		return dbsession.query(db.RoleLink)\
				.filter(db.RoleLink.rp == kwargs.get('rp_id'))\
				.all()

def register_rolelink(*args, **kwargs):
	rl = db.RoleLink()
	rl.rp = kwargs.get('rp_id')
	rl.linked_role = kwargs.get('role_id')
	try:
		dbsession.add(rl)
		dbsession.commit()
		return rl
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_rolelink(*args, **kwargs):
	rl = get_rolelink(*args, **kwargs)
	if rl is None or isinstance(rl, list):
		return False

	try:
		dbsession.delete(rl)
		dbsession.commit()
		return rl
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_all_rolelink(rp_id=None):
	try:
		dbsession.query(db.RoleLink)\
		.filter(db.RoleLink.rp==rp_id)\
		.delete()
		dbsession.commit()
		return True
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def get_rolefollow(*args, **kwargs):
	if kwargs.get('role_id') and kwargs.get('rp_id'):
		return dbsession.query(db.RoleFollow)\
				.filter(db.RoleFollow.down_rp == kwargs.get('rp_id'))\
				.filter(db.RoleFollow.up_role == kwargs.get('role_id'))\
				.first()
	elif kwargs.get('rp_id'):
		return dbsession.query(db.RoleFollow)\
				.filter(db.RoleFollow.down_rp == kwargs.get('rp_id'))\
				.all()
	elif kwargs.get('role_id'):
		return dbsession.query(db.RoleFollow)\
				.filter(db.RoleFollow.up_role == kwargs.get('role_id'))\
				.all()
	else:
		return None

def register_rolefollow(*args, **kwargs):
	rf = db.RoleFollow()
	rf.up_role = kwargs.get('role_id')
	rf.down_rp = kwargs.get('rp_id')
	try:
		dbsession.add(rf)
		dbsession.commit()
		return rf
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_rolefollow(*args, **kwargs):
	rf = get_rolefollow(*args, **kwargs)
	if rf is None or isinstance(rf, list):
		return False

	try:
		dbsession.delete(rf)
		dbsession.commit()
		return rf
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_all_rolefollow(role_id=None):
	try:
		dbsession.query(db.RoleFollow)\
		.filter(db.RoleFollow.role==role_id)\
		.delete()
		dbsession.commit()
		return True
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def get_roleblock(*args, **kwargs):
	if kwargs.get('rp_id') and kwargs.get('role_id'):
		return dbsession.query(db.RoleBlock)\
				.filter(db.RoleBlock.rp == kwargs.get('rp_id'))\
				.filter(db.RoleBlock.blocked_role == kwargs.get('role_id'))\
				.first()
	elif kwargs.get('rp_id'):
		return dbsession.query(db.RoleBlock)\
				.filter(db.RoleBlock.rp == kwargs.get('rp_id'))\
				.all()
	elif kwargs.get('role_id'):
		return dbsession.query(db.RoleBlock)\
				.filter(db.RoleBlock.blocked_role == kwargs.get('role_id'))\
				.all()
	else:
		return None

def register_roleblock(*args, **kwargs):
	rb = db.RoleBlock()
	rb.rp = kwargs.get('rp_id')
	rb.blocked_role = kwargs.get('role_id')
	try:
		dbsession.add(rb)
		dbsession.commit()
		return rb
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_roleblock(*args, **kwargs):
	rb = get_roleblock(*args, **kwargs)
	if rb is None or isinstance(rb, list):
		return False

	try:
		dbsession.delete(rb)
		dbsession.commit()
		return rb
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_all_roleblock(rp_id=None):
	try:
		dbsession.query(db.RoleBlock)\
		.filter(db.RoleBlock.rp==rp_id)\
		.delete()
		dbsession.commit()
		return True
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def get_group_by_id(group_id=None):
	return dbsession.query(db.Group)\
			.filter(db.Group.id == group_id)\
			.first()

def get_group_by_name(group_name=None):
	return dbsession.query(db.Group)\
			.filter(db.Group.name == group_name)\
			.first()

def register_group(*args, **kwargs):
	group = db.Group()
	group.name = kwargs.get('name')
	group.open_status = kwargs.get('open_status')
	group.creater_rp = kwargs.get('rp_id')
	try:
		dbsession.add(group)
		dbsession.commit()
		return group
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def update_group(*args, **kwargs):
	group = get_role(kwargs.get('group_id'))
	if group is None:
		return False

	group.name = kwargs.get('name', group.name)
	group.open_status = kwargs.get('name', group.open_status)
	group.modify_time = datetime.now()
	try:
		dbsession.commit()
		return group
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_group(group_id=None):
	group = get_group(group_id)
	if group is None:
		return False

	try:
		dbsession.delete(group)
		dbsession.commit()
		return group
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def get_groupmanager(*args, **kwargs):
	group_id = kwargs.get('group_id')
	manager_rp = kwargs.get('manager_rp')

	if group_id and manager_rp:
		return dbsession.query(db.GroupManager)\
				.filter(db.GroupManager.group_id == group_id)\
				.filter(db.GroupManager.manager_rp == manager_rp)\
				.first()
	elif group_id:
		return dbsession.query(db.GroupManager)\
				.filter(db.GroupManager.group_id == group_id)\
				.all()
	elif manager_rp:
		return dbsession.query(db.GroupManager)\
				.filter(db.GroupManager.manager_rp == manager_rp)\
				.all()
	else:
		return False

def register_groupmanager(*args, **kwargs):
	rp = kwargs.get('manager_rp')
	if not rp:
		return False
	role = get_role_by_rp(rp)

	gid = kwargs.get('group_id')
	if gid is None:
		return False

	rid_list = []
	for gm in get_groupmanager(group_id=gid):
		r = get_role_by_rp(gm.manager_rp)
		if r is not None:
			rid_list.append(r.id)

	if role.id in rid_list:
		return False

	gm = db.GroupManager()
	gm.group_id = gid
	gm.manager_rp = rp
	try:
		dbsession.add(gm)
		dbsession.commit()
		return gm
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_groupmanager(*args, **kwargs):
	gm = get_groupmanager(*args, **kwargs)
	if gm is None or isinstance(gm, list):
		return False

	try:
		dbsession.delete(gm)
		dbsession.commit()
		return gm
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_all_groupmanager(group_id=None):
	try:
		dbsession.query(db.GroupManager)\
		.filter(db.GroupManager.group_id==group_id)\
		.delete()
		dbsession.commit()
		return True
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def get_groupjoiner(*args, **kwargs):
	group_id = kwargs.get('group_id')
	joiner_rp = kwargs.get('joiner_rp')

	if group_id and joiner_rp:
		return dbsession.query(db.GroupJoiner)\
				.filter(db.GroupJoiner.group_id == group_id)\
				.filter(db.GroupJoiner.joiner_rp == joiner_rp)\
				.first()
	elif group_id:
		return dbsession.query(db.GroupJoiner)\
				.filter(db.GroupJoiner.group_id == group_id)\
				.all()
	elif joiner_rp:
		return dbsession.query(db.GroupJoiner)\
				.filter(db.GroupJoiner.joiner_rp == joiner_rp)\
				.all()
	else:
		return False

def register_groupjoiner(*args, **kwargs):
	rp = kwargs.get('joiner_rp')
	if rp is None:
		return False
	role = get_role_by_rp(rp)

	gid = kwargs.get('group_id')
	if gid is None:
		return False

	rid_list = []
	for gj in get_groupjoiner(group_id=gid):
		role = get_role_by_rp(gj.joiner_rp)
		if role is not None:
			rid_list.append(role.id)

	if role.id in rid_list:
		return False

	gj = db.GroupJoiner()
	gj.group_id = gid
	gj.joiner_rp = rp
	try:
		dbsession.add(gj)
		dbsession.commit()
		return gj
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_groupjoiner(*args, **kwargs):
	gj = get_groupjoiner(*args, **kwargs)
	if gj is None or isinstance(gj, list):
		return False

	try:
		dbsession.delete(gj)
		dbsession.commit()
		return gj
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_all_groupjoiner(group_id=None):
	try:
		dbsession.query(db.GroupJoiner)\
		.filter(db.GroupJoiner.group_id==group_id)\
		.delete()
		dbsession.commit()
		return True
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

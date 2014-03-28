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
	r1 = session.query(db.Role)\
		.filter(db.Role.name == 'hm_own').first()
	if r1 is None:
		r1 = db.Role()
		r1.name = 'hmown'
		r1.email = 'hmown@gmail.com'
		r1.gender = 1
		r1.location = "Tokyo,Japan"
		try:
			session.add(r1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:role=hm_own register failed.")
			return False

		r1p1 = db.RolePass()
		r1p1.rid = r1.id
		r1p1.key = sha.new('public').hexdigest()
		r1p1.open_flag = 0
		r1p2 = db.RolePass()
		r1p2.rid = r1.id
		r1p2.key = sha.new('group').hexdigest()
		r1p2.open_flag = 1
		r1p3 = db.RolePass()
		r1p3.rid = r1.id
		r1p3.key = sha.new('private').hexdigest()
		r1p3.open_flag = 2
		try:
			session.add(r1p1)
			session.add(r1p2)
			session.add(r1p3)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:hm_own pass register failed.")
			return False

	if not session.query(db.Role)\
		.filter(db.Role.name == 'hm_work').first():
		r2 = db.Role()
		r2.name = 'hm_work'
		r2.email = 'hm_work@gmail.com'
		r2.gender = 1
		r1.location = "Tiba,Japan"
		try:
			session.add(r2)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:role=hm_work register failed.")
			return False

		r2p1 = db.RolePass()
		r2p1.rid = r2.id
		r2p1.key = sha.new('public').hexdigest()
		r2p1.open_flag = 0
		r2p2 = db.RolePass()
		r2p2.rid = r2.id
		r2p2.key = sha.new('group').hexdigest()
		r2p2.open_flag = 1
		r2p3 = db.RolePass()
		r2p3.rid = r2.id
		r2p3.key = sha.new('private').hexdigest()
		r2p3.open_flag = 2
		try:
			session.add(r2p1)
			session.add(r2p2)
			session.add(r2p3)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:hm_work pass register failed.")
			return False

		rl211 = db.RoleLink()
		rl211.rp = r2p1.id
		rl211.linked_role = r1.id
		rl231 = db.RoleLink()
		rl231.rp = r2p3.id
		rl231.linked_role = r1.id
		try:
			session.add(rl211)
			session.add(rl231)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:rolelink register failed.")
			return False

	if not session.query(db.Role)\
		.filter(db.Role.name == 'friend1').first():
		r3 = db.Role()
		r3.name = 'friend1'
		r3.email = 'friend1@gmail.com'
		try:
			session.add(r3)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:role=friend1 register failed.")
			return False

		r3p1 = db.RolePass()
		r3p1.rid = r3.id
		r3p1.key = sha.new('friend1').hexdigest()
		try:
			session.add(r3p1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:friend1 pass register failed.")
			return False

		rf13 = db.RoleFollow()
		rf13.up_role = r1.id
		rf13.down_rp = r3p1.id
		rf31 = db.RoleFollow()
		rf31.up_role = r3.id
		rf31.down_rp = r1p1.id
		try:
			session.add(rf13)
			session.add(rf31)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:rf13 rf31 register failed.")
			return False

	if not session.query(db.Role)\
		.filter(db.Role.name == 'friend2').first():
		r4 = db.Role()
		r4.name = 'friend2'
		r4.email = 'friend2@gmail.com'
		try:
			session.add(r4)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:role=friend2 register failed.")
			return False

		r4p1 = db.RolePass()
		r4p1.rid = r4.id
		r4p1.key = sha.new('friend2').hexdigest()
		try:
			session.add(r4p1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:friend2 pass register failed.")
			return False

		rf14 = db.RoleFollow()
		rf14.up_role = r1.id
		rf14.down_rp = r4p1.id
		try:
			session.add(rf14)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:rf14 register failed.")
			return False

		rf24 = db.RoleBlock()
		rf24.blocker_role_id = r2.id
		rf24.blocked_role_id = r4.id
		try:
			session.add(rf24)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:rf24 register failed.")
			return False

	if not session.query(db.Group)\
		.filter(db.Group.name == 'A_college').first():
		g1 = db.Group()
		g1.name = 'A_college'
		g1.open_status = 0
		g1.creater_rp = r1p1.id
		try:
			session.add(g1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:group1 register failed.")
			return False

		gm1 = db.GroupManager()
		gm1.group_id = g1.id
		gm1.manager_rp = r1p1.id
		try:
			session.add(gm1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:gm1 register failed.")
			return False

		gj1 = db.GroupJoiner()
		gj1.group_id = g1.id
		gj1.joiner_rp = r1p1.id
		try:
			session.add(gj1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:gj1 register failed.")
			return False

	if not session.query(db.Group)\
		.filter(db.Group.name == 'Develop_group').first():
		g2 = db.Group()
		g2.name = 'Develop_group'
		g2.open_status = 0
		g2.creater_rp = r2p1.id
		try:
			session.add(g2)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:group2 register failed.")
			return False

		gm2 = db.GroupManager()
		gm2.group_id = g2.id
		gm2.manager_rp = r2p1.id
		try:
			session.add(gm2)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:gm2 register failed.")
			return False

		gj2 = db.GroupManager()
		gj2.group_id = g2.id
		gj2.joiner_rp = r2p2.id
		try:
			session.add(gm1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			logger.info('%s', "DB_INIT:gj2 register failed.")
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

def register_role(*args, **kwargs):
	role = config.Role()
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
	rp = config.RolePass()
	rp.rip = kwargs.get('role_id')
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

def get_login(rp_id=None):
	return dbsession.query(db.Login)\
		.filter(db.Login.rp == rp_id)\
		.order_by(db.Login.update_time)\
		.first()

def register_login(*args, **kwargs):
	login = config.Login()
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
	profile = config.Profile()
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

def get_rolelink(*args, **kwargs):
	if kwargs.get('role_id'):
		return dbsession.query(db.RoleLink)\
				.filter(db.RoleLink.rp == kwargs.get('rp_id'))\
				.filter(db.RoleLink.role == kwargs.get('role_id'))\
				.first()
	else:
		return dbsession.query(db.RoleLink)\
				.filter(db.RoleLink.rp == kwargs.get('rp_id'))\
				.all()

def register_rolelink(*args, **kwargs):
	rl = config.RoleLink()
	rl.rp = kwargs.get('rp_id')
	rl.role = kwargs.get('role_id')
	try:
		dbsession.add(rl)
		dbsession.commit()
		return profile
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
	rf = config.RoleFollow()
	rf.role = kwargs.get('role_id')
	rf.rp = kwargs.get('rp_id')
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
	if kwargs.get('role_id') and kwargs.get('blocked_role_id'):
		return dbsession.query(db.RoleBlock)\
				.filter(db.RoleBlock.role == kwargs.get('role_id'))\
				.filter(db.RoleBlock.blocked_role == kwargs.get('blocked_role_id'))\
				.first()
	elif kwargs.get('role_id'):
		return dbsession.query(db.RoleBlock)\
				.filter(db.RoleBlock.rp == kwargs.get('role_id'))\
				.all()
	elif kwargs.get('blocked_role_id'):
		return dbsession.query(db.RoleBlock)\
				.filter(db.RoleBlock.role == kwargs.get('blocked_role_id'))\
				.all()
	else:
		return None

def register_roleblock(*args, **kwargs):
	rb = config.RoleBlock()
	rb.role = kwargs.get('role_id')
	rb.blocked_role = kwargs.get('blocked_role_id')
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

def delete_all_roleblock(role_id=None):
	try:
		dbsession.query(db.RoleBlock)\
		.filter(db.RoleBlock.role==role_id)\
		.delete()
		dbsession.commit()
		return True
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def get_group(group_id=None):
	return dbsession.query(db.Group)\
			.filter(db.Group.id == group_id)\
			.first()

def register_group(*args, **kwargs):
	group = config.group()
	group.name = kwargs.get('name')
	group.open_status = kwargs.get('open_status')
	group.creater_id = kwargs.get('role_id')
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
	if rp is None:
		return False
	role = get_role_by_rp(rp)

	gid = kwargs.get('group_id')
	if gid is None:
		return False

	rid_list = []
	for gm in get_groupmanager(group_id=gid):
		role = get_role_by_rp(gm.manager_rp)
		if role is not None:
			rid_list.append(role.id)

	if role.id in rid_list:
		return False

	gm = config.GroupManager()
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

	gj = config.GroupJoiner()
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

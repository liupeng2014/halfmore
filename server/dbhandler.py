# coding: utf-8

import datetime
import hashlib
from sqlalchemy import exc

from server import db, dbsession, logger

def get_activity_by_id (id=None):
	return dbsession.query(db.Activity)\
			.filter(db.Activity.id == id)\
			.first()

def get_activity_by_name (name=None):
	return dbsession.query(db.Activity)\
			.filter(db.Activity.name == name)\
			.first()

def add_activity(*args, **kwargs):
	act = db.Activity()
	act.name = kwargs.get('name')
	try:
		dbsession.add(act)
		dbsession.commit()
		return act
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def mod_activity(*args, **kwargs):
	name = kwargs.get('act_name')
	if (!name)
		return False

	if (kwargs.get('act_id'))
		act = get_activity_by_id(kwargs.get('act_id'))
	else
		act = get_activity_by_name(name)
	if act is None:
		return False

	if (name == act.name)
		return False

	act.name = name
	act.modify_time = datetime.now()
	try:
		dbsession.commit()
		return act
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def del_activity(*args, **kwargs):
	if (kwargs.get('act_id'))
		act = get_activity_by_id(kwargs.get('act_id'))
	else if (kwargs.get('act_name'))
		act = get_activity_by_name(kwargs.get('act_name'))
	if role is None:
		return False

	try:
		dbsession.delete(role)
		dbsession.commit()
		return role
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def get_role_by_id(act_id=None, role_id=None):
	return dbsession.query(db.Role)\
			.filter(db.Role.id == role_id)\
			.filter(db.Role.act_id == act_id)\
			.first()

def get_role_by_name(act_name=None, role_name=None):
	return dbsession.query(db.Role)\
			.filter(db.Role.name == role_name)\
			.filter(db.Activity.name == act_name)\
			.first()

def add_role(*args, **kwargs):
	role = db.Role()
	role.act_id = kwargs.get('act_id')
	role.name = kwargs.get('name')
	role.key = hashlib.sha256(kwargs.get('key')).hexdigest()
	role.email = kwargs.get('email')
	role.open = kwargs.get('open')
	role.status = kwargs.get('status')
	role.gender = kwargs.get('gender')
	role.location = kwargs.get('location')
	try:
		dbsession.add(role)
		dbsession.commit()
		return role
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def mod_role(*args, **kwargs):
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
	return dbsession.query(db.HM_Group)\
			.filter(db.HM_Group.id == group_id)\
			.first()

def get_group_by_name(group_name=None):
	return dbsession.query(db.HM_Group)\
			.filter(db.HM_Group.name == group_name)\
			.first()

def register_group(*args, **kwargs):
	group = db.HM_Group()
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

def get_grouplink(*args, **kwargs):
	gid = kwargs.get('group_id')
	linked_gid = kwargs.get('linked_group_id')

	if gid and linked_gid:
		return dbsession.query(db.GroupLink)\
				.filter(db.GroupLink.group_id == gid)\
				.filter(db.GroupLink.linked_group_id == linked_gid)\
				.first()
	elif gid:
		return dbsession.query(db.GroupLink)\
				.filter(db.GroupLink.group_id == gid)\
				.all()
	elif linked_gid:
		return dbsession.query(db.GroupLink)\
				.filter(db.GroupLink.linked_group_id == linked_gid)\
				.all()
	else:
		return False

def register_grouplink(*args, **kwargs):
	gl = db.GroupLink()
	gl.group_id = kwargs.get('group_id')
	gl.linked_group_id = kwargs.get('linked_group_id')
	try:
		dbsession.add(gl)
		dbsession.commit()
		return gl
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_grouplink(*args, **kwargs):
	gl = get_grouplink(*args, **kwargs)
	if gl is None or isinstance(gl, list):
		return False

	try:
		dbsession.delete(gl)
		dbsession.commit()
		return gl
	except exc.SQLAlchemyError:
		dbsession.rollback()
		return False

def delete_all_grouplink(group_id=None):
	try:
		dbsession.query(db.GroupLink)\
		.filter(db.GroupLink.group_id==group_id)\
		.delete()
		dbsession.commit()
		return True
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
	gm = db.GroupManager()
	gm.group_id = kwargs.get('group_id')
	gm.manager_rp = kwargs.get('manager_rp')
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
	gj = db.GroupJoiner()
	gj.group_id = kwargs.get('group_id')
	gj.joiner_rp = kwargs.get('joiner_rp')
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

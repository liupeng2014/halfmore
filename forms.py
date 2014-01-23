# coding: utf-8

import re, binascii, socket, json, sha
try:
	import ipaddress
except ImportError:
	import ipaddr as ipaddress

from flask import flash
from flask.ext.wtf import Form
from wtforms.fields import FieldList
from wtforms import TextField, PasswordField, SelectField, BooleanField, HiddenField, validators
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func, exc

import db 
from . import cfg, dbsession

class LoginForm(Form):
	username = TextField('username')
	password = PasswordField('password')

	def validate(self):
		if not self.username.data:
			flash(u'Username is required.')
			return False

		if not self.password.data:
			flash(u'Password is required.')
			return False

		return True

	def getUser(self):
		encpassword = sha.new(self.password.data).hexdigest()
		user = dbsession.query(config.User)\
			.filter(config.User.name==self.username.data,\
			config.User.password==encpassword).first()
		if not user:
			flash(u'Wrong username or password.')
			self.username.data = ""
			return False

		return user

class UserRegisterForm(Form):
	userid = None
	username = TextField('username')
	password = PasswordField('password')
	passwordconfirm = PasswordField('passwordconfirm')
	userlevel = BooleanField('userlevel', default=False)

	def validate(self):
		if not self.username.data:
			flash(u'Username is required.')
			return False

		length = len(self.username.data)
		if length > 20 or length < 3:
			flash(u'The length of username should be between 3 and 20.')
			return False

		for c in self.username.data:
			if ord(c) < 255:
				regexp = re.compile(r'^[0-9A-Za-z\-\_\@\.]+$')
				result = regexp.search(c)
				if not result:
					flash(u'Username should be composed of zenkaku, number, alphabet or [-_@.].')
					return False

		if self.op == 'update' :
			if self.password.data == '' and self.passwordconfirm.data == '':
				self.changepwd = False
				return True
			else:
				self.changepwd = True

		if not self.password.data:
			flash(u'Password is required.')
			return False

		length = len(self.password.data)
		if length > 20 or length < 3:
			flash(u'The length of password should be between 3 and 20.')
			return False

		regexp = re.compile(r'^[\x20-\x7E]+$')
		result = regexp.search(self.password.data)
		if not result:
			flash(u'Password should be ASCII.')
			return False

		if not self.passwordconfirm.data:
			flash(u'Passwordconfirm is required.')
			return False

		if self.password.data != self.passwordconfirm.data:
			flash(u'Password does not equal with passwordconfirm.')
			return False

		return True

	def registerUser(self):
		user = config.User()
		user.password = sha.new(self.password.data).hexdigest()
		user.name = self.username.data
		user.is_admin = self.userlevel.data
		try:
			dbsession.add(user)
			dbsession.flush()
			return user
		except exc.IntegrityError:
			dbsession.rollback()
			flash(u'User has already existed.')
			return False
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'User register failed.')
			return False

	def updateUser(self):
		user = dbsession.query(config.User)\
			.filter(config.User.id==self.userid).first()
		if not user:
			flash(u'User does not exist.')
			return False

		if self.changepwd:
			user.password = sha.new(self.password.data).hexdigest()
		if user.is_admin != self.userlevel.data:
			user.is_admin = self.userlevel.data
		try:
			dbsession.commit()
			return user
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'User update failed.')
			return False

class UserListForm(Form):
	userid = HiddenField('userid')
	op = HiddenField('op')
	nextpage = HiddenField('nextpage')

	def deleteUser(self):
		user = dbsession.query(config.User).\
			filter(config.User.id==self.userid.data).first()
		if not user:
			flash(u'User does not exist.')
			return False

		try:
			dbsession.delete(user)
			dbsession.commit()
			return user
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'User delete failed.')
			return False

class DeviceRegisterForm(Form):
	deviceid = None
	macaddr = TextField('macaddr')
	note = TextField('note')

	def validate(self):
		if not self.macaddr.data:
			flash(u'MAC address is required.')
			return False

		if len(self.macaddr.data) != 12:
			flash(u'The length of MAC address should be 12.')
			return False

		regexp = re.compile(r'^[0-9A-Fa-f]+$')
		result = regexp.search(self.macaddr.data)
		if not result:
			flash(u'MAC address should be composed of 0~9, A~F.')
			return False

		length = len(self.note.data)
		if length > 20:
			flash(u'The maximum length of note is 20.')
			return False

		return True

	def registerDevice(self):
		device = config.Device()
		device.mac_hex = self.macaddr.data.upper()
		device.info = self.note.data
		try:
			dbsession.add(device)
			dbsession.commit()
			return device
		except exc.IntegrityError:
			dbsession.rollback()
			flash(u'Device has already existed.')
			return False
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'Device register failed.')
			return False

	def updateDevice(self):
		device = dbsession.query(config.Device).\
			filter(config.Device.id==self.deviceid).first()
		if not device:
			flash(u'Device does not exist.')
			return False

		if device.mac_hex != self.macaddr.data.upper():
			device.mac_hex = self.macaddr.data.upper()
		if device.info != self.note.data:
			device.info = self.note.data
		try:
			dbsession.commit()
			return device
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'Device update failed.')
			return False

class DeviceListForm(Form):
	deviceid = HiddenField('deviceid')
	op = HiddenField('op')
	nextpage = HiddenField('nextpage')

	def deleteDevice(self):
		device = dbsession.query(config.Device)\
			.filter(config.Device.id==self.deviceid.data).first()
		if not device:
			flash(u'Device does not exist.')
			return False

		try:
			dbsession.delete(device)
			dbsession.commit()
			return device
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'Devcie delete failed.')
			return False

class APSwitchRegisterForm(Form):
	apsid = None
	dpid = None
	name = TextField('name')
	ipaddr = TextField('ipaddr')
	datapathid = TextField('datapathid')
	vlan_trunk = TextField('vlan_trunk')

	def validate(self):
		if not self.name.data:
			flash(u'Name is required.')
			return False

		length = len(self.name.data)
		if length > 20:
			flash(u'The maximum length of name is 20.')
			return False

		if not self.ipaddr.data:
			flash(u'IP address is required.')
			return False

		try:
			socket.inet_pton(socket.AF_INET, self.ipaddr.data)
		except socket.error:
			try:
				socket.inet_pton(socket.AF_INET6, self.ipaddr.data)
			except socket.error:
				flash(u'IP address is wrong.')
				return False

		if not self.datapathid.data:
			flash(u'Datapath ID is required.')
			return False

		if len(self.datapathid.data) != 16:
			flash(u'The length of Datapath ID should be 16.')
			return False

		regexp = re.compile(r'^[0-9A-Fa-f]+$')
		result = regexp.search(self.datapathid.data)
		if not result:
			flash(u'Datapath ID should be composed of 0~9, A~F.')
			return False

		if not self.vlan_trunk.data:
			flash(u'Vlan_Trunk is required.')
			return False

		length = len(self.vlan_trunk.data)
		if length > 20:
			flash(u'The maximum length of vlan_trunk is 20.')
			return False

		return True

	def registerAPSwitch(self):
		aps = config.DatapathContainer()
		aps.ip_address = self.ipaddr.data
		aps.ip_address_hex = binascii.b2a_hex(ipaddress.IPNetwork(aps.ip_address).packed)
		aps.name = self.name.data
		try:
			dbsession.add(aps)
			dbsession.commit()
		except exc.IntegrityError:
			dbsession.rollback()
			flash(u'AP/Switch has already existed.')
			return False
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'AP/Switch register failed.')
			return False

		if len(self.datapathid.data) > 0:
			dp = config.Datapath()
			dp.datapath_hex = self.datapathid.data.upper()
			dp.vlan_trunk = self.vlan_trunk.data
			dp.container_id = aps.id
			try:
				dbsession.add(dp)
				dbsession.commit()
			except exc.IntegrityError:
				dbsession.rollback()
				flash(u'Datapath has already existed.')
				return False

		return (aps, dp)

	def updateAPSwitch(self):
		aps = dbsession.query(config.DatapathContainer)\
			.filter(config.DatapathContainer.id==self.apsid).first()
		if not aps:
			flash(u'AP/Switch does not exist.')
			return False

		if aps.ip_address != self.ipaddr.data:
			aps.ip_address = self.ipaddr.data
			aps.ip_address_hex = binascii.b2a_hex(ipaddress.IPNetwork(aps.ip_address).packed)
		if aps.name != self.name.data:
			aps.name = self.name.data

		try:
			dbsession.commit()
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'AP/Switch update failed.')
			return False

		dp = dbsession.query(config.Datapath)\
			.filter(config.Datapath.container_id==aps.id).first()
		if dp:
			if len(self.datapathid.data) > 0:
				if dp.datapath_hex != self.datapathid.data.upper():
					dp.datapath_hex = self.datapathid.data.upper()
				if dp.vlan_trunk != self.vlan_trunk.data:
					dp.vlan_trunk = self.vlan_trunk.data
			else:
				dbsession.delete(dp)
				dp = None
		else:
			if len(self.datapathid.data) > 0:
				dp = config.Datapath()
				dp.datapath_hex = self.datapathid.data.upper()
				dp.vlan_trunk = self.vlan_trunk.data
				dp.container_id = aps.id
				dbsession.add(dp)

		try:
			dbsession.commit()
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'Datapath update failed.')
			return False
		
		return (aps, dp)

class APSwitchListForm(Form):
	apsid = HiddenField('apsid')
	op = HiddenField('op')
	nextpage = HiddenField('nextpage')

	def deleteAPSwitch(self):
		aps = dbsession.query(config.DatapathContainer)\
			.filter(config.DatapathContainer.id==self.apsid.data).first()
		if not aps:
			flash(u'AP/Switch does not exist.')
			return False

		try:
			dbsession.delete(aps)
			dbsession.commit()
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'AP/Switch delete failed.')
			return False

		dp = dbsession.query(config.Datapath).\
				filter(config.Datapath.container_id==aps.id).first()
		if dp:
			try:
				dbsession.delete(dp)
				dbsession.commit()
			except exc.SQLAlchemyError:
				dbsession.rollback()
				flash(u'Datapath delete failed.')
				return False

		return (aps, dp)

class NetworkRegisterForm(Form):
	networkid = TextField('networkid')
	name = TextField('name')
	vlanid = None
	swnode = None
	static_tep_org = None

	def setSwitchNode(self, swnode, request, static_tep):
		self.swnode = swnode
		for sw in self.swnode:
			id = 'tep%d' % sw['id']
			form = BooleanField('tep', _form=self, _name=id)
			if request.values.get(id) == 'y':
				form.data = True
			else:
				form.data = False
			sw['form'] = form
		sn = {}
		for e in static_tep:
			sn[e['switch_node']] = e
		if request.method == 'GET':
			for sw in self.swnode:
				if sn.has_key(sw['name']):
					sw['form'].data = True
		self.static_tep_org = static_tep

	def validate(self):
		if not self.networkid.data:
			flash(u'VLAN ID is required.')
			return False

		try:
			vlanid = int(self.networkid.data, 10)
		except ValueError:
			flash(u'VLAN ID need a number.')
			return False

		if vlanid < 1 or vlanid > 4094:
			flash(u'VLAN ID should be between 1 and 4094.')
			return False

		if not self.name.data:
			flash(u'Name is required.')
			return False

		length = len(self.name.data)
		if length > 20:
			flash(u'The maximum length of name is 20.')
			return False

		return True

	def registerNetwork(self):
		network = config.Network()
		network.id = self.networkid.data
		network.name = self.name.data
		try:
			dbsession.add(network)
			dbsession.commit()
		except exc.IntegrityError:
			dbsession.rollback()
			flash(u'Network has already existed.')
			return False
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'Network register failed.')
			return False

		for sw in self.swnode:
			if sw['form'].data:
				arg = {}
				arg['switch_node'] = sw['name']
				arg['network'] = self.name.data
				arg['vlan'] = None
				resp = restapi._rest_add_static_tep(arg)

		return network

	def updateNetwork(self):
		network = dbsession.query(config.Network)\
			.filter(config.Network.id==self.networkid.data).first()
		if not network:
			flash(u'Network does not exist.')
			return False

		if network.name != self.name.data:
			network.name = self.name.data
		try:
			dbsession.commit()
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'Network update failed.')
			return False

		sn_org = []
		for e in self.static_tep_org:
			sn_org.append(e['switch_node'])
		sn_org = set(sn_org)

		sn_new = []
		for e in self.swnode:
			if e['form'].data:
				sn_new.append(e['name'])
		sn_new = set(sn_new)

		for sw in sn_new - sn_org:
			arg = {}
			arg['switch_node'] = sw
			arg['network'] = self.name.data
			arg['vlan'] = None
			resp = restapi._rest_add_static_tep(arg)

		for sw in sn_org - sn_new:
			for arg in self.static_tep_org:
				if arg['switch_node'] == sw:
					resp = restapi.rest_delete_static_tep(arg['id'])

		return network

class NetworkListForm(Form):
	networkid = HiddenField('networkid')
	op = HiddenField('op')
	nextpage = HiddenField('nextpage')

	def deleteNetwork(self):
		network = dbsession.query(config.Network)\
			.filter(config.Network.id==self.networkid.data).first()
		if not network:
			flash(u'Network does not exist.')
			return False

		try:
			dbsession.delete(network)
			dbsession.commit()
			return network
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'Network delete failed.')
			return False

class PermissionRegisterForm(Form):
	permissionid = None
	user = TextField('user')
	device = TextField('device')
	network = SelectField('network', coerce=int)
	usernames = []
	devices = []
	userid = None
	deviceid = None
	networkid = None
	op = None

	def __init__(self, *args, **kwargs):
		super(PermissionRegisterForm, self).__init__(*args, **kwargs)
		self.network.choices = [(n.id, n.name) for n in \
			dbsession.query(config.Network).\
			filter(config.Network.name != cfg.get('config', 'bootnet'))]
		self.network.choices.insert(0, (0, ''))
		self.usernames = dbsession.query(config.User.name).all()
		self.devices = dbsession.query(config.Device.mac_hex).all()

	def validate(self):
		if not self.network.data or self.network.data == '':
			flash(u'Network is required.')
			return False

		self.networkid = dbsession.query(config.Network.id)\
			.filter(config.Network.id==self.network.data).first()
		if not self.networkid:
			flash(u'Network does not exist.')
			return False
		else:
			self.networkid = self.networkid[0]

		if self.user.data:
			length = len(self.user.data)
			if length > 20:
				flash(u'The maximum length of username is 20.')
				return False

			self.userid = dbsession.query(config.User.id)\
				.filter(config.User.name == self.user.data).first()
			if not self.userid:
				flash(u'User does not exist.')
				return False
			else:
				self.userid = self.userid[0]

		if self.device.data:
			if len(self.device.data) != 12:
				flash(u'The length of MAC address should be 12.')
				return False

			regexp = re.compile(r'^[0-9A-Fa-f]+$')
			result = regexp.search(self.device.data)
			if not result:
				flash(u'MAC address should be composed of 0~9, A~F.')
				return False

			self.deviceid = dbsession.query(config.Device.id)\
				.filter(config.Device.mac_hex == self.device.data).first()
			if not self.deviceid:
				flash(u'Device does not exist.')
				return False
			else:
				self.deviceid = self.deviceid[0]

		if not self.user.data:
			if not self.device.data:
				flash(u'User or Device should be specified at least one.')
				return False
			else:
				usernotnull = dbsession.query(config.Permission)\
					.filter(config.Permission.device_id == self.deviceid)\
					.filter(config.Permission.network_id == self.networkid)\
					.filter(config.Permission.user_id != None).all()
				if usernotnull:
					if self.op == 'add':
						flash(u'Permission rule conflict on user.')
						return False
					elif self.op == 'update':
						if len(usernotnull) > 1 or \
							str(usernotnull[0].id) != self.permissionid:
							flash(u'Permission rule conflict on user.')
							return False
		else:
			if self.device.data:
				usernull = dbsession.query(config.Permission)\
					.filter(config.Permission.device_id == self.deviceid)\
					.filter(config.Permission.network_id == self.networkid)\
					.filter(config.Permission.user_id == None).first()
				if usernull and str(usernull.id) != self.permissionid:
					flash(u'Permission rule conflict on user.')
					return False

		if not self.device.data:
			if self.user.data:
				devicenotnull = dbsession.query(config.Permission)\
					.filter(config.Permission.user_id == self.userid)\
					.filter(config.Permission.network_id == self.networkid)\
					.filter(config.Permission.device_id != None).all()
				if devicenotnull:
					if self.op == 'add':
						flash(u'Permission rule conflict on device.')
						return False
					elif self.op == 'update':
						if len(devicenotnull) > 1 or \
							str(devicenotnull[0].id) != self.permissionid:
							flash(u'Permission rule conflict on device.')
							return False
		else:
			if self.user.data:
				devicenull = dbsession.query(config.Permission)\
					.filter(config.Permission.user_id == self.userid)\
					.filter(config.Permission.network_id == self.networkid)\
					.filter(config.Permission.device_id == None).first()
				if devicenull and str(devicenull.id) != self.permissionid:
					flash(u'Permission rule conflict on device.')
					return False

		return True

	def registerPermission(self):
		existmap = dbsession.query(config.Permission)\
			.filter(config.Permission.user_id == self.userid)\
			.filter(config.Permission.device_id == self.deviceid)\
			.filter(config.Permission.network_id == self.networkid).first()
		if existmap:
			flash(u'Permission has already existed.')
			return False

		permission = config.Permission()
		if self.userid:
			permission.user_id = self.userid
		if self.deviceid:
			permission.device_id = self.deviceid
		permission.network_id = self.networkid

		try:
			dbsession.add(permission)
			dbsession.commit()
			return permission
		except exc.IntegrityError:
			dbsession.rollback()
			flash(u'Permission has already existed.')
			return False
		except exc.SQLAlchemyError, e:
			dbsession.rollback()
			flash(u'Permission register failed.')
			print str(e)
			return False

	def updatePermission(self):
		permission = dbsession.query(config.Permission)\
			.filter(config.Permission.id==self.permissionid).first()
		if not permission:
			flash(u'Permission does not exist.')
			return False

		existmap = dbsession.query(config.Permission)\
			.filter(config.Permission.user_id == self.userid)\
			.filter(config.Permission.device_id == self.deviceid)\
			.filter(config.Permission.network_id == self.networkid).first()
		if existmap:
			if int(existmap.id) != int(self.permissionid):
				flash(u'Permission has already existed.')
				return False
			else:
				return existmap

		if self.userid:
			if permission.user_id != self.userid:
				permission.user_id = self.userid
		else:
			permission.user_id = None
		if self.deviceid:
			if permission.device_id != self.deviceid:
				permission.device_id = self.deviceid
		else:
			permission.device_id = None
		if permission.network_id != self.networkid:
			permission.network_id = self.networkid
		try:
			dbsession.commit()
			return permission
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'Permission update failed.')
			return False

class PermissionListForm(Form):
	permissionid = HiddenField('permissionid')
	op = HiddenField('op')
	nextpage = HiddenField('nextpage')

	def deletePermission(self):
		permission = dbsession.query(config.Permission)\
			.filter(config.Permission.id==self.permissionid.data).first()
		if not permission:
			flash(u'Permission does not exist.')
			return False

		try:
			dbsession.delete(permission)
			dbsession.commit()
			return permission
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'Permission delete failed.')
			return False

class SwitchNodeRegisterForm(Form):
	swnodeid = None
	name = TextField('name')
	ipaddr = TextField('ipaddr')
	datapathid = TextField('datapathid')

	def validate(self):
		if not self.name.data:
			flash(u'Name is required.')
			return False

		length = len(self.name.data)
		if length > 20:
			flash(u'The maximum length of name is 20.')
			return False

		if not self.ipaddr.data:
			flash(u'IP address is required.')
			return False

		try:
			socket.inet_pton(socket.AF_INET, self.ipaddr.data)
		except socket.error:
			try:
				socket.inet_pton(socket.AF_INET6, self.ipaddr.data)
			except socket.error:
				flash(u'IP address is wrong.')
				return False

		if not self.datapathid.data:
			flash(u'Datapath ID is required.')
			return False

		if len(self.datapathid.data) != 16:
			flash(u'The length of Datapath ID should be 16.')
			return False

		regexp = re.compile(r'^[0-9A-Fa-f]+$')
		result = regexp.search(self.datapathid.data)
		if not result:
			flash(u'Datapath ID should be composed of 0~9, A~F.')
			return False

		return True

	def registerSwitchNode(self):
		param = {}
		param['name'] = self.name.data
		param['ip'] = self.ipaddr.data
		param['datapath'] = self.datapathid.data
		resp = restapi._rest_add_switch_node(param)
		if resp.status[:3] != '201':
			return None
		swnode = json.loads(resp.data)
		return swnode


class SwitchNodeUpdateForm(Form):
	swnodeid = None
	name = TextField('name')

	def validate(self):
		if not self.name.data:
			flash(u'Name is required.')
			return False

		length = len(self.name.data)
		if length > 20:
			flash(u'The maximum length of name is 20.')
			return False

		return True

	def updateSwitchNode(self):
		param = {'name': self.name.data}
		resp = restapi._rest_update_switch_node(self.swnodeid, param)
		if resp.status[:3] != '200':
			return None
		swnode = json.loads(resp.data)
		return swnode

class SwitchNodeListForm(Form):
	swnodeid = HiddenField('swnodeid')
	op = HiddenField('op')
	nextpage = HiddenField('nextpage')

	def deleteSwitchNode(self):
		resp = restapi.rest_get_switch_node(self.swnodeid.data)
		if resp.status[:3] == '204':
			flash(u'SwitchNode does not exist.')
			return False
		swnode = json.loads(resp.data)
		resp = restapi.rest_delete_switch_node(self.swnodeid.data)
		if resp.status[:3] == '404':
			return False
		
		return swnode

class SystemRegisterForm(Form):
	timeout = TextField('timeout')
	tout = None

	def validate(self):
		if not self.timeout.data:
			flash(u'Timeout is required.')
			return False

		try:
			tout = int(self.timeout.data, 10)
		except ValueError:
			flash(u'Timeout need a number.')
			return False

		if tout > 4294967295 or tout < 1:
			flash(u'Timeout should be between 1 and 4294967295.')
			return False

		return True

	def getTimeout(self):
		return dbsession.query(config.Config)\
			.filter(config.Config.name == cfg.get('config', 'timeout')).first()

	def registerTimeout(self):
		time = self.getTimeout()
		if not time:
			time = config.Config()
			time.name = cfg.get('config', 'timeout')
			time.value = self.timeout.data
			dbsession.add(time)
		else:
			if time.value != self.timeout.data:
				time.value = self.timeout.data

		try:
			dbsession.commit()
		except exc.SQLAlchemyError:
			dbsession.rollback()
			flash(u'Timeout register failed.')
			return False

		return time

class ConnectionForm(Form):
	mac = HiddenField('mac')

class LogForm(Form):
	logtype = HiddenField('logtype')

	def getAuthLog(self):
		logs = logsession.query(eventlog.Event)\
			.filter(eventlog.Event.name == cfg.get('eventlog', 'authlog'))\
			.order_by(eventlog.Event.timestamp).all()
		return logs

	def getConnLog(self):
		logs = logsession.query(eventlog.Event)\
			.filter(eventlog.Event.name == cfg.get('eventlog', 'connlog'))\
			.order_by(eventlog.Event.timestamp).all()
		return logs

class NetworkSelectForm(Form):
	networkid = HiddenField('networkid')

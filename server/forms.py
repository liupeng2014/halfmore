# coding: utf-8

import re, binascii, socket

from flask import flash
from flask.ext.wtf import Form
from wtforms.fields import FieldList
from wtforms import TextField, PasswordField, SelectField, BooleanField, HiddenField, validators
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func, exc
from sqlalchemy.orm import sessionmaker

from server import db, dbsession

import rolepass as rp
import dbhandler as dbh

class LoginForm(Form):
	rolename = TextField('role')
	password = PasswordField('pass')

	def validate(self):
		if not self.rolename.data:
			flash(u'Role is required.')
			return False

		if not self.password.data:
			flash(u'Password is required.')
			return False

		return True		

class HomeForm(Form):
	def __init__(self):
		self.rp = None
		self.role = None
		self.links = []
		self.ups = []
		self.follows = []
		self.blocks = []
		self.groupm = None
		self.groupj = None

class RoleRegisterForm(Form):
	userid = None
	rolename = TextField('rolename')
	password = PasswordField('password')
	passwordconfirm = PasswordField('passwordconfirm')
	openflag = SelectField('openflag', coerce=int)

	def __init__(self, *args, **kwargs):
		super(RoleRegisterForm, self).__init__(*args, **kwargs)
		self.openflag.choices.insert([(0, (0, 'All')), (1, (1, 'Secret')),
									  (2, (2, 'Friend')), (3, (3, 'Group'))])

	def validate(self):
		if not self.rolename.data:
			flash(u'Role is required.')
			return False

		length = len(self.rolename.data)
		if length > 100 or length < 3:
			flash(u'The length of role should be between 3 and 100.')
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
		if length > 20 or length < 6:
			flash(u'The length of password should be between 6 and 20.')
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

	def registerRole(self):
		role = config.Role()
		role.password = sha.new(self.password.data).hexdigest()
		role.name = self.username.data
		role.is_admin = self.userlevel.data
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
			.filter(db.User.id==self.userid).first()
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

# coding: utf-8

import sys, os, sha
import binascii
import ConfigParser

from flask import Flask
from server import db
import logging
from logging import FileHandler, Formatter
from sqlalchemy import exc, create_engine
from sqlalchemy.orm import sessionmaker

try:
	configfile = sys.argv[1]
except:
	print "Please specify configuration file."
	sys.exit()
cfg = ConfigParser.SafeConfigParser()
cfg.read(configfile)

app = Flask(__name__)
app.csrf_enabled = True
app.secret_key = os.urandom(24)
logfile_handler = FileHandler(filename=cfg.get('web', 'logfile'))
logfile_handler.setFormatter(Formatter('%(asctime)sZ %(message)s'))
logger = logging.getLogger('OmniWebLog')
logger.addHandler(logfile_handler)
logger.setLevel(logging.DEBUG)

def db_insert_default(session):
	r1 = session.query(db.Role)\
		.filter(db.Role.name == 'liupeng').first()
	if r1 is None:
		r1 = db.Role()
		r1.name = 'liupeng'
		r1.email = 'liupeng@gmail.com'
		try:
			session.add(r1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:role=liupeng register failed.'
			return False

		r1p1 = db.Password()
		r1p1.rid = r1.id
		r1p1.key = sha.new('lp').hexdigest()
		try:
			session.add(r1p1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:liupeng pass register failed.'
			return False

	if not session.query(db.Role)\
		.filter(db.Role.name == 'liupeng_company').first():
		r2 = db.Role()
		r2.name = 'liupeng_company'
		r2.email = 'liupeng_company@gmail.com'
		try:
			session.add(r2)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:role=liupeng_company register failed.'
			return False

		r2p1 = db.Password()
		r2p1.rid = r2.id
		r2p1.key = sha.new('lpc').hexdigest()
		try:
			session.add(r2p1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:liupeng_company pass register failed.'
			return False

		rl12 = db.RoleLink()
		rl12.up_rp = r1p1.id
		rl12.dn_rp = r2p1.id
		try:
			session.add(rl12)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:rl12 register failed.'
			return False

	if not session.query(db.Role)\
		.filter(db.Role.name == 'liupeng_private').first():
		r3 = db.Role()
		r3.name = 'liupeng_private'
		r3.email = 'liupeng_private@gmail.com'
		try:
			session.add(r3)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:role=liupeng_private register failed.'
			return False

		r3p1 = db.Password()
		r3p1.rid = r3.id
		r3p1.key = sha.new('lpp').hexdigest()
		try:
			session.add(r3p1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:liupeng_private pass1 register failed.'
			return False

		r3p2 = db.Password()
		r3p2.rid = r3.id
		r3p2.key = sha.new('lpphoto').hexdigest()
		try:
			session.add(r3p2)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:liupeng_private pass2 register failed.'
			return False

		r3p3 = db.Password()
		r3p3.rid = r3.id
		r3p3.key = sha.new('lpsport').hexdigest()
		try:
			session.add(r3p3)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:liupeng_private pass3 register failed.'
			return False

		rl13 = db.RoleLink()
		rl13.up_rp = r1p1.id
		rl13.dn_rp = r3p1.id
		try:
			session.add(rl13)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:rl13 register failed.'
			return False

		rl13 = db.RoleLink()
		rl13.up_rp = r1p1.id
		rl13.dn_rp = r3p1.id
		try:
			session.add(rl13)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:rl13 register failed.'
			return False

		rl32 = db.RoleLink()
		rl32.up_rp = r3p1.id
		rl32.dn_rp = r3p2.id
		try:
			session.add(rl32)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:rl32 register failed.'
			return False

		rl33 = db.RoleLink()
		rl33.up_rp = r3p1.id
		rl33.dn_rp = r3p3.id
		try:
			session.add(rl33)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:rl33 register failed.'
			return False

	if not session.query(db.Role)\
		.filter(db.Role.name == 'friend').first():
		r4 = db.Role()
		r4.name = 'friend'
		r4.email = 'friend@friend.com'
		try:
			session.add(r4)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:role=friend register failed.'
			return False

		r4p1 = db.Password()
		r4p1.rid = r4.id
		r4p1.key = sha.new('friend').hexdigest()
		try:
			session.add(r4p1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:friend pass register failed.'
			return False

		rf14 = db.RoleFollow()
		rf14.center_role = r1.id
		rf14.follow_rp = r4p1.id
		try:
			session.add(rf14)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:rf14 register failed.'
			return False

dbsession = db.db_init(cfg.get('database', 'url')+'?check_same_thread=False')
db_insert_default(dbsession)

import views

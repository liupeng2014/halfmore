# coding: utf-8

import sys, os
import binascii
import ConfigParser
try:
	import ipaddress
except ImportError:
	import ipaddr as ipaddress

from flask import Flask
from . import db
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

dbsession = db.db_init(cfg.get('config', 'url')+'?check_same_thread=False')
db_insert_default(dbsession)

def db_insert_default(session):
	if not session.query(config.Role)\
		.filter(db.Role.name == 'liupeng').first():
		r1 = db.Role()
		r1.name = 'liupeng'
		r1.email = 'liupengtuxio@gmail.com'
		r1.create_date = 'password'
		try:
			session.add(user1)
			session.commit()
		except exc.SQLAlchemyError:
			session.rollback()
			print 'DB_INIT:user=admin register failed.'
			return False

import views

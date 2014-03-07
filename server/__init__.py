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

from hmlib import dbhandler as dbh

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

dbsession = db.db_init(cfg.get('database', 'url')+'?check_same_thread=False')
dbh.db_insert_default(dbsession)

import views

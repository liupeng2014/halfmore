# coding: utf-8

import sys, os
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
logfile_handler.setFormatter(Formatter('%(asctime)s-15s %(levelname)s - %(message)s'))
logger = logging.getLogger('HMWebLog')
logger.addHandler(logfile_handler)
logger.setLevel(logging.DEBUG)
logger.debug('%s', "=== HM web start ===")

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
	ACT1_NAME = "act1"
	ACT2_NAME = "act2"
	R1_NAME = "role1"
	R2_NAME = "role2"

	if not dbh.get_act_by_name(ACT1_NAME):
		if not dbh.add_act(name=ACT1_NAME):
			logger.info("DB_INIT: activity=%s add failed.", ACT1_NAME)
			return False

	if not dbh.get_act_by_name(ACT2_NAME):
		if not dbh.add_act(name=ACT2_NAME):
			logger.info("DB_INIT: activity=%s add failed.", ACT2_NAME)
			return False

	if not dbh.get_role_by_name(ACT1_NAME, R1_NAME):
		if not dbh.add_role(act_name=ACT1_NAME,
							role_name=R1_NAME,
							key="hoge",
							email="aaa@AAA.com",
							open=0, status=0, gender=0, location="Beijing"):
			logger.info("DB_INIT: role=%s@%s add failed.", R1_NAME, ACT1_NAME)
			return False

	if not dbh.get_role_by_name(ACT1_NAME, R2_NAME):
		if not dbh.add_role(act_name=ACT1_NAME,
							role_name=R2_NAME,
							key="hoge",
							email="bbb@AAA.com",
							open=1, status=0, gender=1, location="Yokohama"):
			logger.info("DB_INIT: role=%s@%s add failed.", R2_NAME, ACT1_NAME)
			return False

	if not dbh.get_role_by_name(ACT2_NAME, R1_NAME):
		if not dbh.add_role(act_name=ACT2_NAME,
							role_name=R1_NAME,
							key="hoge",
							email="aaa@BBB.com",
							open=2, status=0, gender=2, location="Tokyo"):
			logger.info("DB_INIT: role=%s@%s add failed.", R1_NAME, ACT2_NAME)
			return False

	if not dbh.get_role_by_name(ACT2_NAME, R2_NAME):
		if not dbh.add_role(act_name=ACT2_NAME,
							role_name=R2_NAME,
							key="hoge",
							email="bbb@BBB.com",
							open=3, status=0, gender=3, location="Tiba"):
			logger.info("DB_INIT: role=%s@%s add failed.", R2_NAME, ACT2_NAME)
			return False

	'''
	r1p1 = dbh.register_rp(role_id=r1.id, key='public', open_flag=0)
	if not r1p1:
		logger.info('%s', "DB_INIT:hmown p1 register failed.")
		return False

	r1p2 = dbh.register_rp(role_id=r1.id, key='group', open_flag=1)
	if not r1p2 :
		logger.info('%s', "DB_INIT:hmown p2 register failed.")
		return False

	r1p3 = dbh.register_rp(role_id=r1.id, key='private', open_flag=2)
	if not r1p3 :
		logger.info('%s', "DB_INIT:hmown p3 register failed.")
		return False

	r2 = dbh.register_role(name='hmwork', email='hmwork@gmail.com', gender=1, location='Tiba,Japan')
	if not r2 :
		logger.info('%s', "DB_INIT:role=hmwork register failed.")
		return False

	r2p1 = dbh.register_rp(role_id=r2.id, key='public', open_flag=0)
	if not r2p1 :
		logger.info('%s', "DB_INIT:hmwork p1 register failed.")
		return False

	r2p2 = dbh.register_rp(role_id=r2.id, key='group', open_flag=1)
	if not r2p2 :
		logger.info('%s', "DB_INIT:hmwork p2 register failed.")
		return False

	r2p3 = dbh.register_rp(role_id=r2.id, key='private', open_flag=2)
	if not r2p3 :
		logger.info('%s', "DB_INIT:hmwork p3 register failed.")
		return False

	rl211 = dbh.register_rolelink(rp_id=r2p1.id, role_id=r1.id)
	if not rl211 :
		logger.info('%s', "DB_INIT:rl211 register failed.")
		return False

	rl231 = dbh.register_rolelink(rp_id=r2p3.id, role_id=r1.id)
	if not rl231 :
		logger.info('%s', "DB_INIT:rl231 register failed.")
		return False

	r3 = dbh.register_role(name='friend1', email='friend1@gmail.com', gender=1, location='Osaka,Japan')
	if not r3 :
		logger.info('%s', "DB_INIT:role=friend1 register failed.")
		return False

	r3p1 = dbh.register_rp(role_id=r3.id, key='friend1', open_flag=0)
	if not r3p1 :
		logger.info('%s', "DB_INIT:friend1 p1 register failed.")
		return False

	rf131 = dbh.register_rolefollow(rp_id=r3p1.id, role_id=r1.id)
	if not rf131 :
		logger.info('%s', "DB_INIT:rf131 register failed.")
		return False

	rf311 = dbh.register_rolefollow(rp_id=r1p1.id, role_id=r3.id)
	if not rf311 :
		logger.info('%s', "DB_INIT:rf311 register failed.")
		return False

	r4 = dbh.register_role(name='friend2', email='friend2@gmail.com', gender=0, location='Yokohama,Japan')
	if not r4 :
		logger.info('%s', "DB_INIT:role=friend2 register failed.")
		return False

	r4p1 = dbh.register_rp(role_id=r4.id, key='friend2', open_flag=0)
	if not r4p1 :
		logger.info('%s', "DB_INIT:friend2 p1 register failed.")
		return False

	rf141 = dbh.register_rolefollow(rp_id=r4p1.id, role_id=r1.id)
	if not rf141 :
		logger.info('%s', "DB_INIT:rf141 register failed.")
		return False

	rb214 = dbh.register_roleblock(rp_id=r2p1.id, role_id=r4.id)
	if not rb214 :
		logger.info('%s', "DB_INIT:rb214 register failed.")
		return False

	g1 = dbh.register_group(name='hmcollege', open_status=0, creater_rp=r1p1.id)
	if not g1 :
		logger.info('%s', "DB_INIT:g1 register failed.")
		return False

	gm111 = dbh.register_groupmanager(group_id=g1.id, manager_rp=r1p1.id)
	if not gm111 :
		logger.info('%s', "DB_INIT:gm111 register failed.")
		return False

	gj111 = dbh.register_groupjoiner(group_id=g1.id, joiner_rp=r1p1.id)
	if not gj111 :
		logger.info('%s', "DB_INIT:gj111 register failed.")
		return False

	gm121 = dbh.register_groupmanager(group_id=g1.id, manager_rp=r2p1.id)
	if not gm121 :
		logger.info('%s', "DB_INIT:gm121 register failed.")
		return False

	gj121 = dbh.register_groupjoiner(group_id=g1.id, joiner_rp=r2p1.id)
	if not gj121 :
		logger.info('%s', "DB_INIT:gj121 register failed.")
		return False

	gj131 = dbh.register_groupjoiner(group_id=g1.id, joiner_rp=r3p1.id)
	if not gj131 :
		logger.info('%s', "DB_INIT:gj131 register failed.")
		return False

	g2 = dbh.register_group(name='hmcompany', open_status=0, creater_rp=r1p1.id)
	if not g2 :
		logger.info('%s', "DB_INIT:g2 register failed.")
		return False

	gl12 = dbh.register_grouplink(group_id=g1.id, linked_group_id=g2.id)
	if not gl12 :
		logger.info('%s', "DB_INIT:gl12 register failed.")
		return False

	gm211 = dbh.register_groupmanager(group_id=g2.id, manager_rp=r1p1.id)
	if not gm211 :
		logger.info('%s', "DB_INIT:gm211 register failed.")
		return False

	gj211 = dbh.register_groupjoiner(group_id=g2.id, joiner_rp=r1p1.id)
	if not gm211 :
		logger.info('%s', "DB_INIT:gm211 register failed.")
		return False

	gj231 = dbh.register_groupjoiner(group_id=g2.id, joiner_rp=r3p1.id)
	if not gj231:
		logger.info('%s', "DB_INIT:gj231 register failed.")
		return False

	gj241 = dbh.register_groupjoiner(group_id=g2.id, joiner_rp=r4p1.id)
	if not gj241:
		logger.info('%s', "DB_INIT:gj241 register failed.")
		return False
	'''

dbsession = db.db_init(cfg.get('database', 'url')+'?check_same_thread=False')
import dbhandler as dbh
db_insert_default(dbsession)

import views

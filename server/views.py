# coding: utf-8

import time
import datetime
import urllib
import json
import threading
import logging
import kazoo.exceptions
from flask import Flask, session, render_template, redirect, url_for, request, jsonify, abort, flash

from server import app, forms, logger
from server import dbhandler as dbh

def checkSession():
	if session.get('operation') is not None:
		session.pop('operation', None)
	if session.get('rpid') is None:
		return False
	return True

def LOG(*args):
	message = ""
	for item in enumerate(args):
		if isinstance(item[1], (int, long)):
			message += " " + str(item[1])
		else:
			message += " " + item[1]
	logger.info('%s %s:%s', request.remote_addr, session.get('username'), message)

@app.route('/')
def index():
	form = forms.LoginForm()

	return render_template('login.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = forms.LoginForm()

	print "liu1"
	if request.method == 'POST' and form.validate():
		print "liu2"
		rp = dbh.get_rp(role_name=form.rolename.data, key=form.password.data)
		print "liu3"
		if rp:
			print "liu4"
			session['rpid'] = rp.id
#			LOG('login')
			return redirect(url_for('homepage'))

	return render_template('login.html', form=form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
#	LOG('logout')

	session.pop('rpid', None)
	session.pop('rolename', None)
	if session.get('operation') is not None:
		session.pop('operation', None)
	if session.get('networkname') is not None:
		session.pop('networkname', None)
	if session.get('networkid') is not None:
		session.pop('networkid', None)
	if session.get('logtype') is not None:
		session.pop('logtype', None)

	form = forms.LoginForm()
	return render_template('login.html', form=form)

@app.route('/homepage')
def homepage():
	if not checkSession():
		form = forms.LoginForm()
		return render_template('login.html', form=form)

	form = forms.HomeForm()
	form.rpid = session.get('rpid')
	form.role = dbh.get_role_by_rp(form.rpid)
	for l in dbh.get_rolelink(rp_id=form.rpid):
		form.links.append(dbh.get_role_by_id(l.linked_role))
	for f in dbh.get_rolefollow(rp_id=form.rpid):
		form.follows.append(dbh.get_role_by_rp(f.down_rp))
	for b in dbh.get_roleblock(role_id=form.role.id):
		form.blocks = dbh.get_role_by_id(b.blocked_role_id)
	form.groupm = dbh.get_groupmanager(manager_rp=form.rpid)
	form.groupj = dbh.get_groupjoiner(joiner_rp=form.rpid)

	return render_template('homepage.html', form=form)

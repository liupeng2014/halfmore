# coding: utf-8

import time
import datetime
import urllib
import json
import threading
import logging
from flask import Flask, session, render_template, redirect, url_for, request, jsonify, abort, flash

from server import app, forms, logger
from server import dbhandler as dbh

def checkSession():
	if session.get('operation') is not None:
		session.pop('operation', None)
	if session.get('rp') is None:
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
def root():
	form = forms.LoginForm()

	return render_template('halfmore.html', form=form)

@app.route('/index')
def index():
	form = forms.LoginForm()

	return render_template('index.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = forms.LoginForm()

	if request.method == 'POST' and form.validate():
		rp = dbh.get_rp(role_name=form.rolename.data, key=form.password.data)
		if rp:
			role = dbh.get_role_by_rp(rp.id)
			session['rp'] = json.dumps(rp.serialize)
			session['role'] = json.dumps(role.serialize)
			return redirect(url_for('homepage'))
		else:
			flash(u"Wrong rolename or password.")

	return render_template('login.html', form=form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
	session.pop('rp', None)
	session.pop('role', None)
	if session.get('operation') is not None:
		session.pop('operation', None)

	form = forms.LoginForm()
	return render_template('login.html', form=form)

@app.route('/homepage')
def homepage():
	if not checkSession():
		form = forms.LoginForm()
		return render_template('login.html', form=form)

	form = forms.HomeForm()
	form.rp = json.loads(session.get('rp'))
	form.role = json.loads(session.get('role'))
	for l in dbh.get_rolelink(rp_id=int(form.rp.get('id'))):
		form.links.append(dbh.get_role_by_id(l.linked_role))
	# get up_role
	for fu in dbh.get_rolefollow(rp_id=int(form.rp.get('id'))):
		form.ups.append(dbh.get_role_by_id(fu.up_role))
	# get followers
	for fd in dbh.get_rolefollow(role_id=int(form.rp.get('rid'))):
		form.follows.append(dbh.get_role_by_rp(fd.down_rp))
	for b in dbh.get_roleblock(role_id=int(form.role.get('id'))):
		form.blocks.append(dbh.get_role_by_id(b.blocked_role))
	for g in dbh.get_groupmanager(manager_rp=int(form.rp.get('id'))):
		form.gm.append(dbh.get_group_by_id(g.group_id))
	for g in dbh.get_groupjoiner(joiner_rp=int(form.rp.get('id'))):
		form.gj.append(dbh.get_group_by_id(g.group_id))
	return render_template('homepage.html', form=form)

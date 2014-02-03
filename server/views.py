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
from server import db, dbsession


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

	if session.get('pagecount') is not None:
		session.pop('pagecount', None)

	return render_template('login.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = forms.LoginForm()

	if session.get('pagecount') is not None:
		session.pop('pagecount', None)

	if request.method == 'POST' and form.validate():
		rp = form.getRP()
		if rp:
			session['rpid'] = rp.id
			session['rolename'] = rp.role.name
			LOG('login')
			return redirect(url_for('homepage'))

	return render_template('login.html', form=form)

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
	LOG('logout')

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
	if session.get('pagecount') is not None:
		session.pop('pagecount', None)
	if session.get('pageshow') is not None:
		session.pop('pageshow', None)

	form = forms.LoginForm()
	return render_template('login.html', form=form)


@app.route('/homepage')
def homepage():
	if not checkSession():
		form = forms.LoginForm()
		return render_template('login.html', form=form)

	rpid = session.get('rpid')
	in_rpid = dbsession.query(db.RoleLink)\
		.filter(db.RoleLink.out_rp == rpid).all()
	for id in in_rpid:
		role = dbsession.query(db.Role)\
			.filter(db.Role.id)

	return render_template('homepage.html')

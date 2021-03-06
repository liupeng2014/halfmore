# coding: utf-8

import time
import datetime
import urllib
import json
import threading
import logging
from flask import Flask, session, render_template, redirect, url_for, request, jsonify, abort, flash
from flask.ext.socketio import SocketIO, emit

from server import app, forms, logger
from server import dbhandler as dbh

socketio = SocketIO(app)

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
	logger.debug('%s:%s', request.remote_addr, message)

@app.route('/')
def root():
	return redirect(url_for('index'))

@app.route('/index')
def index():
	form = forms.LoginForm()
	session["role_list"] = json.dumps([], sort_keys=True, ensure_ascii=False, indent=2)
	return render_template('index.html', form=form, error=json.dumps(""))

@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = forms.LoginForm()
	rolelist = session.get('role_list', None)
	if rolelist is not None:
		LOG("rolelist2= " + rolelist)
		rolelist = json.loads(rolelist, "utf-8")

	if request.method == 'POST':
		actname = form.hdn_act.data
		rolename = form.hdn_rol.data
		key = form.hdn_pwd.data
		role = dbh.check_role(act_name=actname, role_name=rolename, key=key)
		if role:
			if rolelist:
				for r in rolelist:
					LOG("whole_id= " + r["whole_id"])
					LOG(rolename + "@" + actname)
					LOG(str(role.id) + "@" + str(role.act_id))
					if r["whole_id"] == (str(role.id) + "@" + str(role.act_id)):
						LOG(rolename + "@" + actname + " has already entered.")
						return render_template('index.html', form=form, error=json.dumps(""))
			else:
				rolelist = []

			role_dict = role.serialize;
			role_dict["act_name"] = actname
			role_dict["whole_id"] = str(role.id) + "@" + str(role.act_id)
			role_dict["whole_name"] = rolename + "@" + actname
			rolelist.append(role_dict)
			session["role_list"] = json.dumps(rolelist, sort_keys=True, ensure_ascii=False, indent=2)
			LOG("rolelist1= " + session["role_list"])
			LOG(rolename + "@" + actname + " entered.")
			return render_template('index.html', form=form, error=json.dumps(""))
		else:
			error = rolename + "@" + actname + " NOT exist."
			LOG(rolename + "@" + actname + ":" + key + " NOT exist.")
			return render_template('index.html', form=form, error=json.dumps(error))

	return redirect(url_for('index'))

def list_up_role(top, rolelist):
	for i in range(len(rolelist)):
		if (rolelist[i]["whole_id"] == top):
			if (i == 0):
				break
			else:
				tmp_rol = rolelist[0]
				rolelist[0] = rolelist[i]
				rolelist[i] = tmp_rol
			break
	return rolelist

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
	form = forms.LoginForm()
	rolelist = session.get('role_list', None)
	if rolelist is not None:
		LOG("rolelist4= " + rolelist)
		rolelist = json.loads(rolelist, "utf-8")

	if request.method == 'POST':
		actname = form.hdn_act.data
		rolename = form.hdn_rol.data
		currole = form.hdn_cur.data
		for r in rolelist:
			if r["whole_name"] == (rolename + "@" + actname):
				rolelist.remove(r)
				rolelist = list_up_role(currole, rolelist)
				session["role_list"] = json.dumps(rolelist, sort_keys=True, ensure_ascii=False, indent=2)
				LOG("rolelist3= " + session["role_list"])
				LOG(rolename + "@" + actname + " exited.")
				return render_template('index.html', form=form, error=json.dumps(""))

		rolelist = list_up_role(currole, rolelist)
		error = rolename + "@" + actname + " NOT login."
		LOG(rolename + "@" + actname + " NOT login.")
		return render_template('index.html', form=form, error=json.dumps(error))

	return redirect(url_for('index'))

@app.route('/create', methods = ['POST'])
def login():
	form = forms.CreateForm()
	if request.method == 'POST':
		newtype = form.hdn_type.data

		if (newtype == "act"):
			actname = form.hdn_act.data
			act = dbh.get_act_by_name(actname)
			if (act is None):
				act = dbh.add_act(name=actname)
				if (act is None):
					LOG("Add new act(" + actname + ") failed.")
					error = actname + " create failed."
					return render_template('index.html', form=form, op="add_act_ng", error=json.dumps(error))
				else
					session["new_act"] = json.dumps(act, sort_keys=True, ensure_ascii=False, indent=2)
					LOG("Add new act(" + actname + ") successed.")
					return render_template('index.html', form=form, op="add_act_ok")
			else:
				LOG("act(" + actname + ") existed.")
				return render_template('index.html', form=form, op="add_act_dup")
		elif (newtype == "role"):
		else:
			LOG(newtype + "is not supported.")

	return redirect(url_for('index'))

@socketio.on('get_chat', namespace='/chat')
def get_chat(chat):
	emit('chat_message', {'data': 'test chat'})

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

# coding: utf-8

import time
import datetime
import urllib
import json
import threading
import logging
import restapi
import kazoo.exceptions
from flask import Flask, session, render_template, redirect, url_for, request, jsonify, abort, flash

from . import app, forms, logger
from . import db as dbsession


def checkSession():
	if session.get('operation') is not None:
		session.pop('operation', None)
	if session.get('userid') is None:
		return False
	return True

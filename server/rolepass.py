# coding: utf-8

class hmc_role:
	def __init__(self, id):
		self.id = id

class hmc_olepass:
	def __init__(self, *args, **kwargs):
		if kwargs.get('rp_id'):
			self.rp_id = kwargs['rp_id']
		else:
			self.role_id = kwargs['role_id']
			self.key = kwargs['key']

class hmc_session:
	def __init__(self):
		self.rplist = []

	def addRole(self, rp):
		self.rplist.append(rp)

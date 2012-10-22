# -*- coding: utf8 -*-

class Users:
	def __init__(self):
		self.users = dict()

	def init(self, chan, users):
		"""Initialisation de la liste des utilisateurs connectes"""

		print "------ {Users} : init[" + chan + "]"
		print "=> " + str(users)

		self.users[chan] = users

    def update(self, chan, users):
		"""Mise á jour de la liste des utilisateur connectes"""

		print "------ {Users} : update[" + chan + "]"
		print "=> " + str(users)

		self.users[chan] = users

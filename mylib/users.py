# -*- coding: utf8 -*-

class Users:
	def __init__(self):
		self.users = dict()

	def add(self, chan, pseudo):
		"""Ajoute un utilisateur á la liste des utilisateurs connectes"""

		if not chan in self.users.keys():
			self.users[chan] = []

		self.users[chan].append(pseudo)

	def connected(self, chan, pseudo):
		"""Regarde si un utilisateur est connecte ou non"""

		try:
			return pseudo in self.users[chan]
		except:
			return false

	def get(self, chan):
		"""Recupere la liste des utilisateurs connectes"""

		try:
			return self.users[chan]
		except:
			return []

	def init(self, chan, users):
		"""Initialisation de la liste des utilisateurs connectes"""

		print "------ {Users} : init[" + chan + "]"
		print "=> " + str(users)

		self.users[chan] = users

	def rm(self, chan, pseudo):
		"""Supprime un utilisateur de la liste des utilisateurs connectes"""

		if chan == None:
			for ch in self.users.keys():
				self._rm(ch, pseudo)
		else:
			self._rm(chan, pseudo)

	def _rm(self, chan, pseudo):
		if chan in self.users.keys():
			if pseudo in self.users[chan]:
				self.users[chan].remove(pseudo)

	def update(self, chan, users):
		"""Mise á jour de la liste des utilisateur connectes"""

		print "------ {Users} : update[" + chan + "]"
		print "=> " + str(users)

		self.users[chan] = users

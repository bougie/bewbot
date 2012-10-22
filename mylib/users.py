# -*- coding: utf8 -*-

class Users:
	def __init__(self):
		self.users = dict()

	def init(self, chan, users):
		print "------ {Users} : init[" + chan + "]"
		print "=> " + str(users)

		self.users[chan] = users

    def update(self, chan, users):
		print "------ {Users} : update[" + chan + "]"
		print "=> " + str(users)

		self.users[chan] = users

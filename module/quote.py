# -*- coding: utf8 -*-

import os
import random
import time
import re
import sqlite3

import config

db_file = os.path.join(config.DATA_DIR, 'dataq.db')

class Quote:
	def __init__(self, chans):
		self.conn = None
        
		self.load()

	def add(self, srv, pseudo, chan, txt):
		"""Add a new quote"""

		print "------ {Quote} : Ajout d'une quote"

		if len(txt) > 0:
			try:
				date = str(time.time())

				req_id = "SELECT MAX(COALESCE(q_id, 0)) + 1 FROM quotes WHERE q_chan = '%s'" % (chan)
				req = "INSERT INTO quotes VALUES (?, ?, ?, ?, ?)"

				curr = self.con.cursor()

				# Get a new quote ID
				curr.execute(req_id)
				id = curr.fetchone()[0]
				if id == None:
					id = 0
				else:
					id = int(id)

				# Insert a new quote
				curr.execute(req, (id, chan, pseudo, date, txt))
				self.con.commit()

				srv.privmsg(chan, "Quote #%s ajoutée" % (int(id) + 1))
			except Exception, e:
				print str(e)
				srv.privmsg(chan, "ERREUR: Quote non ajoutée")
		else:
			srv.privmsg(chan, "ERREUR: Quote non ajoutée")

	def admin(self):
		return False

	def get(self, srv, chan, args):
		"""Get a quote by an id, a search pattern or randomly"""

		print "------ {Quote} : Recuperation d'une quote"

		# Get a quote for a given ID
		if "qid" in args and args['qid'] > 0:
			req = "SELECT q_id, q_txt FROM quotes WHERE q_id = %s" % (args['qid'] - 1)
		# Get a quote for a given search pattern
		elif "regexp" in args:
			req = "SELECT q_id, q_txt FROM quotes WHERE q_chan = '%s' AND q_txt GLOB '*%s*' ORDER BY RANDOM() LIMIT 1" % (chan, args['regexp'])
		# Get a random quote
		else:
			req = "SELECT q_id, q_txt FROM quotes WHERE q_chan = '%s' ORDER BY RANDOM() LIMIT 1" % (chan)

		try:
			curr = self.con.cursor()
			curr.execute(req)
			row = curr.fetchone()

			srv.privmsg(chan, "[%s] %s" % (int(row[0]) + 1, row[1]))
		except Exception, e:
			pass

	def list(self, srv, pseudo, chan):
		"""Print all quotes in a private message"""

		print "------ {Quote} : Liste des quotes du chan %s" % (chan)

		req = "SELECT q_id, q_txt FROM quotes WHERE q_chan = '%s'" % (chan)
		try:
			curr = self.con.cursor()
			for row in curr.execute(req):
				srv.privmsg(pseudo, "[%s] %s" % (int(row[0]) + 1, row[1]))
		except Exception, e:
			print str(e)
			pass

	def load(self):
		"""Connection to the database. Create it if it does not exist"""

		print "------ {Quote} : Chargement des quotes"
			
		if os.path.exists(db_file) == False:
			self.con = sqlite3.connect(db_file)
			curr = self.con.cursor()
				
			curr.execute('''CREATE TABLE quotes (
				q_id int,
				q_chan text,
				q_pseudo text,
				q_date text,
				q_txt text,
				PRIMARY KEY (q_id, q_chan))''')
			self.con.commit()
		else:
			self.con = sqlite3.connect(db_file)
            
	def run(self, srv, chan, pseudo, txt):
		"""Main"""

		if self.con == None:
			return

		if txt[0] == 'get':
			args = dict()

			if len(txt) > 1: # We have some extra arguments like quote ID or regexp
				if re.search('^[0-9]+$', txt[1]) != None:
					args["qid"] = int(txt[1])
				else:
					args["regexp"] = txt[1]

			ret = self.get(srv, chan, args)

		elif txt[0] == 'add':
			self.add(srv, pseudo, chan, " ".join(txt[1:]))
		elif txt[0] == 'list':
			self.list(srv, pseudo, chan)

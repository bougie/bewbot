# -*- coding: utf8 -*-

import os
import sqlite3
import time

db_file = 'data.db'

class Note:
	def __init__(self):
		self.con = ''
		
		self.load()

	def add(self, srv, chan, pseudo, txt):
		print "------ ajout d'une note"

		if len(txt) > 1:
			curr = self.con.cursor()

			pseudo_src = str(pseudo)
			pseudo_dst = str(txt[0])
			date = str(time.time())
			txt = str(' '.join(txt[1:]))

			id = "(SELECT MAX(COALESCE(n_id, 0)) + 1 FROM notes WHERE n_chan = '" + chan + "')"
			req = "INSERT INTO notes VALUES(" + id + ", '" + chan + "', '" + pseudo_src + "', '" + pseudo_dst + "', '" + date + "', '" + txt + "')"

			print "------------ req : " + req

			curr.execute(req)
			self.con.commit()

			srv.privmsg(chan, "Note ajoutée")
		else:
			print "------------ len : " + str(len(txt))

	def admin(self):
		return True

	def list(self, srv, chan):
		print "------ liste des notes"

		curr = self.con.cursor()
		for row in curr.execute("SELECT * FROM notes WHERE n_chan = '" + chan + "'"):
			print row
		
	def load(self):
		print "------ Chargement des notes"
		
		if os.path.exists(db_file) == False:
			self.con = sqlite3.connect(db_file)
			curr = self.con.cursor()
			
			curr.execute('''CREATE TABLE notes (
				n_id int,
				n_chan text,
				n_pseudo_src text,
				n_pseudo_dst text,
				n_date text,
				n_txt text,
				PRIMARY KEY (n_id, n_chan))''')
			self.con.commit()
		else:
			self.con = sqlite3.connect(db_file)
			
	def on_join(self, srv, chan, pseudo, connected_users)
		pass
		
	def rm(self):
		print "------ Suppression d'une note"
		
	def runAdmin(self, srv, chan, pseudo, txt):
		run(self, srv, chan, pseudo, txt)

	def run(self, srv, chan, pseudo, txt):
		cmd = txt[0]
		
		if cmd == 'list':
			self.list(srv, chan)
		elif cmd == 'add':
			if len(txt) > 1:
				self.add(srv, chan, pseudo, txt[1:])
		elif cmd == 'rm':
			pass

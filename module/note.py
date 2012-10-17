# -*- coding: utf8 -*-

import sqlite3

db_file = 'data.db'

class Note:
    def __init__(self):
        self.con = sqlite3.connect(db_file)
		
	def add(self):
		pass
		
	def list(self):
		pass
		
	def load(self):
		if os.path.exists(db_file) == False:
			curr = self.con.cursor()
			
			c.execute('''CREATE TABLE notes (
				n_id int,
				n_pseudo_src text,
				n_pseudo_dst text,
				n_date text,
				n_txt text)''')
			self.con.commit()

    def admin(self):
        return True
		
	def rm(self):
		pass
		
	def runAdmin(self, srv, chan, pseudo, txt):
		run(self, srv, chan, pseudo, txt)

    def run(self, srv, chan, pseudo, txt):
        cmd = txt[0]
		
		if cmd == 'list':
			pass
		elif cmd == 'add':
			pass
		elif cmd == 'rm':
			pass

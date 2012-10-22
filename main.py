#!/usr/bin/env python
# -*- coding: utf8 -*-

from mylib import bewbot

#
# Program main function
#
def main():
	servers = [("roubaix2.fr.epiknet.org", 6667)]
	pseudo = "gridaniaroxeuse"
	chan = ["#hugland"]
	admins = ['bougie', 'Bougie']
	modules = ['quote', 'talk', 'note']

	bot = mylib.Bewbot(servers, chan, pseudo, admins)

	bot.load_modules(modules)
	bot.start()

if __name__ == "__main__":
	main()

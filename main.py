#!/usr/bin/env python
# -*- coding: utf8 -*-

from mylib import bewbot
import config

#
# Program main function
#
def main():
	for srv in config.SERVERS:
		bot = bewbot.Bewbot(srv["server"], srv["chans"], srv["pseudo"], srv["admins"])

		bot.load_modules(srv["modules"])
		bot.start()

if __name__ == "__main__":
	main()

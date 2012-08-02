#!/usr/bin/env python
# -*- coding: utf8 -*-

from module import quote, talk

import subprocess
import lib.irclib as irclib
import lib.ircbot as ircbot

pub_command_list = ['quote']
priv_command_list = ['quit']

def command_exists(list, name):
    for cmd in pub_command_list:
        if name == name:
            return True
            
    return False

def can_exec(cmd, pseudo):
    return True

class Bewbot(ircbot.SingleServerIRCBot):
    def __init__(self, servers, chans, pseudo, admins):
        self.adminsuser = admins
        self.chans = chans
        self.pseudo = pseudo
        self.modules = dict()

        ircbot.SingleServerIRCBot.__init__(self,
            servers,
            pseudo,
            "Bot ultrasupra awesome")
            
    def load_modules(self, list):
        for mod in list:
            if mod == 'talk':
                self.modules[mod] = talk.Talk()
            elif mod == 'quote':
                self.modules[mod] = quote.Quote(self.chans)

    def on_welcome(self, srv, evt):
        """Connected to the server"""
        
        for chan in self.chans:
            srv.join(chan)

    def on_join(self, srv, evt):
        """Method called when a user join a chan"""
        
        pseudo = irclib.nm_to_n(evt.source())
        chan = evt.target()
		
        if pseudo == self.pseudo:
            srv.action(chan, "is in da place")

    def on_kick(self, srv, evt):
        """Method called when a user was kicked"""
        
        pseudo = evt.arguments()[0]
        chan = evt.target()
        
        if pseudo == self.pseudo:
            srv.join(chan)

    def on_pubmsg(self, srv, evt):
        """Method called when a public message arrives in a channel"""
        
        pseudo = irclib.nm_to_n(evt.source())
        chan = evt.target()
        msg = evt.arguments()[0]

        print chan + ' <' + pseudo + '> ' + msg
        
        if msg[0] == '!':
            cmd = msg[1:].split(' ')[0]
            
            if cmd == "quit":
                if pseudo in self.adminsuser:
                    srv.disconnect()
                    self.die()
            elif cmd in self.modules:
                msgs = msg.split(' ')
                self.modules[cmd].run(srv, chan, msgs[1:])

    def on_privmsg(self, srv, evt):
        """Method called when an user talk to the bot"""
        
        pseudo = irclib.nm_to_n(evt.source())
        msgs = evt.arguments()[0].split(' ')
        
        cmd = msgs[0]
        if cmd[0] == '!':
            cmd = cmd[1:]
            
            if cmd in self.modules:
                if self.modules[cmd].admin() == True and pseudo in self.adminsuser or self.modules[cmd].admin() == False:
                    self.modules[cmd].run(srv, msgs[1:])

#
# Program main function
#
def main():
    servers = [("roubaix2.fr.epiknet.org", 6667)]
    pseudo = "gridania"
    chan = ["#hugland"]
    admins = ['bougie']
    modules = ['quote', 'talk']

    bot = Bewbot(servers, chan, pseudo, admins)
    
    bot.load_modules(modules)
    bot.start()

if __name__ == "__main__":
    main()

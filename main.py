#!/usr/bin/env python
# -*- coding: utf8 -*-

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
    
class Quote:
    def __init__(self):
        pass
        
    def add(self):
        pass

    def get(self):
        pass

class Bewbot(ircbot.SingleServerIRCBot):
    def __init__(self, servers, chans, pseudo, admins):
        self.adminsuser = admins
        self.chans = chans
        self.pseudo = pseudo

        ircbot.SingleServerIRCBot.__init__(self,
            servers,
            pseudo,
            "Bot ultrasupra awesome")

    def on_welcome(self, srv, evt):
        """Connected to the server"""
        
        srv.join(self.chans)

    def on_join(self, srv, evt):
        """Method called when a user join a chan"""
        
        pseudo = irclib.nm_to_n(evt.source())
        chan = evt.target()
		
        if pseudo == self.pseudo:
            srv.action(chan, "is in da place")

    def on_pubmsg(self, srv, evt):
        """Method called when a public message arrives in a channel"""
        
        pseudo = irclib.nm_to_n(evt.source())
        chan = evt.target()
        msg = evt.arguments()[0]

        print chan + ' <' + pseudo + '>' + msg
        
        if msg[0] == '!':
            if msg[1] == "quit":
                if pseudo in self.adminsuser:
                    srv.disconnect()
                    self.die()

#
# Program main function
#
def main():
    pseudo = "gridania"
    chan = "#hugland"
    admins = ['bougie']

    Bewbot([("roubaix2.fr.epiknet.org", 6667)], chan, pseudo, admins).start()

if __name__ == "__main__":
    main()

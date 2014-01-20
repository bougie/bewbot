# -*- coding: utf8 -*-

from module import quote, talk, url, note
from mylib import users

import subprocess
import lib.irclib as irclib
import lib.ircbot as ircbot

alias = dict()
alias['getquote'] = 'quote get'
alias['addquote'] = 'quote add'
alias['listquote'] = 'quote list'

alias['addnote'] = 'note add'
alias['delnote'] = 'note del'
alias['listnote'] = 'note list'

class Bewbot(ircbot.SingleServerIRCBot):
    def __init__(self, server, chans, pseudo, admins):
        self.adminsuser = admins
        self.chans = chans
        self.pseudo = pseudo
        self.modules = dict()
        self.redirpvlist = dict()
        self.users = users.Users()

        ircbot.SingleServerIRCBot.__init__(self,
            [server],
            pseudo,
            "Bot ultrasupra awesome")

    def on_endofnames(self, srv, evt):
        """Methode appellee lors de la fin de la commande /names"""

        chan = evt.arguments()[0]

        print "------ {Bewbot} : endofnames [" + chan + "]"
        self.users.init(chan, self.channels[chan].users())
            
    def load_modules(self, list):
        """Chargement des modules utilises par le bot"""

        for mod in list:
            if mod == 'talk':
                self.modules[mod] = talk.Talk()
            elif mod == 'quote':
                self.modules[mod] = quote.Quote(self.chans)
            elif mod == 'note':
                self.modules[mod] = note.Note()

    def on_welcome(self, srv, evt):
        """Methode appellee une fois que le bot est connecte á un serveur"""

        print "------ {Bewbot} : welcome"
        
        for chan in self.chans:
            srv.join(chan)

    def on_join(self, srv, evt):
        """Methode appellee lorsqu'un utilisateur join un canal"""

        pseudo = irclib.nm_to_n(evt.source())
        chan = evt.target()

        print "------ {Bewbot} : join[" + chan + "][" + pseudo + "]"
		
        if pseudo == self.pseudo:
            srv.action(chan, "à votre service depuis 1337 ans")
        else:
            self.users.add(chan, pseudo)

        for mod in self.modules:
            try:
                mod.on_join(srv, chan, pseudo, self.users)
            except:
                pass

    def on_kick(self, srv, evt):
        """Methode appellee lorsqu'un utilisateur est kicke d'un canal"""
        
        pseudo = evt.arguments()[0]
        chan = evt.target()

        print "------ {Bewbot} : kick[" + chan + "][" + pseudo + "]"

        self.users.rm(chan, pseudo)
        
        if pseudo == self.pseudo:
            srv.join(chan)

    def on_part(self, srv, evt):
        """Methode appellee lorsqu'un utilisateur /part d'un canal"""

        pseudo = irclib.nm_to_n(evt.source())
        chan = evt.target()

        print "------ {Bewbot} : part[" + chan + "][" + pseudo + "]"

        self.users.rm(chan, pseudo)

    def on_pubmsg(self, srv, evt):
        """Methode appellee lorsqu'un message publique arrive sur un canal"""
        
        pseudo = irclib.nm_to_n(evt.source())
        chan = evt.target()
        msg = evt.arguments()[0]

        print chan + ' <' + pseudo + '> ' + msg
        
        if msg[0] == '!':
            cmd = msg[1:].split(' ')[0]

            if cmd in alias:
                msg = msg.replace(cmd, alias[cmd])
                cmd = msg[1:].split(' ')[0]
            
            if cmd == "quit":
                if pseudo in self.adminsuser:
                    srv.disconnect()
                    self.die()
            elif cmd in self.modules:
                msgs = msg.split(' ')
                
                try:
                    self.modules[cmd].run(srv, chan, pseudo, msgs[1:])
                except:
                    pass
        else:
            url.parser(srv, chan, msg)

    def on_privmsg(self, srv, evt):
        """Methode appellee losque l'on parle en prive au bot"""
        
        pseudo = irclib.nm_to_n(evt.source())
        chan = evt.target()
        msgs = evt.arguments()[0]
        
        print chan + ' <' + pseudo + '> ' + msgs
        for p in self.redirpvlist:
            if p != pseudo:
                if self.redirpvlist[p] == True:
                    srv.privmsg(p, '<' + pseudo + '> ' + msgs)
        
        msgs = evt.arguments()[0].split(' ')
        
        cmd = msgs[0]
        if cmd[0] == '!':
            cmd = cmd[1:]
            
            if pseudo in self.adminsuser:
                if cmd == 'join':
                    if len(msgs[1]) > 0:
                        self.chans.append(msgs[1])
                        srv.join(msgs[1])
                        
                        if 'quote' in self.modules:
                            self.modules['quote'].addChan(msgs[1])
                elif cmd == 'pseudo':
                    if len(msgs[1]) > 0:
                        try:
                            srv.nick(msgs[1]);
                            self.pseudo = msgs[1]
                        except:
                            pass
                elif cmd == 'addredirpv':
                    if pseudo not in self.redirpvlist:
                        self.redirpvlist[pseudo] = True
                        srv.privmsg(pseudo, "Redirection ajoutee")
                elif cmd == 'rmredirpv':
                    if pseudo in self.redirpvlist:
                        self.redirpvlist[pseudo] = False
                        srv.privmsg(pseudo, "Redirection supprimee")
            
            if cmd in self.modules:
                if self.modules[cmd].admin() == True and pseudo in self.adminsuser:
                    self.modules[cmd].runAdmin(srv, chan, pseudo, msgs[1:])

    def on_quit(self, srv, evt):
        """Methode appellee lorsqu'un utilisateur quit le serveur"""

        pseudo = irclib.nm_to_n(evt.source())
        self.users.rm(None, pseudo)

        print "------ {Bewbot} : quit[][" + pseudo + "]"

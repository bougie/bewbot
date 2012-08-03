# -*- coding: utf8 -*-

class Talk:
    def __init__(self):
        pass

    def admin(self):
        return True

    def runAdmin(self, srv, pseudo, msg):
        chan = msg[0]
        
        if chan[0] == '#':
            if msg[1] == '/me':
                srv.action(chan, " ".join(msg[2:]))
            else:
                srv.privmsg(chan, " ".join(msg[1:]))

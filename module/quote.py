# -*- coding: utf8 -*-

import os
import random

file = 'quotes.txt'

class Quote:
    def __init__(self, chans):
        self.quotes = dict()
        self.chans = chans
        
        self.load()

    def add(self, chan, txt):
        ret = ""

        if len(txt) > 0:
            try:
                filehdl = open(file, 'a')

                if chan in self.quotes:
                    self.quotes[chan].append(txt)
                    filehdl.write(chan + ' ' + txt + "\n")
                    
                    ret = "Quote ajoutée avec succés"
                else:
                    ret = "Erreur lors de l'ajout de la quote - chan non reconnu"

                filehdl.close()
            except:
                ret = "Erreur lors de l'ajout de la quote"
        else:
            ret = "Quote vide"
        
        return ret
        
    def addChan(self, chan):
        self.quotes[chan] = []
    
    def admin(self):
        return True

    def get(self, chan):
        if chan in self.quotes:
            if len(self.quotes[chan]) < 2:
                i = 0
            else:
                i = random.randint(0, len(self.quotes[chan]) - 1)
            
            try:
                return self.quotes[chan][i]
            except:
                return ""
        else:
            return ""
    
    def load(self):
        self.quotes = dict()

        for chan in self.chans:
            self.quotes[chan] = []
        
        try:
            if os.path.exists(file) == False:
                hdl = open(file, 'a+')
                hdl.write('')
                hdl.close()
            
            filehdl = open(file, 'r')
            filehdl.seek(0)
            for qt in filehdl:
                c = qt.split(' ')

                if c[0] in self.chans:
                    self.quotes[c[0]].append(" ".join(c[1:]))

            filehdl.close()
        except:
            print '[QUOTE] Erreur ouverture fichier'
            
    def run(self, srv, chan, txt):
        if txt[0] == 'get':
            ret = self.get(chan)
            
            if len(ret) > 0:
                srv.privmsg(chan, ret)
        elif txt[0] == 'add':
            ret = self.add(chan, " ".join(txt[1:]))

            srv.privmsg(chan, ret)
    
    def runAdmin(self, srv, pseudo, txt):
        if txt[0] == 'reload':
            self.load()

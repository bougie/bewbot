# -*- coding: utf8 -*-

import os
import random
import time
import re

file = 'quotes.txt'

class Quote:
    def __init__(self, chans):
        self.quotes = dict()
        self.chans = chans
        self.used = dict()
        
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
        self.used[chan] = dict()
    
    def admin(self):
        return True

    def get(self, chan, args):
        if chan in self.quotes:
            if len(self.used[chan]) == len(self.quotes[chan]):
                self.used[chan] = dict()
            
            if "qid" in args:
                if args["qid"] > 0:
                    i = args["qid"] - 1
                else:
                    i = -1
            else:
                run = True
                
                if "regexp" in args:
                    nb = 0
                    while run:
                        if len(self.quotes[chan]) < 2:
                            i = 0
                            run = False
                        else:
                            i = random.randint(0, len(self.quotes[chan]) - 1)
                            
                            ret = re.search(args["regexp"], self.quotes[chan][i])
                            if ret != None:
                                run = False
                            elif nb == len(self.quotes[chan]):
                                i = -1
                                run = False
                        nb += 1
                else:
                    while run:
                        if len(self.quotes[chan]) < 2:
                            i = 0
                        else:
                            i = random.randint(0, len(self.quotes[chan]) - 1)
                            
                        if i not in self.used[chan].values():
                            run = False
            
            try:
                if i != -1:
                    if "qid" not in args:
                        currTimestamp = time.time()

                        oldTimestamp = currTimestamp - len(self.quotes[chan])
                        for usedIdTimestamp in self.used[chan].keys():
                            if usedIdTimestamp < oldTimestamp:
                                del self.used[chan][usedIdTimestamp]
                        
                        self.used[chan][currTimestamp] = i

                    return "[" + str(i + 1) + "] " + self.quotes[chan][i]
                else:
                    return ""
            except:
                return ""
        else:
            return ""
    
    def load(self):
        self.quotes = dict()

        for chan in self.chans:
            self.quotes[chan] = []
            self.used[chan] = dict()
        
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
            
    def run(self, srv, chan, pseudo, txt):
        if txt[0] == 'get':
            args = dict()

            if len(txt) > 1: #We have some extra arguments like quote ID or regexp
                if re.search('^[0-9]$', txt[1]) != None:
                    args["qid"] = int(txt[1])
                else:
                    args["regexp"] = txt[1]

            ret = self.get(chan, args)
            
            if len(ret) > 0:
                srv.privmsg(chan, ret)
        elif txt[0] == 'add':
            ret = self.add(chan, " ".join(txt[1:]))

            srv.privmsg(chan, ret)
        elif txt[0] == 'list':
            if chan in self.quotes:
                i = 1
                for qt in self.quotes[chan]:
                    srv.privmsg(pseudo, "[" + str(i) + "] " + qt)
                    i += 1
    
    def runAdmin(self, srv, pseudo, txt):
        if txt[0] == 'reload':
            self.load()

# -*- coding: utf8 -*-

import re
import urllib2

def parser(srv, chan, line):
    obj = re.match('.*((http://(.+[a-zA-Z0-9/\._-]))\s.*', line, flags=re.DOTALL | re.UNICODE)
    
    if obj == None:
        obj = re.match('.*(http://(.+[a-zA-Z0-9/\._-]))$', line, flags=re.DOTALL | re.UNICODE)
    
    if obj == None:
        obj = re.match('(http://(.+[a-zA-Z0-9/\._-]))$', line, flags=re.DOTALL | re.UNICODE)
    
    if obj != None:
        try:
            content = urllib2.urlopen(obj.group(1)).read()
            
            if len(content) > 0:
                obj2 = re.search('<title>(.*)</title>', content, flags=re.IGNORECASE | re.DOTALL | re.UNICODE)

                if obj2 != None:
                    t = obj2.group(1).split("\n")
                    title = ""
                    
                    for x in t:
                        if len(title) == 0:
                            title = x.strip()
                        else:
                            title = title + " " + x.strip()

                    srv.privmsg(chan, '[Link Info] title :' + title)
        except:
            pass

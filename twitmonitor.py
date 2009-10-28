# test: twistd -ny twitmonitor.py
# prod: twistd --pidfile=/var/run/comet.pid --logfile=/var/log/comet.log \
#    --reactor=epoll --uid=www-data --gid=www-data --python=twitmonitor.py

from twisted.internet import reactor, task
from twisted.web.server import Site
from twisted.web import server
from twisted.web.resource import Resource
from twisted.web import client
from twisted.python import log
from twisted.application import internet, service

import urllib
import time
import re
import simplejson
import sys

url_pattern = re.compile('(http://.+?/.+?(\s|$))+', re.I)

class TwitMonitor(Resource):
        isLeaf = True
        def __init__(self):
            self.lastsearchresult = None
            self.presence=[]
            self.last_search_id=0
            loopingCall = task.LoopingCall(self.__update_search)
            loopingCall.start(20, False)
            Resource.__init__(self)

        def render_GET(self, request):
            request.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">')
            request.write('<head>')
            request.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
            request.write('<style>li.even {  background-color: #ccf; list-style: none; }')
            request.write('li.odd {  background-color: #eee; list-style: none; }')
            request.write('li.red {  background-color: #a00; list-style: none; } </style>')
            request.write('</head>')
            request.write('<body>')
            request.write('Welcome<br><b>%s</b>: %s<br>' % (time.ctime(),self.lastsearchresult))
            request.write('<ul>')
            self.presence.append(request)
            d = request.notifyFinish()
            d.addCallback(self.__client_disconnected, request)
            d.addErrback(self.__client_disconnected, request)
            return server.NOT_DONE_YET
        
        def __update_search(self):
            if len(self.presence) == 0:
                log.msg("No clients connected")
                return
            else:
                log.msg("%d clients connected" % len(self.presence))
            search = 'fail'
            if self.last_search_id == 0:
                url = "http://search.twitter.com/search.json?q=%s" % (urllib.quote_plus(search))
            else:
                url = "http://search.twitter.com/search.json?q=%s&since_id=%s" % (urllib.quote_plus(search), self.last_search_id)
            deferred = client.getPage(url)
            deferred.addCallbacks(self.__process_search, self.__search_error)
            deferred.addErrback(log.err)
        
        def __process_search(self, res): 
            if res == None:
                log.msg("Error fetching search results")
                return
            statuses = simplejson.loads(res)
            self.last_search_id=statuses['max_id']
            i=False
            for p in self.presence:
                for a in statuses['results']:
                    txt=re.sub(url_pattern, r'<a href="\g<1>">\g<1></a>', a['text'])
                    msg="%s %s: %s<br>\n" %(a['created_at'], a['from_user'], txt)
                    try:
                        if i==False: 
                            p.write('<li class=odd>%s</li>' % (msg.encode('utf-8')))
                            i=True
                        else:
                            p.write('<li class=even>%s</li>' % (msg.encode('utf-8')))
                            i=False
                        p.write("<script>window.scrollBy(0,1000);</script>\n")
                    except:
                        log.msg("Cleaning stale connection")
                        self.presence.remove(p)


        def __search_error(self, response):
            log.msg ("Search error: %s" % response )

        def __client_disconnected(self, r, req):
            self.presence.remove(req)
            log.msg("Client %s disconnected %s" % (self, r))

resource = TwitMonitor()
application = service.Application('web')
isc = service.IServiceCollection(application)
srv = internet.TCPServer(8000, server.Site(resource), interface='127.0.0.1')
srv.setServiceParent(isc)



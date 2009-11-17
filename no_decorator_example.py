#!/usr/bin/python

import urllib2
import urllib
import memcache
import simplejson



def searchresults(si):
    url = "http://search.twitter.com/search.json?q=%s" % urllib.quote(si)
    try:
        f = urllib2.urlopen(url)
        data = f.read()
        f.close()
    except urllib2.URLError, e:
        print e.code
        print e.read()
    
    d = simplejson.loads(data)
    results = d["results"]
    fmt_results=[]
    for s in results:
        fmt_results.append("%s: %s" % (s['from_user'], s['text']))
    return fmt_results

if __name__ == "__main__":
    searchitems = ['#followfriday', '#fail']
    for si in searchitems:
        li=searchresults(si)
        for i in li:
            print "[%s] %s" % (si, i)

#!/usr/bin/python

import urllib2
import urllib
import memcache
import simplejson


# memcached decorator

def cache_me(): # the decorator itself (you could pass a parameter here, like namespace)
    def dec(f): # the function the decorator will return instead of the original f
        def wrapper(*args, **kwargs): # an inside wrapper function to work parameters
            mc = memcache.Client(["127.0.0.1:11211"])
            param = args[0]
            print "---------------- %s ------------ " % param
            rp = mc.get(param) # check if there any value under this key
            if rp == None:
                print "No cache"
                rp=f(*args, **kwargs) # execute original func
                mc.set(param, rp, 60) # set cache with 60 seconds expiration time
            return rp
        return wrapper
    return dec


@cache_me()
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

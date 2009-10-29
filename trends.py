import simplejson
import twitter
import pickle, re, os, urllib
# code from http://zenmachine.wordpress.com/2009/08/19/data-mining-harvesting-from-twitter/

detect_url_pattern = re.compile('(http://.+?/.+?(\s|$))+', re.I)


filename = "last_topic_ids.db"

if os.path.exists(filename):  
    last_topic_ids = pickle.load(file(filename, 'r+b'))  
else:  
    last_topic_ids = {}


api = twitter.Api()
trends_current = simplejson.loads(api._FetchUrl("http://search.twitter.com/trends/current.json"))
c = trends_current["trends"]
for a in c[c.keys()[0]]:
    if a['query'] not in last_topic_ids.keys():
        url = "http://search.twitter.com/search.json?q=%s" % (urllib.quote_plus(a['query']))
    else:
        url = "http://search.twitter.com/search.json?q=%s&since_id=%s" % (urllib.quote_plus(a['query']), last_topic_ids[a['query']])
    print "--------------------------------------"
    print "%s: %s" % (a['name'], url)
    statuses = simplejson.loads(api._FetchUrl(url))
    for s in statuses['results']:
        urls = detect_url_pattern.findall(s['text'])
        if len(urls) > 0:
            print urls[0]

    last_topic_ids[a['query']] = statuses['max_id']
    print "--------------------------------------"

print last_topic_ids
pickle.dump(last_topic_ids, file(filename, 'w+b')) 


import twitter
from urllib import urlencode
import simplejson
import urllib2
import os
import pickle

GOOGLE_API_URL = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s'

my_user_name = ''
my_pass = ''
filename = "statuses.db"

if os.path.exists(filename):  
    last_statuses = pickle.load(file(filename, 'r+b'))  
else:  
    last_statuses = {}

api = twitter.Api(username=my_user_name, password=my_pass)

def query(wot):
    params = {'q': wot, 'rsz': 'small'}
    url = GOOGLE_API_URL % urlencode(params)
    try:
    # Query Google
        resp = urllib2.urlopen(url)
    except URLError, e:
        print e.reason
        return "Ouch, got an error trying to search what you asked me :("

    print resp.geturl()
    
    response = resp.read()
    # Parse response
    try:
        data = simplejson.loads(response)
        results = data['responseData']['results']

        if results:
            resp.close()
            return 'Feeling lucky: %s (+ %s results from Google)' % (results[0]['unescapedUrl'], 
                    data['responseData']['cursor'].get('estimatedResultCount'))

    except (ValueError, KeyError), e:
        print "Couldn't parse Google response due to %r: %s" % (e, response)
        return "Ouch, got some unknown error :("
    
    resp.close();
    return "Google returned 0 results for: %s" % wot

reps = api.GetReplies()
updated = False

for s in reps:
    if s.user.screen_name == my_user_name:
        continue
    if s.id in last_statuses.keys():
        continue
    print "%s (status id: %s): %s" % (s.user.screen_name, s.id, s.text)
    q = s.text.replace("@%s"% s.in_reply_to_screen_name, '')
    r = query(q)
    api.PostUpdate('@%s %s' % (s.user.screen_name, r))
    last_statuses[s.id] = True
    updated = True
    print last_statuses

if updated == True: 
    pickle.dump(last_statuses, file(filename, 'w+b')) 

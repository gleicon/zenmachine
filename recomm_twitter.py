import twitter
from urllib import urlencode
import simplejson
from collections import defaultdict


my_user_name = ''  #here goes your twitter username
my_pass = '' #here goes the passwd

api = twitter.Api(username=my_user_name, password=my_pass)
api.SetUserAgent("ZenMachine recommender")

# keep checking this user's rate limit
print simplejson.loads(api._FetchUrl("https://twitter.com/account/rate_limit_status.json"))  

friends_of_friends = defaultdict(lambda: 0)

def download_friends(screen_name):
    if screen_name == None: return []
    friends = simplejson.loads(api._FetchUrl("http://twitter.com/friends/ids/%s.json" % screen_name))  
    # limiting friends avoid bashing twitter's api, but it can bias the result or taint it
    # with people you already have as friend. Do it only if you have a LOT of friends
    return friends #[:20]  

def download_friends_by_id(id):
    if id == None: return []
    friends = simplejson.loads(api._FetchUrl("http://twitter.com/friends/ids.json?user_id=%s" % id))  
    # limiting here wouldn't affect twitter's api...
    return friends

def compute_friends_of_friends(my_friends):
    for friend in my_friends:
        ff = download_friends_by_id(friend)
        for af in ff:
            if af not in my_friends:
                friends_of_friends[af]+=1
    return friends_of_friends

def generate_friend_recommendation_ranking(friends_of_friends):
    friend_list = []
    for a in friends_of_friends.keys():
        if friends_of_friends[a] > 1:
            # order by count of similar friends and translate user id into screen_name
            u_info = api.GetUser(a)
            print "http://twitter.com/%s (%d): %d" % (u_info.screen_name, a, friends_of_friends[a])
            friend_list.append({"id": a, "screen_name":u_info.screen_name, "ranking": friends_of_friends[a]})
            friend_list.sort(key = lambda x: x['ranking'])
    return friend_list

def main():
    # my friends list
    my_friends = download_friends(my_user_name)
    my_info = api.GetUser(my_user_name)

    # then, for each friend, I get all of his/her friends and fill a dict
    # as an extra pass, I already exclude the ones I already have in my friends list
    # in a Map/reduce setup, this would be a good candidate to Map
    # the trick for limiting is chop down my friends here and filter them again later
     
    friends_of_friends = compute_friends_of_friends(my_friends[:20])
    
    # filter friends of friends again. The initial filtering may be disabled if you want.

    for fr in friends_of_friends.keys():
        if fr in my_friends:
            del(friends_of_friends[fr])
    # delete myself, if I happen to be on the list 

    del(friends_of_friends[my_info.id]) 
    
    # and this one would be a good candidate to be Reduce
    friend_list = generate_friend_recommendation_ranking(friends_of_friends)
    print friend_list
    

if __name__ == "__main__":
    main()

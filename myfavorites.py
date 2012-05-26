# mytweets.py - Creates an archive of your favorite tweets as a Git repo
# Sankha Narayan Guria <sankha93@gmail.com>
# Modified by @Unuruu

import sys, httplib, os.path, json, subprocess

con = httplib.HTTPConnection("api.twitter.com")

def getTweets(num):
	request = "";
	if(num == -1):
		request = "/1/favorites.json?screen_name=" + sys.argv[1] + "&count=200"
	else:
		request = "/1/favorites.json?screen_name=" + sys.argv[1] + "&count=200&since_id=" + num
	return doRequest(request)

def doRequest(request):
	con.request("GET", request)
	r = con.getresponse()
	return json.load(r)

def processTweets(obj):
	if(len(obj) == 200):
		maxid = (obj[-1])['id'] - 1
		if(tweet_id == -1):
			request = "/1/favorites.json?screen_name=" + sys.argv[1] + "&count=200&max_id=" + str(maxid)
		else:
			request = "/1/favorites.json?screen_name=" + sys.argv[1] + "&count=200&max_id=" + str(maxid) + "&since_id=" + tweet_id
		processTweets(doRequest(request))
		
	for tweet in reversed(obj):
		f = open("fav_tweet_id",'w')
		f.write(tweet['id_str'])
		f.close()
		subprocess.call(["git", "add", "."])
		subprocess.call(["git", "commit", "--date", tweet['created_at'], "-m", tweet['text']])

if len(sys.argv) > 1:
	if(os.path.exists("fav_tweet_id")):
		tweet_id = open("fav_tweet_id", 'r').read()
	else:
		tweet_id = -1
	processTweets(getTweets(tweet_id))
else:
	print("Usage: python myfavorites.py username")

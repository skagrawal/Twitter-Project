import time
import datetime
import sys
import json
import csv

 
import tweepy
from tweepy import Cursor
#get tweepy set up

 #auth issueSS
consumer_key="xeqUGGr9BnoqbvLJ3MSPUBUII"
consumer_secret="6Rdh1ujQjKN2Dk4Ss3BRNTUVXEsuhUw3Kyy1ts8mJImymsha8L"
access_token="2918967031-qEffGGTcme4mkjkJyQIQsnVRuDf6OiNg4vyuLWu"
access_token_secret="OqR7e90NeKkkFl46mJJD0Wush918QbKiXAKa0OVEQrXx8"
'''
'''#auth issue 
'''
consumer_key="efYhxnD5Sq7ROQuLTfdfvHTGS"
consumer_secret="OW3zbRWYJJzBuSaTPBk6zm42CpgC4EWg9WdWMdNayUFLStU7UF"
access_token="1233464466-ALmCWhhCAmYqxMssz3TSZQwM6q2QhIwwIPMOnVM"
access_token_secret="1zs4xJXyvr9OuzYG9WIQQpoUSggtAAHYk0aY42bYfeECq"

consumer_key="qkSdMsKYVypkrxsXbwleLjUhX"
consumer_secret="d7pXMWjGDBSt9X5RjsHSflf7PDj9SdTxMei2lxOQbNNdf5EmcZ"
access_token="120195021-aspJslOwQ9sB5hZAWwkr3ngP14b1Zt93Evla7dM0"
access_token_secret="vj5bHkunOHTApw83EtEu3GVZSlDcdFYsF7pl3cvWbwgRj"

consumer_key="mfYKSufLPUbN33z3myrbJz0AF"
consumer_secret="in0xbjbAW6iLNsQGutXGHFs0OpZ0ljxW5aXZJm0URJOSwy7wU6"
access_token="2918967031-qEffGGTcme4mkjkJyQIQsnVRuDf6OiNg4vyuLWu"
access_token_secret="OqR7e90NeKkkFl46mJJD0Wush918QbKiXAKa0OVEQrXx8"

consumer_key="Fa9bWrXqZYa3Y73bMf9pd4UM0"
consumer_secret="ndoDhU61jLzVXgeT2W2cPY6DBwnxD9oG8icJXo5Sb5cOWV77P2"
access_token="2918967031-qEffGGTcme4mkjkJyQIQsnVRuDf6OiNg4vyuLWu"
access_token_secret="OqR7e90NeKkkFl46mJJD0Wush918QbKiXAKa0OVEQrXx8" '''

consumer_key="xPb6EAUUrrRXnQbtH5U7ukNi4"
consumer_secret="WQpTdlWjEWtzGVsfyYtKlKS44Pgnl1d8Dt76qlALCGJvS8ojMd"
access_token="2927528912-c1DWZRpdXvCN8vCOSY49b0puWsiYKpsyZrlHPVG"
access_token_secret="0vxnmMcri6G3XOJuYY2XmH3z7ns4h3ohhS1LsiNbz8hbr"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


#get neo4j set up
#note, you have to have neo4j running and on the default port
from py2neo import neo4j
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data")


# Add uniqueness constraints.
neo4j.CypherQuery(graph_db, "CREATE CONSTRAINT ON (t:Tweet) ASSERT t.id IS UNIQUE;").run()
neo4j.CypherQuery(graph_db, "CREATE CONSTRAINT ON (u:User) ASSERT u.screen_name IS UNIQUE;").run()
neo4j.CypherQuery(graph_db, "CREATE CONSTRAINT ON (h:Hashtag) ASSERT h.name IS UNIQUE;").run()
neo4j.CypherQuery(graph_db, "CREATE CONSTRAINT ON (l:Link) ASSERT l.url IS UNIQUE;").run()
neo4j.CypherQuery(graph_db, "CREATE CONSTRAINT ON (s:Source) ASSERT s.name IS UNIQUE;").run()
neo4j.CypherQuery(graph_db, "CREATE CONSTRAINT ON (c:State) ASSERT c.name IS UNIQUE;").run()

total_tweets = 0
COUNT = 0
LAST_ID = ''
def addTweets(tweets, search, state='add', geocode=None, max_id=None):
    #print "MAX_ID="
    #print max_id
    print 'addTweets Called:'
    print 'search=%s' % search
    print 'state=%s' % state
    print 'geocode=%s' % geocode
    #max_id = tweets[0]._json['id']

    #tweets = json.dumps(tweets)

    tweet_list = []

    i = 0
    #print '^^^^^^^^'
    #print tweets[0]._json
    global total_tweets
    for tweet in tweets:
        #if tweet._json['id'] < max_id:
        max_id = tweet._json['id']
        tweet_list.append(tweet._json)
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet._json['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
        #print ts
        #print 'ts=>>>>>'

        ts = datetime.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")


        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = ts - epoch
        total_seconds = delta.days*86400+delta.seconds+delta.microseconds/1e6
        milli_seconds = total_seconds*1000
        tweet._json['created_at'] = milli_seconds
        #print 'created at'
        #print tweet._json['created_at']
        #print tweet._json['text']
        #print str(tweet._json['created_at'])
        #print str(tweet._json['entities']['user_mentions'])
        #print str(tweet._json['retweet_count'])
        #print str(tweet._json['in_reply_to_user_id'])
        #print str(tweet._json['user']['profile_location'])
        #print str(tweet._json['user']['location'])
        #print str(tweet._json['entities']['hashtags'])
        #print str(tweet._json['id'])
        #print tweet
        #print "****************************************************"
        #print i
        i +=  1
        #print 'adding node'
        #print max_id
        #print i
        total_tweets = total_tweets + 1


    state_name = state
    tweets = tweet_list
    #tweets = json.dumps(tweet_dict)
    # Pass dict to Cypher and build query.
    query = """
        UNWIND {tweets} AS t
        WITH t
        ORDER BY t.id
        WITH t,
             t.entities AS e,
             t.user AS u,
             t.retweeted_status AS retweet
        MERGE (tweet:Tweet {id:t.id})
        SET tweet.text = t.text,
            tweet.created_at = t.created_at,
            tweet.retweeted = t.retweeted,
            tweet.retweet_count = t.retweet_count
        MERGE (user:User {screen_name:u.screen_name})
        SET user.name = u.name,
            user.location = u.location,
            user.followers = u.followers_count,
            user.following = u.friends_count,
            user.verified = u.verified
        MERGE (user)-[:POSTED]->(tweet)
        MERGE (source:Source {name:t.source})
        MERGE (tweet)-[:USING]->(source)
        MERGE (state: State {name: {state_name}})
        MERGE (tweet)-[:FROM]->(state)
        FOREACH (h IN e.hashtags |
          MERGE (tag:Hashtag {name:h.text})
          MERGE (tag)-[:TAGGED]->(tweet)
        )
        """



    # Send Cypher query.
    neo4j.CypherQuery(graph_db, query).run(tweets=tweets, state_name=state_name)
    print("Tweets added to graph!\n")


    getTweet(search, state, geocode, max_id-1)
    #xgetTweets(hashtag, max_id-1)


def xgetTweets(hashtag, max_id=None):
    print 'get tweets called**********'
    global COUNT
    COUNT += 1
    if COUNT < 24:
        #try:
          tweets = api.search(q=hashtag, count=100, max_id=max_id)
          if len(tweets) != 0:
            addTweets(tweets, hashtag, max_id)
        #except Exception, e:
        #  print "exception caught"
        #  print e
        # sys.exit(0)
    else:
      pass


def getTweet(search, state, geocode, max_id=None):
    print 'getTweetcalled:'
    print 'search tweets for %s' % search
    print 'state=%s' % state
    print 'geocode=%s' % geocode
    global COUNT
    COUNT += 1
    if COUNT < 100:
        #try:
          tweets = api.search(q=search, count=100, max_id=max_id, geocode=geocode)
          if len(tweets) != 0:
            addTweets(tweets, search, state, geocode, max_id)
          else:
            print tweets
            print 'No tweets found!'
    else:
      print "Don't fetch more more tweets"
      pass


def getGeoCodes():
  print 'getGeoCodes called:'
  dict_object = {}
  with open('us_cities.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      state = row[1]
      geocode = row[2] + ',-' + row[3] + ',200mi'
      dict_object[geocode] = state
  return dict_object


def getGeoTweets(search):
    print 'getGeoTweets called:'
    print 'search tweets for%s' % search
    #geocodes = {'new york': '37.09024,-95.712891,100000mi'}
    geocodes = getGeoCodes()
    geo_count = 0
    #geocodes = {'new york':'37.3860517000,-122.0838511000,10000mi'}
    for geocode, state in geocodes.iteritems():
      geo_count = geo_count+1
      if geo_count > 20000 and geo_count < 21000:
        #print 'state'
        #print state
        #print geocode
        #print 'geocode'
        getTweet(search, state, geocode, None)


        


#get Tweets.
xsearch=['#USSenate', '#Senate',
          '#senate2014', 
          '#FlipTheSenate', '#Democrats', '#WHITEHOUSE2014', '#JoniErnst', '#ObamaResign', 
          '#Clinton2016', '#StopHillary', '#Obama']

search = ['obama'] 

for value in search:
  COUNT = 0
  print 'search tweets for'
  print value
  #getGeoTweets(hashtag=hashtags)
  getGeoTweets(search=value)

print "total tweets"
print total_tweets
print 'requests sent:%s' % COUNT
#getTweets(hashtag='#Obama')
#for hashtag in hashtags:
#  getTweets(hashtag=hashtag)

# removed tags #florida ##senate2014 results' '#senate2014 immigration'





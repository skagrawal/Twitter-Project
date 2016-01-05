# Return top K most retweeted tweets
MATCH (t:Tweet) where t.retweet_count>0 AND t.retweeted = false return t.retweet_count AS count,t.text as Tweet order by t.retweet_count desc limit 10;


# Return top K hash tags that travel the most number of states
MATCH (c:State)<-[FROM]-(t:Tweet)<-[TAGGED]-(h:Hashtag) return (count(distinct(c.name))) AS Longest_Path,h.name AS Hashtag order by Longest_Path desc limit 10;

# Return the longest path of states that a particular hash tag travels within a given time period.
MATCH (c:State)<-[FROM]-(t:Tweet)<-[TAGGED]-(h:Hashtag) where h.name = "obama" and t.created_at < 1417803604449 and t.created_at > 1351798658000 return (count(distinct(c.name))) AS Longest_Path;

# Show contents of the most retweeted tweet for a hash tag Y and the state X where it was posted originally.
match (c:State)<-[FROM]-(t:Tweet)<-[:TAGGED]-(h:Hashtag)  where c.name = "CA" and h.name = "Obama" and t.retweeted = false  return t.text AS Tweet,c.name AS Location,t.retweet_count AS Retweet_Count order by t.retweet_count desc limit 1;

# Return users and their location, which have used hash tag A and also used hash tag B and hash tag C in their tweets.

MATCH (h1:Hashtag)-[TAGGED]->(t:Tweet)<-[:TAGGED]-(h2:Hashtag) where h1.name = "damage" AND h2.name = "america"  with t MATCH (h3:Hashtag)-[TAGGED]->(t)<-[POSTED]-(u:User) WHERE h3.name = "tyrants" return u.name AS Name,u.location AS Location;;

#  Return max k platform used for tweeting of a certain hash tag.
MATCH (h:Hashtag)-[:TAGGED] -> (t:Tweet)-[:USING] -> (s:Source) where h.name = "obama"  RETURN s as Source_Name, count(t) as Tweet_Count ORDER BY Tweet_Count DESC LIMIT 10;

# List the top tweeting user for state X for a hash tag Y.

MATCH (h:Hashtag)-[TAGGED]->(t)<-[POSTED]-(u:User) WHERE h.name = "obama" and t.retweeted = false return count(t) AS Count,u.name AS User order by Count desc Limit 10;


# Return the maximum count of tweet using certain hash tag, by a user who has maximum followers.

MATCH (u:User)-[POSTED]->(t:Tweet)<-[TAGGED]-(h:Hashtag) WITH u ORDER BY u.followers DESC LIMIT 1 MATCH (u)-[POSTED]->(t:Tweet)<-[TAGGED]-(h:Hashtag) where h.name = "Obama" return count(t) as Count order by Count desc limit 1;

# print the verified users for a particular hashtag.


match (h:Hashtag)-[TAGGED]->(t:Tweet)<-[:POSTED]-(u:User) where h.name='Obama' and u.verified=true return count(u);







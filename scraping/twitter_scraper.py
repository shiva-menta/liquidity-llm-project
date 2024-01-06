from tweety import Twitter

#Function to sort the tweets in descending order (present to past)
def sort_tweets(tweets):
    tweet_ids = [( tweet.id, tweet ) for tweet in tweets]
    tweet_ids.sort(reverse=True)
    return [tweet for id, tweet in tweet_ids]

#Get tweets of a particular user
app = Twitter("session")
user = app.get_user_info(username="FinanceHammer")

#Returns a maximum of 100 tweets at a time
#replies = True parameter in get_tweets is giving an error
tweets = app.get_tweets(username = user)
sorted_tweets = sort_tweets(tweets)
print(sorted_tweets[:5])

i=0
for tweet in tweets:
    print(type(tweet))
    print(tweet)
    print(tweet.text)

    # get_comments() function giving an error
    # comments = tweet.get_comments()
    # for comment in comments:
    #     print(comment)

    print("________________________________________________________________")

    #Remove this condition when scraping all tweets
    if i>5:
        break
    i+=1

#Need to be logged in to use other functionalities
#Enter twitter username and password
username = ""
password = ""
app.sign_in(username, password)
print(app.user)

print("________________________________________________________________")
print("________________________________________________________________")

#Search tweets based on keyword
search_tweets = app.search('SVB')
for tweet in tweets:
    print(tweet)
    print(tweet.text)
    break
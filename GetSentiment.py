import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 

class TwitterClient(object): 
    ''' 
    Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
     
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'vbZpnPT4wH73Bm6HdQi1deIvC'
        consumer_secret = 'NiieP39shq08TIQbqKkBojiVzKSIetXHuWFpBGupkp7G1zincF'
        access_token = '291262752-7WmW9GYXJ92hykLSJiHiRrfGwRcotfuH9h9x0gaR'
        access_token_secret = 'FPKdS0aLV9Ctks5ZcFebidCH49VQjIy1zmGwirP0DIdoZ'
  
        # attempt authentication 
        try:        
            self.auth = OAuthHandler(consumer_key, consumer_secret)        
            self.auth.set_access_token(access_token, access_token_secret)       
            self.api = tweepy.API(self.auth)
			#Filter with location of lebanon
            GEOBOX_Lebanon = [34.7721449721,33.0673855135,36.6074569833,34.7015692408]
            twitterStream = Stream(auth, listener())
            twitterStream.filter(locations = GEOBOX_Lebanon )            
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        #Clean tweet by regex statements.
        return ' '.join(re.sub("(@[A-Za-z0-9]+) | (^[0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ",tweet).split() )
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 50): 
         
        #Main function to fetch tweets and parse them. 
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
            for tweet in fetched_tweets: 
                parsed_tweet = {} 
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
					else: 
                    tweets.append(parsed_tweet) 
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  
def main(): 
    api = TwitterClient() 
    # calling function to get tweets wihtout retweets
    tweets = api.get_tweets(query = 'Corona'+ '-filter:retweets' , count = 200) 
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
  
    # printing first X positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:20]: 
        print(tweet['text']) 
  
    # printing first X negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:20]: 
        print(tweet['text']) 
  
if __name__ == "__main__": 
    # calling main function 
    main() 
	
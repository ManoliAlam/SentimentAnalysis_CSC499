import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import matplotlib.pyplot as plt 

class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'vbZpnPT4wH73Bm6HdQi1deIvC'
        consumer_secret = 'NiieP39shq08TIQbqKkBojiVzKSIetXHuWFpBGupkp7G1zincF'
        access_token = '291262752-7WmW9GYXJ92hykLSJiHiRrfGwRcotfuH9h9x0gaR'
        access_token_secret = 'FPKdS0aLV9Ctks5ZcFebidCH49VQjIy1zmGwirP0DIdoZ'
  
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth)
           
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+) | (^[0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ",tweet).split() )

    def translator(user_string):
     user_string = user_string.split(" ")
     j = 0
     for _str in user_string:
        # File path which consists of Abbreviations.
        fileName = "/Users/JDSeo/Desktop/Daily-Neural-Network-Practice-2/NLP/cleaning/slang.txt"

        # File Access mode [Read Mode]
        with open(fileName, "r") as myCSVfile:
            # Reading file as CSV with delimiter as "=", so that abbreviation are stored in row[0] and phrases in row[1]
            dataFromFile = csv.reader(myCSVfile, delimiter="=")
            # Removing Special Characters.
            _str = re.sub('[^a-zA-Z0-9]+', '', _str)
            for row in dataFromFile:
                # Check if selected word matches short forms[LHS] in text file.
                if _str.upper() == row[0]:
                    # If match found replace it with its appropriate phrase in text file.
                    user_string[j] = row[1]
            myCSVfile.close()
        j = j + 1
     return ' '.join(user_string)  

    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
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
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets
        tweets = [] 
    
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
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
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
 
    tweets = api.get_tweets(query = 'corona', count = 200)
    
    
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 

      

    stop_words = set(stopwords.words('english'))
    # printing first 5 positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:50]: 
      #Remove stop words then print
      word_tokens = word_tokenize(tweet['text'])
      filtered_tweet = [w for w in word_tokens if not w in stop_words]
      filtered_tweet = [] 
  
      for w in word_tokens: 
        if w not in stop_words: 
          filtered_tweet.append(w) 

      filtered_tweet = (" ").join(filtered_tweet)
      print(filtered_tweet)

      #Print without stop words
      #print(tweet['text'])
  
    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:50]: 
     #Remove stop words then print
      word_tokens = word_tokenize(tweet['text'])
      filtered_tweet = [w for w in word_tokens if not w in stop_words]
      filtered_tweet = [] 
  
      for w in word_tokens: 
        if w not in stop_words: 
          filtered_tweet.append(w) 

      filtered_tweet = (" ").join(filtered_tweet)
      print(filtered_tweet) 

      #Print without stop words
      #print(tweet['text']) 
      
   

if __name__ == "__main__": 
    # calling main function 
    main() 
	

import tweepy
import pandas as pd
import json
import config
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# Lists to hold sentiments
compound_list = []
positive_list = []
negative_list = []
neutral_list = []
mention_list = []          

#plot the results function to call in PlotBot   
def plot_create(dataframe, term, author):
    plt.plot(dataframe.index, dataframe["Compound"], marker="o", alpha=.5 )
    plt.xlim(500, 0)
    plt.ylim(-1,1)
    plt.grid(linestyle='--')
    plt.xlabel("Tweets Ago")
    plt.ylabel("Tweet Polarity")
    plt.title("Sentiment Analysis of " + term + " Tweets")
    #replace with savefig to tweet out
    plot_name = term + "_plot.jpg"
    plt.savefig(plot_name)

    #tweet the figure out
    api.update_with_media(plot_name, 
                          "New Tweet Analysis {}: Thank you @{}!".format(term, author))
    
    print ("Plotted {} and Tweeted {} Successfully".format(term, author))

    
    #plt.show()

    return

def PlotBot():
    
    #target_term = ""

    """Search for mentions of @anselm0_jr, then extract the target_term to analyze, graph, and retweet"""
    #search for the most recent tweet directed to account
    mentions = api.mentions_timeline(count = 1)
    for mention in mentions:
        #print(json.dumps(mention, sort_keys=True, indent=4, separators=(',', ': ')))
        #check to see if index value with second mention exists
        if len(mention["entities"]["user_mentions"]) == 2:
                        
            if mention["id"] in mention_list:
                    
                print ("No new mentions.")
                            
                return
                        
            else:
                target_term = "@" + mention["entities"]["user_mentions"][1]["screen_name"]
                tweet_author = mention["user"]["screen_name"]
                #last_id = mention["id"]
                mention_list.append(mention["id"])
            
                break
    
        else:
            tweet_author = mention["user"]["screen_name"]
        
            print("You were mentioned by @" + tweet_author +", but no new requests for PlotBot")
                
            return

    #break
    
    oldest_tweet = ""
    sent_df = None
    
    #search for the most recent 500 tweets directed to account
    for x in range(5):
    
        public_tweets = api.search(target_term, count=100, result_type="recent", max_id = oldest_tweet)    
        
        # Loop through all tweets
        for tweet in public_tweets["statuses"]:
                    
            #print(json.dumps(tweet, sort_keys=True, indent=4, separators=(',', ': ')))
                
            # Run Vader Analysis on each tweet
            results = analyzer.polarity_scores(tweet["text"])
            compound = results["compound"]
            pos = results["pos"]
            neu = results["neu"]
            neg = results["neg"]

            # Add each value to the appropriate array
            compound_list.append(compound)
            positive_list.append(pos)
            negative_list.append(neg)
            neutral_list.append(neu)
        
            #create the graph (external function perhaps)
            # Store the Average Sentiments
            sentiment = {"Compound": compound_list,
                         "Positive": positive_list,
                         "Neutral": negative_list,
                         "Negative": neutral_list}
            
            sent_df = None
        
            sent_df = pd.DataFrame.from_dict(sentiment).sort_index(ascending=False)
            
            
            # Reassign the the oldest tweet (i.e. the max_id)
            oldest_tweet = tweet["id_str"]
                    
    return plot_create(sent_df, target_term, tweet_author)
    


def clear_sentiments():
    del compound_list[:]
    del positive_list[:]
    del negative_list[:]
    del neutral_list[:]
    
    return

# Set timer to run every minute for 5 minutes max
t_end = time.time() + (60 * 60)

while time.time() < t_end:
    #mention_checker()
    PlotBot()
    clear_sentiments()
    time.sleep(60)


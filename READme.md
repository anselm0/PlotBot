

```python
import tweepy
import requests as req
import pandas as pd
import json
import config
import numpy as np
import time
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

```


```python
def mention_checker():
        
    """function checks to see when most recent tweet was directed to account, then extract
    the new target phrase to graph"""
    
    #search for the most recent tweet directed to account
    mentions = api.mentions_timeline(count = 1)
    
    try:

        for mention in mentions:
            #print(json.dumps(mention, sort_keys=True, indent=4, separators=(',', ': ')))

            #check to see if index value with second mention exists
            if len(mention["entities"]["user_mentions"]) == 2:
                analyze_term = "@" + mention["entities"]["user_mentions"][1]["screen_name"]
                tweet_author = mention["user"]["screen_name"]
                last_id = mention["id"]

                return (last_id, tweet_author, analyze_term)
            else:
                tweet_author = mention["user"]["screen_name"]
                print("You were mentioned by @" + tweet_author +", but no new requests for PlotBot")
                
                continue
        
    except Exception:
        print ("No new mention.")                
    

```


```python
def PlotBot(target_term):
    
    """Search for mentions of @anselm0_jr, then extract the target_term to analyze, graph, and retweet"""
    original_id = last_id
    
    oldest_tweet = ""
    
    for x in range(5):
    
        #search for the most recent 500 tweets directed to account
        public_tweets = api.search(target_term, count=100, result_type="recent", max_id = oldest_tweet)    
        
        # Loop through all tweets
        for tweet in public_tweets["statuses"]:
            
            #tweet_id = tweet["id"]
        
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
        
            sent_df = pd.DataFrame.from_dict(sentiment).sort_index(ascending=False)
            
            
            # Reassign the the oldest tweet (i.e. the max_id)
            oldest_tweet = tweet["id_str"]
                    
    return sent_df
    
```


```python
last_id, tweet_author, analyze_term = mention_checker()

PlotBot(analyze_term)
```

    {
        "contributors": null,
        "coordinates": null,
        "created_at": "Thu Mar 08 00:11:46 +0000 2018",
        "entities": {
            "hashtags": [],
            "symbols": [],
            "urls": [],
            "user_mentions": [
                {
                    "id": 78106821,
                    "id_str": "78106821",
                    "indices": [
                        0,
                        11
                    ],
                    "name": "Anselmo Garza Jr",
                    "screen_name": "anselm0_jr"
                },
                {
                    "id": 1367531,
                    "id_str": "1367531",
                    "indices": [
                        21,
                        29
                    ],
                    "name": "Fox News",
                    "screen_name": "FoxNews"
                }
            ]
        },
        "favorite_count": 0,
        "favorited": false,
        "geo": null,
        "id": 971538931991941120,
        "id_str": "971538931991941120",
        "in_reply_to_screen_name": "anselm0_jr",
        "in_reply_to_status_id": null,
        "in_reply_to_status_id_str": null,
        "in_reply_to_user_id": 78106821,
        "in_reply_to_user_id_str": "78106821",
        "is_quote_status": false,
        "lang": "en",
        "place": null,
        "retweet_count": 0,
        "retweeted": false,
        "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
        "text": "@anselm0_jr Analyze: @FoxNews",
        "truncated": false,
        "user": {
            "contributors_enabled": false,
            "created_at": "Tue Feb 10 22:33:53 +0000 2015",
            "default_profile": true,
            "default_profile_image": false,
            "description": "",
            "entities": {
                "description": {
                    "urls": []
                }
            },
            "favourites_count": 38,
            "follow_request_sent": false,
            "followers_count": 51,
            "following": false,
            "friends_count": 133,
            "geo_enabled": false,
            "has_extended_profile": false,
            "id": 3028935389,
            "id_str": "3028935389",
            "is_translation_enabled": false,
            "is_translator": false,
            "lang": "en",
            "listed_count": 1,
            "location": "",
            "name": "freedumbbell",
            "notifications": false,
            "profile_background_color": "C0DEED",
            "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
            "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
            "profile_background_tile": false,
            "profile_banner_url": "https://pbs.twimg.com/profile_banners/3028935389/1441940456",
            "profile_image_url": "http://pbs.twimg.com/profile_images/565278209894125568/w8O0YHoM_normal.png",
            "profile_image_url_https": "https://pbs.twimg.com/profile_images/565278209894125568/w8O0YHoM_normal.png",
            "profile_link_color": "1DA1F2",
            "profile_sidebar_border_color": "C0DEED",
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_text_color": "333333",
            "profile_use_background_image": true,
            "protected": false,
            "screen_name": "freedumbbell",
            "statuses_count": 276,
            "time_zone": "Central Time (US & Canada)",
            "translator_type": "none",
            "url": null,
            "utc_offset": -21600,
            "verified": false
        }
    }





<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Compound</th>
      <th>Negative</th>
      <th>Neutral</th>
      <th>Positive</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>499</th>
      <td>-0.5719</td>
      <td>0.821</td>
      <td>0.179</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>498</th>
      <td>-0.8020</td>
      <td>0.647</td>
      <td>0.353</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>497</th>
      <td>-0.3612</td>
      <td>0.693</td>
      <td>0.186</td>
      <td>0.121</td>
    </tr>
    <tr>
      <th>496</th>
      <td>-0.5719</td>
      <td>0.821</td>
      <td>0.179</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>495</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>494</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>493</th>
      <td>-0.5106</td>
      <td>0.645</td>
      <td>0.355</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>492</th>
      <td>0.3361</td>
      <td>0.695</td>
      <td>0.094</td>
      <td>0.211</td>
    </tr>
    <tr>
      <th>491</th>
      <td>-0.2406</td>
      <td>0.836</td>
      <td>0.164</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>490</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>489</th>
      <td>-0.3612</td>
      <td>0.800</td>
      <td>0.200</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>488</th>
      <td>0.3832</td>
      <td>0.852</td>
      <td>0.000</td>
      <td>0.148</td>
    </tr>
    <tr>
      <th>487</th>
      <td>-0.1280</td>
      <td>0.933</td>
      <td>0.067</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>486</th>
      <td>-0.5719</td>
      <td>0.821</td>
      <td>0.179</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>485</th>
      <td>-0.5859</td>
      <td>0.730</td>
      <td>0.270</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>484</th>
      <td>-0.2732</td>
      <td>0.718</td>
      <td>0.167</td>
      <td>0.115</td>
    </tr>
    <tr>
      <th>483</th>
      <td>0.0516</td>
      <td>0.728</td>
      <td>0.131</td>
      <td>0.141</td>
    </tr>
    <tr>
      <th>482</th>
      <td>0.2924</td>
      <td>0.757</td>
      <td>0.097</td>
      <td>0.146</td>
    </tr>
    <tr>
      <th>481</th>
      <td>0.0772</td>
      <td>0.939</td>
      <td>0.000</td>
      <td>0.061</td>
    </tr>
    <tr>
      <th>480</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>479</th>
      <td>-0.7906</td>
      <td>0.720</td>
      <td>0.280</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>478</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>477</th>
      <td>0.6908</td>
      <td>0.787</td>
      <td>0.000</td>
      <td>0.213</td>
    </tr>
    <tr>
      <th>476</th>
      <td>-0.3612</td>
      <td>0.800</td>
      <td>0.200</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>475</th>
      <td>0.4585</td>
      <td>0.813</td>
      <td>0.000</td>
      <td>0.187</td>
    </tr>
    <tr>
      <th>474</th>
      <td>-0.4810</td>
      <td>0.779</td>
      <td>0.221</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>473</th>
      <td>-0.8166</td>
      <td>0.728</td>
      <td>0.272</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>472</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>471</th>
      <td>0.0516</td>
      <td>0.728</td>
      <td>0.131</td>
      <td>0.141</td>
    </tr>
    <tr>
      <th>470</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>29</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>28</th>
      <td>0.3818</td>
      <td>0.729</td>
      <td>0.000</td>
      <td>0.271</td>
    </tr>
    <tr>
      <th>27</th>
      <td>-0.7725</td>
      <td>0.758</td>
      <td>0.242</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>26</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>25</th>
      <td>-0.4724</td>
      <td>0.745</td>
      <td>0.255</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>24</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>23</th>
      <td>-0.6486</td>
      <td>0.719</td>
      <td>0.281</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>22</th>
      <td>0.5927</td>
      <td>0.839</td>
      <td>0.000</td>
      <td>0.161</td>
    </tr>
    <tr>
      <th>21</th>
      <td>0.1280</td>
      <td>0.685</td>
      <td>0.123</td>
      <td>0.192</td>
    </tr>
    <tr>
      <th>20</th>
      <td>-0.6908</td>
      <td>0.773</td>
      <td>0.227</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>19</th>
      <td>0.4019</td>
      <td>0.828</td>
      <td>0.000</td>
      <td>0.172</td>
    </tr>
    <tr>
      <th>18</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>17</th>
      <td>-0.5255</td>
      <td>0.702</td>
      <td>0.298</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>16</th>
      <td>-0.3612</td>
      <td>0.743</td>
      <td>0.156</td>
      <td>0.100</td>
    </tr>
    <tr>
      <th>15</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>14</th>
      <td>-0.8020</td>
      <td>0.573</td>
      <td>0.427</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>13</th>
      <td>-0.3612</td>
      <td>0.800</td>
      <td>0.200</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>12</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>11</th>
      <td>0.8225</td>
      <td>0.752</td>
      <td>0.000</td>
      <td>0.248</td>
    </tr>
    <tr>
      <th>10</th>
      <td>-0.2411</td>
      <td>0.849</td>
      <td>0.151</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>8</th>
      <td>-0.8166</td>
      <td>0.728</td>
      <td>0.272</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>7</th>
      <td>-0.5719</td>
      <td>0.821</td>
      <td>0.179</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>6</th>
      <td>-0.4215</td>
      <td>0.781</td>
      <td>0.219</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-0.5709</td>
      <td>0.791</td>
      <td>0.209</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>-0.7184</td>
      <td>0.727</td>
      <td>0.273</td>
      <td>0.000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.3400</td>
      <td>0.833</td>
      <td>0.000</td>
      <td>0.167</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.7351</td>
      <td>0.526</td>
      <td>0.000</td>
      <td>0.474</td>
    </tr>
    <tr>
      <th>0</th>
      <td>0.0000</td>
      <td>1.000</td>
      <td>0.000</td>
      <td>0.000</td>
    </tr>
  </tbody>
</table>
<p>500 rows × 4 columns</p>
</div>




```python
#plot the results   
def plot_create(dataframe):
    plt.plot(dataframe.index, dataframe["Compound"], marker="o" )
    plt.xlim(500, 0)
    plt.ylim(-1,1)
    plt.grid(linestyle='--')
    plt.xlabel("Tweets Ago")
    plt.ylabel("Tweet Polarity")
    plt.title("Sentiment Analysis of " + analyze_term + " Tweets")
    #replace with savefig to tweet out
    plt.show()

```


```python
plot_create(df)
```


![png](output_5_0.png)



```python
last_id = None

# Set timer
#t_end = time.time() + 60 * 5
#while time.time() < t_end:
#    print("Last", last_id)
last_id = PlotBot(mention_check())
    #time.sleep(60)
```

    {
        "contributors": null,
        "coordinates": null,
        "created_at": "Thu Mar 08 00:11:46 +0000 2018",
        "entities": {
            "hashtags": [],
            "symbols": [],
            "urls": [],
            "user_mentions": [
                {
                    "id": 78106821,
                    "id_str": "78106821",
                    "indices": [
                        0,
                        11
                    ],
                    "name": "Anselmo Garza Jr",
                    "screen_name": "anselm0_jr"
                },
                {
                    "id": 1367531,
                    "id_str": "1367531",
                    "indices": [
                        21,
                        29
                    ],
                    "name": "Fox News",
                    "screen_name": "FoxNews"
                }
            ]
        },
        "favorite_count": 0,
        "favorited": false,
        "geo": null,
        "id": 971538931991941120,
        "id_str": "971538931991941120",
        "in_reply_to_screen_name": "anselm0_jr",
        "in_reply_to_status_id": null,
        "in_reply_to_status_id_str": null,
        "in_reply_to_user_id": 78106821,
        "in_reply_to_user_id_str": "78106821",
        "is_quote_status": false,
        "lang": "en",
        "metadata": {
            "iso_language_code": "en",
            "result_type": "recent"
        },
        "place": null,
        "retweet_count": 0,
        "retweeted": false,
        "source": "<a href=\"http://twitter.com/download/iphone\" rel=\"nofollow\">Twitter for iPhone</a>",
        "text": "@anselm0_jr Analyze: @FoxNews",
        "truncated": false,
        "user": {
            "contributors_enabled": false,
            "created_at": "Tue Feb 10 22:33:53 +0000 2015",
            "default_profile": true,
            "default_profile_image": false,
            "description": "",
            "entities": {
                "description": {
                    "urls": []
                }
            },
            "favourites_count": 38,
            "follow_request_sent": false,
            "followers_count": 51,
            "following": false,
            "friends_count": 133,
            "geo_enabled": false,
            "has_extended_profile": false,
            "id": 3028935389,
            "id_str": "3028935389",
            "is_translation_enabled": false,
            "is_translator": false,
            "lang": "en",
            "listed_count": 1,
            "location": "",
            "name": "freedumbbell",
            "notifications": false,
            "profile_background_color": "C0DEED",
            "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
            "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
            "profile_background_tile": false,
            "profile_banner_url": "https://pbs.twimg.com/profile_banners/3028935389/1441940456",
            "profile_image_url": "http://pbs.twimg.com/profile_images/565278209894125568/w8O0YHoM_normal.png",
            "profile_image_url_https": "https://pbs.twimg.com/profile_images/565278209894125568/w8O0YHoM_normal.png",
            "profile_link_color": "1DA1F2",
            "profile_sidebar_border_color": "C0DEED",
            "profile_sidebar_fill_color": "DDEEF6",
            "profile_text_color": "333333",
            "profile_use_background_image": true,
            "protected": false,
            "screen_name": "freedumbbell",
            "statuses_count": 276,
            "time_zone": "Central Time (US & Canada)",
            "translator_type": "none",
            "url": null,
            "utc_offset": -21600,
            "verified": false
        }
    }



    ---------------------------------------------------------------------------

    UnboundLocalError                         Traceback (most recent call last)

    <ipython-input-618-a7b29b3bae06> in <module>()
          5 #while time.time() < t_end:
          6 #    print("Last", last_id)
    ----> 7 last_id = PlotBot(mention_check())
          8     #time.sleep(60)


    <ipython-input-614-8c45b004f185> in PlotBot(target_term)
         44             oldest_tweet = tweet["id_str"]
         45 
    ---> 46     return sent_df
         47 


    UnboundLocalError: local variable 'sent_df' referenced before assignment



```python
def reply(figure):
    #tweeting media
    api.update_with_media("too-much-big-data.jpg",
                      f"Thank you @{tweet_author}!",
                in_reply_to_status_id=original_id)
```


```python
last_id = None
#timer
while(True):
    PlotBot()
    time.sleep(300)
```

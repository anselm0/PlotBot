

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

mention_list = []
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
                
                if mention["entities"]["user_mentions"][1]["screen_name"] in mention_list:
                    print ("This has already been Analyzed, here is the plot: return stored plot here")
                else:
                    analyze_term = "@" + mention["entities"]["user_mentions"][1]["screen_name"]
                    tweet_author = mention["user"]["screen_name"]
                    last_id = mention["id"]
                    mention_list.append(analyze_term)

                    return (last_id, tweet_author, analyze_term)
            else:
                tweet_author = mention["user"]["screen_name"]
                print("You were mentioned by @" + tweet_author +", but no new requests for PlotBot")
                
                continue
        
    except Exception:
        print ("No new mention.")                
    

```


```python
#plot the results function to call in PlotBot   
def plot_create(dataframe):
    plt.plot(dataframe.index, dataframe["Compound"], marker="o", alpha=.5 )
    plt.xlim(500, 0)
    plt.ylim(-1,1)
    plt.grid(linestyle='--')
    plt.xlabel("Tweets Ago")
    plt.ylabel("Tweet Polarity")
    plt.title("Sentiment Analysis of " + analyze_term + " Tweets")
    #replace with savefig to tweet out
    plot_name = analyze_term + "_plot.jpg"
    plt.savefig(plot_name)
    
    #tweet the figure out
    api.update_with_media(plot_name, 
                          f"New Tweet Analysis {analyze_term}: Thank you @{tweet_author}!")
    
    #plt.show()

```


```python
def PlotBot(target_term):
    
    """Search for mentions of @anselm0_jr, then extract the target_term to analyze, graph, and retweet"""
    
    oldest_tweet = ""
    
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
        
            sent_df = pd.DataFrame.from_dict(sentiment).sort_index(ascending=False)
            
            
            # Reassign the the oldest tweet (i.e. the max_id)
            oldest_tweet = tweet["id_str"]
                    
    return plot_create(sent_df)
    
```


```python
def clear_sentiments():
    compound_list = []
    positive_list = []
    negative_list = []
    neutral_list = []
```


```python
# Set timer to run every minute for 5 minutes max
t_end = time.time() + (60 * 5)

while time.time() < t_end:
    last_id, tweet_author, analyze_term = mention_checker()
    PlotBot(analyze_term)
    clear_sentiments()
    time.sleep(60)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/urllib3/connectionpool.py in _make_request(self, conn, method, url, timeout, chunked, **httplib_request_kw)
        379             try:  # Python 2.7, use buffering of HTTP responses
    --> 380                 httplib_response = conn.getresponse(buffering=True)
        381             except TypeError:  # Python 2.6 and older, Python 3


    TypeError: getresponse() got an unexpected keyword argument 'buffering'

    
    During handling of the above exception, another exception occurred:


    WantReadError                             Traceback (most recent call last)

    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/urllib3/contrib/pyopenssl.py in recv_into(self, *args, **kwargs)
        279         try:
    --> 280             return self.connection.recv_into(*args, **kwargs)
        281         except OpenSSL.SSL.SysCallError as e:


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/OpenSSL/SSL.py in recv_into(self, buffer, nbytes, flags)
       1624             result = _lib.SSL_read(self._ssl, buf, nbytes)
    -> 1625         self._raise_ssl_error(self._ssl, result)
       1626 


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/OpenSSL/SSL.py in _raise_ssl_error(self, ssl, result)
       1430         if error == _lib.SSL_ERROR_WANT_READ:
    -> 1431             raise WantReadError()
       1432         elif error == _lib.SSL_ERROR_WANT_WRITE:


    WantReadError: 

    
    During handling of the above exception, another exception occurred:


    KeyboardInterrupt                         Traceback (most recent call last)

    <ipython-input-98-538391a5ae65> in <module>()
          4 while time.time() < t_end:
          5     last_id, tweet_author, analyze_term = mention_checker()
    ----> 6     PlotBot(analyze_term)
          7     clear_sentiments()
          8     time.sleep(60)


    <ipython-input-94-9d182748a162> in PlotBot(target_term)
          8 
          9         #search for the most recent 500 tweets directed to account
    ---> 10         public_tweets = api.search(target_term, count=100, result_type="recent", max_id = oldest_tweet)
         11 
         12         # Loop through all tweets


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/tweepy/binder.py in _call(*args, **kwargs)
        243             return method
        244         else:
    --> 245             return method.execute()
        246 
        247     # Set pagination mode


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/tweepy/binder.py in execute(self)
        185                                                 timeout=self.api.timeout,
        186                                                 auth=auth,
    --> 187                                                 proxies=self.api.proxy)
        188                 except Exception as e:
        189                     raise TweepError('Failed to send request: %s' % e)


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/requests/sessions.py in request(self, method, url, params, data, headers, cookies, files, auth, timeout, allow_redirects, proxies, hooks, stream, verify, cert, json)
        506         }
        507         send_kwargs.update(settings)
    --> 508         resp = self.send(prep, **send_kwargs)
        509 
        510         return resp


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/requests/sessions.py in send(self, request, **kwargs)
        616 
        617         # Send the request
    --> 618         r = adapter.send(request, **kwargs)
        619 
        620         # Total elapsed time of the request (approximately)


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/requests/adapters.py in send(self, request, stream, timeout, verify, cert, proxies)
        438                     decode_content=False,
        439                     retries=self.max_retries,
    --> 440                     timeout=timeout
        441                 )
        442 


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/urllib3/connectionpool.py in urlopen(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, body_pos, **response_kw)
        599                                                   timeout=timeout_obj,
        600                                                   body=body, headers=headers,
    --> 601                                                   chunked=chunked)
        602 
        603             # If we're going to release the connection in ``finally:``, then


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/urllib3/connectionpool.py in _make_request(self, conn, method, url, timeout, chunked, **httplib_request_kw)
        381             except TypeError:  # Python 2.6 and older, Python 3
        382                 try:
    --> 383                     httplib_response = conn.getresponse()
        384                 except Exception as e:
        385                     # Remove the TypeError from the exception chain in Python 3;


    ~/anaconda/envs/PythonData/lib/python3.6/http/client.py in getresponse(self)
       1329         try:
       1330             try:
    -> 1331                 response.begin()
       1332             except ConnectionError:
       1333                 self.close()


    ~/anaconda/envs/PythonData/lib/python3.6/http/client.py in begin(self)
        295         # read until we get a non-100 response
        296         while True:
    --> 297             version, status, reason = self._read_status()
        298             if status != CONTINUE:
        299                 break


    ~/anaconda/envs/PythonData/lib/python3.6/http/client.py in _read_status(self)
        256 
        257     def _read_status(self):
    --> 258         line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
        259         if len(line) > _MAXLINE:
        260             raise LineTooLong("status line")


    ~/anaconda/envs/PythonData/lib/python3.6/socket.py in readinto(self, b)
        584         while True:
        585             try:
    --> 586                 return self._sock.recv_into(b)
        587             except timeout:
        588                 self._timeout_occurred = True


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/urllib3/contrib/pyopenssl.py in recv_into(self, *args, **kwargs)
        290                 raise
        291         except OpenSSL.SSL.WantReadError:
    --> 292             rd = util.wait_for_read(self.socket, self.socket.gettimeout())
        293             if not rd:
        294                 raise timeout('The read operation timed out')


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/urllib3/util/wait.py in wait_for_read(socks, timeout)
         31     or optionally a single socket if passed in. Returns a list of
         32     sockets that can be read from immediately. """
    ---> 33     return _wait_for_io_events(socks, EVENT_READ, timeout)
         34 
         35 


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/urllib3/util/wait.py in _wait_for_io_events(socks, events, timeout)
         24             selector.register(sock, events)
         25         return [key[0].fileobj for key in
    ---> 26                 selector.select(timeout) if key[1] & events]
         27 
         28 


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/urllib3/util/selectors.py in select(self, timeout)
        511 
        512             kevent_list = _syscall_wrapper(self._kqueue.control, True,
    --> 513                                            None, max_events, timeout)
        514 
        515             for kevent in kevent_list:


    ~/anaconda/envs/PythonData/lib/python3.6/site-packages/urllib3/util/selectors.py in _syscall_wrapper(func, _, *args, **kwargs)
         62         and recalculate their timeouts. """
         63         try:
    ---> 64             return func(*args, **kwargs)
         65         except (OSError, IOError, select.error) as e:
         66             errcode = None


    KeyboardInterrupt: 



```python

```

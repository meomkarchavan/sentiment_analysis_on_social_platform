import tweepy
import time
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import date
from datetime import timedelta
class Twitter():
    def __init__(self):
        self.auth=tweepy.OAuthHandler(os.getenv('api_key'), os.getenv('api_secret_key'))
        self.auth.set_access_token(os.getenv("access_token"), os.getenv("access_token_secret"))
        self.api = tweepy.API(self.auth)
        self.sleep_time=60 * 15
    
    def get_tweets(self,search_keywords,max_tweets=1000,is_first_run=False):
        print('Getting Tweets')
        searched_tweets = []
        last_id = -1
        if is_first_run:    
            for i in range(0,6):
                date_until=(date.today() - timedelta(days=i)).strftime('%Y-%m-%d')
                date_since=(date.today() - timedelta(days=i+1)).strftime('%Y-%m-%d')
                while len(searched_tweets) < max_tweets:
                    count = max_tweets - len(searched_tweets)
                    try:
                        new_tweets = self.api.search(q=search_keywords,
                                                    count=count,
                                                    since=date_since,
                                                    until=date_until,
                                                    max_id=str(last_id - 1))
                        if not new_tweets:
                            break
                        searched_tweets.extend(new_tweets)
                        last_id = new_tweets[-1].id
                    except tweepy.TweepError:
                        print('sleeping')
                        time.sleep(self.sleep_time)
                        continue
                    except StopIteration:
                        break
        else:
            while len(searched_tweets) < max_tweets:
                count = max_tweets - len(searched_tweets)
                try:
                    new_tweets = self.api.search(q=search_keywords,
                                                count=count,
                                                max_id=str(last_id - 1))
                    if not new_tweets:
                        break
                    searched_tweets.extend(new_tweets)
                    last_id = new_tweets[-1].id
                except tweepy.TweepError:
                    print('sleeping')
                    time.sleep(self.sleep_time)
                    continue
                except StopIteration:
                    break
        tweeter_data= [[tweet.created_at,tweet.user.screen_name, tweet.user.location,tweet.text] for tweet in searched_tweets]
        tweet_df = pd.DataFrame(data=tweeter_data, 
                    columns=['date','user', "location","comment"])
        return tweet_df
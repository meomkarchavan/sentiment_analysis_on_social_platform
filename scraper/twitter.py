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
        
        if is_first_run:
            max_tweets = 200
            all_tweets=[]
            for i in range(5,-1,-1):
                date_until=(date.today() - timedelta(days=i)).strftime('%Y-%m-%d')
                date_since=(date.today() - timedelta(days=i+1)).strftime('%Y-%m-%d')
                print(date_since,date_until)
                last_id = -1
                searched_tweets = []

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
                        all_tweets.extend(searched_tweets)
                        last_id = new_tweets[-1].id
                    except tweepy.TweepError:
                        print('sleeping')
                        time.sleep(60 * 15)
                        continue
                    except StopIteration:
                        break
        else:
            all_tweets = []
            last_id = -1
            while len(all_tweets) < max_tweets:
                count = max_tweets - len(all_tweets)
                try:
                    new_tweets = self.api.search(q=search_keywords,
                                                count=count,
                                                max_id=str(last_id - 1))
                    if not new_tweets:
                        break
                    all_tweets.extend(new_tweets)
                    last_id = new_tweets[-1].id
                except tweepy.TweepError:
                    print('sleeping')
                    time.sleep(self.sleep_time)
                    continue
                except StopIteration:
                    break
        tweeter_data= [[tweet.created_at,tweet.user.screen_name, tweet.user.location,tweet.text] for tweet in all_tweets]
        tweet_df = pd.DataFrame(data=tweeter_data, 
                    columns=['date','user', "location","comment"])
        return tweet_df
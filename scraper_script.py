import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from scraper.twitter import Twitter
from scraper.reddit import Reddit
from scraper.youtube import Youtube
from helpers.helpers import read_and_concat
from datetime import datetime

def main():
    main_path=os.path.abspath(os.getenv('data_path'))
    keywords_list=pd.read_csv(os.getenv('keyword_csv_path'))['keywords'].to_list()
    twitter=Twitter()
    reddit=Reddit()
    youtube=Youtube()
    for keywords in keywords_list:
        path=(os.path.abspath(os.path.join(main_path,'_'.join(keywords.split()),'raw')))
        os.makedirs(path, exist_ok=True)
        twitter_df=twitter.get_tweets(search_keywords=keywords,max_tweets=1000)
        twitter_path=os.path.abspath(os.path.join(path,f'twitter{datetime.now().date()}.csv'))
        if os.path.exists(twitter_path):
            read_and_concat(twitter_path,twitter_df,'date')
        else:
            twitter_df.to_csv(twitter_path)
        reddit_df=reddit.get_post(search_keywords=keywords)
        reddit_path=os.path.abspath(os.path.join(path,f'reddit{datetime.now().date()}.csv'))
        if os.path.exists(reddit_path):
            read_and_concat(reddit_path,reddit_df,'date')
        else:
            reddit_df.to_csv(reddit_path)
        
        youtube_df=youtube.get_comments(search_keywords=keywords)
        youtube_path=os.path.abspath(os.path.join(path,f'youtube{datetime.now().date()}.csv'))
        if os.path.exists(youtube_path):
            read_and_concat(youtube_path,youtube_df,date_column=None)
        else:
            youtube_df.to_csv(youtube_path)

if __name__=='__main__':
    main()
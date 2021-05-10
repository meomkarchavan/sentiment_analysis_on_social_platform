from datetime import datetime
from helpers.helpers import read_and_clean_csv, read_and_concat
from helpers.analyzer import Analyzer
import pandas as pd
import os
import datetime as dt

analyzer=Analyzer()
from dotenv import load_dotenv
load_dotenv()
from os.path import exists
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
def main():
    main_path=os.path.abspath(os.getenv('data_path'))
    keywords_list=pd.read_csv(os.getenv('keyword_csv_path'))['keywords'].to_list()
    for keywords in keywords_list:
        save_path=(os.path.abspath(os.path.join(main_path,'_'.join(keywords.split()),'analyzed')))
        os.makedirs(save_path, exist_ok=True)
        file_path=(os.path.abspath(os.path.join(main_path,'_'.join(keywords.split()),'raw')))
        os.makedirs(file_path, exist_ok=True)
        
        twitter_path=os.path.abspath(os.path.join(file_path,f'twitter{datetime.now().date()}.csv'))
        if exists(twitter_path):
            twitter_df=read_and_clean_csv(twitter_path,'date')
            twitter_df=analyzer.clean_and_analyze(twitter_df,'comment')
            
            twitter_save_path=os.path.abspath(os.path.join(save_path,f'twitter.csv'))
            if exists(twitter_save_path):
                read_and_concat(twitter_save_path,twitter_df,'date')
            else:
                twitter_df.to_csv(twitter_save_path)
        reddit_path=os.path.abspath(os.path.join(file_path,f'reddit{datetime.now().date()}.csv'))
        if exists(reddit_path):
            reddit_df=read_and_clean_csv(reddit_path,'date')
            reddit_df=analyzer.clean_and_analyze(reddit_df,'comment')
            
            reddit_save_path=os.path.abspath(os.path.join(save_path,f'reddit.csv'))
            if exists(reddit_save_path):
                read_and_concat(reddit_save_path,reddit_df,'date')
            else:
                reddit_df.to_csv(reddit_save_path)
        youtube_path=os.path.abspath(os.path.join(file_path,f'youtube{datetime.now().date()}.csv'))     
        if exists(youtube_path):
            youtube_df=read_and_clean_csv(youtube_path,)
            youtube_df=analyzer.clean_and_analyze(youtube_df,'comment')
            youtube_save_path=os.path.abspath(os.path.join(save_path,f'youtube.csv'))
            if exists(youtube_save_path):
                read_and_concat(youtube_save_path,youtube_df,date_column=None)
            else:
                youtube_df.to_csv(youtube_save_path)
        trends_path=os.path.abspath(os.path.join(file_path,f'trends{datetime.now().date()}.csv'))     
        if exists(trends_path):
            trends_df=read_and_clean_csv(trends_path,'date')
            trends_df['date']=pd.to_datetime(trends_df['date'],)
            trends_df['date']=trends_df['date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d %H:%M:%S'))
            trends_save_path=os.path.abspath(os.path.join(save_path,f'trends.csv'))
            if exists(trends_save_path):
                read_and_concat(trends_save_path,trends_df,'date')
            else:
                trends_df.to_csv(trends_save_path)

if __name__=='__main__':
    main()
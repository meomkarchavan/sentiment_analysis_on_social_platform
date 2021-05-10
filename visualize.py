from datetime import datetime
from helpers.visualizer import Visualizer
from helpers.helpers import read_and_clean_csv, read_and_concat
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
def main():
    
    
    main_path=os.path.abspath(os.getenv('data_path'))
    keywords_list=pd.read_csv(os.getenv('keyword_csv_path'))['keywords'].to_list()
    
    visualizer=Visualizer()
    for keywords in keywords_list:
        path=(os.path.abspath(os.path.join(main_path,'_'.join(keywords.split()),'analyzed')))
        os.makedirs(path, exist_ok=True)
        twitter_path=os.path.abspath(os.path.join(path,f'twitter.csv'))
        reddit_path=os.path.abspath(os.path.join(path,f'reddit.csv'))
        youtube_path=os.path.abspath(os.path.join(path,f'youtube.csv'))
        trends_path=os.path.abspath(os.path.join(path,f'trends.csv'))
        
        twitter_df=read_and_clean_csv(twitter_path,'date')
        visualizer.plot_all(twitter_df,name='Twitter')
        
        reddit_df=read_and_clean_csv(reddit_path,'date')
        visualizer.plot_all(reddit_df,name='Reddit')
        
        youtube_df=read_and_clean_csv(youtube_path,None)
        visualizer.plot_all(youtube_df,name='Youtube',flag=False)
        
        trends_df=read_and_clean_csv(trends_path,'date')
        visualizer.plot_gtrend_chart(trends_df,col=keywords.split()[0],name='Google Trends')
        


if __name__=='__main__':
    main()
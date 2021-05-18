from datetime import datetime
from helpers.visualizer import Visualizer
from helpers.helpers import read_and_clean_csv, read_and_concat
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
def main():
    
    
    main_path=os.getenv('data_path')
    if not main_path:
        main_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),'Data')
    keywords_list_path=os.getenv('keyword_csv_path')
    if not keywords_list_path:
        keywords_list_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),'keywords.csv')
    keywords_list=pd.read_csv(keywords_list_path)['keywords'].to_list()
    
    visualization_path=os.getenv('visualization_path')
    if not visualization_path:
        visualization_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),'Visualization')
    
    
    visualizer=Visualizer()
    for keywords in keywords_list:
        print(keywords)
        path=(os.path.abspath(os.path.join(main_path,'_'.join(keywords.split()),'analyzed')))
        twitter_path=os.path.abspath(os.path.join(path,f'twitter.csv'))
        reddit_path=os.path.abspath(os.path.join(path,f'reddit.csv'))
        youtube_path=os.path.abspath(os.path.join(path,f'youtube.csv'))
        trends_path=os.path.abspath(os.path.join(path,f'trends.csv'))
        save_path=os.path.join(visualization_path,'_'.join(keywords.split()),datetime.now().date().strftime('%Y_%m_%d'))
        os.makedirs(save_path, exist_ok=True)
        
        twitter_df=read_and_clean_csv(twitter_path,'date')
        visualizer.plot_all(twitter_df,name='Twitter',save=True,save_path=save_path)
        
        reddit_df=read_and_clean_csv(reddit_path,'date')
        visualizer.plot_all(reddit_df,name='Reddit',save=True,save_path=save_path)
        
        youtube_df=read_and_clean_csv(youtube_path,None)
        visualizer.plot_all(youtube_df,name='Youtube',flag=False,save=True,save_path=save_path)
        
        trends_df=read_and_clean_csv(trends_path,'date')
        visualizer.plot_gtrend_chart(trends_df,col=keywords.split()[0],name='Google Trends',save=True,save_path=save_path)
        


if __name__=='__main__':
    main()
from datetime import datetime

from numpy import e
from helpers.visualizer import Visualizer
from helpers.helpers import read_and_clean_csv, read_and_concat
import pandas as pd
import os
from dotenv import load_dotenv
import sys

load_dotenv()
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
main_path=os.getenv('data_path')
if not main_path:
    main_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),'Data')
keywords_list_path=os.getenv('keyword_csv_path')
if not keywords_list_path:
    keywords_list_path=os.path.join(os.path.dirname(os.path.realpath(__file__)),'keywords.csv')
keywords_list=pd.read_csv(keywords_list_path)['keywords'].to_list()

def main():
    while True:
        os.system('cls||clear')
        print('Select Keywords to Visualize')
        for i in range(len(keywords_list)):
            print(f'{i}) {keywords_list[i]}')
        print('Enter q/quit to exit')
        keyword=input('Enter: ')
        if keyword=='q' or keyword=='quit':
            sys.exit()
        else:
            try:
                int(keyword)
            except ValueError:
                input('Invalid Input Press Enter to Continue....')
                continue
            if int(keyword) not in range(len(keywords_list)):
                input('Invalid Input Press Enter to Continue....')
                continue
            visualizer=Visualizer()
            path=(os.path.abspath(os.path.join(main_path,'_'.join(keywords_list[int(keyword)].split()),'analyzed')))
            twitter_path=os.path.abspath(os.path.join(path,f'twitter.csv'))
            reddit_path=os.path.abspath(os.path.join(path,f'reddit.csv'))
            youtube_path=os.path.abspath(os.path.join(path,f'youtube.csv'))
            trends_path=os.path.abspath(os.path.join(path,f'trends.csv'))
            platfroms={'Twitter':twitter_path,
                       'Reddit':reddit_path,
                       'Youtube':youtube_path,
                       'Google Trends':trends_path}
            while True:
                os.system('cls||clear')
                print('Select the Platfrom you want to Plot')
                for i,k in enumerate(platfroms.keys()):
                    print(f'{i}) {k}')
                print('Enter m/menu to main menu')
                print('Enter q/quit to exit')
                platfrom=input('Enter: ')
                
                if platfrom=='q' or platfrom=='quit':
                    sys.exit()
                elif platfrom=='m' or platfrom=='menu':
                    break
                elif platfrom=='0' or platfrom=='1':
                    while True:
                        os.system('cls||clear')
                        print('Select Type of Plot:')
                        plot_dict={'0':'Word Cloud',
                                '1':'Word Count',
                                '2':'Sentiment Count',
                                '3':'Trend Chart'
                                }
                        for k,v in plot_dict.items():
                            print(f'{k}) {v}')
                        print('Enter b/back to go back')
                        print('Enter q/quit to exit')
                        plot=input('Enter: ')
                        if plot=='q' or plot=='quit':
                            sys.exit()
                        elif plot=='b' or plot=='back':
                            break
                        else:
                            df=read_and_clean_csv(platfroms[list(platfroms.keys())[int(platfrom)]],'date')
                            if plot=='0':
                                visualizer.plot_wordcloud(df,'comment',list(platfroms.keys())[int(platfrom)])
                            elif plot=='1':
                                visualizer.plot_word_count(df,'comment',list(platfroms.keys())[int(platfrom)])
                            elif plot=='2':
                                visualizer.plot_sentiment_count(df,'Analysis',list(platfroms.keys())[int(platfrom)])
                            elif plot =='3':
                                visualizer.plot_trend_chart(df,'Polarity',list(platfroms.keys())[int(platfrom)])
                            else:
                                input('Invalid Input Press Enter to Continue....')
                elif platfrom=='2':
                    while True:
                        os.system('cls||clear')
                        print('Select Type of Plot:')
                        plot_dict={'0':'Word Cloud',
                                '1':'Word Count',
                                '2':'Sentiment Count',
                                }
                        for k,v in plot_dict.items():
                            print(f'{k}) {v}')
                        print('Enter b/back to go back')
                        print('Enter q/quit to exit')
                        plot=input('Enter: ')
                        if plot=='q' or plot=='quit':
                            os.system.exit(0)
                        elif plot=='b' or plot=='back':
                            break
                        else:
                            df=read_and_clean_csv(platfroms[list(platfroms.keys())[int(platfrom)]],None)
                            if plot=='0':
                                visualizer.plot_wordcloud(df,'comment',list(platfroms.keys())[int(platfrom)])
                            elif plot=='1':
                                visualizer.plot_word_count(df,'comment',list(platfroms.keys())[int(platfrom)])
                            elif plot=='2':
                                visualizer.plot_sentiment_count(df,'Analysis',list(platfroms.keys())[int(platfrom)])
                            else:
                                input('Invalid Input Press Enter to Continue....')
                elif platfrom=='3':
                    while True:
                        os.system('cls||clear')
                        print('Select Type of Plot:')
                        plot_dict={'0':'Trend Chart'
                                }
                        for k,v in plot_dict.items():
                            print(f'{k}) {v}')
                        print('Enter b/back to go back')
                        print('Enter q/quit to exit')
                        plot=input('Enter: ')
                        if plot=='q' or plot=='quit':
                            sys.exit()
                        elif plot=='b' or plot=='back':
                            break
                        else:
                            df=read_and_clean_csv(platfroms[list(platfroms.keys())[int(platfrom)]],'date')
                            if plot=='0':
                                visualizer.plot_gtrend_chart(df,col=keywords_list[int(keyword)].split()[0],name=list(platfroms.keys())[int(platfrom)])
                            else:
                                input('Invalid Input Press Enter to Continue....')
                else:
                    input('Invalid Input Press Enter to Continue....')
                
                
            

if __name__=='__main__':
    main()
import pandas as pd
from pytrends.request import TrendReq
import datetime as dt


class Trends():
    def __init__(self):
        self.pytrends = TrendReq()
    
    def gtrends_overtime(self,keyword,category=71, time='all', loc=''):
        print('Getting Google Trends Data')
        self.pytrends.build_payload(keyword, cat=category, timeframe=time, geo=loc, gprop='')
        df_time = self.pytrends.interest_over_time()
        df_time.reset_index(inplace=True)
        df_time['date']=pd.to_datetime(df_time['date'],)
        df_time['date']=df_time['date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d %H:%M:%S'))
        return df_time
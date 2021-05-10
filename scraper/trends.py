from pytrends.request import TrendReq


class Trends():
    def __init__(self):
        self.pytrend = TrendReq()
    
    def gtrends_overtime(self,keyword,category=0, time='all', loc=''):
        
        self.pytrends.build_payload(keyword, cat=category, timeframe=time, geo=loc, gprop='')
        df_time = self.pytrends.interest_over_time()
        df_time.reset_index(inplace=True)
        return df_time
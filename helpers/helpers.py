from datetime import datetime
import pandas as pd
import datetime as dt

dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
def read_and_concat(path,df,date_column):
  if date_column:
    df=pd.concat([df,read_and_clean_csv(path,date_column)])
    df['date']=pd.to_datetime(df['date'],)
    df['date']=df['date'].apply(lambda x: dt.datetime.strftime(x, '%Y-%m-%d %H:%M:%S'))
    df.drop_duplicates(subset=date_column, keep="first", inplace=True)
    df.sort_values(by=[date_column], inplace=True)
  else:
      df=pd.concat([df,read_and_clean_csv(path)]).reset_index(drop=True)
      df.drop_duplicates(subset=None, keep="first", inplace=True)
  df.to_csv(path)
  return df

def read_and_clean_csv(path,date_column=None):
  if date_column:
    df=pd.read_csv(path,parse_dates=[date_column], date_parser=dateparse )
    try:
      df=df.drop('Unnamed: 0',axis=1)
    except KeyError:
      pass
  else:
    df=pd.read_csv(path,index_col=False )
    try:
      df=df.drop('Unnamed: 0',axis=1)
    except KeyError:
      pass
    df = df[df['comment'].notna()]
  return df
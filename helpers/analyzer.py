from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import preprocess_kgptalkie as ps
from tqdm import tqdm
tqdm.pandas()
class Analyzer():
    def __init__(self):
        self.analyser = SentimentIntensityAnalyzer()
    def text_preprocessing(self,df,col_name):
        column = col_name
        df[column] = df[column].progress_apply(lambda x:str(x).lower())
        df[column] = df[column].progress_apply(lambda x: ps.remove_urls(x))
        df[column] = df[column].progress_apply(lambda x: ps.cont_exp(x)) #you're -> you are; i'm -> i am
        df[column] = df[column].progress_apply(lambda x: ps.remove_emails(x))
        df[column] = df[column].progress_apply(lambda x: ps.remove_html_tags(x))
        df[column] = df[column].progress_apply(lambda x: ps.remove_stopwords(x))
        df[column] = df[column].progress_apply(lambda x: ps.remove_special_chars(x))
        df[column] = df[column].progress_apply(lambda x: ps.remove_accented_chars(x))
        df[column] = df[column].progress_apply(lambda x: ps.remove_urls(x)) 
        df[column] = df[column].progress_apply(lambda x: ps.make_base(x)) #ran -> run,
        return(df)
    
    def getVaderPolarity(self,text):
        return self.analyser.polarity_scores(text)['compound']
    
    def getAnalysis(self,score):
        if score <= -0.05:
            return 'Negative'
        elif score >= 0.05:
            return 'Positive'
        else:
            return 'Neutral'
    def clean_and_analyze(self,df,col):
        df_cleaned = self.text_preprocessing(df, col)
        df_cleaned['Polarity']=df_cleaned[col].apply(self.getVaderPolarity)
        df_cleaned['Analysis'] = df_cleaned['Polarity'].apply(self.getAnalysis)
        return df
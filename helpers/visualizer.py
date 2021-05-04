import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
import collections
import seaborn as sns
import pandas as pd
import datetime as dt

sns.set(style="darkgrid")
sns.set(font_scale=1.3)
class Visualizer():
    def __init__(self):
        pass
    def plot_all(self,df,name,flag=True):
        self.plot_wordcloud(df,'comment',name)
        self.plot_word_count(df,'comment',name)
        self.plot_sentiment_count(df,'Analysis',name)
        if flag:
            self.plot_trend_chart(df,'Polarity',name)
    def plot_wordcloud(self,df,col,name):
        allWords = ' '.join([str(twts) for twts in df[col]])
        wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
        plt.imshow(wordCloud, interpolation="bilinear")
        plt.title(f'Word Cloud {name}')
        plt.axis('off')
        plt.show()
        
    
    def plot_sentiment_count(self,df,col,name):
        # Plotting and visualizing the counts
        plt.title(f'Sentiment Analysis Count {name}')
        plt.xlabel('Sentiment')
        plt.ylabel('Counts')
        df[col].value_counts().plot(kind = 'bar')
        plt.show()
        
    def plot_word_count(self,df,col,name):
        cv = CountVectorizer()
        bow = cv.fit_transform(df[col].values.astype('U'))
        word_freq = dict(zip(cv.get_feature_names(), np.asarray(bow.sum(axis=0)).ravel()))
        word_counter = collections.Counter(word_freq)
        word_counter_df = pd.DataFrame(word_counter.most_common(20), columns = ['word', 'freq'])
        _, ax = plt.subplots(figsize=(15, 6))
        sns.barplot(x="word", y="freq", data=word_counter_df, palette="PuBuGn_d", ax=ax,errwidth = 1.5).set_title(f"Words Count {name}")
        plt.show();
        
    def plot_trend_chart(self,df,col,name,date_limit=None):
        df=df.set_index('date')
        df=df.sort_index()
        df['mean'] = df[col].expanding().mean()
        df['rolling'] = df[col].rolling('4h').mean()
        fig = plt.figure(figsize=(20,5))
        ax = fig.add_subplot(111)
        ax.plot(df.index,df['rolling'], color ='r', label='Rolling Mean')
        ax.plot(df.index,df['mean'], color='y', label='Expanding Mean')
        
        if date_limit:
            ax.set_xlim([date_limit[0],date_limit[1]])
        else:
            ax.set_xlim([dt.date(2021,4,1),dt.date(2021,5,31)])
        ax.set(title=f'Trend Over Time {name}', xlabel='Date', ylabel='Sentiment')
        ax.legend(loc='best')
        fig.tight_layout()
        plt.show()
        
        
        
import praw
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
class Reddit():
    def __init__(self,):
        self.reddit = praw.Reddit(client_id=os.getenv('my_client_id'), client_secret=os.getenv('my_client_secret'), user_agent=os.getenv('my_user_agent'),check_for_async=False)
    
    def get_post(self,search_keywords):
        print('Getting Reddit Posts')
        all = self.reddit.subreddit("all")
        reddit_data= [[datetime.fromtimestamp(post.created_utc),post.author,post.url, post.title+post.selftext] for post in all.search(search_keywords, limit=1000)]
        reddit_df = pd.DataFrame(data=reddit_data, 
                    columns=['date','user', "url","post"])
        comments_by_day=[]
        for url in reddit_df['url'].tolist():
            try:
                submission = self.reddit.submission(url=url)
                submission.comments.replace_more(limit=0)
                comments=[(datetime.fromtimestamp(comment.created_utc),comment.body,comment.author,comment.submission.url,comment.submission.title) for comment in submission.comments]
            except:
                comments=''
            comments_by_day.append(comments)
        comments=[]
        for post in comments_by_day:
            for comment in post:
                comments.append(comment)
        reddit_comments_df = pd.DataFrame(data=comments, 
                    columns=['date','comment','user', "post url","post title"])
        return reddit_comments_df
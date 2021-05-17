import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
from youtube_easy_api.easy_wrapper import *

class Youtube():
    def __init__(self):
        self.easy_wrapper = YoutubeEasyWrapper()
        self.easy_wrapper.initialize(api_key=os.getenv('API_KEY_YOUTUBE'))
    
    def get_comments(self,search_keywords):
        print('Getting Youtube Comments')

        results = self.easy_wrapper.search_videos(search_keyword=search_keywords,
                                     order='relevance')
        comments=[]
        for res in results:
            metadata = self.easy_wrapper.get_metadata(video_id=res['video_id'])
            try:
                if metadata['comments']:
                    comments+=metadata['comments']
            except KeyError:
                pass
        youtube_df = pd.DataFrame(data=comments, 
                    columns=['comment'])
        return youtube_df
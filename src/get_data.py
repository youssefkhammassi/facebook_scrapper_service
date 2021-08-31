import pandas as pd

from src.scrapper import FacebookPostsScraper


class FbDataLoader:
    def __init__(self, url, db):
        self._db = db
        self.url = url
        self._email = '52307167' #fb_username
        self._password = '123456kh' #fb_password

    # collecting posts data from facebook page or profile
    def get_data(self):
        fps = FacebookPostsScraper(self._email, self._password, post_url_text='Full Story')
        data = fps.get_posts_from_profile(self.url)
        return data
    # Adding collected data to the database
    def posts_to_db(self):
        if self.get_data() is not None:
            df = pd.DataFrame(self.get_data())
            df.to_sql('FB_POSTS', con=self._db, if_exists='append')
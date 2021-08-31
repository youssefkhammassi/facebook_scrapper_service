import requests as requests
import bs4 as BeautifulSoup
import pickle
import os


class FacebookPostsScraper:

    # We need the email and password to access Facebook
    def __init__(self, email, password, post_url_text='Full Story'):
        self.email = email
        self.password = password
        self.headers = {
            'User-Agent': 'NokiaC3-00/5.0 (07.20) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 AppleWebKit/420+ (KHTML, like Gecko) Safari/420+'
        }
        self.session = requests.session()  # Create the session for the next requests
        self.cookies_path = 'session_facebook.cki'  # Give a name to store the session in a cookie file.
        self.post_url_text = post_url_text

        if self.new_session():
            self.login()

        self.posts = []  # Store the scraped posts

    def new_session(self):
        if not os.path.exists(self.cookies_path):
            return True

        f = open(self.cookies_path, 'rb')
        cookies = pickle.load(f)
        self.session.cookies = cookies
        return False

    # Utility function to make the requests and convert to soup object if necessary
    def make_request(self, url, method='GET', data=None, is_soup=True):
        if len(url) == 0:
            raise Exception(f'Empty Url')

        if method == 'GET':
            resp = self.session.get(url, headers=self.headers)
        elif method == 'POST':
            resp = self.session.post(url, headers=self.headers, data=data)
        else:
            raise Exception(f'Method [{method}] Not Supported')

        if resp.status_code != 200:
            raise Exception(f'Error [{resp.status_code}] > {url}')

        if is_soup:
            return BeautifulSoup.BeautifulSoup(resp.text, 'lxml')
        return resp

    # The first time we login
    def login(self):
        # Get the content of HTML of mobile Login Facebook page
        url_home = "https://m.facebook.com/"
        soup = self.make_request(url_home)
        if soup is None:
            raise Exception("Couldn't load the Login Page")

        # Here we need to extract this tokens from the Login Page
        lsd = soup.find("input", {"name": "lsd"}).get("value")
        jazoest = soup.find("input", {"name": "jazoest"}).get("value")
        m_ts = soup.find("input", {"name": "m_ts"}).get("value")
        li = soup.find("input", {"name": "li"}).get("value")
        try_number = soup.find("input", {"name": "try_number"}).get("value")
        unrecognized_tries = soup.find("input", {"name": "unrecognized_tries"}).get("value")

        # This is the url to send the login params to Facebook
        url_login = "https://m.facebook.com/login/device-based/regular/login/?refsrc=https%3A%2F%2Fm.facebook.com%2F&lwv=100&refid=8"
        payload = {
            "lsd": lsd,
            "jazoest": jazoest,
            "m_ts": m_ts,
            "li": li,
            "try_number": try_number,
            "unrecognized_tries": unrecognized_tries,
            "email": self.email,
            "pass": self.password,
            "login": "Iniciar sesión",
            "prefill_contact_point": "",
            "prefill_source": "",
            "prefill_type": "",
            "first_prefill_source": "",
            "first_prefill_type": "",
            "had_cp_prefilled": "false",
            "had_password_prefilled": "false",
            "is_smart_lock": "false",
            "_fb_noscript": "true"
        }
        soup = self.make_request(url_login, method='POST', data=payload, is_soup=True)
        if soup is None:
            raise Exception(f"The login request couldn't be made: {url_login}")

        redirect = soup.select_one('a')
        if not redirect:
            raise Exception("Please log in desktop/mobile Facebook and change your password")

        url_redirect = redirect.get('href', '')
        resp = self.make_request(url_redirect)
        if resp is None:
            raise Exception(f"The login request couldn't be made: {url_redirect}")

        # Finally we get the cookies from the session and save it in a file for future usage
        cookies = self.session.cookies
        f = open(self.cookies_path, 'wb')
        pickle.dump(cookies, f)

        return {'code': 200}

    def get_posts_from_profile(self, url_profile):
        # Prepare the Url to point to the posts feed
        if "www." in url_profile: url_profile = url_profile.replace('www.', 'm.')
        if 'v=timeline' not in url_profile:
            if '?' in url_profile:
                url_profile = f'{url_profile}&v=timeline'
            else:
                url_profile = f'{url_profile}?v=timeline'

        is_group = '/groups/' in url_profile

        # Make a simple GET request
        soup = self.make_request(url_profile)
        if soup is None:
            print(f"Couldn't load the Page: {url_profile}")
            return []

        # Now the extraction...
        css_profile = '.storyStream > div'  # Select the posts from a user profile
        css_page = '#recent > div > div > div'  # Select the posts from a Facebook page
        css_group = '#m_group_stories_container > div > div'  # Select the posts from a Facebook group
        raw_data = soup.select(f'{css_profile} , {css_page} , {css_group}')  # Now join and scrape it
        posts = []
        for item in raw_data:  # Now, for every post...
            published = item.select_one('abbr')  # Get the formatted datetime of published
            description = item.select('p')  # Get list of all p tag, they compose the description
            images = item.select('a > img')  # Get list of all images

            # Clean the publish date
            if published is not None:
                published = published.get_text()
            else:
                published = ''

            # Join all the text in p tags, else set empty string
            if len(description) > 0:
                description = '\n'.join([d.get_text() for d in description])
            else:
                description = ''

            # Get all the images links
            images = [image.get('src', '') for image in images]
            # Map of url , Posts publish time, Post Description , Image included in post
            post = {'URL': str(url_profile), 'published': str(published), 'description': str(description),
                    'images': str(images)}
            posts.append(post)
            self.posts.append(post)
        return posts

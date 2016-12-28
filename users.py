# from database import connect
from database import CursorFromConnectionFromPool
import oauth2
from twitter_utils import consumer
import json
import urllib.parse as urlparse
import constants

class User:
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id):
    #def __init__(self, email, first_name, last_name, oauth_token, oauth_token_secret, id):
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return "<User {}>".format(self.screen_name)

    # connection = psycopg2.connect(database="learning", user="postgres", password="andi", host="localhost")
    # using this first "with" does commit and close the connection
    # with connection_pool.getconn() as connection:
    # with connect() as connection
    # connection = connection_pool.getconn()
    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO users_twitter (screen_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s)',
                           (self.screen_name, self.oauth_token, self.oauth_token_secret))
            # using the second "with" does close the cursor
            #connection.commit()
            # connection_pool.putconn(connection)

    def save_to_dbvvv(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO users_twitter (email, first_name, last_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s, %s, %s)',
                           (self.email, self.first_name, self.last_name, self.oauth_token, self.oauth_token_secret))
            # using the second "with" does close the cursor
            #connection.commit()
            # connection_pool.putconn(connection)
    @classmethod
    def load_from_db_by_screen_name(cls, screen_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM users_twitter WHERE screen_name = %s', (screen_name,))
            user_data = cursor.fetchone()  # gets the first row
            if user_data:
                # return cls(user_data[1], user_data[2], user_data[3], user_data[0])
                return cls(screen_name=user_data[1], oauth_token=user_data[2],
                           oauth_token_secret=user_data[3], id=user_data[0])
                # connection_pool.putconn(connection) --> this doesn't do anything, with 'return' we exit the method, it is to late


    def twitter_request(self, uri, verb='GET'):
        # Create an 'authorized_token' Token object and use that to perform Twitter API calls on behalf of the user
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        # Make Twitter API Calls!
        response, content = authorized_client.request(uri, verb)
        if response.status != 200:
            print('An error ocurred when searching!')

        return json.loads(content.decode('utf-8'))


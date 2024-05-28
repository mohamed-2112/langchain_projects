import os
import requests
import tweepy


class TwitterProfileScrapper:
    def __init__(self, username):
        self.twitter_client = None
        self.gist_url = ("https://gist.githubusercontent.com/emarco177/827323bb599553d0f0e662da07b9ff68/raw"
                         "/57bf38cf8acce0c87e060f9bb51f6ab72098fbd6/eden-marco-twitter.json")
        self.username = username


    def scrape_user_tweets(self, num_tweets=5, mock: bool = False):
        """Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of
        dictionaries. Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
        """

        if mock:
            response = self.__request_gist()
            data = self.__clean_response(response, mock)
        else:
            self.twitter_client = self.__twitter_client_init()
            response = self.__request_scrape(num_tweets)
            data = self.__clean_response(response.data, mock)
        print(data)
        return data

    def __request_gist(self):
        return requests.get(self.gist_url, timeout=5).json()

    def __request_scrape(self, num_tweets):
        user_id = self.twitter_client.get_user(username=self.username).data.id
        tweets = self.twitter_client.get_users_tweets(
            id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
        )
        return tweets

    def __clean_response(self, tweets, mock):
        tweet_list = []
        for tweet in tweets:
            tweet_dict = {"text": tweet["text"], "url": f"https://twitter.com/{self.username}/status/{tweet['id']}"}
            tweet_list.append(tweet_dict)
        return tweet_list

    def __twitter_client_init(self):
        twitter_client = tweepy.Client(
            bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
            consumer_key=os.environ["TWITTER_API_KEY"],
            consumer_secret=os.environ["TWITTER_API_KEY_SECRET"],
            access_token=os.environ["TWITTER_ACCESS_TOKEN"],
            access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
        )
        return twitter_client

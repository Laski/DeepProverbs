import unittest
from pathlib import Path

import twitter

class TwitterApiClient:
    def __init__(self):
        self.api = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret,
            tweet_mode='extended',
        )

    def get_latest_tweets(self, user, count):
        tweets = self.api.GetUserTimeline(screen_name=user, count=200, include_rts=False, exclude_replies=True)
        yield from tweets
        n_retrieved = len(tweets)
        while n_retrieved < count and len(tweets) > 0:
            print("Downloading new tweets.")
            print(f"Last tweet retrieved was: {tweets}")
            print(f"We already retrieved {n_retrieved} tweets")
            last_id = tweets[-1].id
            tweets = self.api.GetUserTimeline(screen_name=user, count=200, max_id=last_id - 1, include_rts=False,
                                              exclude_replies=True)
            yield from tweets
            n_retrieved += len(tweets)

    def download_latest_tweets(self, user, count, filename):
        tweets = self.get_latest_tweets(user, count)
        with open(Path(filename), 'w') as file:
            for tweet in tweets:
                file.write(tweet.full_text)
                file.write('\n')
                file.write('---\n')
            # write complete data of last tweet
            file.write('---\n')
            file.write(str(tweet))


class TwitbotTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.api = TwitterApiClient()

    def test_api_client_can_get_someones_tweets(self):
        user = '@acaestatodomal'
        tweets = self.api.get_latest_tweets(user, 500)
        tweets = list(tweets)
        print([tweet.full_text for tweet in tweets])
        self.assertTrue(len(tweets) >= 500)

    def test_api_client_can_download_someones_tweets_to_a_file(self):
        user = '@acaestatodomal'
        filename = 'ocho.txt'
        self.api.download_latest_tweets(user, 10000, filename)
        with open(filename, 'r') as file:
            self.assertTrue(len(file.readlines()) > 500)


if __name__ == '__main__':
    unittest.main()

import json
import os
import sys

if "linux" in sys.platform:
    os.environ["LC_AL"] = "C.UTF-8"
    os.environ["LANG"] = "C.UTF-8"
else:
    os.environ["LC_AL"] = "en_US.utf-8"
    os.environ["LANG"] = "en_US.utf-8"

import numpy as np
import tweepy
import re
import logging
import torch
import random
import time
import click

from aitextgen import aitextgen

logging.basicConfig(
    format="%(asctime)s — %(levelname)s — %(name)s — %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.DEBUG
)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
logging.info(f'Using device: {device}')

ai = aitextgen(model="rnn/pytorch_model.bin",
               config="rnn/config.json",
               vocab_file="rnn/aitextgen-vocab.json",
               merges_file="rnn/aitextgen-merges.json",
               to_gpu=False)


def authenticate(consumer_key=None, consumer_secret=None, access_key=None, access_secret=None):
    consumer_key = consumer_key or os.environ["CONSUMER_KEY"]
    consumer_secret = consumer_secret or os.environ["CONSUMER_SECRET"]
    access_key = access_key or os.environ["ACCESS_KEY"]
    access_secret = access_secret or os.environ["ACCESS_SECRET"]

    # Authenticate with the Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    return api


def new_tweet_text(temperature=0.7):
    # generate a tweet
    generated_text = ai.generate_one(temperature=temperature)
    while len(generated_text) >= 280:
        generated_text = ai.generate_one(temperature=temperature)

    #if 'https://' in generated_text:
    #    generated_text = re.sub('https\:\/\/t\.co[\S]*', '', generated_text)

    print(generated_text)
    return generated_text


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api

    def on_status(self, status):
        if status.author.id == 190461974:
            if status.in_reply_to_status_id or status.is_quote_status:
            	# do not consider replies or retweets
            	return
            seconds = random.randint(60, 300)
            print(f"new tweet. will wait {seconds} seconds and then tweet")
            time.sleep(seconds)
            tweet_text = new_tweet_text()
            print(tweet_text)
            self.api.update_status(tweet_text)


@click.group()
def main():
    pass


@main.command("wait-and-tweet")
def wait_and_tweet():
    api = authenticate()
    myStreamListener = MyStreamListener(api=api)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(follow=["190461974"])  # blocks


@main.command("post-tweet")
def post_tweet():
    api = authenticate()
    api.update_status(new_tweet_text())


if __name__ == "__main__":
    main()

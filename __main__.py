#!/usr/bin/env python3

# REFERENCES: https://realpython.com/twitter-bot-python-tweepy/#how-to-make-a-twitter-bot-in-python-with-tweepy
#             https://stackoverflow.com/questions/49731259/tweepy-get-tweets-between-two-dates
#             https://stackoverflow.com/questions/39985434/python-tweepy-how-to-use-lookup-friendships
# THANKS!

import tweepy
from config import *
import time
import datetime

def is_already_reacted(tweetid):
    with open('reacted_tweet_ids.txt', 'r') as file:
        for _, line in enumerate(file):
                if line == str(tweetid) + "\n":
                    return True
    return False

def has_firm_friendship(api, tw):
    infomation = api.show_friendship(source_screen_name=MY_SCREEN_NAME, target_id=tw.user.id_str)
    return True if (infomation[0].following and infomation[0].followed_by and infomation[1].following and infomation[1].followed_by) else False
    return False

def check_mentions(api, keywords, since_id):
    print("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            if is_already_reacted(tweet.id):
                continue
            startDate = datetime.datetime(2020, 5, 19, 0, 0, 0)
            if tweet.created_at > startDate:
                if has_firm_friendship(api, tweet) or tweet.user.screen_name == MY_SCREEN_NAME:
                    print(f"Replying to {tweet.user.name}(@{tweet.user.screen_name}, {tweet.user.id_str}): ")
                    print(f"\"{tweet.text}\"")
                    api.update_status(
                        status=f"Hello, {tweet.user.name}! I'm {MY_SCREEN_NAME}, Nice2meetu.",
                        in_reply_to_status_id=tweet.id,
                        auto_populate_reply_metadata="true"
                    )
                    with open('reacted_tweet_ids.txt', 'a') as file:
                        print(tweet.id, file=file)
                else:
                    print(f"The user {tweet.user.name}(@{tweet.user.screen_name}, {tweet.user.id_str}) and you/I (@{MY_SCREEN_NAME}) seem to have no firm frindship...(They don't seem to be following each other.)")
            #else:
            #    print(f"Ignore: {tweet.text} from {tweet.user.name} cuz it's a old tweet...")
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["野獣先輩", "nnn1590", "help", "hi" ], since_id)
        print("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()

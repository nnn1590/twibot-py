#!/usr/bin/env python3

# REFERENCES: https://realpython.com/twitter-bot-python-tweepy/#how-to-make-a-twitter-bot-in-python-with-tweepy
#             https://stackoverflow.com/questions/49731259/tweepy-get-tweets-between-two-dates
#             https://stackoverflow.com/questions/39985434/python-tweepy-how-to-use-lookup-friendships
# THANKS!

import tweepy
from config import *
import time
import datetime
import random

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
    print("\033[34mRetrieving mentions\033[0m")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id,count=3).items():
        print(f"\033[1;32mFound tweet\033[0m: {tweet.user.name}(@{tweet.user.screen_name}, {tweet.user.id_str}) at {tweet.created_at}(UTC?) (lang: {tweet.lang}): ")
        print(f"\"{tweet.text}\"")
        new_since_id = max(tweet.id, new_since_id)
        #if tweet.in_reply_to_status_id is not None:
        #    print(f"=> \033[33mIgnored\033[0m: It's a reply...")
        #    continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            if is_already_reacted(tweet.id):
                print(f"=> \033[33mIgnored\033[0m: It's a tweet that has already reacted...")
                continue
            startDate = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=15)
            if tweet.created_at.replace(tzinfo=None) > startDate.replace(tzinfo=None):
                if has_firm_friendship(api, tweet) or tweet.user.screen_name == MY_SCREEN_NAME:
                    print(f"=> \033[34mReplying...\033[0m")
                    if tweet.lang == "ja":
                        status_text=f"BOT/乱数(範囲: 0~114514) :{random.randint(0,114514)}"
                    else:
                        status_text=f"BOT/RANDOM(RANGE: 0~114514) :{random.randint(0,114514)}"
                    api.update_status(
                        status=status_text,
                        #status=f"Hello, {tweet.user.name}! I'm {MY_SCREEN_NAME}, Nice2meetu.",
                        in_reply_to_status_id=tweet.id,
                        auto_populate_reply_metadata="true"
                    )
                    with open('reacted_tweet_ids.txt', 'a') as file:
                        print(tweet.id, file=file)
                else:
                    print(f"=> \033[33mIgnored\033[0m: The user {tweet.user.name}(@{tweet.user.screen_name}, {tweet.user.id_str}) and you/I (@{MY_SCREEN_NAME}) seem to have no firm frindship...(They don't seem to be following each other.)")
            else:
                print(f"=> \033[33mIgnored\033[0m: It's a old tweet...")
        else:
            print(f"=> \033[33mIgnored\033[0m: Probably a tweet that this bot shouldn't react to...")
    return new_since_id

def main():
    api = create_api()
    since_id = 1265677854387269632  # 1
    while True:
        #since_id = check_mentions(api, ["野獣先輩", "nnn1590", "help", "hi" ], since_id)
        since_id = check_mentions(api, ["乱数", "ランダム数字", "randomnumber", "random number", "rand" ], since_id)
        print("\033[36mWaiting...\033[0m")
        time.sleep(60)

if __name__ == "__main__":
    main()

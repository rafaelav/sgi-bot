#!/bin/bash

python random_wait_script.py && python save_data_script.py && python follow_script.py && (python unfollow_script.py & python favorite_script.py & python tweet_script.py & python retweet_script.py)


#!/usr/bin/env python

import yaml
import json
import time
import subprocess
import requests
import praw
import os.path
import unicodedata
import time

# Config values
moderators = None
slack_name=""
slack_key=""
slack_room=""
reddit_user=""
reddit_password=""
subreddit = ""
user_agent = "modlog slackbot"
fname=""
def update_last_message(id):
    target = open(fname, 'w')
    target.write(str(id))
    target.close()

def get_last_message():
    if (not os.path.isfile(fname)):
        update_last_message(time.time());
    target = open(fname, 'r')
    last_message = target.read()
    target.close()
    return last_message

def load_config():
    with open("config.yml", 'r') as stream:
        config = yaml.load(stream)
        return config
    return None

def isModerator(user):
    global moderators
    if (not moderators):
        moderators = r.get_moderators(subreddit)
    return user in moderators


def send_message(message):
    url = slack_url + "?token=" + slack_key + "&channel=%23" + slack_room
    r = requests.post(url,data=message,headers={"content-type":"application/json"})
config = load_config()
slack_name = config['slack']['name']
slack_key = config['slack']['key']
slack_room = config['slack']['room']
slack_url = "https://" + slack_name + ".slack.com/services/hooks/slackbot" 
reddit_user = config['reddit']['user']
reddit_password = config['reddit']['password']
subreddit = config['reddit']['subreddit']
fname=config['last_message_file']

#log into reddit
r = praw.Reddit(user_agent=user_agent)
r.login(reddit_user,reddit_password)

reddit = r.get_subreddit(subreddit)
before = get_last_message()
mod_mail = r.get_mod_mail(subreddit, before=before, limit=20)
first = True
max_created = before
for msg in mod_mail:
    if float(msg.created) > float(max_created):
        max_created = msg.created
    if msg.parent_id is not None or isModerator(msg.author):
        continue
    if float(msg.created) <= float(before):
        continue
    send_message("New modmail from " + str(msg.author) + " https://www.reddit.com/message/messages/"  + str(msg.id)  + "\n" + str(msg.subject) +  " :\n" +"--------------------\n" +  msg.body + "\n--------------------")


update_last_message(max_created)

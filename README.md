#Reddit Modchat Slackbot

I created this bot so that reddit moderators using slack as a chat room can have easy integration with moderator mail.

##How it Works
https://api.slack.com/slackbot
The program uses slackbot remote control to post new top level mod mail messages that are not sent by moderators. This allows moderators to have real time discussion about a topic before responding.

##Dependencies
On a fresh install of Ubuntu 14.04 the only python module I had to install for this is praw
sudo pip install praw

##Configuration
The program expects a config.yml in the same directory as modlog_slackbot.py. Look at config.yml.default

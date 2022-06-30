# Tofu-Discord-Cheat
## Cheat for discord Tofu bot 

## Features

- Multiple accounts
- Summon
- Daily
- Mini game
- Grabbing
- Fusion tokens
- Logging





## Installation

Tofu-Discord-Cheat requires [Python 3.8](https://www.python.org/) to run.

Install the dependencies.

```
pip3 install -r requirements.txt
```


## configuration

**You need to get discord bot token**

**GUIDE**
1. Go to the Discord Developer Portal
2. Click the “New Application” button
3. Give Your Bot a Name
4. Click “Bot” button on the left side
5. Click “Add Bot” button on the right side
6. Click the “Yes, do it!" button
7. Click the “Reset Token" button
8. Copy the token and paste it to config.cfg file | example: bot_token = 'paste your token here'
9. Turn **Presence Intent**, **Server Members Intent** and **Message Content Intent** on
10. Click “OAuth2” button on the left side
11. Click “URL GENERATOR” button on under the “OAuth2” button
12. Select bot
13. Scroll down and copy generated url
14. Paste link in your browser
15. Add bot to your "cheating" server

**You need to get discord "workers" tokens**

**GUIDE**
1. Login to your "worker" account on Discord's website
2. Press Ctrl + Shift + I 
3. Click Network from the toolbar at the top
4. Go to random dm
5. Wait for network tab to chill
6. Send message, content doesn't matter
7. Click the Headers tab, scroll down until you see authorization
8. Store token, username and id somewhere
9. Launch "worker_manager.py" and select 1st option

**You need to set your tofu prefix and tofu_channel_id**'
1. If your tofu prefix is "t" just write it after the "=" sign | example: prefix = 't'
2. "tofu_channel_id" is id of the channel where all "workers" will be "working", all workers must have acces to this cahnnel | example:  tofu_channel_id = 595727408058073090

## Helper bot guide

```!cd - shows info about "worker" cooldowns```

```!stats - shows info about "worker" stats, such as the number of summons, minigames or redeemed dailys```

## License

MIT



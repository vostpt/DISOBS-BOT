# VOSTPT Discord OBS bot

**_(A more detailed README is being prepared)_**

# Installation
Bot tested in Python 3.6.7.

Before anything else, install Python and its dependencies:
```sh
pip install -U discord.py
pip install -U python-dotenv
```

# Configuration
After installing the dependencies, it's time for a quick configuration.

Create a `.env` file in the project root.

```sh
cp keys.env.example keys.env
```
 
Add and replace values where needed:

```
#Insert here token, channel id and authorized editors

DISCORD_TOKEN = <Discord bot token>
CHANNEL_ID = <Discord channel ID>
AUTHOR_RESTRICT = true
AUTHORIZED_AUTHORS = <list of authorized Discord users, separated by comma>
```

# Running

Execute `discord_api.py`, and enjoy!
# VOSTPT Discord OBS bot

# Installation
Bot tested in [Python 3.6.7](https://www.python.org/downloads/release/python-367/).

Installation instructions in Windows (tested version: 10) and Linux (tested version: Ubuntu 18.10):

## Windows
To install Python, go to Python website, download the executable, and follow instructions.
To install Python dependencies, go to command line (cmd), and execute the following commands inside DISOBS-BOT folder:
```sh
py -3 -m pip install -U discord.py
py -3 -m pip install -U python-dotenv
```

## Linux
To install Python and its dependencies in Linux, open terminal in DISOBS-BOT folder and run the script `install_linux.sh`, with the command `./install_linux.sh`.
If you don't like scripts, execute the following commands:
Install Python:
```sh
sudo apt-get -y install python3 python3-pip
```
Install dependencies:
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

# Execute bot

## Windows

Open command line (cmd), and execute the following command in DISOBS-BOT folder:
```sh
discord_api.py
```

## Linux

Open terminal, and execute the following command in DISOBS-BOT folder:
```sh
python3 discord_api.py
```

## OBS

After bot starts, open OBS, select the text option, and choose the import from file option, select `footer.txt`, and enjoy!

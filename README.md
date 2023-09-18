## Project Description
My first project on GitHub. All help is welcomed! <br/>
Help with making code more readable/efficient and help with the site's looks are especially appreciated! <br/>
ybot is a [Discord](https://discord.com/) bot that works with APIs to enhance small quality of life changes to the discord user experience

The APIs used: <br/>
[discord.py](https://discordpy.readthedocs.io/en/stable/) API Wrapper <br/>
[Steam Web API](https://steamcommunity.com/dev) <br/>
[The Cat API](https://thecatapi.com/)

API Authentication Used: <br/>
[Oauth2](https://discord.com/developers/docs/topics/oauth2) through Discord's official API

## Python Version
[Python 3.11.5](https://www.python.org/downloads/release/python-3115/)

## Requirements
```python
discord.py==2.0.1
flask==2.2.2
requests==2.31.0
python-dotenv==1.0.0
```
## Installation
Clone the repo and use [pip](https://pip.pypa.io/en/stable/) to install the packages listed in the [`requirements.txt`](https://github.com/korok0/ybot/blob/main/requirements.txt) file. 

```bash 
pip install -r requirements.txt
```

## Setup
Create a `.env` file in your `src` directory and fill in the values
```python
BOT_SECRET_TOKEN = 
BOT_APPLICATION_ID = 
BOT_OAUTH_SECRET = 
BOT_OAUTH_LINK = 
REDIRECT_URI = 
STEAM_SECRET_TOKEN = 
```
Run `setup.py` to setup the local database<br/>
Run `yeoui.py` and `ysite.py` <br/>
Go to discord `settings>connections` and link your steam profile. Then run `/link` command 
![image](https://github.com/korok0/ybot/assets/140355502/bf0aa017-5b26-4c36-97fc-64540b85fe2a) <br/>
![image](https://github.com/korok0/ybot/assets/140355502/f41cd001-184d-4518-a2b3-8821afbe175e) <br/>
![image](https://github.com/korok0/ybot/assets/140355502/2aae649a-4a62-4b93-abe8-9a2ca0897a15)



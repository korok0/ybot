import os
import requests

# Load the BOT_SECRET_TOKEN from the environment variables using dotenv
# Make sure you have python-dotenv installed (pip install python-dotenv)
from dotenv import load_dotenv
load_dotenv()

users = {
    '258375730583306241' : 'mrHQdc8Yb0FWjaLlf4KwRVbIX08ZgB'
}
TOKEN = os.getenv("BOT_SECRET_TOKEN")

url = 'https://discord.com/api/v10/users/@me/connections'
headers = {
    'Authorization': f'Bearer jzid8rohv6TU5nJluyTFYEZ9oTpHtp'
}

API_ENDPOINT = "https://discord.com/api/v10"
CLIENT_ID = '1027772366476017677'
CLIENT_SECRET = TOKEN
REDIRECT_URI = 'https://example.com/callback'
class DiscordOauth:
    def get_info(self):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Request was successful, parse the JSON response
            connections = response.json()
            # e = [connection["id"] for connection in connections if connection["type"] == "steam"][0]
            #print(e)
            print(connections)
            for connection in connections:
                if connection["type"] == "steam":
                    print(f'Name: {connection["name"]}\nType: {connection["type"]}\nID: {connection["id"]}')
                    return connection["id"]
                    
            return



        else:
            # Request failed, print the status code and reason
            print(f"Request failed with status code: {response.status_code}, Reason: {response.reason}")
            return
a = DiscordOauth()
print(a.get_info())

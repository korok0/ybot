import requests
import os
from dotenv import load_dotenv
import sqlite3
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\.."))
print(f"PR Utility: {project_root}")
sys.path.append(project_root)

# key = discord id
# value = steam id
load_dotenv()
url = 'https://discord.com/api/v10/users/@me'
API_ENDPOINT = "https://discord.com/api/v10"
CLIENT_ID = os.getenv("BOT_APPLICATION_ID")
CLIENT_SECRET = os.getenv("BOT_OAUTH_SECRET")
REDIRECT_URI = 'http://127.0.0.1:5000/e'


# custom utility commands for handling databases and discord data
class Utility:
    def unpack(self, index, data, index_name) -> str:
        """
        :param index: int
        :param data: Any
        :param index_name: str (str index for json data)
        :return: str
        """

        person = list(data.values())[index]['players']
        return person[0][index_name]
    
    def get_steam_data(self, url: str):
        res = requests.get(url)
        data = res.json()
        print(data)
        return data
    
    def register(self, code):
        conn = sqlite3.connect(os.path.join(project_root, "src\\bot\\members.db"), check_same_thread=False)
        c = conn.cursor()
        ec = self._exchange_code(code)
        print(ec)
        bearer_token = ec["access_token"]
        # refresh_token = ec["refresh_token"]
        headers = {
            'Authorization': f'Bearer {bearer_token}'
        }
        print(f'ec: {ec}')
        print(f"Bearer Token: {bearer_token}")
        response = requests.get(url=url,headers=headers)
        user=response.json()
        member_id = int(user["id"])

        try:
            c.execute(f"INSERT INTO users VALUES ({member_id}, '{bearer_token}')")
            print(f"attempting to register user: {member_id}")
        except Exception as e:
            print(e)
            print(f"unique id: {member_id} already exists in database")

        c.execute("SELECT * FROM users")
        print(c.fetchall())
        conn.commit()
        conn.close()
        return
    
    def unregister(self, id) -> bool:

        conn = sqlite3.connect(os.path.join(project_root, "src\\bot\\members.db"), check_same_thread=False)
        c = conn.cursor()
        # check if user is registered using registered_id
        if self.is_registered(id):
            c.execute(f"DELETE FROM users WHERE id={id}")
            print(f"unregistered id: {id}")
            conn.commit()
            data = c.fetchall()
        else:
            return False
        conn.close()
        return True
    
    def is_registered(self, id):
        """
        iterate through data base and check if id exists in database, if it does, return true
        """
        conn = sqlite3.connect(os.path.join(project_root, "src\\bot\\members.db"), check_same_thread=False)
        c = conn.cursor()
        c.execute(f"SELECT id FROM users WHERE id={id}")
        conn.commit()
        data = c.fetchone()
        print(f"data: {data}")
        if data is not None:
            if id == data[0]:
                print(f"id {id}")
                print(f"data 0: {data[0]}")
                conn.close()
                return True
            conn.close()
        return False
    
    def test_token(self, id) -> bool:
        test = self.fetch_token(id)
        headers = {
            'Authorization': f'Bearer {test}'
        }
        response = requests.get(url=url,headers=headers)
        user=response.json()
        if response.status_code != 200:
            self.unregister(id)
            return False
            
        return True

    def fetch_token(self, id):
        conn = sqlite3.connect(os.path.join(project_root, "src\\bot\\members.db"), check_same_thread=False)
        c = conn.cursor()
        # to avoid Type Error
        
        c.execute(f"SELECT token FROM users WHERE id={id}")
        conn.commit()
        token = c.fetchone()[0]
        conn.close()
        return token

    def get_user_steam(self, token):
        url = 'https://discord.com/api/v10/users/@me/connections'
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            connections = response.json()
            for connection in connections:
                if connection["type"] == "steam":
                    return connection["id"]
        else:
            # Request failed, print the status code and reason
            print(f"Request failed with status code: {response.status_code}, Reason: {response.reason}")
        return None

    # Need to create full-fledged/hosted website for this
    def _exchange_code(self, code):
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post(f'{API_ENDPOINT}/oauth2/token', data=data, headers=headers)
        return r.json()

    """def _refresh_token(self, refresh_token):
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post(f'{API_ENDPOINT}/oauth2/token', data=data, headers=headers)
        r.raise_for_status()
        return r.json()"""





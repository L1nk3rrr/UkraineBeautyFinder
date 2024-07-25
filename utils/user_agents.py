import os
import requests

from dotenv import load_dotenv

load_dotenv()

SCRAPEOPS_API_KEY = os.environ.get('SCRAPEOPS_API_KEY', 'YOUR API KEY')


class UserAgentManager:
    def __init__(self):
        self.__user_agent_list = self._fetch_user_agents()
        self.request_count = 0

    def _fetch_user_agents(self):
        response = requests.get(f'http://headers.scrapeops.io/v1/user-agents?api_key={SCRAPEOPS_API_KEY}')
        json_response = response.json()
        return json_response.get('result', [])

    @property
    def user_agent_list(self):
        print(self.request_count)
        self.request_count += 1
        if self.request_count >= 1000:
            self.user_agent_list = self._fetch_user_agents()
            self.request_count = 0
        return self.__user_agent_list

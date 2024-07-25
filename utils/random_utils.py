import random

from utils.user_agents import UserAgentManager


class Randomizer:
    def __init__(self):
        self.user_agent_manager = UserAgentManager()

    @property
    def user_agent(self):
        return random.choice(self.user_agent_manager.user_agent_list)

    @classmethod
    @property
    def proxy(cls):
        host = 'x.x.x.x'
        port = 1111

        if random.randint(0, 1) == 1:
            return {
                'http': f'http://{host}:{port}',
                'https': f'http://{host}:{port}'
            }
        return {}

    @classmethod
    @property
    def sleep(cls):
        return random.randint(2, 5)
import requests
from config.settings import API_KEY


class ApiClient:
    BASE_URL = 'https://api.verrancodex.com/'

    def __init__(self):
        self.api_key = API_KEY

    def get_data(self):
        response = requests.get(f'{self.BASE_URL}armors', headers={'x-api-key': f'{self.api_key}'})
        return response.json()

import logging
import requests
from config.settings import API_KEY

# Configure logging
logger = logging.getLogger(__name__)


class ApiClient:
    BASE_URL = 'https://api.verrancodex.com/'
    TIMEOUT = 15

    def __init__(self):
        self.api_key = API_KEY

    def get_data(self, endpoint):
        """
        Makes the API call based on the argument provided.

        Args:
            endpoint (str): The endpoint to call

        Returns:
            list: A formatted string.
        """
        logger.debug('Getting data from %s%s', self.BASE_URL, endpoint)
        response = requests.get(f'{self.BASE_URL}{endpoint}',
                                headers={'x-api-key': f'{self.api_key}'},
                                timeout=self.TIMEOUT)
        return response.json()

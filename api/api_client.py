from typing import Dict, Any
from datetime import datetime, timedelta, timezone
import logging
import requests
from config.settings import API_KEY, CACHE_DURATION

# Configure logging
logger = logging.getLogger(__name__)


class ApiClient:
    BASE_URL = "https://api.verrancodex.com/"
    TIMEOUT = 15

    def __init__(self):
        self.api_key = API_KEY
        self.cache_duration = timedelta(minutes=int(CACHE_DURATION))
        # Cache will be a dictionary where keys are endpoints
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_time: Dict[str, datetime] = {}

    async def fetch_data_with_cache(self, endpoint: str) -> dict:
        current_time = datetime.now(timezone.utc)

        # Check if cache for the specific endpoint is valid
        if endpoint in self.cache and endpoint in self.cache_time:
            if current_time - self.cache_time[endpoint] < self.cache_duration:
                logger.debug("Using cached data for endpoint: %s", endpoint)
                return self.cache[endpoint]

        # Fetch new data and update cache
        logger.debug("Fetching new data for endpoint: %s", endpoint)
        data = self.get_data(endpoint)
        self.cache[endpoint] = data
        self.cache_time[endpoint] = current_time
        return data

    def get_data(self, endpoint: str) -> Dict[str, Any]:
        """
        Makes the API call based on the argument provided.

        Args:
            endpoint (str): The endpoint to call

        Returns:
            dict: The JSON response from the API.
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"x-api-key": self.api_key}

        logger.debug("Getting data from %s", url)

        try:
            response = requests.get(url, headers=headers, timeout=self.TIMEOUT)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Failed to get data from %s: %s", url, e)
            raise e

import json
import logging
import requests
from enum import Enum
from diskcache import Cache
from tempfile import gettempdir

# Set Logging
logging.basicConfig(level=logging.INFO)


class RequestType(Enum):
    """
    Enum class for RequestType containing 4 values - GET, POST, PUT, PATCH, DELETE
    """

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class AyJay:
    """
    Class for calling APIs providing json data with caching.
    """

    def __init__(
        self,
        disable_caching: bool = False,
        cache_path: str = None,
        cache_expiry: int = None,
    ):
        """
        Function to initialise the ayjay API Class.
        """
        self.logger = logging.getLogger(__name__)
        self.headers = {"Content-Type": "application/json"}
        self.cache_expire = cache_expiry
        self.disable_caching = disable_caching
        if not disable_caching:
            file_path = cache_path if cache_path else gettempdir()
            try:
                self.cache = Cache(file_path + "ayjay_cache.dat")
            except (IOError, ValueError):
                self.cache = {}

    def call_api_raw(
        self, request_type: str, endpoint: str, payload: dict | str = None
    ) -> str:
        """
        Function to call the API via the Requests Library
        :param request_type: Type of Request.
               Supported Values - GET, POST, PUT, PATCH, DELETE.
               Type - String
        :param endpoint: API Endpoint. Type - String
        :param payload: API Request Parameters or Query String.
               Type - String or Dict
        :return: Response. Type - JSON Formatted String
        """
        try:
            response = ""
            if request_type == "GET":
                response = requests.get(endpoint, timeout=30, params=payload)
            elif request_type == "POST":
                response = requests.post(
                    endpoint, headers=self.headers, timeout=30, json=payload
                )

            if response.status_code in (200, 201):
                return response.json()
            elif response.status_code == 401:
                return json.dumps(
                    {"ERROR": "Authorization Error. " "Please check API Key"}
                )
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logging.error(errh)
        except requests.exceptions.ConnectionError as errc:
            logging.error(errc)
        except requests.exceptions.Timeout as errt:
            logging.error(errt)
        except requests.exceptions.RequestException as err:
            logging.error(err)

    def get(self, endpoint: str, params: dict):
        """
        Function for for getting a response from to the endpoint.
        :param params: Query String Parameters. Type - Dict
        :return: Response. Type - JSON Formatted String
        """
        if isinstance(params, dict):
            response = self._cache(
                self.call_api_raw(
                    request_type=RequestType.GET.value,
                    endpoint=endpoint,
                    payload=params,
                )
            )
        else:
            raise ValueError("ERROR - Parameter 'params' should be of Type Dict")
        return response

    def post(self, endpoint: str, payload: dict):
        """
        Function for for posting to the endpoint.
        :param params: Query String Parameters. Type - Dict
        :return: Response. Type - JSON Formatted String
        """
        if isinstance(payload, dict):
            response = self.call_api_raw(
                request_type=RequestType.POST.value, endpoint=endpoint, payload=payload
            )
        else:
            raise ValueError("ERROR - Parameter 'payload' should be of Type Dict")
        return response

    def _cache(self, original_func):
        def cached_func(*args, **kwargs):
            if not self.disable_caching:
                key = original_func.__name__ + str(args) + str(kwargs)
                if key not in self.cache:
                    self.cache[key] = original_func(*args, **kwargs)
                return self.cache[key]
            else:
                return original_func(*args, **kwargs)

        return cached_func

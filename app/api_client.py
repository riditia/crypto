import time
import json
import requests
import urllib
from urllib.parse import urlparse, urlencode, unquote_plus
from cryptography.hazmat.primitives.asymmetric import ed25519
from collections import OrderedDict

class CoinSwitchAPIClient:
    def __init__(self, api_key, secret_key):
        self.base_url = "https://coinswitch.co"
        self.api_key = api_key
        self.secret_key = secret_key

    def _get_server_time(self):
        """Fetches the official server time."""
        try:
            url = self.base_url + "/trade/api/v2/time"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()["serverTime"]
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch server time: {e}")
            return None

    def _generate_signature(self, method, endpoint, params, epoch_time):
        """Generates the required signature for API requests."""
        unquote_endpoint = endpoint
        if method == "GET" and params:
            # Use OrderedDict to ensure params are sorted alphabetically by key
            sorted_params = OrderedDict(sorted(params.items()))
            endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(sorted_params)
            unquote_endpoint = unquote_plus(endpoint)

        signature_msg = method + unquote_endpoint + str(epoch_time)

        request_string = bytes(signature_msg, 'utf-8')
        secret_key_bytes = bytes.fromhex(self.secret_key)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
        signature_bytes = private_key.sign(request_string)
        signature = signature_bytes.hex()

        return signature

    def _request(self, method, path, params=None):
        """Constructs and sends a request to the API."""
        if params is None:
            params = {}

        server_time = self._get_server_time()
        if not server_time:
            return None # Stop if we can't get the server time

        signature = self._generate_signature(method, path, params, server_time)

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-SIGNATURE': signature,
            'X-AUTH-APIKEY': self.api_key,
            'X-AUTH-EPOCH': str(server_time)
        }

        url = self.base_url + path

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            else:
                response = requests.request(method, url, headers=headers, json=params)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            if e.response is not None:
                print(f"Error response from server: {e.response.text}")
            return None

    def get_candles(self, symbol, interval, start_time, end_time, exchange='coinswitchx'):
        """Fetches candle data for a given symbol."""
        path = "/trade/api/v2/candles"
        params = {
            "symbol": symbol,
            "interval": str(interval),
            "start_time": str(start_time),
            "end_time": str(end_time),
            "exchange": exchange
        }
        return self._request("GET", path, params=params)

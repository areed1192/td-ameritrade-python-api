import json
import requests
import logging
import pathlib

from typing import Dict


class TdAmeritradeSession():

    """Serves as the Session for TD Ameritrade API."""

    def __init__(self, td_client: object) -> None:
        """Initializes the `TdAmeritradeSession` client.

        ### Overview
        ----
        The `TdAmeritradeSession` object handles all the requests made
        for the different endpoints on the TD Ameritrade API.

        ### Parameters
        ----
        client : object
            The `TdAmeritradeClient` Python Client.

        ### Usage:
        ----
            >>> td_session = TdAmeritradeSession()
        """

        from td.client import TdAmeritradeClient

        # We can also add custom formatting to our log messages.
        log_format = '%(asctime)-15s|%(filename)s|%(message)s'

        self.client: TdAmeritradeClient = td_client
        self.resource_url = 'https://api.tdameritrade.com/'
        self.version = 'v1/'

        if not pathlib.Path('logs').exists():
            pathlib.Path('logs').mkdir()
            pathlib.Path('logs/log_file_custom.log').touch()

        logging.basicConfig(
            filename="logs/log_file_custom.log",
            level=logging.INFO,
            encoding="utf-8",
            format=log_format
        )

    def build_headers(self) -> Dict:
        """Used to build the headers needed to make the request.

        ### Parameters
        ----
        mode: str, optional
            The content mode the headers is being built for, by default `json`.

        ### Returns
        ----
        Dict:
            A dictionary containing all the components.
        """

        # Fake the headers.
        headers = {
            "Authorization": "Bearer {access_token}".format(access_token=self.client.td_credentials.access_token),
            "Content-Type": "application/json"
        }

        return headers

    def build_url(self, endpoint: str) -> str:
        """Build the URL used the make string.

        ### Parameters
        ----
        endpoint : str
            The endpoint used to make the full URL.

        ### Returns
        ----
        str:
            The full URL with the endpoint needed.
        """

        url = self.resource_url + self.version + endpoint

        return url

    def make_request(
        self,
        method: str,
        endpoint: str,
        params: dict = {},
        data: dict = {},
        json_payload: dict = {}
    ) -> Dict:
        """Handles all the requests in the library.

        ### Overview
        ---
        A central function used to handle all the requests made in the library,
        this function handles building the URL, defining Content-Type, passing
        through payloads, and handling any errors that may arise during the
        request.

        ### Parameters
        ----
        method : str 
            The Request method, can be one of the following: 
            ['get','post','put','delete','patch']

        endpoint : str
            The API URL endpoint, example is 'quotes'

        params : dict (optional, Default={})
            The URL params for the request.

        data : dict (optional, Default={})
        A data payload for a request.

        json_payload : dict (optional, Default={})
            A json data payload for a request

        ### Returns
        ----
        Dict: 
            A Dictionary object containing the 
            JSON values.
        """

        self.client.td_credentials._validate_token()

        # Build the URL.
        url = self.build_url(endpoint=endpoint)

        # Define the headers.
        headers = self.build_headers()

        logging.info(
            "URL: {url}".format(url=url)
        )

        # Define a new session.
        request_session = requests.Session()
        request_session.verify = True

        # Define a new request.
        request_request = requests.Request(
            method=method.upper(),
            headers=headers,
            url=url,
            params=params,
            data=data,
            json=json_payload
        ).prepare()

        # Send the request.
        response: requests.Response = request_session.send(
            request=request_request
        )

        # Close the session.
        request_session.close()

        # If it's okay and no details.
        if response.ok and len(response.content) > 0:

            return response.json()

        elif len(response.content) > 0 and response.ok:
            return {
                'message': 'response successful',
                'status_code': response.status_code
            }
        elif not response.ok:

            if len(response.content) == 0:
                response_data = ''
            else:
                response_data = response.json()

            response.request.headers['Authorization'] = 'Bearer XXXXXXX'

            # Define the error dict.
            error_dict = {
                'error_code': response.status_code,
                'response_url': response.url,
                'response_body': response_data,
                'response_request': dict(response.request.headers),
                'response_method': response.request.method,
            }

            # Log the error.
            logging.error(
                msg=json.dumps(obj=error_dict, indent=4)
            )

            raise requests.HTTPError()

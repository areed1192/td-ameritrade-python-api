from datetime import date, datetime
import json
import requests
import webbrowser
import urllib
import pathlib

from urllib.parse import parse_qs
from urllib.parse import urlparse

from typing import Union


class TdCredentials():

    """
    ### Overview
    ----
    TD Ameritrade uses an oAuth protocol
    to authenticate it's users. The `TdCredential`
    object helps the user manage the credentials to ensure
    the are properly authenticated.
    """

    def __init__(self, client_id: str, redirect_uri: str, credential_dict: dict = None, credential_file: Union[str, pathlib.Path] = None) -> None:
        """Initializes the `TdCredential` object."""

        self._access_token = ''
        self._refresh_token = ''
        self._scope = []
        self._token_type = ''
        self._expires_in = 0
        self._refresh_token_expires_in = 0
        self._is_expired = True
        self._client_id = client_id
        self._redirect_uri = redirect_uri

        self._refresh_token_expiration_time = 0
        self._access_token_expiration_time = 0

        self.resource_url = 'https://api.tdameritrade.com/'
        self.version = 'v1/'
        self.token_endpoint = 'oauth2/token'
        self.authorization_url = 'https://auth.tdameritrade.com/auth?'
        self.authorization_code = ""
        self._loaded_from_file = False
        self._file_path = ""

        if credential_file:

            if isinstance(credential_file, pathlib.Path):
                credential_file = credential_file.resolve()

            self._loaded_from_file = True
            self._file_path = credential_file
            self.from_credential_file(file_path=credential_file)

        elif credential_dict:
            self.from_credential_dict(token_dict=credential_dict)
        else:
            self.from_workflow()

    @property
    def redirect_uri(self) -> str:
        """Returns the user's redirect URI.

        ### Returns
        ----
        str
            The User's redirect URI.

        ### Usage
        ----
            >>> td_credential = TdCredentials()
            >>> td_credential.redirect_uri
        """

        return self._redirect_uri

    @property
    def client_id(self) -> str:
        """Returns the Client ID.

        ### Returns
        ----
        str
            The users Client Id.

        ### Usage
        ----
            >>> td_credential = TdCredentials()
            >>> td_credential.client_id
        """
        return self._client_id

    @property
    def access_token(self) -> str:
        """Returns the Access token.

        ### Returns
        ----
        str
            A valid Access Token.

        ### Usage
        ----
            >>> td_credential = TdCredentials()
            >>> td_credential.access_token
        """

        return self._access_token

    @property
    def refresh_token(self) -> str:
        """Returns the Refresh token.

        ### Returns
        ----
        str
            A valid Refresh Token.

        ### Usage
        ----
            >>> td_credential = TdCredentials()
            >>> td_credential.refresh_token
        """
        return self._refresh_token

    @property
    def refresh_token_expiration_time(self) -> datetime:
        """Returns when the Refresh Token will expire.

        ### Returns
        ----
        datetime
            The date and time of the refresh token
            expiration.

        ### Usage
        ----
            >>> td_credential = TdCredentials()
            >>> td_credential.refresh_token_expiration_time
        """
        return self._refresh_token_expiration_time

    @property
    def is_refresh_token_expired(self) -> bool:
        """Specifies whether the current Refresh Token is expired
        or not.

        ### Returns
        ----
        bool
            `True` if the Refresh Token is expired,
            `False` otherwise.

        ### Usage
        ----
            >>> td_credential = TdCredentials()
            >>> td_credential.is_refresh_token_expired
        """

        if (self.refresh_token_expiration_time.timestamp() - 20) < datetime.now().timestamp():
            return True
        else:
            return False

    def from_token_dict(self, token_dict: dict) -> None:
        """Converts a token dicitonary to a `TdCredential`
        object.

        ### Parameters
        ----
        token_dict : dict
            A dictionary containing all the
            original token details.

        ### Usage
        ----
            >>> td_credential = TdCredentials()
            >>> td_credential.from_dict(
                token_dict={
                    'access_token': '',
                    'refresh_token': ',
                    'scope': '',
                    'expires_in': 0,
                    'refresh_token_expires_in': 0,
                    'token_type': ''
                }
            )
        """

        self._access_token = token_dict.get('access_token', '')
        self._refresh_token = token_dict.get('refresh_token', '')
        self._scope = token_dict.get('scope', [])
        self._token_type = token_dict.get('token_type', '')
        self._expires_in = token_dict.get('expires_in', 0)

        self._refresh_token_expires_in = token_dict.get(
            'refresh_token_expires_in',
            0
        )
        self._refresh_token_expiration_time = token_dict.get(
            'refresh_token_expiration_time', 0
        )

        self._access_token_expiration_time = token_dict.get(
            'access_token_expiration_time', 0
        )

        # Calculate the Refresh Token expiration time.
        if isinstance(self._refresh_token_expiration_time, str):
            self._refresh_token_expiration_time = datetime.fromisoformat(
                self._refresh_token_expiration_time
            )
        elif isinstance(self._refresh_token_expiration_time, float):
            self._refresh_token_expiration_time = datetime.fromtimestamp(
                self._refresh_token_expiration_time
            )
        else:
            self._calculate_refresh_token_expiration(
                expiration_secs=self._refresh_token_expires_in
            )

        # Calculate the Access Token Expiration Time.
        if isinstance(self._access_token_expiration_time, str):
            self._access_token_expiration_time = datetime.fromisoformat(
                self._access_token_expiration_time
            )
        elif isinstance(self._access_token_expiration_time, float):
            self._access_token_expiration_time = datetime.fromtimestamp(
                self._access_token_expiration_time
            )
        else:
            self._calculate_access_token_expiration(
                expiration_secs=self._expires_in,
            )

        self._validate_token()

    def to_token_dict(self) -> dict:
        """Converts the TdCredential object
        to a dictionary object.

        ### Returns
        ----
        dict
            A dictionary containing all the
            original token details.

        ### Usage
        ----
            >>> td_credential = TdCredentials()
            >>> td_credential.to_dict()
        """

        token_dict = {
            'access_token': self._access_token,
            'refresh_token': self._refresh_token,
            'scope': self._scope,
            'expires_in': self._expires_in,
            'refresh_token_expires_in': self._refresh_token_expires_in,
            'token_type': self._token_type,
            'refresh_token_expiration_time': self.refresh_token_expiration_time.isoformat(),
            'access_token_expiration_time': self.access_token_expiration_time.isoformat(),
        }

        return token_dict

    def _calculate_refresh_token_expiration(self, expiration_secs: int) -> None:
        """Calculates the number of seconds until the refresh token
        expires.

        ### Parameters
        ----
        expiration_secs : int
            The number of seconds until expiration.
        """

        expiration_time = datetime.now().timestamp() + expiration_secs
        self._refresh_token_expiration_time = datetime.fromtimestamp(
            expiration_time
        )

    def _calculate_access_token_expiration(self, expiration_secs: int) -> None:
        """Calculates the number of seconds until the access token
        expires.

        ### Parameters
        ----
        expiration_secs : int
            The number of seconds until expiration.
        """

        expiration_time = datetime.now().timestamp() + expiration_secs
        self._access_token_expiration_time = datetime.fromtimestamp(
            expiration_time
        )

    @property
    def access_token_expiration_time(self) -> datetime:
        """Returns when the Access Token will expire.

        ### Returns
        ----
        datetime
            The date and time of the access token
            expiration.

        ### Usage
        ----
            >>> td_credential = TdCredentials()
            >>> td_credential.access_token_expiration_time
        """
        return self._access_token_expiration_time

    @property
    def is_access_token_expired(self) -> bool:
        """Specifies whether the current Access Token is expired
        or not.

        ### Returns
        ----
        bool
            `True` if the Access Token is expired,
            `False` otherwise.

        ### Usage
        ----
            >>> td_credential = TdCredentials()
            >>> td_credential.is_access_token_expired
        """

        if (self.access_token_expiration_time.timestamp() - 20) < datetime.now().timestamp():
            return True
        else:
            return False

    def from_workflow(self) -> None:
        """Grabs an Access toke and refresh token using
        the oAuth workflow.

        ### Usage
        ----
            >>> td_credentials = TdCredentials(
                client_id=client_id,
                redirect_uri=redirect_uri,
                credential_file='config/td_credentials.jsonc'
            )
            >>> td_credentials.from_workflow()
        """

        self._grab_authorization_code()
        token_dict = self.exchange_code_for_token(return_refresh_token=True)
        self.from_token_dict(token_dict=token_dict)

    def from_credential_file(self, file_path: str) -> None:

        with open(file=file_path, mode='r') as token_file:
            token_dict = json.load(fp=token_file)
            self.from_token_dict(token_dict=token_dict)

    def to_token_file(self, file_path: Union[str, pathlib.Path]) -> None:
        """Takes the token dictionary and saves it to a JSON file.

        ### Parameters
        ----
        file_path : Union[str, pathlib.Path]
            The file path to the credentials file.

        ### Usage
        ----
            >>> td_credentials.to_token_file(
                    file_path='config/td_credentials.json'
                )
        """

        if isinstance(file_path, pathlib.Path):
            file_path = file_path.resolve()

        with open(file=file_path, mode='w+') as token_file:
            json.dump(obj=self.to_token_dict(), fp=token_file, indent=2)

    def from_credential_dict(self, token_dict: dict) -> None:
        """Loads the credentials from a token dictionary.

        ### Parameters
        ----
        token_dict : dict
            The token dictionary with the required
            authentication tokens.

        ### Usage
        ----
            >>> td_credentials.from_credential_dict(
                    file_path='config/td_credentials.json'
                )
        """

        self.from_token_dict(token_dict=token_dict)
        self._validate_token()

    def _grab_authorization_code(self) -> None:
        """Generates the URL to grab the authorization code."""

        data = {
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id + "@AMER.OAUTHAP"
        }

        # url encode the data.
        params = urllib.parse.urlencode(data)

        # build the full URL for the authentication endpoint.
        url = self.authorization_url + params

        webbrowser.open(url=url)

        code_url = input("Please Paste the Authorization Code Here: ")

        query = urlparse(url=code_url)
        parse_code = parse_qs(qs=query.query)

        self.authorization_code = parse_code['code'][0]

    def exchange_code_for_token(self, return_refresh_token: bool) -> dict:
        """Access token handler for AuthCode Workflow.

        ### Overview
        ----
        This takes the authorization code parsed from
        the auth endpoint to call the token endpoint
        and obtain an access token.

        ### Parameters
        ----
        return_refresh_token: bool
            If set to `True`, will request a refresh token in
            the request. Otherwise, will only request an access
            token along.

        ### Returns
        ----
        dict :
            The token dictionary with the content.
        """

        # Define the parameters of our access token post.
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id + '@AMER.OAUTHAP',
            'code': self.authorization_code,
            'redirect_uri': self.redirect_uri
        }

        if return_refresh_token:
            data['access_type'] = 'offline'

        # Make the request.
        response = requests.post(
            url="https://api.tdameritrade.com/v1/oauth2/token",
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=data
        )

        if response.ok:
            return response.json()
        else:
            raise requests.HTTPError()

    def grab_access_token(self) -> dict:
        """Refreshes the current access token.

        This takes a valid refresh token and refreshes
        an expired access token. This is different from
        exchanging a code for an access token.

        ### Returns
        ----
        dict:
            The dictionary contain all the token
            info.
        """

        # build the parameters of our request
        data = {
            'client_id': self.client_id,
            'grant_type': 'refresh_token',
            'access_type': 'offline',
            'refresh_token': self.refresh_token
        }

        # Make the request.
        response = requests.post(
            url="https://api.tdameritrade.com/v1/oauth2/token",
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=data
        )

        if response.ok:
            return response.json()
        else:
            raise requests.HTTPError()

    def _validate_token(self) -> None:
        """Validates the access token and refresh token.

        ### Overview
        ----
        A TD Ameritrade Access token is only valid for 30 minutes,
        and a TD Ameritrade Refresh token is only valid for 90 days.
        When an access token expires, a new one is retrieved using the
        refresh token. If the refresh token is expired the oAuth workflow
        starts again.
        """

        if self.is_refresh_token_expired:
            print("Refresh Token Expired, initiating oAuth workflow.")
            self.from_workflow()

        if self.is_access_token_expired:
            print("Access Token Expired, refreshing access token.")
            token_dict = self.grab_access_token()
            self.from_token_dict(token_dict=token_dict)

            if self._loaded_from_file:
                self.to_token_file(file_path=self._file_path)

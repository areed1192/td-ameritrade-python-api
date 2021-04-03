import json
import requests
import webbrowser
import urllib

from urllib.parse import parse_qs
from urllib.parse import urlparse

from datetime import datetime
# from td.server import AuthCodeRedirectServer
from td.credentials import TdCredentials
# from td.client import TdAmeritradeClient

# grant_type
# (required)
# The grant type of the oAuth scheme. Possible values are authorization_code, refresh_token

# refresh_token
# Required if using refresh token grant

# access_type
# Set to offline to receive a refresh token on an authorization_code grant type request. Do not set to offline on a refresh_token grant type request.

# code
# Required if trying to use authorization code grant

# client_id
# (required)
# OAuth User ID of your application

# redirect_uri
# Required if trying to use authorization code grant

# https://github.com/Azure/azure-sdk-for-python/blob/873435f4bd7b749f9c87b07442b96ba42ccfaf90/sdk/identity/azure-identity/azure/identity/_internal/auth_code_redirect_handler.py#L54


class TdAmeritradeOauth():

    def __init__(self, client_id: str, redirect_uri: str) -> None:

        self.resource_url = 'https://api.tdameritrade.com/'
        self.version = 'v1/'
        self.token_endpoint = 'oauth2/token'
        self.authorization_url = 'https://auth.tdameritrade.com/auth?'
        self.refresh_token = ""
        self.access_token = ""
        self.authorization_code = ""
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self._credentials = TdCredentials()

    def from_workflow(self) -> None:

        self._grab_authorization_code()
        token_dict = self.exchange_code_for_token(return_refresh_token=True)
        self._credentials.from_token_dict(token_dict=token_dict)
        print(self._credentials)

    def from_credential_file(self, file_path: str) -> None:

        with open(file=file_path, mode='r') as token_file:
            token_dict = json.load(fp=token_file)
            self._credentials.from_token_dict(token_dict=token_dict)

        self._validate_token()

    def from_credential_dict(self, token_dict: dict) -> None:

        self._credentials.from_token_dict(token_dict=token_dict)
        self._validate_token()


    def _grab_authorization_code(self) -> str:

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

        # Returns:
        ----
        {bool} -- `True` if successful, `False` otherwise.
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

        if self._credentials.is_refresh_token_expired:
            print("Refresh Token Expired, initiating oAuth workflow.")
            self.from_workflow()

        if self._credentials.is_access_token_expired:
            print("Access Token Expired, refreshing access token.")
            token_dict = self.grab_access_token()
            self._credentials.from_token_dict(token_dict=token_dict)

    # def _state_manager(self, action: str) -> None:
    #     """Manages the session state.

    #     Manages the self.state dictionary. Initalize State will set
    #     the properties to their default value. Save will save the
    #     current state if 'cache_state' is set to TRUE.

    #     ### Arguments:
    #     ----
    #     action {str}: action argument must of one of the following:
    #         'init' -- Initalize State.
    #         'save' -- Save the current state.
    #     """

    #     credentials_file_exists = self.credentials_path.exists()

    #     # if they allow for caching and the file exists then load it.
    #     if action == 'init' and credentials_file_exists:
    #         with open(file=self.credentials_path, mode='r') as json_file:
    #             self.state.update(json.load(json_file))

    #     # if they want to save it and have allowed for caching then load the file.
    #     elif action == 'save':
    #         with open(file=self.credentials_path, mode='w+') as json_file:
    #             json.dump(obj=self.state, fp=json_file, indent=4)

    # def login(self) -> bool:
    #     """Logs the user into the TD Ameritrade API.

    #     Ask the user to authenticate  themselves via the TD Ameritrade Authentication Portal. This will
    #     create a URL, display it for the User to go to and request that they paste the final URL into
    #     command window. Once the user is authenticated the API key is valide for 90 days, so refresh
    #     tokens may be used from this point, up to the 90 days.

    #     ### Returns:
    #     ----
    #     {bool} -- Specifies whether it was successful or not.
    #     """

    #     # Only attempt silent SSO if the credential file exists.
    #     if self.credentials_path.exists() and self._silent_sso():
    #         self.authstate = True
    #         return True
    #     else:
    #         self.oauth()
    #         self.authstate = True
    #         return True

    #     if self._flask_app and self.auth_flow == 'flask':
    #         run(flask_client=self._flask_app, close_after=True)

    # def grab_refresh_token(self) -> bool:
    #     """Grabs a new refresh token if expired.

    #     This takes a valid refresh token and requests
    #     a new refresh token along with an access token.
    #     This is similar to `grab_access_token` but it
    #     does not include the `access_type` argument.
    #     Which specifies to return a new refresh token
    #     along with an access token.

    #     ### Returns:
    #     ----
    #     {bool} -- `True` if successful, `False` otherwise.
    #     """

    #     # build the parameters of our request
    #     data = {
    #         'client_id': self._td_client.client_id,
    #         'grant_type': 'refresh_token',
    #         'access_type': 'offline',
    #         'refresh_token': self.refresh_token
    #     }

    #     # Make the request.
    #     response = requests.post(
    #         url="https://api.tdameritrade.com/v1/oauth2/token",
    #         headers={'Content-Type': 'application/x-www-form-urlencoded'},
    #         data=data
    #     )

    #     if response.ok:

    #         self._token_save(
    #             token_dict=response.json(),
    #             includes_refresh=True
    #         )

    #         return True

    #     else:
    #         raise TknExpError(response.json())

    # def grab_url(self) -> dict:
    #     """Builds the URL that is used for oAuth."""

    #     # prepare the payload to login
    #     data = {
    #         'response_type': 'code',
    #         'redirect_uri': self._td_client.redirect_uri,
    #         'client_id': self._td_client.redirect_uri + '@AMER.OAUTHAP'
    #     }

    #     # url encode the data.
    #     params = urllib.parse.urlencode(data)

    #     # build the full URL for the authentication endpoint.
    #     url = "https://auth.tdameritrade.com/auth?" + params

    #     return url

    # def oauth(self) -> None:
    #     """Runs the oAuth process for the TD Ameritrade API."""

    #     # Create the Auth URL.
    #     url = self.grab_url()

    #     # Print the URL.
    #     print(
    #         'Please go to URL provided authorize your account: {}'.format(url)
    #     )

    #     # Paste it back and store it.
    #     self.code = input(
    #         'Paste the full URL redirect here: '
    #     )

    #     # Exchange the Code for an Acess Token.
    #     self.exchange_code_for_token(
    #         code=self.code,
    #         return_refresh_token=True
    #     )

    # def validate_token(self) -> bool:
    #     """Validates whether the tokens are valid or not.

    #     ### Returns
    #     -------
    #     bool
    #         Returns `True` if the tokens were valid, `False` if
    #         the credentials file doesn't exist.
    #     """

    #     if 'refresh_token_expires_at' in self.state and 'access_token_expires_at' in self.state:

    #         # Grab the Expire Times.
    #         refresh_token_exp = self.state['refresh_token_expires_at']
    #         access_token_exp = self.state['access_token_expires_at']

    #         refresh_token_ts = datetime.datetime.fromtimestamp(
    #             refresh_token_exp)
    #         access_token_ts = datetime.datetime.fromtimestamp(access_token_exp)

    #         # Grab the Expire Thresholds.
    #         refresh_token_exp_threshold = refresh_token_ts - timedelta(days=2)
    #         access_token_exp_threshold = access_token_ts - timedelta(minutes=5)

    #         # Convert to Seconds.
    #         refresh_token_exp_threshold = refresh_token_exp_threshold.timestamp()
    #         access_token_exp_threshold = access_token_exp_threshold.timestamp()

    #         # See if we need a new Refresh Token.
    #         if datetime.datetime.now().timestamp() > refresh_token_exp_threshold:
    #             print("Grabbing new refresh token...")
    #             self.grab_refresh_token()

    #         # See if we need a new Access Token.
    #         if datetime.datetime.now().timestamp() > access_token_exp_threshold:
    #             print("Grabbing new access token...")
    #             self.grab_access_token()

    #         return True

    #     else:

    #         pprint.pprint(
    #             {
    #                 "credential_path": str(self.credentials_path),
    #                 "message": "The credential file does not contain expiration times for your tokens, please go through the oAuth process."
    #             }
    #         )

    #         return False

    # def _silent_sso(self) -> bool:
    #     """
    #     Overview:
    #     ----
    #     Attempt a silent authentication, by checking whether current
    #     access token is valid and/or attempting to refresh it. Returns
    #     True if we have successfully stored a valid access token.

    #     ### Returns:
    #     ----
    #     {bool} -- Specifies whether it was successful or not.
    #     """

    #     if self.validate_token():
    #         return True
    #     else:
    #         return False

    # def _token_save(self, token_dict: dict, includes_refresh: bool = False) -> dict:
    #     """Parses the token and saves it.

    #     Overview:
    #     ----
    #     Parses an access token from the response of a POST request and saves it
    #     in the state dictionary for future use. Additionally, it will store the
    #     expiration time and the refresh token.

    #     ### Arguments:
    #     ----
    #     token_dict {dict} -- A response object recieved from the `grab_refresh_token` or
    #         `grab_access_token` methods.

    #     ### Returns:
    #     ----
    #     {dict} -- A token dictionary with the new added values.
    #     """

    #     # store token expiration time
    #     access_token_expire = time.time() + int(token_dict['expires_in'])
    #     acc_timestamp = datetime.datetime.fromtimestamp(access_token_expire)
    #     acc_timestamp = acc_timestamp.isoformat()

    #     # Save to the State.
    #     self.state['access_token'] = token_dict['access_token']
    #     self.state['access_token_expires_at'] = access_token_expire
    #     self.state['access_token_expires_at_date'] = acc_timestamp

    #     if includes_refresh:

    #         refresh_token_expire = time.time(
    #         ) + int(token_dict['refresh_token_expires_in'])
    #         ref_timestamp = datetime.datetime.fromtimestamp(
    #             refresh_token_expire)
    #         ref_timestamp = ref_timestamp.isoformat()

    #         # Save to the State.
    #         self.state['refresh_token'] = token_dict['refresh_token']
    #         self.state['refresh_token_expires_at'] = refresh_token_expire
    #         self.state['refresh_token_expires_at_date'] = ref_timestamp

    #     self.state['logged_in'] = True
    #     self._state_manager('save')

    #     return self.state

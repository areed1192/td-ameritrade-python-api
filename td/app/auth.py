import time
import json
import pathlib

from configparser import ConfigParser
from requests_oauthlib import OAuth2Session
from datetime import datetime
from td.utils import StatePath

from typing import Union
from typing import List
from typing import Tuple


class FlaskTDAuth():

    def __init__(self, client_id: str, redirect_uri: str, credentials_file: pathlib.Path) -> None:
        
        self.client_id: str = client_id    
        self.client_id_auth: str = client_id + '@AMER.OAUTHAP'
        self.redirect_uri: str = redirect_uri
        self.credentials_file: StatePath = credentials_file
        self.authorization_base_url = 'https://auth.tdameritrade.com/auth'
        self.token_url = 'https://api.tdameritrade.com/v1/oauth2/token'        
        self.td_ouath_session: OAuth2Session = self._initate_oauth_workflow()
        
    def _initate_oauth_workflow(self):

        # Create a new OAuth Session.
        td_ameritrade = OAuth2Session(
            client_id=self.client_id_auth,
            redirect_uri=self.redirect_uri
        )

        return td_ameritrade

    def authorization_url(self) -> Tuple:

        # Create a new OAuth Session.
        authorization_url_ret, state = self.td_ouath_session.authorization_url(
            url=self.authorization_base_url,
            state=""
        )

        return (authorization_url_ret, state)

    def grab_access_token_and_refresh_token(self, url: str):
        
        # Grabs the token dict
        token_dict = self.td_ouath_session.fetch_token(
            token_url=self.token_url,
            access_type='offline',
            authorization_response=url,
            include_client_id=True
        )

        self.save_state(token_dict=token_dict)

        self.access_token_dict = token_dict

        return token_dict

    def grab_refresh_token(self):
        
        refresh_token_dict = self.td_ouath_session.refresh_token(
            token_url=self.token_url,
            client_id=self.client_id,
            access_type='offline',
            refresh_token=self.access_token_dict['refresh_token']
        )

        self.save_state(token_dict=refresh_token_dict)

        return refresh_token_dict

    def save_token(self, token_dict: dict) -> dict:
        
        # make sure there is an access token before proceeding.
        if 'access_token' not in token_dict:
            return False

        state = {}

        # save the access token and refresh token
        state['access_token'] = token_dict['access_token']
        state['refresh_token'] = token_dict['refresh_token']

        # store token expiration time
        access_token_expire = time.time() + int(token_dict['expires_in'])
        refresh_token_expire = time.time() + int(token_dict['refresh_token_expires_in'])
        state['access_token_expires_at'] = access_token_expire
        state['refresh_token_expires_at'] = refresh_token_expire
        state['access_token_expires_at_date'] = datetime.fromtimestamp(access_token_expire).isoformat()
        state['refresh_token_expires_at_date'] = datetime.fromtimestamp(refresh_token_expire).isoformat()
        state['logged_in'] = True
        
        return state

    def save_state(self, token_dict: dict) -> None:

        if self.credentials_file.exists():
            token_dict = self.save_token(token_dict=token_dict)
            credentials_file_path = self.credentials_file.get_file_path

            # if they want to save it and have allowed for caching then load the file.
            with open(credentials_file_path, 'w+') as json_file:
                json.dump(obj=token_dict, fp=json_file, indent=4)





    

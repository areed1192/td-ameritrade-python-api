from typing import List
from typing import Dict
from typing import Union

from td.session import TdAmeritradeSession
from td.oauth import TdAmeritradeOauth

class TdAmeritradeClient():

    """
    ### Overview
    ----
    Implements OAuth 2.0 Authorization Code Grant workflow, handles configuration
    and state management, adds token for authenticated calls, and performs request 
    to the TD Ameritrade API.
    """

    def __init__(self, client_id: str, redirect_url: str) -> None:

        self.client_id = client_id
        self.redirect_uri = redirect_url
        self._td_session = TdAmeritradeSession(td_client=self)
        # self.oauth_client = TdAmeritradeOauth(td_client=self)

    def __repr__(self):
        pass

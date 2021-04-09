from typing import List
from typing import Dict
from typing import Union

from td.session import TdAmeritradeSession
from td.credentials import TdCredentials
from td.quotes import Quotes

class TdAmeritradeClient():

    """
    ### Overview
    ----
    Implements OAuth 2.0 Authorization Code Grant workflow, handles configuration
    and state management, adds token for authenticated calls, and performs request 
    to the TD Ameritrade API.
    """

    def __init__(self, credentials: TdCredentials) -> None:

        self.td_credentials = credentials
        self.td_session = TdAmeritradeSession(td_client=self)

    def __repr__(self):
        pass
    
    def quotes(self) -> Quotes:
        """Used to access the `Quotes` Services and metadata.

        ### Returns
        ---
        Quotes:
            The `Quotes` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient(
                    credentials=td_credentials
                )
            >>> quotes_service = td_client.quotes()
        """

        object: Quotes = Quotes(session=self.td_session)

        return object


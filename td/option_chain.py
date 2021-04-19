from typing import List
from td.session import TdAmeritradeSession


class OptionsChain():

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `OptionsChain` services.

        ### Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession   
            object.
        """

        self.session = session

    def _get_option_chain(self, instrument=str) -> dict:
        """Grabs real-time quotes for an instrument.

        ### Overview
        ----
        Serves as the mechanism to make a request to the Get
        Quote and Get Quotes Endpoint. If one item is provided
        a Get Quote request will be made and if more than one
        item is provided then a Get Quotes request will be made.

        ### Documentation
        ----
        https://developer.tdameritrade.com/quotes/apis

        ### Parameters
        ----
        instruments: str
            A list of different financial instruments.

        ### Usage
        ----
            >>> quote_service = td_client.quotes()
            >>> quote_service.get_quote(instrument='AAPL')
        """

        params = {
            'symbol': instrument
        }

        content = self.session.make_request(
            method='get',
            endpoint='marketdata/quotes',
            params=params
        )

        return content

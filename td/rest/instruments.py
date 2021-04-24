from typing import List
from typing import Union
from datetime import datetime
from datetime import date
from td.session import TdAmeritradeSession
from enum import Enum


class Instruments():

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `Instruments` services.

        ### Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession   
            object.
        """

        self.session = session

    def search_instruments(self, symbol: str, projection: Union[str, Enum]) -> dict:
        """Search or retrieve instrument data, including fundamental data.

        ### Documentation
        ----
        https://developer.tdameritrade.com/instruments/apis/get/instruments

        ### Parameters
        ----
        symbol: str
            The symbol of the financial instrument you would 
            like to search.

        projection: Union[str, Enum]
            The type of request, default is "symbol-search". The type of request
            include the following: `symbol-search`, `symbol-regex`, `desc-search`,
            `desc-regex` ,`fundamental`. For more info on these search types, please
            refer to the documentation link provided above.

        ### Usage
        ----
            >>> from td.enums import Instruments
            >>> instruments_service = td_client.instruments()
            >>> instruments_service.search_instruments(
                symbol='MSFT',
                projection='symbol-search'
            )
        """

        if isinstance(projection, Enum):
            projection = projection.value

        params = {
            'symbol': symbol,
            'projection': projection
        }

        content = self.session.make_request(
            method='get',
            endpoint='instruments',
            params=params
        )

        return content

    def get_instrument(self, cusip: str) -> dict:
        """Get an instrument by CUSIP.

        ### Documentation
        ----
        https://developer.tdameritrade.com/instruments/apis/get/instruments/%7Bcusip%7D

        ### Parameters
        ----
        cusip: str
            The CUSIP Id.

        ### Usage
        ----
            >>> from td.enums import Instruments
            >>> instruments_service = td_client.instruments()
            >>> instruments_service.get_instrument(
                cusip='617446448'
            )
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'instruments/{cusip}'
        )

        return content

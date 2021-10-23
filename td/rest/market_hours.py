from enum import Enum
from typing import Union
from datetime import datetime
from datetime import date
from td.session import TdAmeritradeSession


class MarketHours():

    """
    ## Overview
    ----
    Allows the user query the different market hours for
    the different financial markets.
    """

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `MarketHours` services.

        ### Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession
            object.
        """

        self.session = session

    def get_multiple_market_hours(self, markets: list, date: Union[str, datetime, date]) -> dict:
        """Returns the market hours for all the markets.

        ### Documentation
        ----
        https://developer.tdameritrade.com/market-hours/apis

        ### Parameters
        ----
        markets: list
            A list of market IDs you want to return hours for.
            Possible values are: `EQUITY`, `OPTION`, `FUTURE`,
            `BOND`, or `FOREX`.

        date: Union[str, datetime, date]
            The date you wish to recieve market hours for.
            Valid ISO-8601 formats are: yyyy-MM-dd and
            yyyy-MM-dd'T'HH:mm:ssz

        ### Usage
        ----
            >>> from td.enums import Markets
            >>> market_hours_service = td_client.market_hours()
            >>> market_hours_service.get_multiple_market_hours(
                markets=['EQUITY', Markets.Bond],
                date='2021-12-31'
            )
        """

        for index, market in enumerate(markets):
            if isinstance(market, Enum):
                markets[index] = market.value

        if isinstance(date, (date, datetime)):
            date = date.isoformat()

        params = {
            'markets': ','.join(markets),
            'date': date
        }

        content = self.session.make_request(
            method='get',
            endpoint='marketdata/hours',
            params=params
        )

        return content

    def get_market_hours(self, market: Union[str, Enum], date: Union[str, datetime, date]) -> dict:
        """Returns the market hours for the specified market.

        ### Documentation
        ----
        https://developer.tdameritrade.com/market-hours/apis

        ### Parameters
        ----
        market: Union[str, Enum]
            A list of market IDs you want to return hours for.
            Possible values are: `EQUITY`, `OPTION`, `FUTURE`,
            `BOND`, or `FOREX`.

        date: Union[str, datetime, date]
            The date you wish to recieve market hours for.
            Valid ISO-8601 formats are: yyyy-MM-dd and
            yyyy-MM-dd'T'HH:mm:ssz

        ### Usage
        ----
            >>> from td.enums import Markets
            >>> market_hours_service = td_client.market_hours()
            >>> market_hours_service.get_market_hours(
                markets='EQUITY',
                date='2021-12-31'
            )
        """

        if isinstance(market, Enum):
            market = market.value

        if isinstance(date, (date, datetime)):
            date = date.isoformat()

        params = {
            'date': date
        }

        content = self.session.make_request(
            method='get',
            endpoint=f'marketdata/{market}/hours',
            params=params
        )

        return content

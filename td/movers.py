from typing import List
from typing import Union
from td.session import TdAmeritradeSession
from enum import Enum


class Movers():

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `Movers` services.

        ### Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession   
            object.
        """

        self.session = session

    def get_movers(self, index=str, direction: Union[str, Enum] = None, change: Union[str, Enum] = None) -> dict:
        """Gets Active movers for a specific Index.

        ### Overview
        ----
        Top 10 (up or down) movers by value or percent for
        a particular market.

        ### Documentation
        ----
        https://developer.tdameritrade.com/movers/apis/get/marketdata

        ### Parameters
        ----
        market: str
            The index symbol to get movers for, can be 
            `$DJI`, `$COMPX`, or `$SPX.X`.

        direction: Union[str, Enum] (optional, default=None)
            To return movers with the specified directions
            of up or down. Valid values are `up` or `down`

        change: Union[str, Enum] (optional, default=None)
            To return movers with the specified change 
            types of percent or value. Valid values are 
            `percent` or `value`.   

        ### Usage
        ----
            >>> movers_service = td_client.movers()
            >>> movers_service.get_movers(instrument='AAPL')
        """

        if isinstance(direction, Enum):
            direction = direction.value

        if isinstance(change, Enum):
            change = change.value

        params = {
            'direction': direction,
            'change': change
        }

        content = self.session.make_request(
            method='get',
            endpoint=f'marketdata/{index}/movers',
            params=params
        )

        return content

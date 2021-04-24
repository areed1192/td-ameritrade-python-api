from typing import Union
from td.session import TdAmeritradeSession
from enum import Enum
from datetime import datetime


class PriceHistory():

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `PriceHistory` services.

        ### Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession   
            object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> price_history_service = td_client.price_history()
        """

        self.session = session
        self._period_type = ""
        self._period = ""
        self._frequency = ""
        self._start_date = ""
        self._end_date = ""
        self._frequency_type = ""
        self._extended_hours_needed = True

    def get_price_history(
        self,
        symbol: str,
        frequency_type: Union[str, Enum],
        frequency: str,
        period_type: Union[str, Enum] = 'day',
        period: int = None,
        start_date: Union[datetime] = None,
        end_date: Union[datetime] = None,
        extended_hours_needed: bool = True
    ) -> dict:
        """Gets historical candle data for a financial instrument.

        ### Documentation
        ----
        https://developer.tdameritrade.com/price-history/apis

        ### Parameters
        ----
        symbol: str
            The ticker symbol to request data for. 

        frequency_type:  Union[str, Enum]
            The type of frequency with  which a new candle
            is formed.

        frequency: str 
            The number of the frequency type 
            to be included in each candle.

        period_type: Union[str, Enum] (optional, Default='day')
            The type of period to show.  Valid values are `day`,
            `month`, `year`, or `ytd` (year to date).

        period: int (optional, Default=None)
            The number of periods to show.

        start_date: Union[str, datetime] (optional, Default=None)
            Start date as milliseconds since epoch.

        end_date: Union[str, datetime] (optional, Default=None)
            Start date as milliseconds since epoch.

        extended_hours: bool (optional, Default=True)
            True to return extended hours data, false for regular
            market hours only.

        ### Usage
        ----
            >>> price_history_service = td_client.price_history()
            >>> price_history = price_history_service.get_price_history(
                symbol='MSFT',
                frequency_type='minute',
                frequency=1,
                period_type='day',
                period=10,
                extended_hours_needed=False
            )
        """

        # Fail early, can't have a period with start and end date specified.
        if (start_date and end_date and period):
            raise ValueError('Cannot have Period with Start Date and End Date')

        # Handle datetimes.
        if isinstance(start_date, datetime):
            start_date = int(start_date.timestamp() * 1000)

        if isinstance(end_date, datetime):
            end_date = int(end_date.timestamp() * 1000)

        # Handle Enums.
        if isinstance(frequency_type, Enum):
            frequency_type = frequency_type.value

        if isinstance(period_type, Enum):
            period_type = period_type.value

        # Gets a little confusing here, so let's add some notes.
        # Step 1: check to see if we have a frequency type value provided.
        if frequency_type:

            valid_chart_values = {
                'minute': {
                    'day': [1, 2, 3, 4, 5, 10]
                },
                'daily': {
                    'month': [1, 2, 3, 6],
                    'year': [1, 2, 3, 5, 10, 15, 20],
                    'ytd': [1]
                },
                'weekly': {
                    'month': [1, 2, 3, 6],
                    'year': [1, 2, 3, 5, 10, 15, 20],
                    'ytd': [1]
                },
                'monthly': {
                    'year': [1, 2, 3, 5, 10, 15, 20]
                }
            }

            # If what was provided is not a valid frequency type then raise an error.
            if frequency_type not in valid_chart_values:
                raise KeyError(
                    "The frequency you provided is not a valid frequency."
                )
            else:

                # Step 2: Validate the period type BASED ON the frequency type.
                if period_type not in valid_chart_values[frequency_type]:
                    raise KeyError(
                        f"The period type you provided is not a valid for frequency: {frequency_type}"
                    )

                # Step 3: Finally validate the period, if a start date or end date was not provided.
                # You shouldn't have a period to validate if the start date or end date was provided.
                if period not in valid_chart_values[frequency_type][period_type] and (start_date is None or end_date is None):
                    raise KeyError(
                        f"The period you provided is not a valid for period type: {period_type}"
                    )

        params = {
            'period': period,
            'periodType': period_type,
            'startDate': start_date,
            'endDate': end_date,
            'frequency': frequency,
            'frequencyType': frequency_type,
            'needExtendedHoursData': extended_hours_needed
        }

        content = self.session.make_request(
            method='get',
            endpoint=f'marketdata/{symbol}/pricehistory',
            params=params
        )

        return content

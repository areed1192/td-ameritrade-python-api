from enum import Enum
from typing import Union
from typing import List
from datetime import datetime


class StreamingServices():

    def __init__(self, streaming_api_client: object) -> None:
        """Initializes the `StreamingServices` object.

        ### Parameters
        ----
        streaming_api_client : StreamingApiClient
            The streaming API client that handles sending requests.
        """

        from td.streaming.client import StreamingApiClient

        self.streaming_api_client: StreamingApiClient = streaming_api_client

    def _new_request_template(self) -> dict:
        """Serves as a template to build new service requests.

        ### Overview
        ----
        This takes the Request template and populates the required fields
        for a subscription request.

        ### Returns
        ----
        dict:
            The service request with the standard fields
            filled out.
        """

        # Grab the current count of the services.
        service_count = len(
            self.streaming_api_client.data_requests['requests']
        ) + 1

        request = {
            "service": None,
            "requestid": service_count,
            "command": None,
            "account": self.streaming_api_client.user_principal_data['accounts'][0]['accountId'],
            "source": self.streaming_api_client.user_principal_data['streamerInfo']['appId'],
            "parameters": {
                "keys": None,
                "fields": None
            }
        }

        return request

    def quality_of_service(self, qos_level: Union[str, Enum]) -> None:
        """Quality of Service Subscription.

        ### Overview
        ----
        Allows the user to set the speed at which they recieve
        messages from the TD Server.

        ### Parameters
        ----
        qos_level: Union[str, Enum]
            The Quality of Service level that you wish to set. 
            Ranges from 0 to 5 where 0 is the fastest and 5 is
            the slowest.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.quality_of_service(
                qos_level='1'
            )
        """

        # Build the request
        request = self._new_request_template()
        request['service'] = 'ADMIN'
        request['command'] = 'QOS'
        request['parameters']['qoslevel'] = qos_level
        self.streaming_api_client.data_requests['requests'].append(request)

    def level_one_quotes(self, symbols: List[str], fields: Union[List[Enum], List[str], List[int]]) -> None:
        """Provides access to level one streaming quotes.

        ### Parameters
        ----
        symbols: List[str]
            A List of symbols you wish to stream quotes for.

        fields: Union[List[Enum], List[str], List[int]]
            The fields you want returned from the Endpoint, can either
            be the numeric representation or the key value representation.
            For more info on fields, refer to the documentation.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.level_one_quotes(
                symbols=['AAPL','SQ'],
                fields=LevelOneQuotes.All
            )
        """

        if isinstance(fields, list):
            new_fields = []
            for field in fields:
                if isinstance(field, int):
                    field = str(int)
                elif isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

        if isinstance(fields, Enum):
            fields = fields.value

        # Build the request
        request = self._new_request_template()
        request['service'] = 'QUOTE'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.streaming_api_client.data_requests['requests'].append(request)

    def level_one_options(self, symbols: List[str], fields: Union[List[Enum], List[str], List[int]]) -> None:
        """Provides access to level one streaming options quotes.

        ### Parameters
        ----
        symbols: List[str]
            A List of symbols you wish to stream quotes for.

        fields: Union[List[Enum], List[str], List[int]]
            The fields you want returned from the Endpoint, can either
            be the numeric representation or the key value representation.
            For more info on fields, refer to the documentation.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.level_one_options(
                symbols=['MSFT_043021C120'],
                fields=LevelOneOptions.All
            )
        """

        if isinstance(fields, list):
            new_fields = []
            for field in fields:
                if isinstance(field, int):
                    field = str(int)
                elif isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

        if isinstance(fields, Enum):
            fields = fields.value

        # Build the request
        request = self._new_request_template()
        request['service'] = 'OPTION'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.streaming_api_client.data_requests['requests'].append(request)

    def level_one_futures(self, symbols: List[str], fields: Union[List[Enum], List[str], List[int]]) -> None:
        """Provides access to level one streaming futures quotes.

        ### Parameters
        ----
        symbols: List[str]
            A List of symbols you wish to stream quotes for.

        fields: Union[List[Enum], List[str], List[int]]
            The fields you want returned from the Endpoint, can either
            be the numeric representation or the key value representation.
            For more info on fields, refer to the documentation.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.level_one_futures(
                symbols=['/ES'],
                fields=LevelOneFutures.All
            )
        """

        if isinstance(fields, list):
            new_fields = []
            for field in fields:
                if isinstance(field, int):
                    field = str(int)
                elif isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

        if isinstance(fields, Enum):
            fields = fields.value

        # Build the request
        request = self._new_request_template()
        request['service'] = 'LEVELONE_FUTURES'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.streaming_api_client.data_requests['requests'].append(request)

    def level_one_futures_options(self, symbols: List[str], fields: Union[List[Enum], List[str], Enum]) -> None:
        """Provides access to level one streaming futures options quotes.

        ### Parameters
        ----
        symbols: List[str]
            A List of symbols you wish to stream quotes for.

        fields: Union[List[Enum], List[str]]
            The fields you want returned from the Endpoint, can either
            be the numeric representation or the key value representation.
            For more info on fields, refer to the documentation.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.level_one_futures(
                symbols=['./EW2J20C2675'],
                fields=LevelOneFutures.All
            )
        """

        if isinstance(fields, list):
            new_fields = []
            for field in fields:
                if isinstance(field, int):
                    field = str(int)
                elif isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

        if isinstance(fields, Enum):
            fields = fields.value

        # Build the request
        request = self._new_request_template()
        request['service'] = 'LEVELONE_FUTURES_OPTIONS'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.streaming_api_client.data_requests['requests'].append(request)

    def level_one_forex(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """Provides access to level one streaming forex quotes.

        ### Parameters
        ----
        symbols: List[str]
            A List of symbols you wish to stream quotes for.

        fields: Union[List[Enum], List[str], List[int]]
            The fields you want returned from the Endpoint, can either
            be the numeric representation or the key value representation.
            For more info on fields, refer to the documentation.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.level_one_forex(
                symbols=['EUR/USD'],
                fields=LevelOneForex.All
            )
        """

        if isinstance(fields, list):
            new_fields = []
            for field in fields:
                if isinstance(field, int):
                    field = str(int)
                elif isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

        if isinstance(fields, Enum):
            fields = fields.value

        # Build the request
        request = self._new_request_template()
        request['service'] = 'LEVELONE_FOREX'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.streaming_api_client.data_requests['requests'].append(request)

    def account_activity(self) -> None:
        """
        ### Overview
        ----
        Represents the ACCOUNT_ACTIVITY endpoint of the TD
        Streaming API. This service is used to request streaming
        updates for one or more accounts associated with
        the logged in User ID. Common usage would involve issuing
        the OrderStatus API request to get all transactions for an
        account, and subscribing to ACCT_ACTIVITY to get any updates.
        """

        # Build the request
        request = self._new_request_template()
        request['service'] = 'ACCT_ACTIVITY'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = self.streaming_api_client.user_principal_data['streamerSubscriptionKeys']['keys'][0]['key']
        request['parameters']['fields'] = '0,1,2,3'

        self.streaming_api_client.data_requests['requests'].append(request)

    def news_headline(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """Provides access to streaming News Articles.

        ### Parameters
        ----
        symbols: List[str]
            A List of symbols you wish to stream quotes for.

        fields: Union[List[Enum], List[str], List[int]]
            The fields you want returned from the Endpoint, can either
            be the numeric representation or the key value representation.
            For more info on fields, refer to the documentation.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.news_headline(
                symbols=['MSFT', 'GOOG', 'AAPL'],
                fields=NewsHeadlines.All
            )
        """

        if isinstance(fields, list):
            new_fields = []
            for field in fields:
                if isinstance(field, int):
                    field = str(int)
                elif isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

        if isinstance(fields, Enum):
            fields = fields.value

        # Build the request
        request = self._new_request_template()
        request['service'] = 'NEWS_HEADLINE'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.streaming_api_client.data_requests['requests'].append(request)

    def chart(self, service: Union[str, Enum], symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """Subscribes to the Chart Service.

        ### Overview
        ----
        Represents the CHART_EQUITY, CHART_FUTRUES, and CHART_OPTIONS endpoint that can
        be used to stream info needed to recreate charts.

        ### Parameters
        ---
        service: Union[str, Enum]
            The type of Chart Service you wish to recieve. Can be either
            `CHART_EQUITY`, `CHART_FUTURES` or `CHART_OPTIONS`

        symbols: List[str]
            A List of symbols you wish to stream quotes for.

        fields: Union[List[Enum], List[str], List[int]]
            The fields you want returned from the Endpoint, can either
            be the numeric representation or the key value representation.
            For more info on fields, refer to the documentation.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.chart(
                service=ChartServices.ChartEquity,
                symbols=['MSFT', 'GOOG', 'AAPL'],
                fields=ChartEquity.All
            )
        """

        if isinstance(service, Enum):
            service = service.value

        if isinstance(fields, list):
            new_fields = []
            for field in fields:
                if isinstance(field, int):
                    field = str(int)
                elif isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

        if isinstance(fields, Enum):
            fields = fields.value

        # Build the request
        request = request = self._new_request_template()
        request['service'] = service
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)
        self.streaming_api_client.data_requests['requests'].append(request)

    def timesale(self, service: str, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
        """Stream Time & Sales Data.

        ### Parameters
        ---
        service: Union[str, Enum]
            The different timesale services, can be `TIMESALE_EQUITY`,
            `TIMESALE_OPTIONS`, `TIMESALE_FUTURES`.

        symbols: List[str]
            A List of symbols you wish to stream quotes for.

        fields: Union[List[Enum], List[str], List[int]]
            The fields you want returned from the Endpoint, can either
            be the numeric representation or the key value representation.
            For more info on fields, refer to the documentation.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.timesale(
                service=TimesaleServices.TimesaleEquity,
                symbols=['MSFT', 'GOOG', 'AAPL'],
                fields=Timesale.All
            )
        """

        if isinstance(service, Enum):
            service = service.value

        if isinstance(fields, list):
            new_fields = []
            for field in fields:
                if isinstance(field, int):
                    field = str(int)
                elif isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

        if isinstance(fields, Enum):
            fields = fields.value

        # Build the request
        request = self._new_request_template()
        request['service'] = service
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.streaming_api_client.data_requests['requests'].append(request)

    def actives(self, service: Union[str, Enum], venue: Union[str, Enum], duration: Union[str, Enum]) -> None:
        """Stream most actively traded stocks for a specific exchange.

        ### Parameters
        ---
        service: Union[str, Enum]
            One of the different actives services. For a full
            list please refer to the `enums` file.

        service: Union[str, Enum]
            One of the exchanges. For a full
            list please refer to the `enums` file.

        duration: Union[str, Enum]
            Specifies the look back period for collecting most
            actively traded instrument. For a full list please
            refer to the `enums` file. 

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.actives(
                service=ActivesServices.ActivesNasdaq,
                venue=ActivesVenues.NasdaqExchange,
                duration=ActivesDurations.All                
            )
        """

        if isinstance(service, Enum):
            service = service.value

        if isinstance(venue, Enum):
            venue = venue.value

        if isinstance(duration, Enum):
            duration = duration.value

        # Build the request
        request = self._new_request_template()
        request['service'] = service
        request['command'] = 'SUBS'
        request['parameters']['keys'] = venue + '-' + duration
        request['parameters']['fields'] = '1'
        self.streaming_api_client.data_requests['requests'].append(request)

    def chart_history_futures(
        self,
        symbols: List[str],
        frequency: Union[str, Enum],
        period: Union[str, Enum] = None,
        start_time: Union[str, datetime] = None,
        end_time: Union[str, datetime] = None
    ) -> None:
        """Stream historical futures prices for charting. For normal equity charts, please use the
        the `get_historical_prices` method.

        ### Parameters
        ---
        symbols: List[str]
            A List of symbols you wish to stream quotes for.

        frequency: Union[str, Enum]
            The frequency at which you want the data to appear.

        period: Union[str, Enum] (optional, Default=None)
            The period you wish to return historical data for. Not
            required if `start_time` or `end_time` is set.

        start_time: Union[str, datetime] (optional, Default=None)
            Start time of chart in milliseconds since Epoch.

        end_time: Union[str, datetime] (optional, Default=None)
            End time of chart in milliseconds since Epoch.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.chart_history_futures(
                symbols=['/ES', '/CL'],
                frequency=ChartFuturesFrequencies.OneMinute,
                period=ChartFuturesPeriods.OneDay
            )
        """

        # Handle datetimes.
        if isinstance(start_time, datetime):
            start_time = int(start_time.timestamp() * 1000)

        if isinstance(end_time, datetime):
            end_time = int(end_time.timestamp() * 1000)

        if isinstance(frequency, Enum):
            frequency = frequency.value

        if isinstance(period, Enum):
            period = period.value

        # define the valid inputs.
        valid_frequencies = ['m1', 'm5', 'm10', 'm30', 'h1', 'd1', 'w1', 'n1']
        valid_periods = ['d1', 'd5', 'w4', 'n10', 'y1', 'y10']

        # validate the frequency input.
        if frequency not in valid_frequencies:
            raise ValueError(
                "The FREQUENCY you have chosen is not correct please choose a valid option:['m1', 'm5', 'm10', 'm30', 'h1', 'd1', 'w1', 'n1']"
            )

        # validate the period input.
        if period not in valid_periods and start_time is None and end_time is None:
            raise ValueError(
                "The PERIOD you have chosen is not correct please choose a valid option:['d5', 'w4', 'n10', 'y1', 'y10']"
            )

        # Build the request
        request = self._new_request_template()
        request['service'] = 'CHART_HISTORY_FUTURES'
        request['command'] = 'GET'
        request['parameters']['symbol'] = ','.join(symbols)
        request['parameters']['frequency'] = frequency

        # handle the case where we get a start time or end time. DO FURTHER VALIDATION.
        if start_time is not None or end_time is not None:
            request['parameters']['END_TIME'] = end_time
            request['parameters']['START_TIME'] = start_time
        else:
            request['parameters']['period'] = period

        del request['parameters']['keys']
        del request['parameters']['fields']

        request['requestid'] = str(request['requestid'])
        self.streaming_api_client.data_requests['requests'].append(request)

    def level_two_quotes(self, symbols: List[str], fields: Union[Enum, List[str], List[int]]) -> None:
        """Stream Level Two Equity Quotes.

        ### Parameters
        ---
        symbols: List[str]
            A List of symbols you wish to stream quotes for.

        fields: Union[List[Enum], List[str], List[int]]
            The fields you want returned from the Endpoint, can either
            be the numeric representation or the key value representation.
            For more info on fields, refer to the documentation.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.level_two_quotes(
                symbols=['MSFT', 'PINS'],
                fields=LevelTwoQuotes.All
            )
        """

        if isinstance(fields, list):
            new_fields = []
            for field in fields:
                if isinstance(field, int):
                    field = str(int)
                elif isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

        if isinstance(fields, Enum):
            fields = fields.value

        # Build the request
        request = self._new_request_template()
        request['service'] = 'LISTED_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.streaming_api_client.data_requests['requests'].append(request)

    def level_two_options(self, symbols: List[str], fields: Union[Enum, List[str], List[int]]) -> None:
        """Stream Level Two Options Quotes.

        ### Parameters
        ---
        symbols: List[str]
            A List of symbols you wish to stream quotes for.

        fields: Union[List[Enum], List[str], List[int]]
            The fields you want returned from the Endpoint, can either
            be the numeric representation or the key value representation.
            For more info on fields, refer to the documentation.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
            >>> streaming_services.level_two_options(
                symbols=['MSFT_043021C120'],
                fields=LevelTwoOptions.All
            )
        """

        if isinstance(fields, list):
            new_fields = []
            for field in fields:
                if isinstance(field, int):
                    field = str(int)
                elif isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

        if isinstance(fields, Enum):
            fields = fields.value

        # Build the request
        request = self._new_request_template()
        request['service'] = 'OPTIONS_BOOK'
        request['command'] = 'SUBS'
        request['parameters']['keys'] = ','.join(symbols)
        request['parameters']['fields'] = ','.join(fields)

        self.streaming_api_client.data_requests['requests'].append(request)

    # def level_two_nasdaq(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:
    #     """
    #         EXPERIMENTAL: USE WITH CAUTION!

    #         Represents the LEVEL_TWO_QUOTES_NASDAQ endpoint for the streaming API. Documentation on this
    #         service does not exist, but it appears that we can pass through 1 of 3 fields.

    #         NAME: symbols
    #         DESC: A List of symbols you wish to stream time level two quotes for.
    #         TYPE: List<String>

    #         NAME: fields
    #         DESC: The fields you want returned from the Endpoint, can either be the numeric representation
    #               or the key value representation. For more info on fields, refer to the documentation.
    #         TYPE: List<Integer> | List<Strings>

    #     """
    #     # valdiate argument.
    #     fields = self._validate_argument(
    #         argument=fields,
    #         endpoint='level_two_nasdaq'
    #     )

    #     # Build the request
    #     request = self._new_request_template()
    #     request['service'] = 'NASDAQ_BOOK'
    #     request['command'] = 'SUBS'
    #     request['parameters']['keys'] = ','.join(symbols)
    #     request['parameters']['fields'] = ','.join(fields)

    #     self.streaming_api_client.data_requests['requests'].append(request)

    # def level_two_total_view(self, symbols: List[str], fields: Union[List[str], List[int]]) -> None:

    #     fields = [str(field) for field in fields]

    #     # Build the request
    #     request = self._new_request_template()
    #     request['service'] = 'TOTAL_VIEW'
    #     request['command'] = 'SUBS'
    #     request['parameters']['keys'] = ','.join(symbols)
    #     request['parameters']['fields'] = ','.join(fields)

    #     self.streaming_api_client.data_requests['requests'].append(request)

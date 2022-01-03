from td.session import TdAmeritradeSession
from td.credentials import TdCredentials
from td.rest.quotes import Quotes
from td.rest.movers import Movers
from td.rest.accounts import Accounts
from td.rest.market_hours import MarketHours
from td.rest.instruments import Instruments
from td.rest.user_info import UserInfo
from td.rest.price_history import PriceHistory
from td.rest.options_chain import OptionsChain
from td.rest.watchlists import Watchlists
from td.rest.orders import Orders
from td.rest.saved_orders import SavedOrders
from td.streaming.client import StreamingApiClient


class TdAmeritradeClient():

    """
    ### Overview
    ----
    Handles initializing all the different API Services and ensures
    that your session is authenticated.
    """

    def __init__(self, credentials: TdCredentials) -> None:
        """Initializes the `TdClient` object.

        ### Parameters
        credentials : TdCredentials
            Your TD Credentials stored in your credentials object
            so that you can authenitcate with TD.
        """

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
            >>> td_client = TdAmeritradeClient()
            >>> quotes_service = td_client.quotes()
        """

        return Quotes(session=self.td_session)

    def movers(self) -> Movers:
        """Used to access the `Movers` Services and metadata.

        ### Returns
        ---
        Movers:
            The `Movers` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> movers_service = td_client.movers()
        """

        return Movers(session=self.td_session)

    def accounts(self) -> Accounts:
        """Used to access the `Accounts` Services and metadata.

        ### Returns
        ---
        Accounts:
            The `Accounts` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> accounts_service = td_client.accounts()
        """

        return Accounts(session=self.td_session)

    def market_hours(self) -> MarketHours:
        """Used to access the `MarketHours` Services and metadata.

        ### Returns
        ---
        MarketHours:
            The `MarketHours` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> market_hours_service = td_client.market_hours()
        """

        return MarketHours(session=self.td_session)

    def instruments(self) -> Instruments:
        """Used to access the `Instruments` Services and metadata.

        ### Returns
        ---
        Instruments:
            The `Instruments` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> instruments_service = td_client.instruments()
        """

        return Instruments(session=self.td_session)

    def user_info(self) -> UserInfo:
        """Used to access the `UserInfo` Services and metadata.

        ### Returns
        ---
        UserInfo:
            The `UserInfo` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> user_info_service = td_client.user_info()
        """

        return UserInfo(session=self.td_session)

    def price_history(self) -> PriceHistory:
        """Used to access the `PriceHistory` Services and metadata.

        ### Returns
        ---
        PriceHistory:
            The `PriceHistory` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> price_history_service = td_client.price_history()
        """

        return PriceHistory(session=self.td_session)

    def options_chain(self) -> OptionsChain:
        """Used to access the `OptionsChain` Services and metadata.

        ### Returns
        ---
        OptionsChain:
            The `OptionsChain` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> options_chain_service = td_client.options_chain()
        """

        return OptionsChain(session=self.td_session)

    def watchlists(self) -> Watchlists:
        """Used to access the `Watchlists` Services and metadata.

        ### Returns
        ---
        Watchlists:
            The `Watchlists` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> watchlists_service = td_client.watchlists()
        """

        return Watchlists(session=self.td_session)

    def orders(self) -> Orders:
        """Used to access the `Orders` Services and metadata.

        ### Returns
        ---
        Orders:
            The `Orders` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> orders_service = td_client.orders()
        """

        return Orders(session=self.td_session)

    def saved_orders(self) -> SavedOrders:
        """Used to access the `SavedOrders` Services and metadata.

        ### Returns
        ---
        SavedOrders:
            The `SavedOrders` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> saved_orders_service = td_client.saved_orders()
        """

        return SavedOrders(session=self.td_session)

    def streaming_api_client(self) -> StreamingApiClient:
        """Used to access the `StreamingApiClient` Services and metadata.

        ### Returns
        ---
        StreamingApiClient:
            The `StreamingApiClient` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> streaming_api_service = td_client.streaming_api_client()
        """

        return StreamingApiClient(session=self.td_session)

from td.session import TdAmeritradeSession
from td.credentials import TdCredentials
from td.quotes import Quotes
from td.movers import Movers
from td.accounts import Accounts
from td.market_hours import MarketHours
from td.instruments import Instruments
from td.user_info import UserInfo
from td.price_history import PriceHistory
from td.options_chain import OptionsChain
from td.watchlists import Watchlists

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
            >>> td_client = TdAmeritradeClient()
            >>> quotes_service = td_client.quotes()
        """

        object: Quotes = Quotes(session=self.td_session)

        return object

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

        object: Movers = Movers(session=self.td_session)

        return object

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

        object: Accounts = Accounts(session=self.td_session)

        return object

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

        object: MarketHours = MarketHours(session=self.td_session)

        return object

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

        object: Instruments = Instruments(session=self.td_session)

        return object

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

        object: UserInfo = UserInfo(session=self.td_session)

        return object

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

        object: PriceHistory = PriceHistory(session=self.td_session)

        return object

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

        object: OptionsChain = OptionsChain(session=self.td_session)

        return object

    def watchlists(self) -> Watchlists:
        """Used to access the `Watchlists` Services and metadata.

        ### Returns
        ---
        Watchlists:
            The `Watchlists` services Object.

        ### Usage
        ----
            >>> td_client = TdAmeritradeClient()
            >>> watchlists_service = td_client.watchlists_service()
        """

        object: Watchlists = Watchlists(session=self.td_session)

        return object
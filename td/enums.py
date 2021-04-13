from enum import Enum


class Direction(Enum):
    """Represents the direction options for the
    `Movers` service.

    ### Usage:
    ----
        >>> from td.enums import Directions
        >>> Directions.Up.value
    """

    Up = 'up'
    Down = 'down'


class Change(Enum):
    """Represents the change options for the
    `Movers` service.

    ### Usage:
    ----
        >>> from td.enums import Change
        >>> Change.Percent.value
    """

    Percent = 'percent'
    Value = 'value'


class TransactionTypes(Enum):
    """Represents the types of transaction you
    can query from TD Ameritrade using the `Accounts`
    services.

    ### Usage:
    ----
        >>> from td.enums import TransactionTypes
        >>> TransactionTypes.Trade.value
    """

    All = 'ALL'
    Trade = 'TRADE'
    BuyOnly = 'BUY_ONLY'
    SellOnly = 'SELL_ONLY'
    CashInOrCashOut = 'CASH_IN_OR_CASH_OUT'
    Checking = 'CHECKING'
    Dividend = 'DIVIDEND'
    Interest = 'INTEREST'
    Other = 'OTHER'
    AdvisorFees = 'ADVISOR_FEES'


class Markets(Enum):
    """Represents the different markets you can request
    hours for the `MarketHours` service.

    ### Usage:
    ----
        >>> from td.enums import Markets
        >>> Markets.Bond.Value
    """

    Bond = 'BOND'
    Equity = 'EQUITY'
    Option = 'OPTION'
    Forex = 'FOREX'
    Futures = 'FUTURES'


class Projections(Enum):
    """Represents the different search types you can use for
    the `Instruments` service.

    ### Usage:
    ----
        >>> from td.enums import Projections
        >>> Projections.Bond.Value
    """

    SymbolSearch = 'symbol-search'
    SymbolRegex = 'symbol-regex'
    DescriptionSearch = 'desc-search'
    DescriptionRegex = 'desc-regex'
    Fundamental = 'fundamental'

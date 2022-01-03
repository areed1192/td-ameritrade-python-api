from enum import Enum


class Direction(Enum):
    """Represents the direction options for the
    `Movers` service.

    ### Usage
    ----
        >>> from td.enums import Directions
        >>> Directions.Up.value
    """

    Up = 'up'
    Down = 'down'


class Change(Enum):
    """Represents the change options for the
    `Movers` service.

    ### Usage
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

    ### Usage
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

    ### Usage
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

    ### Usage
    ----
        >>> from td.enums import Projections
        >>> Projections.Bond.Value
    """

    SymbolSearch = 'symbol-search'
    SymbolRegex = 'symbol-regex'
    DescriptionSearch = 'desc-search'
    DescriptionRegex = 'desc-regex'
    Fundamental = 'fundamental'


class DefaultOrderLegInstruction(Enum):
    """Represents the different Default Order Leg Instructions
    for the `UserInfo` service.

    ### Usage
    ----
        >>> from td.enums import DefaultOrderLegInstruction
        >>> DefaultOrderLegInstruction.Sell.Value
    """

    Buy = 'BUY'
    Sell = 'SELL'
    BuyToCover = 'BUY_TO_COVER'
    SellShort = 'SELL_SHORT'
    NoneSpecified = 'NONE'


class DefaultOrderType(Enum):
    """Represents the different Default Order Type
    for the `UserInfo` service.

    ### Usage
    ----
        >>> from td.enums import DefaultOrderType
        >>> DefaultOrderType.Market.Value
    """

    Market = 'MARKET'
    Limit = 'LIMIT'
    Stop = 'STOP'
    StopLimit = 'STOP_LIMIT'
    TrailingStop = 'TRAILING_STOP'
    MarketOnClose = 'MARKET_ON_CLOSE'
    NoneSpecified = 'NONE'


class DefaultOrderPriceLinkType(Enum):
    """Represents the different Default Order Price Link Type
    for the `UserInfo` service.

    ### Usage
    ----
        >>> from td.enums import DefaultOrderPriceLinkType
        >>> DefaultOrderPriceLinkType.Value.Value
    """

    Value = 'VALUE'
    Percent = 'PERCENT'
    NoneSpecified = 'NONE'


class DefaultOrderDuration(Enum):
    """Represents the different Default Order Duration
    for the `UserInfo` service.

    ### Usage
    ----
        >>> from td.enums import DefaultOrderDuration
        >>> DefaultOrderDuration.Day.Value
    """

    Day = 'DAY'
    GoodTillCancel = 'GOOD_TILL_CANCEL'
    FillOrKill = 'FILL_OR_KILL'
    NoneSpecified = 'NONE'


class DefaultOrderMarketSession(Enum):
    """Represents the different Default Order Market Session
    for the `UserInfo` service.

    ### Usage
    ----
        >>> from td.enums import DefaultOrderMarketSession
        >>> DefaultOrderMarketSession.Day.Value
    """

    Am = 'AM'
    Pm = 'PM'
    Normal = 'NORMAL'
    Seamless = 'SEAMLESS'
    NoneSpecified = 'NONE'


class TaxLotMethod(Enum):
    """Represents the different Tax Lot Methods
    for the `UserInfo` service.

    ### Usage
    ----
        >>> from td.enums import MutualFundTaxLotMethod
        >>> MutualFundTaxLotMethod.Day.Value
    """

    Fifo = 'FIFO'
    Lifo = 'LIFO'
    HighCost = 'HIGH_COST'
    LowCost = 'LOW_COST'
    MinimumTax = 'MINIMUM_TAX'
    AverageCost = 'AVERAGE_COST'
    NoneSpecified = 'NONE'


class DefaultAdvancedToolLaunch(Enum):
    """Represents the different Default Advanced Tool
    Lauch for the `UserInfo` service.

    ### Usage
    ----
        >>> from td.enums import DefaultAdvancedToolLaunch
        >>> DefaultAdvancedToolLaunch.Tos.Value
    """

    Ta = 'Ta'
    No = 'N'
    Yes = 'Y'
    Tos = 'TOS'
    Cc2 = 'CC2'
    NoneSpecified = 'NONE'


class AuthTokenTimeout(Enum):
    """Represents the different Auth Token Timeout
    properties for the `UserInfo` service.

    ### Usage
    ----
        >>> from td.enums import AuthTokenTimeout
        >>> AuthTokenTimeout.FiftyFiveMinutes.Value
    """

    FiftyFiveMinutes = 'FIFTY_FIVE_MINUTES'
    TwoHours = 'TWO_HOURS'
    FourHours = 'FOUR_HOURS'
    EightHours = 'EIGHT_HOURS'


class FrequencyType(Enum):
    """Represents the different chart frequencies
    for the `PriceHistory` service.

    ### Usage
    ----
        >>> from td.enums import PriceFrequency
        >>> PriceFrequency.Daily.Value
    """

    Minute = 'minute'
    Daily = 'daily'
    Weekly = 'weekly'
    Monthly = 'monthly'


class PeriodType(Enum):
    """Represents the different chart periods
    for the `PriceHistory` service.

    ### Usage
    ----
        >>> from td.enums import PriceFrequency
        >>> PeriodType.Daily.Value
    """

    Day = 'day'
    Month = 'month'
    Year = 'year'
    YearToDate = 'ytd'


class StrategyType(Enum):
    """Represents the different strategy types
    when querying the `OptionChain` service.

    ### Usage
    ----
        >>> from td.enums import StrategyType
        >>> StrategyType.Analytical.Value
    """

    Analytical = 'ANALYTICAL'
    Butterfly = 'BUTTERFLY'
    Calendar = 'CALENDAR'
    Collar = 'COLLAR'
    Condor = 'CONDOR'
    Covered = 'COVERED'
    Diagonal = 'DIAGONAL'
    Roll = 'ROLL'
    Single = 'SINGLE'
    Straddle = 'STRADDLE'
    Strangle = 'STRANGLE'
    Vertical = 'VERTICAL'


class OptionaRange(Enum):
    """Represents the different option range types
    when querying the `OptionChain` service.

    ### Usage
    ----
        >>> from td.enums import OptionaRange
        >>> OptionaRange.InTheMoney.Value
    """

    All = 'ALL'
    InTheMoney = 'ITM'
    NearTheMoney = 'NTM'
    OutTheMoney = 'OTM'
    StrikesAboveMarket = 'SAK'
    StrikesBelowMarket = 'SBK'
    StrikesNearMarket = 'SNK'


class ExpirationMonth(Enum):
    """Represents the different option expiration months
    when querying the `OptionChain` service.

    ### Usage
    ----
        >>> from td.enums import ExpirationMonth
        >>> ExpirationMonth.Janurary.Value
    """

    All = 'ALL'
    Janurary = 'JAN'
    Feburary = 'FEB'
    March = 'MAR'
    April = 'April'
    May = 'MAY'
    June = 'JUN'
    July = 'JUL'
    August = 'AUG'
    September = 'SEP'
    October = 'OCT'
    November = 'NOV'
    December = 'DEC'


class ContractType(Enum):
    """Represents the different option contract types
    when querying the `OptionChain` service.

    ### Usage
    ----
        >>> from td.enums import ContractType
        >>> ContractType.Call.Value
    """

    All = 'ALL'
    Call = 'CALL'
    Put = 'PUT'


class OptionType(Enum):
    """Represents the different option types
    when querying the `OptionChain` service.

    ### Usage
    ----
        >>> from td.enums import OptionType
        >>> OptionType.Call.Value
    """

    All = 'ALL'
    StandardContracts = 'S'
    NonStandardContracts = 'NS'


class OrderStatus(Enum):
    """Represents the different order status types
    when querying the `Orders` service.

    ### Usage
    ----
        >>> from td.enums import OrderStatus
        >>> OrderStatus.Working.Value
    """

    AwaitingParentOrder = 'AWAITING_PARENT_ORDER'
    AwaitingCondition = 'AWAITING_CONDITION'
    AwaitingManualReview = 'AWAITING_MANUAL_REVIEW'
    Accepted = 'ACCEPTED'
    AwaitingUrOut = 'AWAITING_UR_OUT'
    PendingActivation = 'PENDING_ACTIVATION'
    Queded = 'QUEUED'
    Working = 'WORKING'
    Rejected = 'REJECTED'
    PendingCancel = 'PENDING_CANCEL'
    Canceled = 'CANCELED'
    PendingReplace = 'PENDING_REPLACE'
    Replaced = 'REPLACED'
    Filled = 'FILLED'
    Expired = 'EXPIRED'


class OrderStrategyType(Enum):
    """Represents the different order strategy types
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import OrderStrategyType
        >>> OrderStrategyType.Single.Value
    """

    Single = 'SINGLE'
    Oco = 'OCO'
    Trigger = 'TRIGGER'


class QuantityType(Enum):
    """Represents the different order quantity types
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import QuantityType
        >>> QuantityType.Dollars.Value
    """

    AllShares = 'ALL_SHARES'
    Dollars = 'DOLLARS'
    Shares = 'SHARES'


class AssetType(Enum):
    """Represents the different order Asset types
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import AssetType
        >>> AssetType.Equity.Value
    """

    Equity = 'EQUITY'
    Option = 'OPTION'
    Index = 'INDEX'
    MutualFund = 'MUTUAL_FUND'
    CashEquivalent = 'CASH_EQUIVALENT'
    FixedIncome = 'FIXED_INCOME'
    Currency = 'CURRENCY'


class ComplexOrderStrategyType(Enum):
    """Represents the different order Asset types
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import ComplexOrderStrategyType
        >>> ComplexOrderStrategyType.IronCondor.Value
    """

    NoneProvided = 'NONE'
    Covered = 'COVERED'
    Vertical = 'VERTICAL'
    BackRatio = 'BACK_RATIO'
    Calendar = 'CALENDAR'
    Diagonal = 'DIAGONAL'
    Straddle = 'STRADDLE'
    Strangle = 'STRANGLE'
    CollarSynthetic = 'COLLAR_SYNTHETIC'
    Butterfly = 'BUTTERFLY'
    Condor = 'CONDOR'
    IronCondor = 'IRON_CONDOR'
    VerticalRoll = 'VERTICAL_ROLL'
    CollarWithStock = 'COLLAR_WITH_STOCK'
    DoubleDiagonal = 'DOUBLE_DIAGONAL'
    UnbalancedButterfly = 'UNBALANCED_BUTTERFLY'
    UnbalancedCondor = 'UNBALANCED_CONDOR'
    UnbalancedIronCondor = 'UNBALANCED_IRON_CONDOR'
    UnbalancedVerticalRoll = 'UNBALANCED_VERTICAL_ROLL'
    Custom = 'CUSTOM'


class OrderInstructions(Enum):
    """Represents the different order instructions
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import OrderInstructions
        >>> OrderInstructions.SellShort.Value
    """

    Buy = 'BUY'
    Sell = 'SELL'
    BuyToCover = 'BUY_TO_COVER'
    SellShort = 'SELL_SHORT'
    BuyToOpen = 'BUY_TO_OPEN'
    BuyToClose = 'BUY_TO_CLOSE'
    SellToOpen = 'SELL_TO_OPEN'
    SellToClose = 'SELL_TO_CLOSE'
    Exchange = 'EXCHANGE'


class RequestedDestination(Enum):
    """Represents the different order requested
    destinations when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import RequestedDestination
        >>> RequestedDestination.Cboe.Value
    """

    Inet = 'INET'
    EcnArca = 'ECN_ARCA'
    Cboe = 'CBOE'
    Amex = 'AMEX'
    Phlx = 'PHLX'
    Ise = 'ISE'
    Box = 'BOX'
    Nyse = 'NYSE'
    Nasdaq = 'NASDAQ'
    Bats = 'BATS'
    C2 = 'C2'
    Auto = 'AUTO'


class StopPriceLinkBasis(Enum):
    """Represents the different stop price link basis
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import StopPriceLinkBasis
        >>> StopPriceLinkBasis.Trigger.Value
    """

    Manual = 'MANUAL'
    Base = 'BASE'
    Trigger = 'TRIGGER'
    Last = 'LAST'
    Bid = 'BID'
    Ask = 'ASK'
    AskBid = 'ASK_BID'
    Mark = 'MARK'
    Average = 'AVERAGE'


class StopPriceLinkType(Enum):
    """Represents the different stop price link type
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import StopPriceLinkType
        >>> StopPriceLinkType.Trigger.Value
    """

    Value = 'VALUE'
    Percent = 'PERCENT'
    Tick = 'TICK'


class StopType(Enum):
    """Represents the different stop type
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import StopType
        >>> StopType.Standard.Value
    """

    Standard = 'STANDARD'
    Bid = 'BID'
    Ask = 'ASK'
    Last = 'LAST'
    Mark = 'MARK'


class PriceLinkBasis(Enum):
    """Represents the different price link basis
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import PriceLinkBasis
        >>> PriceLinkBasis.Manual.Value
    """

    Manual = 'MANUAL'
    Base = 'BASE'
    Trigger = 'TRIGGER'
    Last = 'LAST'
    Bid = 'BID'
    Ask = 'ASK'
    AskBid = 'ASK_BID'
    Mark = 'MARK'
    Average = 'AVERAGE'


class PriceLinkType(Enum):
    """Represents the different price link type
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import PriceLinkType
        >>> PriceLinkType.Trigger.Value
    """

    Value = 'VALUE'
    Percent = 'PERCENT'
    Tick = 'TICK'


class OrderType(Enum):
    """Represents the different order type
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import OrderType
        >>> OrderType.Market.Value
    """

    Market = 'MARKET'
    Limit = 'LIMIT'
    Stop = 'STOP'
    StopLimit = 'STOP_LIMIT'
    TrailingStop = 'TRAILING_STOP'
    MarketOnClose = 'MARKET_ON_CLOSE'
    Exercise = 'EXERCISE'
    TrailingStopLimit = 'TRAILING_STOP_LIMIT'
    NetDebit = 'NET_DEBIT'
    NetCredit = 'NET_CREDIT'
    NetZero = 'NET_ZERO'


class PositionEffect(Enum):
    """Represents the different position effects
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import PositionEffect
        >>> PositionEffect.Opening.Value
    """

    Opening = 'OPENING'
    Closing = 'CLOSING'
    Automatic = 'AUTOMATIC'


class OrderTaxLotMethod(Enum):
    """Represents the different order tax lot methods
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import OrderTaxLotMethod
        >>> OrderTaxLotMethod.Fifo.Value
    """

    Fifo = 'FIFO'
    Lifo = 'LIFO'
    HighCost = 'HIGH_COST'
    LowCost = 'LOW_COST'
    AverageCost = 'AVERAGE_COST'
    SpecificLot = 'SPECIFIC_LOT'


class SpecialInstructions(Enum):
    """Represents the different order special instructions
    when constructing and `Order` object.

    ### Usage
    ----
        >>> from td.enums import SpecialInstructions
        >>> SpecialInstructions.AllOrNone.Value
    """

    AllOrNone = 'ALL_OR_NONE'
    DoNotReduce = 'DO_NOT_REDUCE'
    AllOrNoneDoNotReduce = 'ALL_OR_NONE_DO_NOT_REDUCE'


class LevelOneQuotes(Enum):
    """Represents the different fields for the Level One
    Quotes Feed.

    ### Usage
    ----
        >>> from td.enums import LevelOneQuotes
        >>> LevelOneQuotes.All.Value
    """

    All = [str(item) for item in range(0, 53)]
    Symbol = 0
    BidPrice = 1
    AskPrice = 2
    LastPrice = 3
    BidSize = 4
    AskSize = 5
    AskId = 6
    BidId = 7
    TotalVolume = 8
    LastSize = 9
    TradeTime = 10
    QuoteTime = 11
    HighPrice = 12
    LowPrice = 13
    BidTick = 14
    ClosePrice = 15
    ExchangeId = 16
    Marginable = 17
    Shortable = 18
    IslandBid = 19
    IslandAsk = 20
    IslandVolume = 21
    QuoteDay = 22
    TradeDay = 23
    Volatility = 24
    Description = 25
    LastId = 26
    Digits = 27
    OpenPrice = 28
    NetChange = 29
    FiftyTwoWeekHigh = 30
    FiftyTwoWeekLow = 31
    PeRatio = 32
    DividendAmount = 33
    DividendYield = 34
    IslandBidSize = 35
    IslandAskSize = 36
    Nav = 37
    FundPrice = 38
    ExchangeName = 39
    DividendDate = 40
    RegularMarketQuote = 41
    RegularMarketTrade = 42
    RegularMarketLastPrice = 43
    RegularMarketLastSize = 44
    RegularMarketTradeTime = 45
    RegularMarketTradeDay = 46
    RegularMarketNetChange = 47
    SecurityStatus = 48
    Mark = 49
    QuoteTimeInLong = 50
    TradeTimeInLong = 51
    RegularMarketTradeTimeInLong = 52


class LevelOneOptions(Enum):
    """Represents the different fields for the Level One
    Options Feed.

    ### Usage
    ----
        >>> from td.enums import LevelOneOptions
        >>> LevelOneOptions.All.Value
    """

    All = [str(item) for item in range(0, 42)]
    Symbol = 0
    Description = 1
    BidPrice = 2
    AskPrice = 3
    LastPrice = 4
    HighPrice = 5
    LowPrice = 6
    ClosePrice = 7
    TotalVolume = 8
    OpenInterest = 9
    Volatility = 10
    QuoteTime = 11
    TradeTime = 12
    MoneyIntrinsicValue = 13
    QuoteDay = 14
    TradeDay = 15
    ExpirationYear = 16
    Multiplier = 17
    Digits = 18
    OpenPrice = 19
    BidSize = 20
    AskSize = 21
    LastSize = 22
    NetChange = 23
    StrikePrice = 24
    ContractType = 25
    Underlying = 26
    ExpirationMonth = 27
    Deliverables = 28
    TimeValue = 29
    ExpirationDay = 30
    DaysToExpiration = 31
    Delta = 32
    Gamma = 33
    Theta = 34
    Vega = 35
    Rho = 36
    SecurityStatus = 37
    TheoreticalOptionValue = 38
    UnderlyingPrice = 39
    UvExpirationType = 40
    Mark = 41


class LevelOneFutures(Enum):
    """Represents the different fields for the Level One
    Futures Feed.

    ### Usage
    ----
        >>> from td.enums import LevelOneFutures
        >>> LevelOneFutures.All.Value
    """

    All = [str(item) for item in range(0, 36)]
    Symbol = 0
    BidPrice = 1
    AskPrice = 2
    LastPrice = 3
    BidSize = 4
    AskSize = 5
    AskId = 6
    BidId = 7
    TotalVolume = 8
    LastSize = 9
    QuoteTime = 10
    TradeTime = 11
    HighPrice = 12
    LowPrice = 13
    ClosePrice = 14
    ExchangeId = 15
    Description = 16
    LastId = 17
    OpenPrice = 18
    NetChange = 19
    FuturePercentChange = 20
    ExhangeName = 21
    SecurityStatus = 22
    OpenInterest = 23
    Mark = 24
    Tick = 25
    TickAmount = 26
    Product = 27
    FuturePriceFormat = 28
    FutureTradingHours = 29
    FutureIsTradable = 30
    FutureMultiplier = 31
    FutureIsActive = 32
    FutureSettlementPrice = 33
    FutureActiveSymbol = 34
    FutureExpirationDate = 35


class LevelOneForex(Enum):
    """Represents the different fields for the Level One
    Forex Feed.

    ### Usage
    ----
        >>> from td.enums import LevelOneForex
        >>> LevelOneForex.All.Value
    """

    All = [str(item) for item in range(0, 30)]
    Symbol = 0
    BidPrice = 1
    AskPrice = 2
    LastPrice = 3
    BidSize = 4
    AskSize = 5
    TotalVolume = 6
    LastSize = 7
    QuoteTime = 8
    TradeTime = 9
    HighPrice = 10
    LowPrice = 11
    ClosePrice = 12
    ExchangeId = 13
    Description = 14
    OpenPrice = 15
    NetChange = 16
    PercentChange = 17
    ExchangeName = 18
    Digits = 19
    SecurityStatus = 20
    Tick = 21
    TickAmount = 22
    Product = 23
    TradingHours = 24
    IsTradable = 25
    MarketMaker = 26
    FiftyTwoWeekHigh = 27
    FiftyTwoWeekLow = 28
    Mark = 29


class NewsHeadlines(Enum):
    """Represents the different fields for the News
    Headline Feed.

    ### Usage
    ----
        >>> from td.enums import NewsHeadlines
        >>> NewsHeadlines.All.Value
    """

    All = [str(item) for item in range(0, 11)]
    Symbol = 0
    ErrorCode = 1
    StoryDatetime = 2
    HeadlineId = 3
    Status = 4
    Headline = 5
    StoryId = 6
    CountForKeyword = 7
    KeywordArray = 8
    IsHot = 9
    StorySource = 10


class LevelOneFuturesOptions(Enum):
    """Represents the different fields for the Level
    One Futures Options feed.

    ### Usage
    ----
        >>> from td.enums import LevelOneFuturesOptions
        >>> LevelOneFuturesOptions.All.Value
    """

    All = [str(item) for item in range(0, 36)]
    Symbol = 0
    BidPrice = 1
    AskPrice = 2
    LastPrice = 3
    BidSize = 4
    AskSize = 5
    AskId = 6
    BidId = 7
    TotalVolume = 8
    LastSize = 9
    QuoteTime = 10
    TradeTime = 11
    HighPrice = 12
    LowPrice = 13
    ClosePrice = 14
    ExchangeId = 15
    Description = 16
    LastId = 17
    OpenPrice = 18
    NetChange = 19
    FuturePercentChange = 20
    ExhangeName = 21
    SecurityStatus = 22
    OpenInterest = 23
    Mark = 24
    Tick = 25
    TickAmount = 26
    Product = 27
    FuturePriceFormat = 28
    FutureTradingHours = 29
    FutureIsTradable = 30
    FutureMultiplier = 31
    FutureIsActive = 32
    FutureSettlementPrice = 33
    FutureActiveSymbol = 34
    FutureExpirationDate = 35


class ChartServices(Enum):
    """Represents the different streaming chart
    services.

    ### Usage
    ----
        >>> from td.enums import ChartServices
        >>> ChartServices.ChartEquity.Value
    """

    ChartEquity = "CHART_EQUITY"
    _ChartFutures = "CHART_FUTURES"
    ChartOptions = "CHART_OPTIONS"


class ChartEquity(Enum):
    """Represents the different streaming chart
    equity fields.

    ### Usage
    ----
        >>> from td.enums import ChartEquity
        >>> ChartEquity.All.Value
    """

    All = [str(item) for item in range(0, 9)]
    Symbol = 0
    OpenPrice = 1
    HighPrice = 2
    LowPrice = 3
    Close_Price = 4
    Volume = 5
    Sequence = 6
    Chart_Time = 7
    Chart_Day = 8


class ChartFutures(Enum):
    """Represents the different streaming chart
    futures fields.

    ### Usage
    ----
        >>> from td.enums import ChartFutures
        >>> ChartFutures.All.Value
    """

    All = [str(item) for item in range(0, 7)]
    Symbol = 0
    ChartTime = 1
    OpenPrice = 2
    HighPrice = 3
    LowPrice = 4
    ClosePrice = 5
    Volume = 6


class TimesaleServices(Enum):
    """Represents the different streaming timesale
    services.

    ### Usage
    ----
        >>> from td.enums import TimesaleServices
        >>> TimesaleServices.TimesaleEquity.Value
    """

    TimesaleEquity = 'TIMESALE_EQUITY'
    TimesaleForex = 'TIMESALE_FOREX'
    TimesaleFutures = 'TIMESALE_FUTURES'
    TimesaleOptions = 'TIMESALE_OPTIONS'


class Timesale(Enum):
    """Represents the different streaming timesale
    fields.

    ### Usage
    ----
        >>> from td.enums import Timesale
        >>> Timesale.All.Value
    """

    All = [str(item) for item in range(0, 5)]
    Symbol = 0
    TradeTime = 1
    LastPrice = 2
    LastSize = 3
    LastSequence = 4


class ActivesServices(Enum):
    """Represents the different streaming actives
    services.

    ### Usage
    ----
        >>> from td.enums import ActivesServices
        >>> ActivesServices.ActivesNasdaq.Value
    """

    ActivesNasdaq = 'ACTIVES_NASDAQ'
    ActivesNyse = 'ACTIVES_NYSE'
    ActivesOptions = 'ACTIVES_OPTIONS'
    ActivesOtcbb = 'ACTIVES_OTCBB'


class ActivesVenues(Enum):
    """Represents the different streaming actives
    venues.

    ### Usage
    ----
        >>> from td.enums import ActivesVenues
        >>> ActivesVenues.Nasdaq.Value
    """

    NasdaqExchange = 'NASDAQ'
    NewYorkStockExchange = 'NYSE'
    OverTheCounterBulletinBoard = 'OTCBB'
    Calls = 'CALLS'
    Puts = 'PUTS'
    Options = 'OPTS'
    CallsDesc = 'CALLS-DESC'
    PutsDesc = 'PUTS-DESC'
    OptionsDec = 'OPTS-DESC'


class ActivesDurations(Enum):
    """Represents the different durations for the
    Actives Service.

    ### Usage
    ----
        >>> from td.enums import ActivesDurations
        >>> ActivesDurations.All.Value
    """

    All = 'ALL'
    SixtySeconds = '60'
    ThreeHundredSeconds = '300'
    SixHundredSeconds = '600'
    EighteenHundredSeconds = '1800'
    ThritySixHundredSeconds = '3600'


class ChartFuturesFrequencies(Enum):
    """Represents the different frequencies for the
    Chart History Futures streaming service.

    ### Usage
    ----
        >>> from td.enums import ChartFuturesFrequencies
        >>> ChartFuturesFrequencies.OneMinute.Value
    """

    OneMinute = 'm1'
    FiveMinute = 'm5'
    TenMinute = 'm10'
    ThirtyMinute = 'm30'
    OneHour = 'h1'
    OneDay = 'd1'
    OneWeek = 'w1'
    OneMonth = 'n1'


class ChartFuturesPeriods(Enum):
    """Represents the different periods for the
    Chart History Futures streaming service.

    ### Usage
    ----
        >>> from td.enums import ChartFuturesPeriods
        >>> ChartFuturesPeriods.OneDay.Value
    """

    OneDay = 'd1'
    FiveDay = 'd5'
    FourWeeks = 'w4'
    TenMonths = 'n10'
    OneYear = 'y1'
    TenYear = 'y10'


class LevelTwoQuotes(Enum):
    """Represents the Level Two Quotes Fields.

    ### Usage
    ----
        >>> from td.enums import LevelTwoQuotes
        >>> LevelTwoQuotes.All.Value
    """

    All = [str(item) for item in range(0, 3)]
    Key = 0
    Time = 1
    Data = 2


class LevelTwoOptions(Enum):
    """Represents the Level Two Options Fields.

    ### Usage
    ----
        >>> from td.enums import LevelTwoOptions
        >>> LevelTwoOptions.All.Value
    """

    All = [str(item) for item in range(0, 3)]
    Key = 0
    Time = 1
    Data = 2

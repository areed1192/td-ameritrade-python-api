from enum import Enum


'''
    ORDERS ENUMS
'''


class ORDER_SESSION(Enum):

    NORMAL = 'NORMAL'
    AM = 'AM'
    PM = 'PM'
    SEAMLESS = 'SEAMLESS'


class DURATION(Enum):

    DAY = 'DAY'
    GOOD_TILL_CANCEL = 'GOOD_TILL_CANCEL'
    FILL_OR_KILL = 'FILL_OR_KILL'


class ORDER_STRATEGY_TYPE(Enum):

    SINGLE = 'SINGLE'
    OCO = 'OCO'
    TRIGGER = 'TRIGGER'


class QUANTITY_TYPE(Enum):

    ALL_SHARES = 'ALL_SHARES'
    DOLLARS = 'DOLLARS'
    SHARES = 'SHARES'


class ORDER_ASSET_TYPE(Enum):

    EQUITY = 'EQUITY'
    OPTION = 'OPTION'
    INDEX = 'INDEX'
    MUTUAL_FUND = 'MUTUAL_FUND'
    CASH_EQUIVALENT = 'CASH_EQUIVALENT'
    FIXED_INCOME = 'FIXED_INCOME'
    CURRENCY = 'CURRENCY'


class COMPLEX_ORDER_STRATEGY_TYPE(Enum):

    NONE = 'NONE'
    COVERED = 'COVERED'
    VERTICAL = 'VERTICAL'
    BACK_RATIO = 'BACK_RATIO'
    CALENDAR = 'CALENDAR'
    DIAGONAL = 'DIAGONAL'
    STRADDLE = 'STRADDLE'
    STRANGLE = 'STRANGLE'
    COLLAR_SYNTHETIC = 'COLLAR_SYNTHETIC'
    BUTTERFLY = 'BUTTERFLY'
    CONDOR = 'CONDOR'
    IRON_CONDOR = 'IRON_CONDOR'
    VERTICAL_ROLL = 'VERTICAL_ROLL'
    COLLAR_WITH_STOCK = 'COLLAR_WITH_STOCK'
    DOUBLE_DIAGONAL = 'DOUBLE_DIAGONAL'
    UNBALANCED_BUTTERFLY = 'UNBALANCED_BUTTERFLY'
    UNBALANCED_CONDOR = 'UNBALANCED_CONDOR'
    UNBALANCED_IRON_CONDOR = 'UNBALANCED_IRON_CONDOR'
    UNBALANCED_VERTICAL_ROLL = 'UNBALANCED_VERTICAL_ROLL'
    CUSTOM = 'CUSTOM'


class ORDER_INSTRUCTIONS(Enum):

    BUY = 'BUY'
    SELL = 'SELL'
    BUY_TO_COVER = 'BUY_TO_COVER'
    SELL_SHORT = 'SELL_SHORT'
    BUY_TO_OPEN = 'BUY_TO_OPEN'
    BUY_TO_CLOSE = 'BUY_TO_CLOSE'
    SELL_TO_OPEN = 'SELL_TO_OPEN'
    SELL_TO_CLOSE = 'SELL_TO_CLOSE'
    EXCHANGE = 'EXCHANGE'


class REQUESTED_DESTINATION(Enum):

    INET = 'INET'
    ECN_ARCA = 'ECN_ARCA'
    CBOE = 'CBOE'
    AMEX = 'AMEX'
    PHLX = 'PHLX'
    ISE = 'ISE'
    BOX = 'BOX'
    NYSE = 'NYSE'
    NASDAQ = 'NASDAQ'
    BATS = 'BATS'
    C2 = 'C2'
    AUTO = 'AUTO'


class STOP_PRICE_LINK_BASIS(Enum):

    MANUAL = 'MANUAL'
    BASE = 'BASE'
    TRIGGER = 'TRIGGER'
    LAST = 'LAST'
    BID = 'BID'
    ASK = 'ASK'
    ASK_BID = 'ASK_BID'
    MARK = 'MARK'
    AVERAGE = 'AVERAGE'


class STOP_PRICE_LINK_TYPE(Enum):

    VALUE = 'VALUE'
    PERCENT = 'PERCENT'
    TICK = 'TICK'


class STOP_TYPE(Enum):

    STANDARD = 'STANDARD'
    BID = 'BID'
    ASK = 'ASK'
    LAST = 'LAST'
    MARK = 'MARK'


class PRICE_LINK_BASIS(Enum):

    MANUAL = 'MANUAL'
    BASE = 'BASE'
    TRIGGER = 'TRIGGER'
    LAST = 'LAST'
    BID = 'BID'
    ASK = 'ASK'
    ASK_BID = 'ASK_BID'
    MARK = 'MARK'
    AVERAGE = 'AVERAGE'


class PRICE_LINK_TYPE(Enum):

    VALUE = 'VALUE'
    PERCENT = 'PERCENT'
    TICK = 'TICK'


class ORDER_TYPE(Enum):

    MARKET = 'MARKET'
    LIMIT = 'LIMIT'
    STOP = 'STOP'
    STOP_LIMIT = 'STOP_LIMIT'
    TRAILING_STOP = 'TRAILING_STOP'
    MARKET_ON_CLOSE = 'MARKET_ON_CLOSE'
    EXERCISE = 'EXERCISE'
    TRAILING_STOP_LIMIT = 'TRAILING_STOP_LIMIT'
    NET_DEBIT = 'NET_DEBIT'
    NET_CREDIT = 'NET_CREDIT'
    NET_ZERO = 'NET_ZERO'


class POSITION_EFFECT(Enum):

    OPENING = 'OPENING'
    CLOSING = 'CLOSING'
    AUTOMATIC = 'AUTOMATIC'


class TAX_LOT_METHOD(Enum):

    FIFO = 'FIFO'
    LIFO = 'LIFO'
    HIGH_COST = 'HIGH_COST'
    LOW_COST = 'LOW_COST'
    AVERAGE_COST = 'AVERAGE_COST'
    SPECIFIC_LOT = 'SPECIFIC_LOT'


class SPECIAL_INSTRUCTIONS(Enum):

    ALL_OR_NONE = 'ALL_OR_NONE'
    DO_NOT_REDUCE = 'DO_NOT_REDUCE'
    ALL_OR_NONE_DO_NOT_REDUCE = 'ALL_OR_NONE_DO_NOT_REDUCE'


class STATUS(Enum):

    AWAITING_PARENT_ORDER = 'AWAITING_PARENT_ORDER'
    AWAITING_CONDITION = 'AWAITING_CONDITION'
    AWAITING_MANUAL_REVIEW = 'AWAITING_MANUAL_REVIEW'
    ACCEPTED = 'ACCEPTED'
    AWAITING_UR_OUT = 'AWAITING_UR_OUT'
    PENDING_ACTIVATION = 'PENDING_ACTIVATION'
    QUEUED = 'QUEUED'
    WORKING = 'WORKING'
    REJECTED = 'REJECTED'
    PENDING_CANCEL = 'PENDING_CANCEL'
    CANCELED = 'CANCELED'
    PENDING_REPLACE = 'PENDING_REPLACE'
    REPLACED = 'REPLACED'
    FILLED = 'FILLED'
    EXPIRED = 'EXPIRED'


class MUTUAL_FUND_TYPES(Enum):

    NOT_APPLICABLE = 'NOT_APPLICABLE'
    OPEN_END_NON_TAXABLE = 'OPEN_END_NON_TAXABLE'
    OPEN_END_TAXABLE = 'OPEN_END_TAXABLE'
    NO_LOAD_NON_TAXABLE = 'NO_LOAD_NON_TAXABLE'
    NO_LOAD_TAXABLE = 'NO_LOAD_TAXABLE'


class CASH_EQUIVALENT_TYPE(Enum):

    SAVINGS = 'SAVINGS'
    MONEY_MARKET_FUND = 'MONEY_MARKET_FUND'


class OPTION_TYPE(Enum):

    VANILLA = 'VANILLA'
    BINARY = 'BINARY'
    BARRIER = 'BARRIER'


class PUT_CALL(Enum):

    PUT = 'PUT'
    CALL = 'CALL'


class CURRENCY_TYPE(Enum):

    USD = 'USD'
    CAD = 'CAD'
    EUR = 'EUR'
    JPY = 'JPY'


'''
    OPTION CHAIN ENUMS
'''


class OPTION_CHAIN_STRATEGY(Enum):

    SINGLE = 'SINGLE'
    ANALYTICAL = 'ANALYTICAL'
    COVERED = 'COVERED'
    VERTICAL = 'VERTICAL'
    CALENDAR = 'CALENDAR'
    STRANGLE = 'STRANGLE'
    STRADDLE = 'STRADDLE'
    BUTTERFLY = 'BUTTERFLY'
    CONDOR = 'CONDOR'
    DIAGONAL = 'DIAGONAL'
    COLLAR = 'COLLAR'
    ROLL = 'ROLL'


class OPTION_CHAIN_RANGE(Enum):

    ITM = 'ITM'
    NTM = 'NTM'
    OTM = 'OTM'
    SAK = 'SAK'
    SBK = 'SBK'
    SNK = 'SNK'
    ALL = 'ALL'


class OPTION_CHAIN_EXP_MONTH(Enum):

    ALL = 'ALL'
    JAN = 'JAN'
    FEB = 'FEB'
    MAR = 'MAR'
    APR = 'APR'
    MAY = 'MAY'
    JUN = 'JUN'
    JUL = 'JUL'
    AUG = 'AUG'
    SEP = 'SEP'
    OCT = 'OCT'
    DEC = 'DEC'


class OPTION_CHAIN_OPTION_TYPE(Enum):

    S = 'S'
    NS = 'NS'
    ALL = 'ALL'


class STREAM_ACTIVES(Enum):
    pass


ENDPOINT_ARGUMENTS = {
    'search_instruments': {
        'projection': ['symbol-search', 'symbol-regex', 'desc-search', 'desc-regex', 'fundamental']
    },
    'get_market_hours': {
        'markets': ['EQUITY', 'OPTION', 'FUTURE', 'BOND', 'FOREX']
    },
    'get_movers': {
        'market': ['$DJI', '$COMPX', '$SPX.X'],
        'direction': ['up', 'down'],
        'change': ['value', 'percent']
    },
    'get_user_principals': {
        'fields': ['streamerSubscriptionKeys', 'streamerConnectionInfo', 'preferences', 'surrogateIds']
    }
}

VALID_CHART_VALUES = {
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

STREAM_FIELD_IDS = {
    "account_activity": {
        "0": "subscription-key",
        "1": "account-id",
        "2": "message-type",
        "3": "message-data"
    },
    "level_one_forex": {
        "0": "symbol",
        "1": "bid-price",
        "2": "ask-price",
        "3": "last-price",
        "4": "bid-size",
        "5": "ask-size",
        "6": "total-volume",
        "7": "last-size",
        "8": "quote-time",
        "9": "trade-time",
        "10": "high-price",
        "11": "low-price",
        "12": "close-price",
        "13": "exchange-id",
        "14": "description",
        "15": "open-price",
        "16": "net-change",
        "17": "percent-change",
        "18": "exchange-name",
        "19": "digits",
        "20": "security-status",
        "21": "tick",
        "22": "tick-amount",
        "23": "product",
        "24": "trading-hours",
        "25": "is-tradable",
        "26": "market-maker",
        "27": "52-week-high",
        "28": "52-week-low",
        "29": "mark"
    },
    "level_one_futures": {
        "0": "symbol",
        "1": "bid-price",
        "2": "ask-price",
        "3": "last-price",
        "4": "bid-size",
        "5": "ask-size",
        "6": "ask-id",
        "7": "bid-id",
        "8": "total-volume",
        "9": "last-size",
        "10": "quote-time",
        "11": "trade-time",
        "12": "high-price",
        "13": "low-price",
        "14": "close-price",
        "15": "exchange-id",
        "16": "description",
        "17": "last-id",
        "18": "open-price",
        "19": "net-change",
        "20": "future-percent-change",
        "21": "exhange-name",
        "22": "security-status",
        "23": "open-interest",
        "24": "mark",
        "25": "tick",
        "26": "tick-amount",
        "27": "product",
        "28": "future-price-format",
        "29": "future-trading-hours",
        "30": "future-is-tradable",
        "31": "future-multiplier",
        "32": "future-is-active",
        "33": "future-settlement-price",
        "34": "future-active-symbol",
        "35": "future-expiration-date"
    },
    "level_one_futures_options": {
        "0": "symbol",
        "1": "bid-price",
        "2": "ask-price",
        "3": "last-price",
        "4": "bid-size",
        "5": "ask-size",
        "6": "ask-id",
        "7": "bid-id",
        "8": "total-volume",
        "9": "last-size",
        "10": "quote-time",
        "11": "trade-time",
        "12": "high-price",
        "13": "low-price",
        "14": "close-price",
        "15": "exchange-id",
        "16": "description",
        "17": "last-id",
        "18": "open-price",
        "19": "net-change",
        "20": "future-percent-change",
        "21": "exhange-name",
        "22": "security-status",
        "23": "open-interest",
        "24": "mark",
        "25": "tick",
        "26": "tick-amount",
        "27": "product",
        "28": "future-price-format",
        "29": "future-trading-hours",
        "30": "future-is-tradable",
        "31": "future-multiplier",
        "32": "future-is-active",
        "33": "future-settlement-price",
        "34": "future-active-symbol",
        "35": "future-expiration-date"
    },
    "level_one_option": {
        "0": "symbol",
        "1": "description",
        "2": "bid-price",
        "3": "ask-price",
        "4": "last-price",
        "5": "high-price",
        "6": "low-price",
        "7": "close-price",
        "8": "total-volume",
        "9": "open-interest",
        "10": "volatility",
        "11": "quote-time",
        "12": "trade-time",
        "13": "money-intrinsic-value",
        "14": "quote-day",
        "15": "trade-day",
        "16": "expiration-year",
        "17": "multiplier",
        "18": "digits",
        "19": "open-price",
        "20": "bid-size",
        "21": "ask-size",
        "22": "last-size",
        "23": "net-change",
        "24": "strike-price",
        "25": "contract-type",
        "26": "underlying",
        "27": "expiration-month",
        "28": "deliverables",
        "29": "time-value",
        "30": "expiration-day",
        "31": "days-to-expiration",
        "32": "delta",
        "33": "gamma",
        "34": "theta",
        "35": "vega",
        "36": "rho",
        "37": "security-status",
        "38": "theoretical-option-value",
        "39": "underlying-price",
        "40": "uv-expiration-type",
        "41": "mark"
    },
    "level_one_quote": {
        "0": "symbol",
        "1": "bid-price",
        "2": "ask-price",
        "3": "last-price",
        "4": "bid-size",
        "5": "ask-size",
        "6": "ask-id",
        "7": "bid-id",
        "8": "total-volume",
        "9": "last-size",
        "10": "trade-time",
        "11": "quote-time",
        "12": "high-price",
        "13": "low-price",
        "14": "bid-tick",
        "15": "close-price",
        "16": "exchange-id",
        "17": "marginable",
        "18": "shortable",
        "19": "island-bid",
        "20": "island-ask",
        "21": "island-volume",
        "22": "quote-day",
        "23": "trade-day",
        "24": "volatility",
        "25": "description",
        "26": "last-id",
        "27": "digits",
        "28": "open-price",
        "29": "net-change",
        "30": "52-week-high",
        "31": "52-week-low",
        "32": "pe-ratio",
        "33": "dividend-amount",
        "34": "dividend-yield",
        "35": "island-bid-size",
        "36": "island-ask-size",
        "37": "nav",
        "38": "fund-price",
        "39": "exchange-name",
        "40": "dividend-date",
        "41": "regular-market-quote",
        "42": "regular-market-trade",
        "43": "regular-market-last-price",
        "44": "regular-market-last-size",
        "45": "regular-market-trade-time",
        "46": "regular-market-trade-day",
        "47": "regular-market-net-change",
        "48": "security-status",
        "49": "mark",
        "50": "quote-time-in-long",
        "51": "trade-time-in-long",
        "52": "regular-market-trade-time-in-long"
    },
    "news_headline": {
        "0": "symbol",
        "1": "error-code",
        "2": "story-datetime",
        "3": "headline-id",
        "4": "status",
        "5": "headline",
        "6": "story-id",
        "7": "count-for-keyword",
        "8": "keyword-array",
        "9": "is-hot",
        "10": "story-source"
    },
    "qos_request": {
        "0": "express",
        "1": "real-time",
        "2": "fast",
        "3": "moderate",
        "4": "slow",
        "5": "delayed"
    },
    "timesale": {
        "0": "symbol",
        "1": "trade-time",
        "2": "last-price",
        "3": "last-size",
        "4": "last-sequence"
    },
    "chart_equity": {
        "seq": "chart-sequence",
        "key": "symbol",
        "1": "open-price",
        "2": "high-price",
        "3": "low-price",
        "4": "close_price",
        "5": "volume",
        "6": "sequence",
        "7": "chart_time",
        "8": "chart_day"
    },
    "chart_options": {
        "seq": "chart-sequence",
        "key": "key",
        "1": "open-price",
        "2": "high-price",
        "3": "low-price",
        "4": "close_price",
        "5": "volume",
        "6": "sequence",
        "7": "chart_time",
        "8": "chart_day"
    },
    "chart_futures": {
        "seq": "chart-sequence",
        "key": "key",
        "1": "open-price",
        "2": "high-price",
        "3": "low-price",
        "4": "close_price",
        "5": "volume",
        "6": "sequence",
        "7": "chart_time",
        "8": "chart_day"
    },
    "level_two_quotes": {
        "0": "key",
        "1": "time",
        "2": "data"
    },
    "level_two_nyse": {
        "0": "key",
        "1": "time",
        "2": "data"
    },
    "level_two_options": {
        "0": "key",
        "1": "time",
        "2": "data"
    },
    "level_two_forex": {
        "0": "key",
        "1": "time",
        "2": "data"
    },
    "level_two_nasdaq": {
        "0": "key",
        "1": "time",
        "2": "data"
    },
    "level_two_futures": {
        "0": "key",
        "1": "time",
        "2": "data"
    }
}


CSV_FIELD_KEYS = {
    "ACTIVES_NASDAQ": {
        "key": "key",
        "1": "data"
    },
    "ACTIVES_OTCBB": {
        "key": "key",
        "1": "data"
    },
    "ACTIVES_NYSE": {
        "key": "key",
        "1": "data"
    },
    "ACTIVES_OPTIONS": {
        "key": "key",
        "1": "data"
    },
    "CHART_EQUITY": {
        "seq": "chart-sequence",
        "key": "symbol",
        "1": "chart-time",
        "2": "open-price",
        "3": "high-price",
        "4": "low-price",
        "5": "close-price",
        "6": "volume",
        "7": "chart-time",
        "8": "chart-day"
    },
    "CHART_FUTURES": {
        "seq": "chart-sequence",
        "key": "symbol",
        "1": "chart-time",
        "2": "open-price",
        "3": "high-price",
        "4": "low-price",
        "5": "close-price",
        "6": "volume"
    },
    "CHART_OPTIONS": {
        "seq": "chart-sequence",
        "key": "symbol",
        "1": "chart-time",
        "2": "open-price",
        "3": "high-price",
        "4": "low-price",
        "5": "close-price",
        "6": "volume"
    },
    "CHART_HISTORY": {
        "seq": "chart-sequence",
        "key": "symbol",
        "1": "chart-time",
        "2": "open-price",
        "3": "high-price",
        "4": "low-price",
        "5": "close-price",
        "6": "volume",
        "7": "chart-time",
        "8": "chart-day"
    },
    "CHART_HISTORY_FUTURES": {
        "seq": "chart-sequence",
        "key": "symbol",
        "0": "key",
        "1": "chart-time",
        "2": "open-price",
        "3": "high-price",
        "4": "low-price",
        "5": "close-price",
        "6": "volume",
        "7": "chart-time",
        "8": "chart-day"
    },
    "LEVELONE_FOREX": {
        "1": "bid-price",
        "10": "high-price",
        "11": "low-price",
        "12": "close-price",
        "13": "exchange-id",
        "14": "description",
        "15": "open-price",
        "16": "net-change",
        "17": "percent-change",
        "18": "exchange-name",
        "19": "digits",
        "2": "ask-price",
        "20": "security-status",
        "21": "tick",
        "22": "tick-amount",
        "23": "product",
        "24": "trading-hours",
        "25": "is-tradable",
        "26": "market-maker",
        "27": "52-week-high",
        "28": "52-week-low",
        "29": "mark",
        "3": "last-price",
        "4": "bid-size",
        "5": "ask-size",
        "6": "total-volume",
        "7": "last-size",
        "8": "quote-time",
        "9": "trade-time",
        "assetMainType": "asset-main-type",
        "assetSubType": "asset-sub-type",
        "cusip": "cusip",
        "delayed": "delayed",
        "key": "symbol",
    },
    "LEVELONE_FUTURES": {
        "1": "bid-price",
        "10": "quote-time",
        "11": "trade-time",
        "12": "high-price",
        "13": "low-price",
        "14": "close-price",
        "15": "exchange-id",
        "16": "description",
        "17": "last-id",
        "18": "open-price",
        "19": "net-change",
        "2": "ask-price",
        "20": "future-percent-change",
        "21": "exhange-name",
        "22": "security-status",
        "23": "open-interest",
        "24": "mark",
        "25": "tick",
        "26": "tick-amount",
        "27": "product",
        "28": "future-price-format",
        "29": "future-trading-hours",
        "3": "last-price",
        "30": "future-is-tradable",
        "31": "future-multiplier",
        "32": "future-is-active",
        "33": "future-settlement-price",
        "34": "future-active-symbol",
        "35": "future-expiration-date",
        "4": "bid-size",
        "5": "ask-size",
        "6": "ask-id",
        "7": "bid-id",
        "8": "total-volume",
        "9": "last-size",
        "assetMainType": "asset-main-type",
        "assetSubType": "asset-sub-type",
        "cusip": "cusip",
        "delayed": "delayed",
        "key": "symbol",
    },
    "LEVELONE_FUTURES_OPTIONS": {
        "1": "bid-price",
        "10": "quote-time",
        "11": "trade-time",
        "12": "high-price",
        "13": "low-price",
        "14": "close-price",
        "15": "exchange-id",
        "16": "description",
        "17": "last-id",
        "18": "open-price",
        "19": "net-change",
        "2": "ask-price",
        "20": "future-percent-change",
        "21": "exhange-name",
        "22": "security-status",
        "23": "open-interest",
        "24": "mark",
        "25": "tick",
        "26": "tick-amount",
        "27": "product",
        "28": "future-price-format",
        "29": "future-trading-hours",
        "3": "last-price",
        "30": "future-is-tradable",
        "31": "future-multiplier",
        "32": "future-is-active",
        "33": "future-settlement-price",
        "34": "future-active-symbol",
        "35": "future-expiration-date",
        "4": "bid-size",
        "5": "ask-size",
        "6": "ask-id",
        "7": "bid-id",
        "8": "total-volume",
        "9": "last-size",
        "assetMainType": "asset-main-type",
        "assetSubType": "asset-sub-type",
        "cusip": "cusip",
        "delayed": "delayed",
        "key": "symbol",
    },
    "OPTION": {
        "1": "description",
        "10": "volatility",
        "11": "quote-time",
        "12": "trade-time",
        "13": "money-intrinsic-value",
        "14": "quote-day",
        "15": "trade-day",
        "16": "expiration-year",
        "17": "multiplier",
        "18": "digits",
        "19": "open-price",
        "2": "bid-price",
        "20": "bid-size",
        "21": "ask-size",
        "22": "last-size",
        "23": "net-change",
        "24": "strike-price",
        "25": "contract-type",
        "26": "underlying",
        "27": "expiration-month",
        "28": "deliverables",
        "29": "time-value",
        "3": "ask-price",
        "30": "expiration-day",
        "31": "days-to-expiration",
        "32": "delta",
        "33": "gamma",
        "34": "theta",
        "35": "vega",
        "36": "rho",
        "37": "security-status",
        "38": "theoretical-option-value",
        "39": "underlying-price",
        "4": "last-price",
        "40": "uv-expiration-type",
        "41": "mark",
        "5": "high-price",
        "6": "low-price",
        "7": "close-price",
        "8": "total-volume",
        "9": "open-interest",
        "assetMainType": "asset-main-type",
        "assetSubType": "asset-sub-type",
        "cusip": "cusip",
        "delayed": "delayed",
        "key": "symbol",
    },
    "QUOTE": {
        "10": "trade-time",
        "11": "quote-time",
        "12": "high-price",
        "13": "low-price",
        "14": "bid-tick",
        "15": "close-price",
        "16": "exchange-id",
        "17": "marginable",
        "18": "shortable",
        "1": "bid-price",
        "19": "island-bid",
        "20": "island-ask",
        "21": "island-volume",
        "22": "quote-day",
        "23": "trade-day",
        "24": "volatility",
        "25": "description",
        "26": "last-id",
        "27": "digits",
        "28": "open-price",
        "2": "ask-price",
        "29": "net-change",
        "30": "52-week-high",
        "31": "52-week-low",
        "32": "pe-ratio",
        "33": "dividend-amount",
        "34": "dividend-yield",
        "35": "island-bid-size",
        "36": "island-ask-size",
        "37": "nav",
        "38": "fund-price",
        "3": "last-price",
        "39": "exchange-name",
        "40": "dividend-date",
        "41": "regular-market-quote",
        "42": "regular-market-trade",
        "43": "regular-market-last-price",
        "44": "regular-market-last-size",
        "45": "regular-market-trade-time",
        "46": "regular-market-trade-day",
        "47": "regular-market-net-change",
        "48": "security-status",
        "4": "bid-size",
        "49": "mark",
        "50": "quote-time-in-long",
        "51": "trade-time-in-long",
        "5": "ask-size",
        "6": "ask-id",
        "7": "bid-id",
        "8": "total-volume",
        "9": "last-size",
        "assetMainType": "asset-main-type",
        "assetSubType": "asset-sub-type",
        "cusip": "cusip",
        "delayed": "delayed",
        "key": "symbol"
    },
    "NEWS_HEADLINE": {
        "1": "error-code",
        "10": "story-source",
        "2": "story-datetime",
        "3": "headline-id",
        "4": "status",
        "5": "headline",
        "6": "story-id",
        "7": "count-for-keyword",
        "8": "keyword-array",
        "9": "is-hot",
        "key": "symbol",
        "seq": "sequence"
    },
    "TIMESALE_EQUITY": {
        "1": "trade-time",
        "2": "last-price",
        "3": "last-size",
        "4": "last-sequence",
        "key": "symbol",
        "seq": "sequence"
    },
    "TIMESALE_FUTURES": {
        "1": "trade-time",
        "2": "last-price",
        "3": "last-size",
        "4": "last-sequence",
        "key": "symbol",
        "seq": "sequence"
    },
    "TIMESALE_FOREX": {
        "1": "trade-time",
        "2": "last-price",
        "3": "last-size",
        "4": "last-sequence",
        "key": "symbol",
        "seq": "sequence"
    },
    "TIMESALE_OPTIONS": {
        "1": "trade-time",
        "2": "last-price",
        "3": "last-size",
        "4": "last-sequence",
        "key": "symbol",
        "seq": "sequence"
    },
}

CSV_FIELD_KEYS_LEVEL_2 = {
    "NASDAQ_BOOK": "nested",
    "OPTIONS_BOOK": "nested",
    "LISTED_BOOK": "nested",
    "FUTURES_BOOK": "nested"
}

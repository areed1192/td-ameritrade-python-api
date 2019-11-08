import json

class SavedOrder():

    def __init__(self, **kwargs):

        '''
            Initalizes the SavedOrder Object and override any default values that are
            passed through.
        '''

        self.saved_order_arguments = {
            'session':['NORMAL', 'AM', 'PM', 'SEAMLESS'],
            'duration':['DAY', 'GOOD_TILL_CANCEL', 'FILL_OR_KILL'],
            'orderType':['MARKET', 'LIMIT', 'STOP', 'STOP_LIMIT', 'TRAILING_STOP', 'MARKET_ON_CLOSE', 
                         'EXERCISE', 'TRAILING_STOP_LIMIT', 'NET_DEBIT', 'NET_CREDIT', 'NET_ZERO'],
            'complexOrderStrategyType': ['NONE', 'COVERED', 'VERTICAL', 'BACK_RATIO', 'CALENDAR', 'DIAGONAL', 'STRADDLE', 
                                        'STRANGLE', 'COLLAR_SYNTHETIC', 'BUTTERFLY', 'CONDOR', 'IRON_CONDOR', 'VERTICAL_ROLL', 
                                        'COLLAR_WITH_STOCK', 'DOUBLE_DIAGONAL', 'UNBALANCED_BUTTERFLY', 'UNBALANCED_CONDOR', 
                                        'UNBALANCED_IRON_CONDOR', 'UNBALANCED_VERTICAL_ROLL', 'CUSTOM'],
            'requestedDestination':['INET', 'ECN_ARCA', 'CBOE', 'AMEX', 'PHLX', 'ISE', 'BOX', 'NYSE', 'NASDAQ', 'BATS', 'C2', 'AUTO'],
            'stopPriceLinkBasis': ['MANUAL', 'BASE', 'TRIGGER', 'LAST', 'BID', 'ASK', 'ASK_BID', 'MARK', 'AVERAGE'],
            'stopPriceLinkType':['VALUE', 'PERCENT', 'TICK'],
            'stopType':['STANDARD', 'BID', 'ASK', 'LAST', 'MARK'],
            'priceLinkBasis':['MANUAL', 'BASE', 'TRIGGER', 'LAST', 'BID', 'ASK', 'ASK_BID', 'MARK', 'AVERAGE'],
            'priceLinkType': ['VALUE', 'PERCENT', 'TICK'],
            'taxLotMethod': ['FIFO', 'LIFO', 'HIGH_COST', 'LOW_COST', 'AVERAGE_COST', 'SPECIFIC_LOT'],
            'orderLegType': ['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY'],
            'instruction': ['BUY', 'SELL', 'BUY_TO_COVER', 'SELL_SHORT', 'BUY_TO_OPEN', 'BUY_TO_CLOSE', 'SELL_TO_OPEN', 'SELL_TO_CLOSE', 
                            'EXCHANGE'],
            'positionEffect': ['OPENING', 'CLOSING', 'AUTOMATIC'],
            'quantityType': ['ALL_SHARES', 'DOLLARS', 'SHARES'],
            'specialInstruction': ['ALL_OR_NONE', 'DO_NOT_REDUCE', 'ALL_OR_NONE_DO_NOT_REDUCE'],
            'orderStrategyType': ['SINGLE', 'OCO', 'TRIGGER'],
            'status': ['AWAITING_PARENT_ORDER', 'AWAITING_CONDITION', 'AWAITING_MANUAL_REVIEW', 'ACCEPTED', 'AWAITING_UR_OUT', 
                       'PENDING_ACTIVATION', 'QUEUED', 'WORKING', 'REJECTED', 'PENDING_CANCEL', 'CANCELED', 'PENDING_REPLACE', 
                       'REPLACED', 'FILLED', 'EXPIRED']
        }

        self.instrument_sub_class_arguments = {
            'Option':{
                'assetType':['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY'],
                'type':['VANILLA', 'BINARY', 'BARRIER'],
                'putCall':['PUT', 'CALL'],
                'optionDeliverables':{
                    'currencyType':['USD', 'CAD', 'EUR', 'JPY'],
                    'assetType':['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY']
                }
            },
            'MutualFund':{
                'assetType':['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY'],
                'type':['NOT_APPLICABLE', 'OPEN_END_NON_TAXABLE', 'OPEN_END_TAXABLE', 'NO_LOAD_NON_TAXABLE', 'NO_LOAD_TAXABLE']
            },
            'CashEquivalent':{
                'assetType':['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY'],
                'type':['SAVINGS', 'MONEY_MARKET_FUND']            
            },
            'Equity':{
                'assetType':['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY']       
            },
            'FixedIncome':{
                'assetType':['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY']                  
            }
        }

        self.order_activity_arguments = {
            'activityType':['EXECUTION', 'ORDER_ACTION'],
            'executionType':['FILL']
        }

    # def create_saved_order(self)


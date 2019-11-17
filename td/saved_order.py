import json
from enum import Enum


class OrderLeg():

    def __init__(self, **kwargs):

        self.order_leg_arguments = {
            'instruction':['BUY', 'SELL', 'BUY_TO_COVER', 'SELL_SHORT', 'BUY_TO_OPEN', 'BUY_TO_CLOSE', 'SELL_TO_OPEN', 'SELL_TO_CLOSE','EXCHANGE'],
            'assetType':['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY'],
            'quantityType': ['ALL_SHARES', 'DOLLARS', 'SHARES']
            }

        if 'template' in kwargs.keys():
            self.template = kwargs['template']
        else:
            self.template = {}

    def order_leg_instruction(self, instruction = None):

        # for any Enum member
        if isinstance(instruction, Enum):
            instruction = instruction.name

        if instruction in self.order_leg_arguments['instruction']:
            self.template['instruction'] = instruction
        else:
            raise ValueError('Incorrect Value for the Instruction paramater')

    def order_leg_asset(self, asset_type = None, symbol = None):

        # for any Enum member
        if isinstance(asset_type, Enum):
            asset_type = asset_type.name

        asset_dict = {'assetType':'','symbol':''}

        if asset_type in self.order_leg_arguments['assetType']:
            asset_dict['assetType'] = asset_type
            asset_dict['symbol'] = symbol
            self.template['instrument'] = asset_dict
        else:
            raise ValueError('Incorrect Value for the asset type paramater')

    def order_leg_quantity(self, quantity = None):        
        self.template['quantity'] = int(quantity)

    def order_leg_price(self, price = None):
        self.template['price'] = float(price)

    def order_leg_quantity_type(self, quantity_type = None):

        # for any Enum member
        if isinstance(quantity_type, Enum):
            quantity_type = quantity_type.name

        if quantity_type in self.order_leg_arguments['quantityType']:
            self.template['quantityType'] = quantity_type
        else:
            raise ValueError('Incorrect Value for the Quantity Type paramater')

    def copy(self):

        template_copy = self.template.copy()

        return OrderLeg(template = template_copy)


class SavedOrder():

    def __init__(self, **kwargs):

        '''
            Initalizes the SavedOrder Object and override any default values that are
            passed through.
        '''

        self.saved_order_arguments = {

            'session':['NORMAL', 'AM', 'PM', 'SEAMLESS'],
            'duration':['DAY', 'GOOD_TILL_CANCEL', 'FILL_OR_KILL'],
            'requestedDestination':['INET', 'ECN_ARCA', 'CBOE', 'AMEX', 'PHLX', 'ISE', 'BOX', 'NYSE', 'NASDAQ', 'BATS', 'C2', 'AUTO'],
            'complexOrderStrategyType': ['NONE', 'COVERED', 'VERTICAL', 'BACK_RATIO', 'CALENDAR', 'DIAGONAL', 'STRADDLE', 
                                        'STRANGLE', 'COLLAR_SYNTHETIC', 'BUTTERFLY', 'CONDOR', 'IRON_CONDOR', 'VERTICAL_ROLL', 
                                        'COLLAR_WITH_STOCK', 'DOUBLE_DIAGONAL', 'UNBALANCED_BUTTERFLY', 'UNBALANCED_CONDOR', 
                                        'UNBALANCED_IRON_CONDOR', 'UNBALANCED_VERTICAL_ROLL', 'CUSTOM'],

            'stopPriceLinkBasis': ['MANUAL', 'BASE', 'TRIGGER', 'LAST', 'BID', 'ASK', 'ASK_BID', 'MARK', 'AVERAGE'],
            'stopPriceLinkType':['VALUE', 'PERCENT', 'TICK'],
            'stopType':['STANDARD', 'BID', 'ASK', 'LAST', 'MARK'],

            'priceLinkBasis':['MANUAL', 'BASE', 'TRIGGER', 'LAST', 'BID', 'ASK', 'ASK_BID', 'MARK', 'AVERAGE'],
            'priceLinkType': ['VALUE', 'PERCENT', 'TICK'],

            'orderType':['MARKET', 'LIMIT', 'STOP', 'STOP_LIMIT', 'TRAILING_STOP', 'MARKET_ON_CLOSE', 
                         'EXERCISE', 'TRAILING_STOP_LIMIT', 'NET_DEBIT', 'NET_CREDIT', 'NET_ZERO'],
            'orderLegType': ['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY'],
            'orderStrategyType': ['SINGLE', 'OCO', 'TRIGGER'],

            'instruction': ['BUY', 'SELL', 'BUY_TO_COVER', 'SELL_SHORT', 'BUY_TO_OPEN', 'BUY_TO_CLOSE', 'SELL_TO_OPEN', 'SELL_TO_CLOSE','EXCHANGE'],
            'positionEffect': ['OPENING', 'CLOSING', 'AUTOMATIC'],
            'quantityType': ['ALL_SHARES', 'DOLLARS', 'SHARES'],            
            'taxLotMethod': ['FIFO', 'LIFO', 'HIGH_COST', 'LOW_COST', 'AVERAGE_COST', 'SPECIFIC_LOT'],
            'specialInstruction': ['ALL_OR_NONE', 'DO_NOT_REDUCE', 'ALL_OR_NONE_DO_NOT_REDUCE'],

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

        # defines the empty template for our order
        self.template = {}

        self.order_legs_collection = []

    '''
        ALEX'S NOTE

        Every trade should need a session. The logic is that if no session is given, then how would we know when
        to execute it?

        Every trade should need a duration. Again, how do we know when to cancel it if at all? Do we just add a 
        default value?

        Every order doesn't need a complex order strategy type. For example, it could be just a simple limit order.
        However, if you do give a complex order strategy type could we use this to determine other arguments that we
        would need? 
        
    '''

    def saved_order_session(self, session = None):
        '''
            Define the session for the trade.
        '''

        # for any Enum member
        if isinstance(session, Enum):
            session = session.name

        if session in self.saved_order_arguments['session']:
            self.template['session'] = session
        else:
            raise ValueError('Incorrect Value for the Session paramater')

    def saved_order_duration(self, duration = None, cancel_time = None):
        '''

        '''

        # for any Enum member
        if isinstance(duration, Enum):
            duration = duration.name

        if duration in self.saved_order_arguments['duration']:
            self.template['duration'] = duration
        else:
            raise ValueError('Incorrect Value for the Session paramater')

        if cancel_time is not None:
            self.template['cancelTime'] = {'date':cancel_time, 'shortFormat':False}

    def complex_order_type(self, complex_order_strategy_type = None):
        '''

        '''

        if complex_order_strategy_type == None:
            self.template['complexOrderStrategyType'] = 'NONE'
        elif complex_order_strategy_type in self.saved_order_arguments['complexOrderStrategyType']:
            self.template['complexOrderStrategyType'] = complex_order_strategy_type
        else:
            raise ValueError('Incorrect Value for the complexOrderStrategyType paramater')

    def order_strategy_type(self, order_strategy_type = None):
        '''

        '''

        if order_strategy_type in self.saved_order_arguments['orderStrategyType']:
            self.template['orderStrategyType'] = order_strategy_type
        else:
            raise ValueError('Incorrect Value for the orderStrategyType paramater')

    def return_order(self):

        self.template['orderLegCollection'] = self.order_legs_collection

        return self.template


    def create_limit_order(self):
        pass

    def create_stop_order(self):
        pass

    def create_child_strategy(self):
        pass

    def create_saved_order(self):
        pass

    def create_order_instructions(self):
        pass


    def add_order_leg(self, order_leg = None):
        self.order_legs_collection.append(order_leg.template)
    
    def delete_from_orders_collection(self):
        pass


    def validate_saved_order(self):
        pass

    def saved_order_to_json(self):
        pass



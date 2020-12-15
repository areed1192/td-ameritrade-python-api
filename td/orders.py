import json
from enum import Enum
from collections import OrderedDict


class OrderLeg():

    '''
        Represents an OrderLeg object that is used to specify instructions
        about the order.
    '''

    def __init__(self, **kwargs):
        '''
            Initalizes the OrderLeg Object and override any default values that are
            passed through.
        '''

        # Define the order Leg arguments used for validation.
        self.order_leg_arguments = {
            'instruction': ['BUY', 'SELL', 'BUY_TO_COVER', 'SELL_SHORT', 'BUY_TO_OPEN', 'BUY_TO_CLOSE', 'SELL_TO_OPEN', 'SELL_TO_CLOSE', 'EXCHANGE'],
            'assetType': ['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY'],
            'quantityType': ['ALL_SHARES', 'DOLLARS', 'SHARES']
        }

        # If the user provides a template use that otherwise create a blank template.
        if 'template' in kwargs.keys():
            self.template = kwargs['template']
        else:
            self.template = {}

    def order_leg_instruction(self, instruction=None):
        '''
            Defines the Instruction argument for the order leg. Can be either
            a string or enum.

            NAME: instruction
            DESC: A the order instruction value.
            TYPE: String | Enum
        '''

        # Grab the enumeration value if an Enum object was passed through.
        if isinstance(instruction, Enum):
            instruction = instruction.name

        # Add it to the OrderLeg.
        if instruction in self.order_leg_arguments['instruction']:
            self.template['instruction'] = instruction
        else:
            raise ValueError('Incorrect Value for the Instruction paramater')

    def order_leg_asset(self, asset_type=None, symbol=None):
        '''
            Defines the asset that is to be purchased/sold in the order. To define an asset
            you need a symbol and an asset type value.

            NAME: asset_type
            DESC: The type of asset to be traded.
            TYPE: String | Enum       

            NAME: symbol
            DESC: The symbol of the asset to be traded.
            TYPE: String
        '''

        # initalize the asset dictionary.
        asset_dict = {'assetType': '', 'symbol': ''}

        # Grab the enumeration value if an Enum object was passed through.
        if isinstance(asset_type, Enum):
            asset_type = asset_type.name

        # Add the values to the asset dictionary and then add that to the template.
        if asset_type in self.order_leg_arguments['assetType']:
            asset_dict['assetType'] = asset_type
            asset_dict['symbol'] = symbol
            self.template['instrument'] = asset_dict
        else:
            raise ValueError('Incorrect Value for the asset type paramater')

    def order_leg_quantity(self, quantity=None):
        '''
            Specifies the quantity of the asset to purchase/sell. Must be an integer.

            NAME: quantity
            DESC: The quantity to be purchased.
            TYPE: Int
        '''

        # make sure it's an Int before adding it.
        if isinstance(quantity, int):
            self.template['quantity'] = quantity
        else:
            raise ValueError('Quantity must be the data type <INT>.')

    def order_leg_price(self, price=None):
        '''
            Defines the price of the order to be made.

            NAME: price
            DESC: The price at which to execute the order.
            TYPE: Float
        '''

        # make sure it's a float before adding it.
        if isinstance(price, float):
            self.template['price'] = price
        else:
            raise ValueError('Price must be the data type <FLOAT>.')

    def order_leg_quantity_type(self, quantity_type=None):
        '''
            Defines the Order Leg Quantity TYPE. Orders can be
            sepcified as either by the number of shares you want to buy
            or the dollar amount you want to buy. This argument defines
            how you want to specify the quantity.
        '''

        # Grab the enumeration value if an Enum object was passed through.
        if isinstance(quantity_type, Enum):
            quantity_type = quantity_type.name

        # Add it to the template.
        if quantity_type in self.order_leg_arguments['quantityType']:
            self.template['quantityType'] = quantity_type
        else:
            raise ValueError('Incorrect Value for the Quantity Type paramater')

    def copy(self):
        '''
            Returns a copy of the Order Leg so that users can easily build another
            one using the copy.

            RTYPE: OrderLeg Object.
        '''

        # copy it and return a new OrderLeg Object.
        template_copy = self.template.copy()
        return OrderLeg(template=template_copy)


class Order():

    def __init__(self, **kwargs):
        '''
            Initalizes the SavedOrder Object and override any default values that are
            passed through.
        '''

        self.saved_order_arguments = {

            'session': ['NORMAL', 'AM', 'PM', 'SEAMLESS'],
            'duration': ['DAY', 'GOOD_TILL_CANCEL', 'FILL_OR_KILL'],
            'requestedDestination': ['INET', 'ECN_ARCA', 'CBOE', 'AMEX', 'PHLX', 'ISE', 'BOX', 'NYSE', 'NASDAQ', 'BATS', 'C2', 'AUTO'],
            'complexOrderStrategyType': ['NONE', 'COVERED', 'VERTICAL', 'BACK_RATIO', 'CALENDAR', 'DIAGONAL', 'STRADDLE',
                                         'STRANGLE', 'COLLAR_SYNTHETIC', 'BUTTERFLY', 'CONDOR', 'IRON_CONDOR', 'VERTICAL_ROLL',
                                         'COLLAR_WITH_STOCK', 'DOUBLE_DIAGONAL', 'UNBALANCED_BUTTERFLY', 'UNBALANCED_CONDOR',
                                         'UNBALANCED_IRON_CONDOR', 'UNBALANCED_VERTICAL_ROLL', 'CUSTOM'],

            'stopPriceLinkBasis': ['MANUAL', 'BASE', 'TRIGGER', 'LAST', 'BID', 'ASK', 'ASK_BID', 'MARK', 'AVERAGE'],
            'stopPriceLinkType': ['VALUE', 'PERCENT', 'TICK'],
            'stopType': ['STANDARD', 'BID', 'ASK', 'LAST', 'MARK'],

            'priceLinkBasis': ['MANUAL', 'BASE', 'TRIGGER', 'LAST', 'BID', 'ASK', 'ASK_BID', 'MARK', 'AVERAGE'],
            'priceLinkType': ['VALUE', 'PERCENT', 'TICK'],

            'orderType': ['MARKET', 'LIMIT', 'STOP', 'STOP_LIMIT', 'TRAILING_STOP', 'MARKET_ON_CLOSE',
                          'EXERCISE', 'TRAILING_STOP_LIMIT', 'NET_DEBIT', 'NET_CREDIT', 'NET_ZERO'],
            'orderLegType': ['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY'],
            'orderStrategyType': ['SINGLE', 'OCO', 'TRIGGER'],

            'instruction': ['BUY', 'SELL', 'BUY_TO_COVER', 'SELL_SHORT', 'BUY_TO_OPEN', 'BUY_TO_CLOSE', 'SELL_TO_OPEN', 'SELL_TO_CLOSE', 'EXCHANGE'],
            'positionEffect': ['OPENING', 'CLOSING', 'AUTOMATIC'],
            'quantityType': ['ALL_SHARES', 'DOLLARS', 'SHARES'],
            'taxLotMethod': ['FIFO', 'LIFO', 'HIGH_COST', 'LOW_COST', 'AVERAGE_COST', 'SPECIFIC_LOT'],
            'specialInstruction': ['ALL_OR_NONE', 'DO_NOT_REDUCE', 'ALL_OR_NONE_DO_NOT_REDUCE'],

            'status': ['AWAITING_PARENT_ORDER', 'AWAITING_CONDITION', 'AWAITING_MANUAL_REVIEW', 'ACCEPTED', 'AWAITING_UR_OUT',
                       'PENDING_ACTIVATION', 'QUEUED', 'WORKING', 'REJECTED', 'PENDING_CANCEL', 'CANCELED', 'PENDING_REPLACE',
                       'REPLACED', 'FILLED', 'EXPIRED']
        }

        self.instrument_sub_class_arguments = {
            'Option': {
                'assetType': ['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY'],
                'type': ['VANILLA', 'BINARY', 'BARRIER'],
                'putCall': ['PUT', 'CALL'],
                'optionDeliverables': {
                    'currencyType': ['USD', 'CAD', 'EUR', 'JPY'],
                    'assetType': ['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY']
                }
            },
            'MutualFund': {
                'assetType': ['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY'],
                'type': ['NOT_APPLICABLE', 'OPEN_END_NON_TAXABLE', 'OPEN_END_TAXABLE', 'NO_LOAD_NON_TAXABLE', 'NO_LOAD_TAXABLE']
            },
            'CashEquivalent': {
                'assetType': ['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY'],
                'type': ['SAVINGS', 'MONEY_MARKET_FUND']
            },
            'Equity': {
                'assetType': ['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY']
            },
            'FixedIncome': {
                'assetType': ['EQUITY', 'OPTION', 'INDEX', 'MUTUAL_FUND', 'CASH_EQUIVALENT', 'FIXED_INCOME', 'CURRENCY']
            }
        }

        self.order_activity_arguments = {
            'activityType': ['EXECUTION', 'ORDER_ACTION'],
            'executionType': ['FILL']
        }

        # defines the empty template for our order
        self.template = {}
        self.order_legs_collection = {}
        self.child_order_strategies = {}
        self.order_legs_count = 0
        self.child_order_count = 0

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

    def _grab_value(self, item=None):
        '''
            Standardizes the process of grabbing values passed through to the order Object.
            This will maintain a single entry point for testing the object type and returning
            the correct value.
        '''

        # Grab the enumeration value if an Enum object was passed through.
        if isinstance(item, Enum):
            item_value = item.name
        else:
            item_value = item

        return item_value

    def order_price(self, price=None):
        '''
            Defines the price of the order to be made.

            NAME: price
            DESC: The price at which to execute the order.
            TYPE: Float
        '''

        # make sure it's a float before adding it.
        if isinstance(price, float):
            self.template['price'] = price
        else:
            raise ValueError('Price must be the data type <FLOAT>.')

    def order_type(self, order_type=None):
        '''
            Defines the Order type for the Order Object. Order Type can either be
            a string or an Enum object from the `enums` file.

            NAME: order_type
            DESC: A valid order type value that is to be associated with the Order
                  object.
            TYPE: String | Enum
        '''

        # Grab the value.
        order_type = self._grab_value(item=order_type)

        if order_type in self.saved_order_arguments['orderType']:
            self.template['orderType'] = order_type
        else:
            raise ValueError('Incorrect Value for the OrderType paramater')

    def stop_price_offset(self, stop_price_offset= None):
        '''
            Defines the stop price of the order to be made.

            NAME: stop_price
            DESC: The stop price at which to execute the order.
            TYPE: Float
        '''

        self.template['stopPriceOffset'] = stop_price_offset

    def stop_type(self, stop_type = None):
        '''
            Defines the stop price of the order to be made.

            NAME: stop_price
            DESC: The stop price at which to execute the order.
            TYPE: Float
        '''

        # Grab the value.
        stop_type = self._grab_value(item = stop_type)

        # Add to template.
        if stop_type in self.saved_order_arguments['stopType']:
            self.template['stopType'] = stop_type
        else:
            raise ValueError('Incorrect Value for the stopType paramater')
        

    def stop_price_link_type(self, stop_price_link_type = None):
        '''
            Defines the stop price of the order to be made.

            NAME: stop_price
            DESC: The stop price at which to execute the order.
            TYPE: Float
        '''

        # Grab the value.
        stop_price_link_type = self._grab_value(item = stop_price_link_type)

        # Add to template.
        if stop_price_link_type.upper() in self.saved_order_arguments['stopPriceLinkType']:
            self.template['stopPriceLinkType'] = stop_price_link_type.upper()
        else:
            raise ValueError('Incorrect Value for the stopPriceLinktype paramater')


    def stop_price_link_basis(self, stop_price_link_basis = None):
        '''
            Defines the stop price of the order to be made.

            NAME: stop_price
            DESC: The stop price at which to execute the order.
            TYPE: Float
        '''

        # Grab the value.
        stop_price_link_basis = self._grab_value(item = stop_price_link_basis)

        # Add to template.
        if stop_price_link_basis.upper() in self.saved_order_arguments['stopPriceLinkBasis']:
            self.template['stopPriceLinkBasis'] = stop_price_link_basis.upper()
        else:
            raise ValueError('Incorrect Value for the stopPriceLinkBasis paramater')

    def stop_price(self, stop_price = None):
        '''
            Defines the stop price of the order to be made.
            
            NAME: stop_price
            DESC: The stop price at which to execute the order.
            TYPE: Float
        '''

        # make sure it's a float before adding it.
        if isinstance(stop_price, float):
            self.template['stopPrice'] = stop_price
        else:
            raise ValueError('Stop Price must be the data type FLOAT.')

    def order_session(self, session=None):
        '''
            Define the session for the trade.

            NAME: session
            DESC: A valid session type for the Order Object.
            TYPE: String | Enum
        '''

        # Grab the enumeration value if an Enum object was passed through.
        if isinstance(session, Enum):
            session = session.name

        # Add it to the dictionary.
        if session in self.saved_order_arguments['session']:
            self.template['session'] = session
        else:
            raise ValueError('Incorrect Value for the Session paramater')

    def order_duration(self, duration=None, cancel_time=None):
        '''
            Defines the order duration for the Order Object. Additionally,
            it will add the cancel time if passed through.

            NAME: duration
            DESC: The duration of the order.
            TYPE: String | Enum

            NAME: cancel_time
            DESC: The time that the order will be canceled.
            TYPE: String      
        '''

        # Grab the enumeration value if an Enum object was passed through.
        if isinstance(duration, Enum):
            duration = duration.name

        # Add the duration value.
        if duration in self.saved_order_arguments['duration']:
            self.template['duration'] = duration
        else:
            raise ValueError('Incorrect Value for the Session paramater')

        # Add the cancel time.
        if cancel_time is not None:
            
            self.template['cancelTime'] = {
                'date': cancel_time, 
                'shortFormat': False
            }

    def complex_order_type(self, complex_order_strategy_type=None):
        '''
            Defines the complex order type for the Order Object. 

            NAME: complex_order_strategy_type
            DESC: The Complex order strategy type for the order.
            TYPE: String | Enum           
        '''

        # Grab the enumeration value if an Enum object was passed through.
        if isinstance(complex_order_strategy_type, Enum):
            complex_order_strategy_type = complex_order_strategy_type.name

        # Add the Complex Order type to the order object.
        if complex_order_strategy_type in self.saved_order_arguments['complexOrderStrategyType']:
            self.template['complexOrderStrategyType'] = complex_order_strategy_type
        else:
            raise ValueError(
                'Incorrect Value for the complexOrderStrategyType paramater')

    def order_strategy_type(self, order_strategy_type=None):
        '''
            Defines the order strategy type for the Order Object. 

            NAME: order_strategy_type
            DESC: The order strategy type for the order.
            TYPE: String | Enum 
        '''

        # Grab the enumeration value if an Enum object was passed through.
        if isinstance(order_strategy_type, Enum):
            order_strategy_type = order_strategy_type.name

        # Add the value to the order object.
        if order_strategy_type in self.saved_order_arguments['orderStrategyType']:
            self.template['orderStrategyType'] = order_strategy_type
        else:
            raise ValueError(
                'Incorrect Value for the orderStrategyType paramater')

    def _grab_order(self):
        '''
            Grabs all the info passed through to the order object, creates an Ordered Dicitonary,
            checks for OrderLegCollection and grabs their values, and checks for ChildOrderStartegies
            and grabs their values.

            RTYPE: OrderedDict
        '''

        # Create an OrderedDict
        data = OrderedDict(self.template.items())

        # Grab any OrderLegCollections that exist.
        if len(list(self.order_legs_collection.values())) > 0:
            self.template['orderLegCollection'] = list(
                self.order_legs_collection.values())
            data['orderLegCollection'] = list(
                self.order_legs_collection.values())

        # Grab any ChildOrderStrategies that exist.
        if len(list(self.child_order_strategies.values())) > 0:
            self.template['childOrderStrategies'] = list(
                self.child_order_strategies.values())
            data['childOrderStrategies'] = list(
                self.child_order_strategies.values())

        return data

    def add_order_leg(self, order_leg=None):
        '''
            Adds a blank OrderLeg Object to the OrderLegs Collection.

            NAME: order_leg
            DESC: A order leg that contains infor about the order purchase.
            TYPE: OrderLeg
        '''

        # First define the key.
        key_id = "order_leg_" + str(len(self.order_legs_collection) + 1)

        # Add it to the collection.
        self.order_legs_collection[key_id] = order_leg.template

        # Update the count.
        self.order_legs_count = self.order_legs_count + 1

    def delete_order_leg(self, key=None, index=None):
        '''
            Deletes a specific OrderLeg from the OrderLeg Collection using
            either it's index (Position) or Key.

            NAME: Index
            DESC: The order leg index you wish to delete, ZERO BASED.
            TYPE: Int

            NAME: Key
            DESC: The unique key value for the OrderLeg object you wish to remove.
            TYPE: String.
        '''

        # sorted_orders_collection = OrderedDict(sorted(self.order_legs_collection.items(), key=lambda t: t[0]))

        # If the key exists, then delete it.
        if key is not None and key in self.order_legs_collection.keys():
            del self.order_legs_collection[key]

        # Raise error if no key was found.
        elif key is not None and key not in self.order_legs_collection.keys():
            raise KeyError(
                'The OrderLeg key you provided does not exist in the OrderLeg collection.')

        # Otherwise delete it based on the index.
        elif index is not None:
            for index_key, key in enumerate(sorted(self.order_legs_collection.items(), key=lambda t: t[0]).keys()):
                if index == index_key:
                    del self.order_legs_collection[index.key]
                else:
                    raise ValueError(
                        "The index you provided does not exist in the OrderLeg collection, please provide a valid index.")

        # Update the count.
        self.order_legs_count = self.order_legs_count - 1

    def _saved_order_to_json(self):
        '''
            Converts the order to a valid JSON string
            to be submitted to the TD API.
        '''
        return json.dumps(self._grab_order())

    def create_child_order_strategy(self):
        '''
            Creates a new Order Object that will represent a Child Order Strategy.

            RTYPE: Order Object
        '''
        return Order()

    def add_child_order_strategy(self, child_order_strategy=None):
        '''
            Adds the ChildOrderStrategy Object to the main PARENT Order object. Additionally,
            it will create a key for that ChildOrder.

            NAME: child_order_strategy
            DESC: The ChildOrderStrategy Object to be added to the main (PARENT) Order Object.
            TYPE: Order Object
        '''

        # Create the key.
        key_id = "child_order_strategy_" + \
            str(len(self.child_order_strategies) + 1)

        # Add it to the Child Order Strategies Collection.
        self.child_order_strategies[key_id] = child_order_strategy._grab_order(
        )

        # Update the count.
        self.child_order_count = self.child_order_count + 1

    def delete_child_order_strategy(self, key=None, index=None):
        '''
            Deletes a specific ChildOrderStrategy from the ChildOrderStrategy Collection using
            either it's index (Position) or Key.

            NAME: Index
            DESC: The child order strategy index you wish to delete, ZERO BASED.
            TYPE: Int

            NAME: Key
            DESC: The unique key value for the child order strategy object you wish to remove.
            TYPE: String.
        '''

        # If the key exists, then delete it.
        if key is not None and key in self.child_order_strategies.keys():
            del self.child_order_strategies[key]

        # Raise error if no key was found.
        elif key is not None and key not in self.child_order_strategies.keys():
            raise KeyError(
                'The ChildOrderStrategy key you provided does not exist in the ChildOrderStrategy collection.')

        # Otherwise delete it based on the index.
        elif index is not None:
            for index_key, key in enumerate(sorted(self.child_order_strategies.items(), key=lambda t: t[0]).keys()):
                if index == index_key:
                    del self.child_order_strategies[index.key]
                else:
                    raise ValueError(
                        "The index you provided does not exist in the ChildOrderStrategy collection, please provide a valid index.")

        # Update the count.
        self.child_order_count = self.child_order_count - 1

        # if key is not None and key in self.child_order_strategies.keys():
        #     del self.child_order_strategies[key]
        # elif index is not None:
        #     for index_key, key in enumerate(sorted(self.child_order_strategies.items(), key=lambda t: t[0]).keys()):
        #         if index ==  index_key:
        #             del self.child_order_strategies[index.key]

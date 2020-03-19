import json
from td.client import TDClient
from td.orders import Order, OrderLeg
from td.enums import ORDER_SESSION, DURATION, ORDER_INSTRUCTIONS, ORDER_ASSET_TYPE, ORDER_STRATEGY_TYPE, ORDER_TYPE, QUANTITY_TYPE

TESTING_FLAG = True

if TESTING_FLAG:
    from config import ACCOUNT_NUMBER, ACCOUNT_PASSWORD, CONSUMER_ID, REDIRECT_URI, TD_ACCOUNT
else:
    ACCOUNT_NUMBER = '<YOUR TD ACCOUNT USERNAME>'
    ACCOUNT_PASSWORD = '<YOUR TD ACCOUNT PASSWORD>'
    CONSUMER_ID = '<YOUR TD DEVELOPER ACCOUNT CONSUMER ID>'
    REDIRECT_URI = '<YOUR TD DEVELOPER ACCOUNT REDIRECT URI>'

# Initalize a new Order Object.
new_order = Order()

# Define the SESSION of the Order - ENUM EXAMPLE.
new_order.order_session(session=ORDER_SESSION.NORMAL)

# Define the DURATION of the Order - ENUM EXAMPLE.
new_order.order_duration(duration=DURATION.GOOD_TILL_CANCEL)

# Define a new OrderLeg Object.
new_order_leg = OrderLeg()

# Define the ORDER INSTRUCTION - ENUM EXAMPLE.
new_order_leg.order_leg_instruction(instruction=ORDER_INSTRUCTIONS.SELL)

# Define the PRICE - CAN ONLY BE A FLOAT.
new_order_leg.order_leg_price(price=112.50)

# Define the QUANTITY - CAN ONLY BE A INTEGER.
new_order_leg.order_leg_quantity(quantity=10)

# Define the ASSET to be traded - ENUM EXAMPLE -- SYMBOL MUST ALWAYS BE A STRING.
new_order_leg.order_leg_asset(asset_type=ORDER_ASSET_TYPE.EQUITY, symbol='MSFT')

# Once we have built our order leg, we can add it to our OrderObject.
new_order.add_order_leg(order_leg=new_order_leg)

# Create a new session
td_session = TDClient(account_number=ACCOUNT_NUMBER,
                      account_password=ACCOUNT_PASSWORD,
                      consumer_id=CONSUMER_ID,
                      redirect_uri=REDIRECT_URI,
                      json_path = r"C:\Users\Alex\OneDrive\Desktop\TDAmeritradeState.json"
                      )

td_session.login()

# # Place the Order
# td_session.place_order(account = '11111', order= new_order)



# Create the Order.
option_order = Order()
option_order.order_session(session = 'NORMAL')
option_order.order_duration(duration = 'GOOD_TILL_CANCEL')
option_order.order_type(order_type = 'LIMIT')
option_order.order_strategy_type(order_strategy_type = 'SINGLE')
option_order.order_price(price = 12.00)

# Create the Order Leg
option_order_leg = OrderLeg()
option_order_leg.order_leg_instruction(instruction = 'BUY_TO_OPEN')
option_order_leg.order_leg_quantity(quantity = int(1))
option_order_leg.order_leg_asset(asset_type = 'OPTION', symbol = 'MSFT_031320C155')

# Add the Order Leg to the Order
option_order.add_order_leg(order_leg = option_order_leg)

print(dict(option_order._grab_order()))


### Initalize a new Order Object.
new_order = Order()
new_order.order_type(order_type = ORDER_TYPE.MARKET)
new_order.order_session(session = ORDER_SESSION.NORMAL)
new_order.order_duration(duration = DURATION.DAY)
new_order.order_strategy_type(order_strategy_type = ORDER_STRATEGY_TYPE.SINGLE)

### Define a new OrderLeg Object.
new_order_leg = OrderLeg()
new_order_leg.order_leg_instruction(instruction = ORDER_INSTRUCTIONS.BUY)
new_order_leg.order_leg_asset(asset_type = ORDER_ASSET_TYPE.EQUITY, symbol = 'GIS')
new_order_leg.order_leg_quantity_type(quantity_type = QUANTITY_TYPE.SHARES)
new_order_leg.order_leg_quantity(quantity=1)

# 
new_order.add_order_leg(order_leg = new_order_leg)

print(json.dumps(dict(new_order._grab_order())))

# # Place the Order
# print(td_session.place_order(account = TD_ACCOUNT, order = new_order))
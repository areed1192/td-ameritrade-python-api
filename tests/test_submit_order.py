from td.client import TDClient
from td.orders import Order, OrderLeg
from td.enums import ORDER_SESSION, DURATION, ORDER_INSTRUCTIONS, ORDER_ASSET_TYPE
from td.config import ACCOUNT_NUMBER, ACCOUNT_PASSWORD, CONSUMER_ID, REDIRECT_URI, TD_ACCOUNT

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
                      redirect_uri=REDIRECT_URI)

td_session.place_order(account = '11111', order= new_order)
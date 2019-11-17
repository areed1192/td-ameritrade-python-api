import pprint
from saved_order import SavedOrder, OrderLeg
from enums import ORDER_SESSION, DURATION, ORDER_INSTRUCTIONS, ORDER_ASSET_TYPE

# initalize a Saved Order Object
new_saved_order = SavedOrder()

# define the session of this saved order.
new_saved_order.saved_order_session(session = ORDER_SESSION.NORMAL)

# define the duration
new_saved_order.saved_order_duration(duration = DURATION.GOOD_TILL_CANCEL)

# define the duration, with string
new_saved_order.saved_order_duration(duration = 'GOOD_TILL_CANCEL')

new_order_leg = OrderLeg()
new_order_leg.order_leg_instruction(instruction = ORDER_INSTRUCTIONS.SELL)
new_order_leg.order_leg_price(price = 112.50)
new_order_leg.order_leg_quantity(quantity = 10)
new_order_leg.order_leg_asset(asset_type = ORDER_ASSET_TYPE.EQUITY, symbol = 'MSFT')

copied_order_leg = new_order_leg.copy()

new_saved_order.add_order_leg(order_leg = new_order_leg)
new_saved_order.add_order_leg(order_leg = copied_order_leg)

pprint.pprint(new_saved_order.return_order())
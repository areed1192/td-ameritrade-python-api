import json
import pprint
from orders import Order, OrderLeg
from enums import ORDER_SESSION, DURATION, ORDER_INSTRUCTIONS, ORDER_ASSET_TYPE

# initalize a Saved Order Object
new_saved_order = Order()

# define the session of this saved order.
new_saved_order.order_session(session = ORDER_SESSION.NORMAL)

# define the duration
new_saved_order.order_duration(duration = DURATION.GOOD_TILL_CANCEL)

# define the duration, with string
new_saved_order.order_duration(duration = 'GOOD_TILL_CANCEL')

new_order_leg = OrderLeg()
new_order_leg.order_leg_instruction(instruction = ORDER_INSTRUCTIONS.SELL)
new_order_leg.order_leg_price(price = 112.50)
new_order_leg.order_leg_quantity(quantity = 10)
new_order_leg.order_leg_asset(asset_type = ORDER_ASSET_TYPE.EQUITY, symbol = 'MSFT')

copied_order_leg = new_order_leg.copy()

new_saved_order.add_order_leg(order_leg = new_order_leg)
new_saved_order.add_order_leg(order_leg = copied_order_leg)

# pprint.pprint(new_saved_order.grab_order())


# create a child order
child_order = new_saved_order.create_child_order_strategy()

# define the session of this saved order.
child_order.order_session(session = ORDER_SESSION.PM)

# define the duration
child_order.order_duration(duration = DURATION.FILL_OR_KILL)

new_order_leg2 = OrderLeg()
new_order_leg2.order_leg_instruction(instruction = ORDER_INSTRUCTIONS.SELL)
new_order_leg2.order_leg_price(price = 300.50)
new_order_leg2.order_leg_quantity(quantity = 30)
new_order_leg2.order_leg_asset(asset_type = ORDER_ASSET_TYPE.EQUITY, symbol = 'AMZN')

child_order.add_order_leg(order_leg = new_order_leg2)

new_saved_order.add_child_order_strategy(child_order_strategy = child_order)

pprint.pprint(new_saved_order.grab_order())

print(json.dumps(new_saved_order.grab_order(), indent = 4))
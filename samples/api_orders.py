from td.orders import Order, OrderLeg
from td.enums import ORDER_SESSION, DURATION, ORDER_INSTRUCTIONS, ORDER_ASSET_TYPE

# Initalize a new Order Object.
new_order = Order()

#
#   MOST OF THE PARAMETERS OF YOUR ORDER CAN BE SPECIFIED EITHER WITH AN ENUM OBJECT
#   OR A STRING VALUE.
#

# Define the SESSION of the Order - ENUM EXAMPLE.
new_order.order_session(session=ORDER_SESSION.NORMAL)

# Define the SESSION of the Order - STRING EXAMPLE.
# new_order.order_session(session = 'NORMAL')


# Define the DURATION of the Order - ENUM EXAMPLE.
new_order.order_duration(duration=DURATION.GOOD_TILL_CANCEL)

# Define the DURATION of the Order - STRING EXAMPLE.
# new_saved_order.order_duration(duration = 'GOOD_TILL_CANCEL')


#
#   AN ORDER OBJECT CONTAINS AN ORDERLEG OBJECT. THE ORDERLEG OBJECT DEFINES
#   ORDER INSTRUCTIONS, INFORMATION ABOUT THE ASSET, AND PRICE/QUANTITY.
#   OR A STRING VALUE.
#


# Define a new OrderLeg Object.
new_order_leg = OrderLeg()

# Define the ORDER INSTRUCTION - ENUM EXAMPLE.
new_order_leg.order_leg_instruction(instruction=ORDER_INSTRUCTIONS.SELL)

# Define the ORDER INSTRUCTION - STRING EXAMPLE.
# new_order_leg.order_leg_instruction(instruction = 'SELL')

# Define the PRICE - CAN ONLY BE A FLOAT.
new_order_leg.order_leg_price(price=112.50)

# Define the QUANTITY - CAN ONLY BE A INTEGER.
new_order_leg.order_leg_quantity(quantity=1)

# Define the ASSET to be traded - ENUM EXAMPLE -- SYMBOL MUST ALWAYS BE A STRING.
new_order_leg.order_leg_asset(asset_type=ORDER_ASSET_TYPE.EQUITY, symbol='AA')

# Define the ASSET to be traded - STRING EXAMPLE -- SYMBOL MUST ALWAYS BE A STRING.
new_order_leg.order_leg_asset(asset_type='EQUITY', symbol='MSFT')

# Order Legs can be copied so you have a template to build off of.
copied_order_leg = new_order_leg.copy()

# Once we have built our order leg, we can add it to our OrderObject.
new_order.add_order_leg(order_leg=new_order_leg)

# Print it out so you can see it, normally this method is called by the TD API when using the td.client object.
print("YOU HAVE {} ORDER(S) IN THE ORDER LEGS COLLECTION.".format(
    new_order.order_legs_count)
)
print('-'*80)

# We could also add a copied order to our order leg collection.
new_order.add_order_leg(order_leg=copied_order_leg)

# Print it out so we can see both now.
print("YOU HAVE {} ORDER(S) IN THE ORDER LEGS COLLECTION.".format(
    new_order.order_legs_count)
)
print('-'*80)


#
#  SOME ORDERS, USUALLY THE MORE COMPLEX ONES, HAVE A CHILD ORDER.
#  A CHILD ORDER IS SIMPLY A REGULAR ORDER OBJECT BUT IS A DESCENDANT OF THE
#  MAIN PARENT ORDER OBJECT. CHILD ORDERS NORMALLY EMPHASIZE CONDITIONS IN
#  TRADING.
#


# Let's take our Order Object and create a new child order using the `create_child_order_strategy` method.
child_order = new_order.create_child_order_strategy()


# Define the SESSION of our CHILD ORDER - ENUM EXAMPLE.
child_order.order_session(session=ORDER_SESSION.PM)

# Define the SESSION of our CHILD ORDER - STRING EXAMPLE.
# child_order.order_session(session = 'PM')


# Define the DURATION of our CHILD ORDER - ENUM EXAMPLE.
child_order.order_duration(duration=DURATION.FILL_OR_KILL)

# Define the DURATION of our CHILD ORDER - STRING EXAMPLE.
child_order.order_duration(duration='FILL_OR_KILL')

# Child Orders, because they're an Order can also have their own OrderLeg Object. Let's create one.
child_order_leg = OrderLeg()


# Define the ORDER LEG INSTRUCTION for the CHILD ORDER LEG - ENUM EXAMPLE.
child_order_leg.order_leg_instruction(instruction=ORDER_INSTRUCTIONS.SELL)

# Define the ORDER LEG INSTRUCTION for the CHILD ORDER LEG - STRING EXAMPLE.
# child_order_leg.order_leg_instruction(instruction = 'SELL')


# Define the PRICE of the CHILD ORDER LEG - MUST BE FLOAT.
child_order_leg.order_leg_price(price=300.50)

# Define the QUANTITY of the CHILD ORDER LEG - MUST BE INTEGER.
child_order_leg.order_leg_quantity(quantity=30)


# Define the ASSET to be traded - ENUM EXAMPLE -- SYMBOL MUST ALWAYS BE A STRING.
child_order_leg.order_leg_asset(
    asset_type=ORDER_ASSET_TYPE.EQUITY,
    symbol='AMZN'
)

# Define the ASSET to be traded - STRING EXAMPLE -- SYMBOL MUST ALWAYS BE A STRING.
child_order_leg.order_leg_asset(asset_type='EQUITY', symbol='AMZN')


# Take the CHILD ORDER LEG and it to the CHILD ORDER STRATEGY'S ORDER LEG COLLECTION.
child_order.add_order_leg(order_leg=child_order_leg)

# Display the count.
print("YOU HAVE {} ORDER(S) IN THE ORDER LEGS COLLECTION.".format(
    child_order.order_legs_count)
)
print('-'*80)

# Add the Child Order Strategy to the PARENT ORDER or in other words the order we created originally.
new_order.add_child_order_strategy(child_order_strategy=child_order)

# Print it so the user can see all the info at once.
print("YOU HAVE {} CHILD ORDER STRATEGIES IN THE CHILD ORDER STRATEGIES COLLECTION.".format(
    new_order.child_order_count)
)

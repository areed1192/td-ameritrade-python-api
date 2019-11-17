from saved_order import SavedOrder
from td_enums import ORDER_SESSION, DURATION

# initalize a Saved Order Object
new_saved_order = SavedOrder()

# define the session of this saved order.
new_saved_order.saved_order_session(session = ORDER_SESSION.NORMAL)

# define the duration
new_saved_order.saved_order_duration(duration = DURATION.GOOD_TILL_CANCEL)

# define the duration, with string
new_saved_order.saved_order_duration(duration = 'GOOD_TILL_CANCEL')

print(new_saved_order.template)
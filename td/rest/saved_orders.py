from typing import List
from typing import Union
from datetime import datetime
from datetime import date
from td.session import TdAmeritradeSession
from enum import Enum
from td.utils.orders import Order


class SavedOrders():

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `SavedOrders` services.

        ### Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession   
            object.
        """

        self.session = session

    def get_saved_orders_by_path(
        self,
        account_id: str
    ) -> dict:
        """Returns the saved orders for a specific account.

        ### Documentation
        ---- 
        https://developer.tdameritrade.com/account-access/apis/get/accounts/%7BaccountId%7D/savedorders-0

        ### Parameters
        ----
        account_id: str 
            The account number that you want to
            query for saved orders.

        ### Usage
        ----
            >>> saved_orders_service = td_client.saved_orders()
            >>> saved_orders_service.get_saved_orders_by_path(
                account_id=account_number
            )
        """

        # Define the endpoint.
        endpoint = f'accounts/{account_id}/savedorders'

        content = self.session.make_request(
            method='get',
            endpoint=endpoint
        )

        return content

    def get_saved_order(
        self,
        account_id: str,
        saved_order_id: str
    ) -> dict:
        """Get a specific saved order for a specific account.

        ### Documentation
        ---- 
        https://developer.tdameritrade.com/account-access/apis/get/accounts/%7BaccountId%7D/savedorders/%7BsavedOrderId%7D-0

        ### Parameters
        ----
        account_id: str 
            The account number that you want to
            query for saved_orders.

        saved_order_id: str
            The order ID you want to query.

        ### Usage
        ----
            >>> saved_orders_service = td_client.saved_orders()
            >>> saved_orders_service.get_order(
                account_id=account_number,
                saved_order_id='12345678;
            )
        """

        # Define the endpoint.
        endpoint = f'accounts/{account_id}/savedorders/{saved_order_id}'

        content = self.session.make_request(
            method='get',
            endpoint=endpoint
        )

        return content

    def place_saved_order(
        self,
        account_id: str,
        saved_order_object: Order = None,
        saved_order_dict: dict = None
    ) -> dict:
        """Place an order for a specific account. Order throttle
        limits may apply.

        ### Documentation
        ---- 
        https://developer.tdameritrade.com/account-access/apis/post/accounts/%7BaccountId%7D/savedorders-0

        ### Parameters
        ----
        account_id: str (optional, Default=None)
            The account number that you want to
            place the order for.

        saved_order_object: SavedOrder (optional, Default=None)
            Represents an `SavedOrder` object that can be used to
            submit a new order to the TD Ameritrade API. This
            is the preferred method as additional checks are
            done to make sure the order is valid.

        saved_order_dict: dict (optional, Default=None)
            Represents an `SavedOrder` constructed from an ordinary python
            dictionary object. No additional checks will be made on the
            inputs to validate them.

        ### Usage
        ----
            >>> saved_orders_service = td_client.saved_orders()
            >>> saved_orders_service.place_saved_order(
                account_id='123456789',
                order_dict={}
            )
        """

        if saved_order_object:
            order = saved_order_object._saved_order_to_json()

        if saved_order_dict:
            order = saved_order_dict

        # Define the endpoint.
        endpoint = f'accounts/{account_id}/savedorders'

        content = self.session.make_request(
            method='post',
            endpoint=endpoint,
            json_payload=order
        )

        return content

    def replace_saved_order(
        self,
        account_id: str,
        saved_order_id: str,
        saved_order_object: Order = None,
        saved_order_dict: dict = None
    ) -> dict:
        """Replace an existing saved order for an account. 

        ### Overview
        ----
        The existing order will be replaced by the new saved order. Once
        replaced, the old saved order will be canceled and a new order
        will be created. Order throttle limits may apply.

        ### Documentation
        ---- 
        https://developer.tdameritrade.com/account-access/apis/put/accounts/%7BaccountId%7D/savedorders/%7BsavedOrderId%7D-0

        ### Parameters
        ----
        account_id: str (optional, Default=None)
            The account number that you want to
            place the order for.

        saved_order_id: str (optional, Default=None)
            The saved order you want to be replaced.

        saved_order_object: SavedOrder (optional, Default=None)
            Represents an `SavedOrder` object that can be used to
            submit a replacing order to the TD Ameritrade API.
            This is the preferred method as additional checks
            are done to make sure the order is valid.

        saved_order_dict: dict (optional, Default=None)
            Represents an `SavedOrder` constructed from an ordinary python
            dictionary object. No additional checks will be made on the
            inputs to validate them.

        ### Usage
        ----
            >>> saved_orders_service = td_client.saved_orders()
            >>> saved_orders_service.replace_saved_order(
                account_id='123456789',
                order_id='12345678',
                order_dict={}
            )
        """

        if saved_order_object:
            order = saved_order_object._saved_order_to_json()

        if saved_order_dict:
            order = saved_order_dict

        # Define the endpoint.
        endpoint = f'accounts/{account_id}/savedorders/{saved_order_id}'

        content = self.session.make_request(
            method='put',
            endpoint=endpoint,
            json_payload=order
        )

        return content

    def cancel_saved_order(
        self,
        account_id: str,
        saved_order_id: str
    ) -> dict:
        """Cancels a saved order for a specific account. Order throttle
        limits may apply.

        ### Documentation
        ---- 
        https://developer.tdameritrade.com/account-access/apis/delete/accounts/%7BaccountId%7D/savedorders/%7BsavedOrderId%7D-0

        ### Parameters
        ----
        account_id: str (optional, Default=None)
            The account number that contains the saved order
            you want to cancel.

        saved_order_id: str (optional, Default=None)
            The saved order ID of the order you want to cancel.

        ### Usage
        ----
            >>> saved_orders_service = td_client.saved_orders()
            >>> saved_orders_service.cancel_saved_order(
                account_id='123456789',
                saved_order_id='12345678'
            )
        """

        # Define the endpoint.
        endpoint = f'accounts/{account_id}/savedorders/{saved_order_id}'

        content = self.session.make_request(
            method='delete',
            endpoint=endpoint
        )

        return content

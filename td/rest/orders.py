from typing import List
from typing import Union
from datetime import datetime
from datetime import date
from td.session import TdAmeritradeSession
from enum import Enum
from td.utils.utils import Order


class Orders():

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `Orders` services.

        ### Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession   
            object.
        """

        self.session = session

    def get_orders_by_path(
        self,
        account_id: str,
        max_results: int = None,
        from_entered_time: Union[datetime, str] = None,
        to_entered_time: Union[datetime, str] = None,
        order_status: Union[Enum, str] = None
    ) -> dict:
        """Returns the orders for a specific account.

        ### Documentation
        ---- 
        https://developer.tdameritrade.com/account-access/apis/get/accounts/%7BaccountId%7D/orders-0

        ### Parameters
        ----
        account_id: str 
            The account number that you want to
            query for orders.

        max_results: int (optional, Default=None)
            The maximum number of orders to retrieve.

        from_entered_time: Union[datetime, str] (optional, Default=None)
            Specifies that no orders entered before this time should be 
            returned. Valid ISO-8601 format yyyy-MM-dd Date must be within
            60 days from today's date. If argument set then 'to_entered_time'
            must also be set.

        to_entered_time: Union[datetime, str] (optional, Default=None)
            Specifies that no orders entered after this time should be 
            returned. Valid ISO-8601 format yyyy-MM-dd Date must be within
            60 days from today's date. If argument set then 'from_entered_time'
            must also be set.

        status: Union[datetime, Enum] (optional, Default=None)
            Specifies that only orders of this status should be returned.

        ### Usage
        ----
            >>> orders_service = td_client.orders()
            >>> orders_service.get_orders_by_path(
                account_id=account_number,
                order_status=OrderStatus.Filled
            )
        """

        # Grab the From Entered Time.
        if isinstance(from_entered_time, datetime):
            from_entered_time = from_entered_time.date().isoformat()
        elif isinstance(from_entered_time, date):
            from_entered_time = from_entered_time.isoformat()

        # Grab the To Entered Time.
        if isinstance(to_entered_time, datetime):
            to_entered_time = to_entered_time.date().isoformat()
        elif isinstance(to_entered_time, date):
            to_entered_time = to_entered_time.isoformat()

        # Grab the Order Status.
        if isinstance(order_status, Enum):
            order_status = order_status.value

        # Define the payload.
        params = {
            "maxResults": max_results,
            "fromEnteredTime": from_entered_time,
            "toEnteredTime": to_entered_time,
            "status": order_status
        }

        # Define the endpoint.
        endpoint = f'accounts/{account_id}/orders'

        content = self.session.make_request(
            method='get',
            endpoint=endpoint,
            params=params
        )

        return content

    def get_order(
        self,
        account_id: str,
        order_id: str
    ) -> dict:
        """Get a specific order for a specific account.

        ### Documentation
        ---- 
        https://developer.tdameritrade.com/account-access/apis/get/accounts/%7BaccountId%7D/orders/%7BorderId%7D-0

        ### Parameters
        ----
        account_id: str 
            The account number that you want to
            query for orders.

        order_id: str
            The order ID you want to query.

        ### Usage
        ----
            >>> orders_service = td_client.orders()
            >>> orders_service.get_order(
                account_id=account_number,
                order_id='12345678;
            )
        """

        # Define the endpoint.
        endpoint = f'accounts/{account_id}/orders/{order_id}'

        content = self.session.make_request(
            method='get',
            endpoint=endpoint
        )

        return content

    def get_orders_by_query(
        self,
        account_id: str = None,
        max_results: int = None,
        from_entered_time: Union[datetime, str] = None,
        to_entered_time: Union[datetime, str] = None,
        order_status: Union[Enum, str] = None
    ) -> dict:
        """Returns the orders for a specific account.

        ### Documentation
        ---- 
        https://developer.tdameritrade.com/account-access/apis/get/accounts/%7BaccountId%7D/orders-0

        ### Parameters
        ----
        account_id: str (optional, Default=None)
            The account number that you want to
            query for orders.

        max_results: int (optional, Default=None)
            The maximum number of orders to retrieve.

        from_entered_time: Union[datetime, str] (optional, Default=None)
            Specifies that no orders entered before this time should be 
            returned. Valid ISO-8601 format yyyy-MM-dd Date must be within
            60 days from today's date. If argument set then 'to_entered_time'
            must also be set.

        to_entered_time: Union[datetime, str] (optional, Default=None)
            Specifies that no orders entered after this time should be 
            returned. Valid ISO-8601 format yyyy-MM-dd Date must be within
            60 days from today's date. If argument set then 'from_entered_time'
            must also be set.

        status: Union[datetime, Enum] (optional, Default=None)
            Specifies that only orders of this status should be returned.

        ### Usage
        ----
            >>> orders_service = td_client.orders()
            >>> orders_service.get_orders_by_query()
        """

        # Grab the From Entered Time.
        if isinstance(from_entered_time, datetime):
            from_entered_time = from_entered_time.date().isoformat()
        elif isinstance(from_entered_time, date):
            from_entered_time = from_entered_time.isoformat()

        # Grab the To Entered Time.
        if isinstance(to_entered_time, datetime):
            to_entered_time = to_entered_time.date().isoformat()
        elif isinstance(to_entered_time, date):
            to_entered_time = to_entered_time.isoformat()

        # Grab the Order Status.
        if isinstance(order_status, Enum):
            order_status = order_status.value

        # Define the payload.
        params = {
            "accountId": account_id,
            "maxResults": max_results,
            "fromEnteredTime": from_entered_time,
            "toEnteredTime": to_entered_time,
            "status": order_status
        }

        # Define the endpoint.
        endpoint = f'orders'

        content = self.session.make_request(
            method='get',
            endpoint=endpoint,
            params=params
        )

        return content

    def place_order(
        self,
        account_id: str,
        order_object: Order = None,
        order_dict: dict = None
    ) -> dict:
        """Place an order for a specific account. Order throttle
        limits may apply.

        ### Documentation
        ---- 
        https://developer.tdameritrade.com/account-access/apis/post/accounts/%7BaccountId%7D/orders-0

        ### Parameters
        ----
        account_id: str (optional, Default=None)
            The account number that you want to
            place the order for.

        order_object: Order (optional, Default=None)
            Represents an `Order` object that can be used to
            submit a new order to the TD Ameritrade API. This
            is the preferred method as additional checks are
            done to make sure the order is valid.

        order_dict: dict (optional, Default=None)
            Represents an Order constructed from an ordinary python
            dictionary object. No additional checks will be made on the
            inputs to validate them.

        ### Usage
        ----
            >>> orders_service = td_client.orders()
            >>> orders_service.place_order(
                account_id='123456789',
                order_dict={}
            )
        """

        if order_object:
            order = order_object._saved_order_to_json()

        if order_dict:
            order = order_dict

        # Define the endpoint.
        endpoint = f'accounts/{account_id}/orders'

        content = self.session.make_request(
            method='post',
            endpoint=endpoint,
            json_payload=order
        )

        return content

    def replace_order(
        self,
        account_id: str,
        order_id: str,
        order_object: Order = None,
        order_dict: dict = None
    ) -> dict:
        """Replace an existing order for an account. 

        ### Overview
        ----
        The existing order will be replaced by the new order. Once
        replaced, the old order will be canceled and a new order
        will be created. Order throttle limits may apply.

        ### Documentation
        ---- 
        https://developer.tdameritrade.com/account-access/apis/put/accounts/%7BaccountId%7D/orders/%7BorderId%7D-0

        ### Parameters
        ----
        account_id: str (optional, Default=None)
            The account number that you want to
            place the order for.

        order_id: str (optional, Default=None)
            The order you want to be replaced.

        order_object: Order (optional, Default=None)
            Represents an `Order` object that can be used to
            submit a replacing order to the TD Ameritrade API.
            This is the preferred method as additional checks
            are done to make sure the order is valid.

        order_dict: dict (optional, Default=None)
            Represents an Order constructed from an ordinary python
            dictionary object. No additional checks will be made on the
            inputs to validate them.

        ### Usage
        ----
            >>> orders_service = td_client.orders()
            >>> orders_service.replace_order(
                account_id='123456789',
                order_id='12345678',
                order_dict={}
            )
        """

        if order_object:
            order = order_object._saved_order_to_json()

        if order_dict:
            order = order_dict

        # Define the endpoint.
        endpoint = f'accounts/{account_id}/orders/{order_id}'

        content = self.session.make_request(
            method='put',
            endpoint=endpoint,
            json_payload=order
        )

        return content

    def cancel_order(
        self,
        account_id: str,
        order_id: str
    ) -> dict:
        """Cancels an order for a specific account. Order throttle
        limits may apply.

        ### Documentation
        ---- 
        https://developer.tdameritrade.com/account-access/apis/delete/accounts/%7BaccountId%7D/orders/%7BorderId%7D-0

        ### Parameters
        ----
        account_id: str (optional, Default=None)
            The account number that contains the order
            you want to cancel

        order_id: str (optional, Default=None)
            The order ID of the order you want to cancel.

        ### Usage
        ----
            >>> orders_service = td_client.orders()
            >>> orders_service.cancel_order(
                account_id='123456789',
                order_id='12345678'
            )
        """

        # Define the endpoint.
        endpoint = f'accounts/{account_id}/orders/{order_id}'

        content = self.session.make_request(
            method='delete',
            endpoint=endpoint
        )

        return content

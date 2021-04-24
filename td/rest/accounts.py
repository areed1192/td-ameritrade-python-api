from typing import List
from typing import Union
from datetime import datetime
from td.session import TdAmeritradeSession
from enum import Enum


class Accounts():

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `Accounts` services.

        ### Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession   
            object.
        """

        self.session = session

    def get_accounts(self, account_id: str = None, include_orders: bool = True, include_positions: bool = True) -> dict:
        """Queries accounts for a user.

        ### Overview
        ----
        Serves as the mechanism to make a request to the 
        "Get Accounts" and "Get Account" Endpoint. If one
        account is provided a "Get Account" request will
        be made and if more than one account is provided
        then a "Get Accounts" request will be made.

        ### Documentation
        ----
        https://developer.tdameritrade.com/account-access/apis

        ### Parameters
        ----
        account_id: str (optional, default=None)
            The account number you wish to recieve data on.
            If no account ID is provided then all accounts will
            be queried.

        include_orders: bool (optional, default=True)
            If set to `True` then account orders will be returned
            from the API. If set to `False` no orders will be
            returned.

        include_positions: bool (optional, default=True)
            If set to `True` then account positions will be returned
            from the API. If set to `False` no positions will be
            returned.

        ### Usage
        ----
            >>> account_services = td_client.accounts()
            >>> account_services.get_accounts(
                account_id='123456789',
                include_orders=True,
                include_positions=True
            )
        """

        fields = []

        if account_id is None:
            endpoint = f'accounts'
        else:
            endpoint = f'accounts/{account_id}'

        if include_orders is True:
            fields.append('orders')

        if include_positions is True:
            fields.append('positions')
        params = {
            'fields': ','.join(fields),
        }

        content = self.session.make_request(
            method='get',
            endpoint=endpoint,
            params=params
        )

        return content

    def get_transactions(
        self,
        account_id: str,
        transaction_type: Union[str, Enum] = None,
        symbol: str = None,
        start_date: Union[str, datetime] = None,
        end_date: Union[str, datetime] = None
    ) -> dict:
        """Queries the transactions for an account.

        ### Documentation
        ----
        https://developer.tdameritrade.com/transaction-history/apis

        ### Parameters
        ----
        account_id: str
            The account number you want to query transactions
            for.

        transaction_type: Union[str, Enum] (optional, default=None)
            The type of transaction you want to query. For more info,
            review the documentation for a full list of transaction
            types, or review the `td.enums` file.

        symbol: str (optional, default=None)
            Filters the transaction to the ones that only include
            the symbol provided.

        start_date: Union[str, datetime] (optional, default=None)
            Only transactions after the start date will be returned.
            Note: The maximum date range is one year. Valid ISO-8601
            formats are: yyyy-MM-dd.

        end_date: Union[str, datetime] (optional, default=None)
            Only transactions before the end date will be returned.
            Note: The maximum date range is one year. Valid ISO-8601
            formats are: yyyy-MM-dd.

        ### Usage
        ----
            >>> account_services = td_client.accounts()
            >>> account_services.get_transactions(
                account_id='123456789',
                transaction_type='ALL'
            )
        """

        if isinstance(transaction_type, Enum):
            transaction_type = transaction_type.value

        if isinstance(start_date, datetime):
            start_date = start_date.date().isoformat()

        if isinstance(end_date, datetime):
            end_date = end_date.date().isoformat()

        params = {
            'type': transaction_type,
            'startDate': start_date,
            'endDate': end_date,
            'symbol': symbol
        }

        content = self.session.make_request(
            method='get',
            endpoint=f'accounts/{account_id}/transactions',
            params=params
        )

        return content

    def get_transaction(self, account_id: str, transaction_id: str) -> dict:
        """Queries a transaction for a specific account.

        ### Overview
        ----
        Serves as the mechanism to make a request to the "Get Transaction"
        Endpoint. The transaction ID will be queried for the specific account
        passed through.

        ### Documentation
        ----
        https://developer.tdameritrade.com/transaction-history/apis

        ### Parameters
        ----
        account_id: str
            The account number you want to query transactions
            for.

        transaction_id: str
            If set to `True` then account orders will be returned
            from the API. If set to `False` no orders will be
            returned.

        ### Usage
        ----
            >>> account_services = td_client.accounts()
            >>> account_services.get_transaction(
                account_id='123456789',
                transaction_id='123456789'
            )
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'accounts/{account_id}/transactions/{transaction_id}'
        )

        return content

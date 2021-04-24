from typing import List
from typing import Union
from td.session import TdAmeritradeSession
from enum import Enum


class Watchlists():

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `Watchlists` services.

        ### Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession   
            object.
        """

        self.session = session

    def get_all_accounts_watchlists(self) -> dict:
        """All watchlists for all of the user's linked accounts.

        ### Documentation
        ----
        https://developer.tdameritrade.com/watchlist/apis/get/accounts/watchlists-0

        ### Usage
        ----
            >>> watchlists_service = td_client.watchlists()
            >>> watchlists_service.get_all_accounts_watchlists()
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'accounts/watchlists'
        )

        return content

    def get_accounts_watchlist(self, account_id: str) -> dict:
        """Gets all the watchlists of an account.

        ### Documentation
        ----
        https://developer.tdameritrade.com/watchlist/apis/get/accounts/%7BaccountId%7D/watchlists-0

        ### Parameters
        ----
        account_id: str
            The account number the watchlist belongs to.

        ### Usage
        ----
            >>> watchlists_service = td_client.watchlists()
            >>> watchlists_service.get_accounts_watchlist(
                account_id='123456789'
            )
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'accounts/{account_id}/watchlists'
        )

        return content

    def get_watchlist(self, account_id: str, watchlist_id: str) -> dict:
        """Gets a specific watchlist for a specific account.

        ### Documentation
        ----
        https://developer.tdameritrade.com/watchlist/apis/get/accounts/%7BaccountId%7D/watchlists/%7BwatchlistId%7D-0

        ### Parameters
        ----
        account_id: str
            The account number the watchlist belongs to.

        watchlist_id: str
            The watchlist ID you want to query.

        ### Usage
        ----
            >>> watchlists_service = td_client.watchlists()
            >>> watchlists_service.get_watchlist(
                account_id='123456789',
                watchlist_id='1365748039'
            )
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'accounts/{account_id}/watchlists/{watchlist_id}'
        )

        return content

    def create_watchlist(self, account_id: str, name: str, watchlist_items: dict) -> dict:
        """Creates a new watchlist.

        ### Overview
        ----
        Create watchlist for specific account. This method does not verify
        that the symbol or asset type are valid.

        ### Documentation
        ----
        https://developer.tdameritrade.com/watchlist/apis/post/accounts/%7BaccountId%7D/watchlists-0

        ### Parameters
        ----        
        account_id: str
            The account number the watchlist belongs to.

        name: str
            The name you want to give your watchlist.

        watchlist_items: dict
            A list of items you want to add to your
            watchlist.

        ### Usage
        ----
            >>> watchlists_service = td_client.watchlists()
            >>> watchlists_service.create_watchlist(
                account_id='123456789',
                name='space companies',
                watchlist_items=[
                    {

                    }
                ]
            )
        """

        # define the payload
        payload = {
            "name": name,
            "watchlistItems": watchlist_items
        }

        content = self.session.make_request(
            method='post',
            endpoint=f'accounts/{account_id}/watchlists',
            json_payload=payload
        )

        return content

    def update_watchlist(self, account_id: str, watchlist_id: str, name: str = None, watchlist_items: dict = None) -> dict:
        """Updates an existing watchlist.

        ### Overview
        ----
        Partially update watchlist for a specific account: change watchlist name, add to the
        beginning/end of a watchlist, update or delete items in a watchlist. This method
        does not verify that the symbol or asset type are valid.

        ### Documentation
        ----
        https://developer.tdameritrade.com/watchlist/apis/patch/accounts/%7BaccountId%7D/watchlists/%7BwatchlistId%7D-0

        ### Parameters
        ----        
        account_id: str
            The account number the watchlist belongs to.

        watchlist_id: str
            The watchlist ID you want to query.

        name: str
            The name you want to give your watchlist.

        watchlist_items: dict
            A list of items you want to add to your
            watchlist.

        ### Usage
        ----
            >>> watchlists_service = td_client.watchlists()
            >>> watchlists_service.update_watchlist(
                account_id='123456789',
                watchlist_id='111111111',
                name='space companies',
                watchlist_items=[
                    {
                        'quantity': 0.0,
                        'averagePrice': 0.0,
                        'commission': 0.0,
                        'instrument': {
                            'symbol': 'UFO',
                            'assetType': 'EQUITY'
                        },
                        'sequenceId': 3
                    }
                ]
            )
        """

        # define the payload
        payload = {
            "name": name,
            "watchlistItems": watchlist_items
        }

        content = self.session.make_request(
            method='patch',
            endpoint=f'accounts/{account_id}/watchlists/{watchlist_id}',
            json_payload=payload
        )

        return content

    def replace_watchlist(self, account_id: str, watchlist_id: str, name: str, watchlist_items: dict) -> dict:
        """Replaces an existing watchlist.

        ### Overview
        ----
        This method does not verify that the symbol or asset type are valid. Additionally,
        this method from what I can see will only append on new values. It will not delete
        an old watchlist.

        ### Documentation
        ----
        https://developer.tdameritrade.com/watchlist/apis/patch/accounts/%7BaccountId%7D/watchlists/%7BwatchlistId%7D-0

        ### Parameters
        ----        
        account_id: str
            The account number the watchlist belongs to.

        watchlist_id: str
            The watchlist ID you want to query.

        name: str
            The name you want to give your watchlist.

        watchlist_items: dict
            A list of items you want to add to your
            watchlist.

        ### Usage
        ----
            >>> watchlists_service = td_client.watchlists()
            >>> watchlists_service.replace_watchlist(
                account_id='123456789',
                watchlist_id='111111111',
                name='space companies',
                watchlist_items=[
                    {
                        'quantity': 0.0,
                        'averagePrice': 0.0,
                        'commission': 0.0,
                        'instrument': {
                            'symbol': 'UFO',
                            'assetType': 'EQUITY'
                        },
                        'sequenceId': 3
                    }
                ]
            )
        """

        # define the payload
        payload = {
            "name": name,
            "watchlistItems": watchlist_items
        }

        content = self.session.make_request(
            method='put',
            endpoint=f'accounts/{account_id}/watchlists/{watchlist_id}',
            json_payload=payload
        )

        return content

    def delete_watchlist(self, account_id: str, watchlist_id: str) -> dict:
        """Deletes a watchlist for a specific account.

        ### Documentation
        ----
        https://developer.tdameritrade.com/watchlist/apis/delete/accounts/%7BaccountId%7D/watchlists/%7BwatchlistId%7D-0.

        ### Parameters
        ----
        account_id: str
            The account number the watchlist belongs to.

        watchlist_id: str
            The watchlist ID you want to query.

        ### Usage
        ----
            >>> watchlists_service = td_client.watchlists()
            >>> watchlists_service.delete_watchlist(
                account_id='123456789',
                watchlist_id='1365748039'
            )
        """

        content = self.session.make_request(
            method='delete',
            endpoint=f'accounts/{account_id}/watchlists/{watchlist_id}'
        )

        return content
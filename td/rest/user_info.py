from typing import List
from typing import Union
from td.session import TdAmeritradeSession
from td.utils.user_preferences import UserPreferences


class UserInfo():

    """
    ## Overview
    ----
    Allows the user to query information about their profile,
    modify settings that are related to the API and retrieve
    streaming keys that can be used with the Streaming API
    client.
    """

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initializes the `UserInfo` services.

        ### Parameters
        ----
        session : TdAmeritradeSession
            An authenticated `TDAmeritradeSession
            object.

        ### Usage
        ----
            >>> user_info_service = td_client.user_service()
        """

        self.session = session

    def get_preferences(self, account_id: str) -> dict:
        """Get's User Preferences for a specific account.

        ### Documentation
        ----
        https://developer.tdameritrade.com/user-principal/apis/get/accounts/%7BaccountId%7D/preferences-0

        ### Parameters
        ----
        account_id: str
            The User's TD Ameritrade account ID.

        ### Usage
        ----
            >>> user_info_service = td_client.user_service()
            >>> user_info_service.get_preferences(
                account_id='123456789'
            )
        """

        content = self.session.make_request(
            method='get',
            endpoint=f'accounts/{account_id}/preferences',
        )

        return content

    def get_streamer_subscription_keys(self, account_ids: List[str]) -> dict:
        """SubscriptionKey for provided accounts or default accounts.

        ### Documentation
        ----
        https://developer.tdameritrade.com/user-principal/apis/get/userprincipals/streamersubscriptionkeys-0

        ### Parameters
        ----
        account_ids: List[str]
            A list of account IDs.

        ### Usage
        ----
            >>> user_info_service = td_client.user_service()
            >>> user_info_service.get_streamer_subscription_keys(
                account_ids=['123456789']
            )
        """

        params = {
            'accountIds': ','.join(account_ids)
        }

        content = self.session.make_request(
            method='get',
            endpoint='userprincipals/streamersubscriptionkeys',
            params=params
        )

        return content

    def get_user_principals(self) -> dict:
        """Get's User principals details.

        ### Documentation
        ----
        https://developer.tdameritrade.com/user-principal/apis/get/userprincipals-0

        ### Usage
        ----
            >>> user_info_service = td_client.user_service()
            >>> user_info_service.get_user_principals()
        """

        params = {
            'fields': 'streamerSubscriptionKeys,streamerConnectionInfo,preferences,surrogateIds'
        }

        content = self.session.make_request(
            method='get',
            endpoint='userprincipals',
            params=params
        )

        return content

    def update_user_preferences(
        self,
        account_id: str,
        preferences: Union[dict, UserPreferences]
    ) -> dict:
        """Update preferences for a specific account.

        ### Documentation
        ----
        https://developer.tdameritrade.com/user-principal/apis/put/accounts/%7BaccountId%7D/preferences-0

        ### Parameters
        ----
        account_id: str
            The User's TD Ameritrade account ID.

        preferences: Union[dict, UserPreferences]
            The preferences you want changed, either as a python
            dict or a `UserPreferences` object.

        ### Usage
        ----
            >>> user_service = td_client.user_service()
            >>> user_info_service.update_user_preferences(
                preferences={
                    'authTokenTimeout': 'EIGHT_HOURS'
                }
            )
        """

        content = self.session.make_request(
            method='put',
            endpoint=f'accounts/{account_id}/preferences',
            json_payload=preferences
        )

        return content

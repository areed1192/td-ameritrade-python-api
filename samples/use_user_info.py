from pprint import pprint
from configparser import ConfigParser
from td.credentials import TdCredentials
from td.client import TdAmeritradeClient

# Initialize the Parser.
config = ConfigParser()

# Read the file.
config.read('config/config.ini')

# Get the specified credentials.
client_id = config.get('main', 'client_id')
redirect_uri = config.get('main', 'redirect_uri')
account_number = config.get('main', 'account_number')

# Intialize our `Crednetials` object.
td_credentials = TdCredentials(
    client_id=client_id,
    redirect_uri=redirect_uri,
    credential_file='config/td_credentials.json'
)

# Initalize the `TdAmeritradeClient`
td_client = TdAmeritradeClient(
    credentials=td_credentials
)

# Initialize the UserInfo service.
user_info_service = td_client.user_info()

# Grab the preferences for a specific account.
pprint(
    user_info_service.get_preferences(
        account_id=account_number
    )
)

# Grab the streamer subscription keys.
pprint(
    user_info_service.get_streamer_subscription_keys(
        account_ids=[account_number]
    )
)

# Grab User Principals.
pprint(
    user_info_service.get_user_principals()
)

# Update the User Preferences.
user_info_service.update_user_preferences(
    account_id=account_number,
    preferences={
        'authTokenTimeout': 'EIGHT_HOURS',
        'defaultAdvancedToolLaunch': 'NONE',
        'defaultEquityOrderDuration': 'DAY',
        'defaultEquityOrderLegInstruction': 'NONE',
        'defaultEquityOrderMarketSession': 'NORMAL',
        'defaultEquityOrderPriceLinkType': 'NONE',
        'defaultEquityOrderType': 'LIMIT',
        'defaultEquityQuantity': 0,
        'equityTaxLotMethod': 'FIFO',
        'expressTrading': True,
        'mutualFundTaxLotMethod': 'FIFO',
        'optionTaxLotMethod': 'FIFO'
    }
)

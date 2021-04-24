from pprint import pprint
from configparser import ConfigParser
from td.credentials import TdCredentials
from td.client import TdAmeritradeClient
from td.utils.enums import OptionaRange
from td.utils.enums import OptionType
from td.utils.enums import ContractType
from td.utils.enums import ExpirationMonth
from td.utils.utils import OptionChainQuery

# Initialize the Parser.
config = ConfigParser()

# Read the file.
config.read('config/config.ini')

# Get the specified credentials.
client_id = config.get('main', 'client_id')
redirect_uri = config.get('main', 'redirect_uri')

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

# Initialize the `OptionsChain` service.
options_chain_service = td_client.options_chain()

# Method 1: Build a Query using the `OptionChainQuery` object.
# This method is preferred because I'll check some of your inputs
# to make sure you are sending the correct parameters.
option_chain_query = OptionChainQuery(
    symbol='MSFT',
    contract_type=ContractType.Call,
    expiration_month=ExpirationMonth.June,
    option_type=OptionType.StandardContracts,
    option_range=OptionaRange.InTheMoney,
    include_quotes=True
)

# Query the Options Data.
options_data = options_chain_service.get_option_chain(
    option_chain_query=option_chain_query
)

pprint(options_data['numberOfContracts'])

# Method 2: Build a Query using a regular `Dictionary` object.
# I do not check any of the inputs on this one, that falls on
# you.
option_chain_dict = {
    'symbol': 'MSFT',
    'contractType': 'CALL',
    'expirationMonth': 'JUN',
    'optionType': 'SC',
    'range': 'ITM',
    'includeQuotes': True
}

# Query the Options Data.
options_data = options_chain_service.get_option_chain(
    option_chain_dict=option_chain_dict
)

pprint(options_data['numberOfContracts'])

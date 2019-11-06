#### Table of Contents

*   [Overview](#overview)
*   [What's in the API](#whats-in-the-api)
*   [Requirements](#requirements)
*   [API Key & Credentials](#api-key-and-credentials)
*   [Installation](#installation)
*   [Usage](#usage)
*   [Features](#features)
*   [Documentation & Resources](#documentation-and-resources)
*   [Support These Projects](#support-these-projects)

----------

## Overview
The unofficial Python API client library for TD Ameritrade allows individuals with TD Ameritrade accounts to manage trades, pull historical and real-time data, manage their accounts, create and modify orders all using the Python programming language.

To learn more about the TD Ameritrade API, please refer to the [official documentation](https://developer.tdameritrade.com/apis).

## What's in the API:

*   Authentication - access tokens, refresh tokens, request authentication.
*   Accounts & Trading
*   Market Hours
*   Instruments
*   Movers
*   Option Chains
*   Price History
*   Quotes
*   Transaction History
*   User Info & Preferences
*   Watchlist

## Requirements

The following requirements must be met to use this API:

*   A TD Ameritrade account, you'll need your account password and account number to use the API.
*   A TD Ameritrade Developer Account
*   A TD Ameritrade Developer API Key
*   A Consumer ID
*   A Redirect URI, sometimes called Redirect URL
*   Python 3.5 or later - VERIFY THIS.

## API Key and Credentials

Each TD Ameritrade API request requires a TD Ameritrade Developer API Key, a consumer ID, an account password, an account number, and a redirect URI. API Keys, consumer IDs, and redirect URIs are generated from the TD Ameritrade developer portal. To set up and create your TD Ameritrade developer account, please refer to the [official documentation](https://developer.tdameritrade.com/content/phase-1-authentication-update-xml-based-api).

Additionally, to authenticate yourself using this library, you will need to provide your account number and password for your main TD Ameritrade account.

**Important:** Your account number, an account password, consumer ID, and API key should be kept secret.

## Installation

PLACE HOLDER FOR PIP INSTALLATION

## Usage

This example demonstrates how to login to the API and demonstrates sending a request using the ``get_quotes`` endpoint, using your API key.

```python
# import the client
from td_api import TDClient

# create a new session
TDSession = TDClient(account_number = 'ACCOUNT_NUMBER',
                     account_password = 'ACCOUNT_PASSWORD',
                     consumer_id = 'CONSUMER_ID',
                     redirect_uri = 'REDIRECT_URI')

# login to the session
TDSession.login()

# grab real-time quotes for 'MSFT' (Microsoft)
msft_quotes = TDSession.get_quotes(instruments='MSFT')

# grab real-time quotes for 'AMZN' (Amazon) and 'SQ' (Square)
multiple_quotes = TDSession.get_quotes(instruments=['AMZN','SQ'])
```

## Features

### Authentication Workflow Support
Automatically will handle the authentication workflow for new users, returning users, and users with expired tokens (refresh token or access token).

### Request Validation
For certain requests, in a limited fashion, it will help validate your request when possible. For example, when using the ``get_movers`` endpoint, it will automatically validate that the market you're requesting data from is one of the valid options.

### Customized Objects for Watchlists, Orders, and Option Chains
Requests for saved orders, regular orders, watchlists, and option chains can be a challenging process that has multiple opportunities to make mistakes. This library has built-in objects that will allow you to quickly build your request and then validate certain portions of your request when possible.

## Documentation and Resources

### Official API Documentation
- [Getting Started](https://developer.tdameritrade.com/content/phase-1-authentication-update-xml-based-api)
- [Endpoints](https://developer.tdameritrade.com/apis)
- [Guides](https://developer.tdameritrade.com/guides)
- [Samples - Price History](https://developer.tdameritrade.com/content/price-history-samples)
- [Samples - Place Order](https://developer.tdameritrade.com/content/place-order-samples)

### Unofficial Documentation
- [TD Ameritrade API - YouTube](https://www.youtube.com/playlist?list=PLcFcktZ0wnNnKvxFkJ5B7pvGaGa81Ny-6)


## Support these Projects

**Patreon:**
Help support this project and future projects by donating to my [Patreon Page](https://www.patreon.com/sigmacoding). I'm always looking to add more content for individuals like yourself, unfortuantely some of the APIs I would require me to pay monthly fees.

**YouTube:**
If you'd like to watch more of my content, feel free to visit my YouTube channel [Sigma Coding](https://www.youtube.com/c/SigmaCoding).

**Hire Me:**
If you have a project, you think I can help you with feel free to reach out at coding.sigma@gmail.com

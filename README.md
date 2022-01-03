# UPDATE

This repo will soon be updated to include the new <https://github.com/areed1192/td-ameritrade-api>
library. The master branch will be overwritten and the old code will need to be updated
to reflect the new changes. If you would like to start rewriting your old code, please
refer to the new branch merge-new-repo or go the link above.

## Unofficial TD Ameritrade Python API Library

## Table of Contents

- [Overview](#overview)
- [What's in the API](#whats-in-the-api)
- [Requirements](#requirements)
- [API Key & Credentials](#api-key-and-credentials)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Documentation & Resources](#documentation-and-resources)
- [Support These Projects](#support-these-projects)
- [Authentication Workflow](#authentication-workflow)

## Overview

Current Version: **0.3.5**

The unofficial Python API client library for TD Ameritrade allows individuals with
TD Ameritrade accounts to manage trades, pull historical and real-time data, manage
their accounts, create and modify orders all using the Python programming language.

To learn more about the TD Ameritrade API, please refer to
the [official documentation](https://developer.tdameritrade.com/apis).

## What's in the API

- Authentication - access tokens, refresh tokens, request authentication.
- Accounts & Trading
- Market Hours
- Instruments
- Movers
- Option Chains
- Price History
- Quotes
- Transaction History
- User Info & Preferences
- Watchlist

## Requirements

The following requirements must be met to use this API:

- A TD Ameritrade account, you'll need your account password and account number to use the API.
- A TD Ameritrade Developer Account
- A TD Ameritrade Developer API Key
- A Consumer ID
- A Redirect URI, sometimes called Redirect URL
- Python 3.7 or later.

## API Key and Credentials

Each TD Ameritrade API request requires a TD Ameritrade Developer API Key, a consumer ID,
an account password, an account number, and a redirect URI. API Keys, consumer IDs, and
redirect URIs are generated from the TD Ameritrade developer portal. To set up and create
your TD Ameritrade developer account, please refer to
the [official documentation](https://developer.tdameritrade.com/content/phase-1-authentication-update-xml-based-api).

Additionally, to authenticate yourself using this library, you will need to provide your
account number and password for your main TD Ameritrade account.

**Important:** Your account number, an account password, consumer ID, and API key should
be kept secret.

## Installation

The project can be found at PyPI, if you'd like to view the project please use
this [link](https://pypi.org/project/td-ameritrade-python-api/).

```bash
pip install td-ameritrade-python-api
```

To upgrade the library run the following command:

```bash
pip install --upgrade td-ameritrade-python-api
```

## Usage

This example demonstrates how to login to the API and demonstrates sending a request
using the `get_quotes` endpoint, using your API key.

**Credentials:**
Please note, that the `credentials_path` is a file path that will house the credentials
like your refresh token and access token. You must specify the `credentials_path` argument
yourself so that you are aware of where the tokens will be stored. For example, if you
specify the `credentials_path` as `C:\Users\Public\Credentials\td_state.json` it would
store your tokens in a JSON file located in a folder called Credentials located under
the Users profile.

```python
# Import the client
from td.client import TDClient

# Create a new session, credentials path is required.
TDSession = TDClient(
    client_id='<CLIENT_ID>',
    redirect_uri='<REDIRECT_URI>',
    credentials_path='<PATH_TO_CREDENTIALS_FILE>'
)

# Login to the session
TDSession.login()

# Grab real-time quotes for 'MSFT' (Microsoft)
msft_quotes = TDSession.get_quotes(instruments=['MSFT'])

# Grab real-time quotes for 'AMZN' (Amazon) and 'SQ' (Square)
multiple_quotes = TDSession.get_quotes(instruments=['AMZN','SQ'])
```

## Features

### Authentication Workflow Support

Automatically will handle the authentication workflow for new users, returning users, and users
with expired tokens (refresh token or access token).

### Request Validation

For certain requests, in a limited fashion, it will help validate your request when possible.
For example, when using the `get_movers` endpoint, it will automatically validate that the
market you're requesting data from is one of the valid options.

### Customized Objects for Watchlists, Orders, and Option Chains

Requests for saved orders, regular orders, watchlists, and option chains can be a challenging
process that has multiple opportunities to make mistakes. This library has built-in objects
that will allow you to quickly build your request and then validate certain portions of your
request when possible.

### Library Requirements

The following requirements must be met before being able to use the TD Ameritrade Python API library.

- You must have a TD Ameritrade Account.
- You must have a TD Ameritrade Developer Account. Please go to following [folder](https://github.com/areed1192/td-ameritrade-python-api/tree/master/samples/resources)
  for instructions on how to create a Developer account.

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
Help support this project and future projects by donating to my [Patreon Page](https://www.patreon.com/sigmacoding).
I'm always looking to add more content for individuals like yourself, unfortuantely some of the APIs I would require
me to pay monthly fees.

**YouTube:**
If you'd like to watch more of my content, feel free to visit my YouTube channel [Sigma Coding](https://www.youtube.com/c/SigmaCoding).

**Hire Me:**
If you have a project, you think I can help you with feel free to reach out at [coding.sigma@gmail.com](mailto:coding.sigma@gmail.com?subject=[GitHub]%20Project%20Proposal) or fill out the [contract request form](https://forms.office.com/Pages/ResponsePage.aspx?id=ZwOBErInsUGliXx0Yo2VfcCSWZSwW25Es3vPV2veU0pUMUs5MUc2STkzSzVQMFNDVlI5NjJVNjREUi4u)

## Authentication Workflow

**Step 1 - Start the Script:**

While in Visual Studio Code, right click anywhere in the code editor while in the file that contains your code.
The following dropdown will appear:

![Terminal Dropdown](https://raw.githubusercontent.com/areed1192/td-ameritrade-python-api/master/samples/instructions/photos/terminal_dropdown.jpg "Terminal Dropdown")

From the dropdown, click `Run Python file in Terminal`, this will start the python script.

**Step 2 - Go to Redirect URL:**

The TD Library will automatically generate the redirect URL that will navigate you to the TD website for for
you authentication. You can either copy the link and paste it into a browser manually or if you're using Visual
Studio Code you can press `CTRL + Click` to have Visual Studio Code navigate you to the URL immeditately.

![Redirect URI](https://raw.githubusercontent.com/areed1192/td-ameritrade-python-api/master/samples/instructions/photos/redirect_uri.jpg "Redirect URI")

**Step 3 - Login to the TD API:**

Once you've arrived at the login screen, you'll need to provide your credentials to authenticate the session.
Please provide your Account Username and Account Password in the userform and then press enter. As a reminder
these, are the same username/password combination you use to login to your regular TD Account.

!["TD Login](https://raw.githubusercontent.com/areed1192/td-ameritrade-python-api/master/samples/instructions/photos/td_login.jpg "TD Login")

**Step 4 - Accept the Terms:**

Accept the Terms of the API by clicking `Allow`, this will redirect you.

![TD Terms](https://raw.githubusercontent.com/areed1192/td-ameritrade-python-api/master/samples/instructions/photos/td_terms.jpg "TD Terms")

**Step 5 - Copy the Authorization Code:**

After accepting the terms, you'll be taken to the URL that you provided as your `redirect URI`. However, at
the end of that URL will be `authorization code`. To complete the authentication workflow, copy the URL as
it appears below. Don't worry if the numbers don't match, as you will have a different code.

![Auth Code](https://raw.githubusercontent.com/areed1192/td-ameritrade-python-api/master/samples/instructions/photos/auth_code.jpg "Auth Code")

**Step 6 - Paste the Authorization Code in the Terminal:**

Take the URL and copy it into the Terminal, after you have pasted it, press `Enter`. The authentication workflow
will complete and the script will start running. At this stage, we are exchanging your authorization code for
an access token. That access token is valid only for 30 minutes. However, a refresh token is also stored that
will refresh your access token when it expires.

![Paste URL](https://raw.githubusercontent.com/areed1192/td-ameritrade-python-api/master/samples/instructions/photos/paste_url.jpg "Paste URL")

After, that the script should run. Additionally, if you go to the location you specified in the `credentials_path`
arugment you will now see `td_state.json` file. This file contains all the info used during a session. Please
DO NOT DELETE THIS FILE OR ELSE YOU WILL NEED TO GO THROUGH THE STEPS ABOVE.

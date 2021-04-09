# Unofficial TD Ameritrade Python API Library

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Support These Projects](#support-these-projects)

## Overview

Current Version: **0.1.0**

The unofficial Python API client library for TD Ameritrade allows individuals with
TD Ameritrade accounts to manage trades, pull historical and real-time data, manage
their accounts, create and modify orders all using the Python programming language.

To learn more about the TD Ameritrade API, please refer to
the [official documentation](https://developer.tdameritrade.com/apis).

## Setup

**Setup - Requirements Install:***

For this particular project, you only need to install the dependencies, to use the project. The dependencies
are listed in the `requirements.txt` file and can be installed by running the following command:

```console
pip install -r requirements.txt
```

After running that command, the dependencies should be installed.

**Setup - Local Install:**

If you are planning to make modifications to this project or you would like to access it
before it has been indexed on `PyPi`. I would recommend you either install this project
in `editable` mode or do a `local install`. For those of you, who want to make modifications
to this project. I would recommend you install the library in `editable` mode.

If you want to install the library in `editable` mode, make sure to run the `setup.py`
file, so you can install any dependencies you may need. To run the `setup.py` file,
run the following command in your terminal.

```console
pip install -e .
```

If you don't plan to make any modifications to the project but still want to use it across
your different projects, then do a local install.

```console
pip install .
```

This will install all the dependencies listed in the `setup.py` file. Once done
you can use the library wherever you want.

<!-- **Setup - PyPi Install:**

To **install** the library, run the following command from the terminal.

```console
pip install td-ameritrade-python
```

**Setup - PyPi Upgrade:**

To **upgrade** the library, run the following command from the terminal.

```console
pip install --upgrade td-ameritrade-python
``` -->

## Usage

Here is a simple example of using the `td` library.

```python
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

# Initialize the Quotes service.
quote_service = td_client.quotes()

# Grab a single quote.
pprint(
    quote_service.get_quote(instrument='AAPL')
)

# Grab multiple quotes.
pprint(
    quote_service.get_quotes(instruments=['AAPL', 'SQ'])
)
```

## Support These Projects

**Patreon:**
Help support this project and future projects by donating to my [Patreon Page](https://www.patreon.com/sigmacoding). I'm
always looking to add more content for individuals like yourself, unfortuantely some of the APIs I would require me to
pay monthly fees.

**YouTube:**
If you'd like to watch more of my content, feel free to visit my YouTube channel [Sigma Coding](https://www.youtube.com/c/SigmaCoding).

**Questions:**
If you have questions please feel free to reach out to me at [coding.sigma@gmail.com](mailto:coding.sigma@gmail.com?subject=[GitHub]%20Fred%20Library)

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

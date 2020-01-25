import asyncio
import datetime
import json
import pprint
import urllib
import dateutil.parser


from OldStreamer import TDStreamerClient
from td.client import TDClient
from td.config import (ACCOUNT_NUMBER, ACCOUNT_PASSWORD, CONSUMER_ID,
                       REDIRECT_URI, TD_ACCOUNT)


def unix_time_millis(dt):
    
    # grab the starting point, so time '0'
    epoch = datetime.datetime.utcfromtimestamp(0)
    
    return (dt - epoch).total_seconds() * 1000.0

# Create a new session
TDSession = TDClient(account_number = ACCOUNT_NUMBER,
                     account_password = ACCOUNT_PASSWORD,
                     consumer_id = CONSUMER_ID,
                     redirect_uri = REDIRECT_URI)

# Login to the session
TDSession.login()

# Grab the Subscription Key
sub_key = TDSession.get_streamer_subscription_keys()['keys'][0]['key']

# Grab the Streamer Info.
userPrincipalsResponse = TDSession.get_user_principals(fields = ['streamerConnectionInfo'])

# Parse the timestamp for the Login
tokenTimeStamp = userPrincipalsResponse['streamerInfo']['tokenTimestamp']
date = dateutil.parser.parse(tokenTimeStamp, ignoretz = True)
tokenTimeStampAsMs = unix_time_millis(date)

# Grab socket 
socket_url = userPrincipalsResponse['streamerInfo']['streamerSocketUrl'] 

# we need to define our credentials that we will need to make our stream
credentials = {"userid": userPrincipalsResponse['accounts'][0]['accountId'],
               "token": userPrincipalsResponse['streamerInfo']['token'],
               "company": userPrincipalsResponse['accounts'][0]['company'],
               "segment": userPrincipalsResponse['accounts'][0]['segment'],
               "cddomain": userPrincipalsResponse['accounts'][0]['accountCdDomainId'],
               "usergroup": userPrincipalsResponse['streamerInfo']['userGroup'],
               "accesslevel":userPrincipalsResponse['streamerInfo']['accessLevel'],
               "authorized": "Y",
               "timestamp": int(tokenTimeStampAsMs),
               "appid": userPrincipalsResponse['streamerInfo']['appId'],
               "acl": userPrincipalsResponse['streamerInfo']['acl'] }

# define a request
login_request = {"requests": [{"service": "ADMIN",
                              "requestid": "0",  
                              "command": "LOGIN",
                              "account": userPrincipalsResponse['accounts'][0]['accountId'],
                              "source": userPrincipalsResponse['streamerInfo']['appId'],
                              "parameters": {"credential": urllib.parse.urlencode(credentials),
                                             "token": userPrincipalsResponse['streamerInfo']['token'],
                                             "version": "1.0"}}]}


# define a request for different data sources
data_request= {"requests": [{"service": "ACTIVES_NASDAQ", 
                             "requestid": "1", 
                             "command": "SUBS", 
                             "account": userPrincipalsResponse['accounts'][0]['accountId'], 
                             "source": userPrincipalsResponse['streamerInfo']['appId'], 
                             "parameters": {"keys": "NASDAQ-60", 
                                            "fields": "0,1"}},
                            {"service": "LEVELONE_FUTURES",
                             "requestid": "2",
                             "command": "SUBS",
                             "account": userPrincipalsResponse['accounts'][0]['accountId'],
                             "source": userPrincipalsResponse['streamerInfo']['appId'],
                             "parameters": {"keys": "/ES,/NQ,/YM,/MME",
                                            "fields": "0,1,2,3,4"}},
                            # {"service":"QUOTE", 
                            #  "requestid":"3",
                            #  "command":"SUBS", 
                            #  "account":userPrincipalsResponse['accounts'][0]['accountId'],
                            #  "source": userPrincipalsResponse['streamerInfo']['appId'],
                            #  "parameters": {"keys":"AAPL,GOOG,TSLA,SQ,QCOM,FB",
                            #                 "fields":"1,2,3,4,5,8,9,10,11,19"}},
                            {"service":"QUOTE", 
                             "requestid":"6",
                             "command":"SUBS", 
                             "account":userPrincipalsResponse['accounts'][0]['accountId'],
                             "source": userPrincipalsResponse['streamerInfo']['appId'],
                             "parameters": {"keys":"AAPL,GOOG,TSLA,SQ,QCOM,FB",
                                            "fields":"0,6,7,12,13,14,16,17,18,20,21,22,23,24,25,26,27,28,29,1,2,3,4,5,8,9,10,11,19"}},
                            {"service":"NASDAQ_BOOK", 
                             "requestid":"4",
                             "command":"STREAM", 
                             "account":userPrincipalsResponse['accounts'][0]['accountId'],
                             "source":userPrincipalsResponse['streamerInfo']['appId']},
                            {"service": "NEWS_HEADLINE",
                             "requestid": "5",
                             "command": "SUBS",
                             "account":userPrincipalsResponse['accounts'][0]['accountId'],
                             "source":userPrincipalsResponse['streamerInfo']['appId'],
                             "parameters": {"keys": "GOOG",
                                            "fields": "0,1,2,3,4"}}]}

# create it into a JSON string, as the API expects a JSON string.
login_encoded = json.dumps(login_request)
data_encoded = json.dumps(data_request)

# Creating client object
client = TDStreamerClient(websocket_url = socket_url)

# Start a loop.
loop = asyncio.get_event_loop()

# Start connection and get client connection protocol
connection = loop.run_until_complete(client.connect())


# Start listener and heartbeat 
tasks = [asyncio.ensure_future(client.receiveMessage(connection)),
         asyncio.ensure_future(client.sendMessage(login_encoded)),
         asyncio.ensure_future(client.sendMessage(data_encoded))]

loop.run_until_complete(asyncio.wait(tasks))

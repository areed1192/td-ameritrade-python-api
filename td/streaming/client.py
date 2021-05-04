import json
import urllib
import pprint
import asyncio
import textwrap
import websockets

from datetime import datetime
from td.rest.user_info import UserInfo
from td.session import TdAmeritradeSession
from td.streaming.services import StreamingServices


class StreamingApiClient():

    """
    Implements a Websocket object that connects to the TD 
    Streaming API, submits requests, handles messages, and
    streams data back to the user.
    """

    def __init__(self, session: TdAmeritradeSession) -> None:
        """Initalizes the Streaming Client.

        ### Overview
        ----
        Initalizes the Client Object and defines different components that will be needed to
        make a connection with the TD Streaming API.

        ### Usage
        ----
            >>> td_streaming_client = td_client.streaming_api()
        """
        self.user_principal_data = UserInfo(
            session=session
        ).get_user_principals()
        self.websocket_url = f"wss://{self.user_principal_data['streamerInfo']['streamerSocketUrl']}/ws"

        # Grab the token timestamp.
        token_timestamp = self.user_principal_data['streamerInfo']['tokenTimestamp']
        token_timestamp = datetime.strptime(
            token_timestamp, "%Y-%m-%dT%H:%M:%S%z"
        )
        token_timestamp = int(token_timestamp.timestamp()) * 1000

        # Define our Credentials Dictionary used for authentication.
        self.credentials = {
            "userid": self.user_principal_data['accounts'][0]['accountId'],
            "token": self.user_principal_data['streamerInfo']['token'],
            "company": self.user_principal_data['accounts'][0]['company'],
            "segment": self.user_principal_data['accounts'][0]['segment'],
            "cddomain": self.user_principal_data['accounts'][0]['accountCdDomainId'],
            "usergroup": self.user_principal_data['streamerInfo']['userGroup'],
            "accesslevel": self.user_principal_data['streamerInfo']['accessLevel'],
            "authorized": "Y",
            "timestamp": token_timestamp,
            "appid": self.user_principal_data['streamerInfo']['appId'],
            "acl": self.user_principal_data['streamerInfo']['acl']
        }

        self.connection: websockets.WebSocketClientProtocol = None
        self.data_requests = {
            "requests": []
        }

        try:
            self.loop = asyncio.get_event_loop()
        except websockets.WebSocketException:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

        self.unsubscribe_count = 0

    def _build_login_request(self) -> str:
        """Builds the Login request for the streamer.

        ### Overview
        ----
        Builds the login request dictionary that will 
        be used as the first service request with the 
        streaming API.

        ### Returns
        ----
        str:
            A JSON string with the login details.
        """

        login_request = {
            "requests": [
                {
                    "service": "ADMIN",
                    "requestid": "0",
                    "command": "LOGIN",
                    "account": self.user_principal_data['accounts'][0]['accountId'],
                    "source": self.user_principal_data['streamerInfo']['appId'],
                    "parameters": {
                        "credential": urllib.parse.urlencode(self.credentials),
                        "token": self.user_principal_data['streamerInfo']['token'],
                        "version": "1.0"
                    }
                }
            ]
        }

        return json.dumps(login_request)

    async def _connect(self) -> websockets.WebSocketClientProtocol:
        """Connects the Client to the TD Websocket.

        ### Overview
        ----
        Connecting to webSocket server websockets.client.connect 
        returns a WebSocketClientProtocol, which is used to send 
        and receive messages

        ### Returns
        ---
        websockets.WebSocketClientProtocol:
            The websocket connection.
        """

        # Grab the login info.
        login_request = self._build_login_request()

        # Create a connection.
        self.connection = await websockets.client.connect(self.websocket_url)

        # See if we are connected.
        is_connected = await self._check_connection()

        # If we are connected then login.
        if is_connected:
            await self._send_message(login_request)

            while True:

                # Grab the Response.
                response = await self._receive_message(return_value=True)
                responses = response.get('response')

                # If we get a code 3, we had a login error.
                if responses[0]['content']['code'] == 3:
                    raise ValueError(
                        f"LOGIN ERROR: {responses[0]['content']['msg']}"
                    )

                # see if we had a login response.
                for r in responses:
                    if r.get('service') == 'ADMIN' and r.get('command') == 'LOGIN':
                        print(
                            "Message: User Login successful, streaming will being shortly."
                        )
                        return self.connection

    async def _check_connection(self) -> bool:
        """Determines if we have an active connection

        ### Overview
        ----
        There are multiple times we will need to check the connection 
        of the websocket, this function will help do that.

        ### Raises
        ----
        ConnectionError:
            An error is raised if we can't connect to the
            websocket.

        ### Returns
        ----
        bool:
            `True` if the connection healthy, `False` otherwise.
        """

        # if it's open we can stream.
        if self.connection.open:
            print("="*80)
            print('Message: Connection established. Streaming will begin shortly.')
            print("-"*80)
            return True
        elif self.connection.close:
            print("="*80)
            print('Message: Connection was never opened and was closed.')
            print("-"*80)
            return False
        else:
            raise ConnectionError

    async def _send_message(self, message: str) -> None:
        """Sends a message to webSocket server

        ### Parameters
        ----
        message: str
            The JSON string with the data streaming
            service subscription.
        """

        await self.connection.send(message)

    async def _receive_message(self, return_value: bool = False) -> dict:
        """Recieves and processes the messages as needed.

        ### Parameters
        ----
        return_value: bool (optional, Default=False)
            Specifies whether the messages should be returned
            back to the calling function or not.

        ### Returns
        ----
        dict:
            The streaming message.
        """

        # Keep going until cancelled.
        while True:

            try:

                message = await self.connection.recv()
                message_decoded = await self._parse_json_message(message=message)
                print(message_decoded)

                if return_value:
                    return message_decoded

                print(textwrap.dedent('='*80))
                print(textwrap.dedent("Message Received:"))
                print(textwrap.dedent('-'*80))
                pprint.pprint(message_decoded)
                print(textwrap.dedent('-'*80))

            except websockets.exceptions.ConnectionClosed:
                await self.close_stream()
                break

    async def _parse_json_message(self, message: str) -> dict:
        """Parses incoming messages from the stream

        ### Parameters
        ----
        message: str
            A JSON string needing to be parsed.

        ### Returns
        ----
        dict:
            The parsed message content.
        """

        try:
            message_decoded = json.loads(message)
        except:
            message = message.encode(
                'utf-8'
            ).replace(b'\xef\xbf\xbd', bytes('"None"', 'utf-8')).decode('utf-8')
            message_decoded = json.loads(message)

        return message_decoded

    async def heartbeat(self) -> None:
        """Sending heartbeat to server every 5 seconds."""

        while True:
            try:
                await self.connection.send('ping')
                await asyncio.sleep(5)
            except websockets.exceptions.ConnectionClosed:
                self.close_stream()
                break

    def services(self) -> StreamingServices:
        """Returns the streaming services that can be added
        before the stream runs.

        ### Returns
        ----
        StreamingServices
            The `StreamingServices` offered by the API.

        ### Usage
        ----
            >>> streaming_api_service = td_client.streaming_api_client()
            >>> streaming_services = streaming_api_service.services()
        """

        return StreamingServices(streaming_api_client=self)

    def open_stream(self) -> None:
        """Starts the stream and prints the output to the console.

        ### Overview
        ----
        Initalizes the stream by building a login request, starting 
        an event loop, creating a connection, passing through the 
        requests, and keeping the loop running.
        """

        # Connect to the Websocket.
        self.loop.run_until_complete(self._connect())

        # Send the data requests, and start getting messages.
        data_requests = json.dumps(self.data_requests)
        asyncio.ensure_future(self._send_message(data_requests))
        asyncio.ensure_future(self._receive_message(return_value=False))
        self.loop.run_forever()

    async def close_stream(self) -> None:
        """Closes the connection to the streaming service."""

        # close the connection.
        await self.connection.close()

        # Define the Message.
        message = textwrap.dedent("""
        {lin_brk}
        CLOSING PROCESS INITIATED:
        {lin_brk}
        WebSocket Closed: True
        Event Loop Closed: True
        {lin_brk}
        """).format(lin_brk="="*80)

        # Shutdown all asynchronus generators.
        await self.loop.shutdown_asyncgens()

        # Stop the loop.
        if self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop())
            print(message)
            await asyncio.sleep(3)

    async def build_pipeline(self) -> websockets.WebSocketClientProtocol:
        """Builds a data pipeine for processing data.

        ### Overview
        ----
        Often we want to take the data we are streaming and
        use it in other functions or store it in other platforms.
        This method makes the process of building a pipeline easy
        by handling all the connection setup and request setup.

        ### Returns
        ----
        websockets.WebSocketClientProtocol
            The websocket connection.
        """

        # In this case, we don't want things printing to the console.
        self.print_to_console = True

        # Connect to Websocket.
        await self._connect()

        # Build the Data Request.
        await self._send_message(json.dumps(self.data_requests))

        return self.connection

    async def start_pipeline(self) -> dict:
        """Recieves the data as it streams in.

        ### Returns
        ----
        dict
            The data coming from the websocket.
        """

        return await self._receive_message(return_value=True)

    async def unsubscribe(self, service: str) -> dict:
        """Unsubscribe from a service.

        ### Parameters
        ----
        service: str
            The name of the service, to unsubscribe from.
            For example, "LEVELONE_FUTURES" or "QUOTES".

        ### Returns
        ----
        dict:
            A message from the websocket specifiying whether
            the unsubscribe command was successful.
        """

        self.unsubscribe_count += 1

        service_count = len(
            self.data_requests['requests']
        ) + self.unsubscribe_count

        request = {
            "requests": [
                {
                    "service": service.upper(),
                    "requestid": service_count,
                    "command": 'UNSUBS',
                    "account": self.user_principal_data['accounts'][0]['accountId'],
                    "source": self.user_principal_data['streamerInfo']['appId']
                }
            ]
        }

        await self._send_message(json.dumps(request))

        return await self._receive_message(return_value=True)

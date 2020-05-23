import json

from datetime import datetime
from typing import Union
from typing import List


class StreamingMessage():

    """
        Represents a `Stream` message that can then be
        parsed. The `StreamingMessage` objects makes working
        with the messages easier and more standard.
    """

    def __init__(self, message: str) -> None:
        """Initalizes the `StreamingMessage` object.

        During the initalization process, the raw message
        will be decoded and parsed.

        Arguments:
        ----
        message {str} -- The raw text message from a stream.
        """

        self.raw_message = message
        self.decoded_message = self.parse(message=self.raw_message)

    def parse(self, message: str) -> dict:
        """Parses the Raw JSON string and converts it to a Dictionary.

        Parse will also do some very basic text normalization for messy
        characters.

        Arguments:
        ----
        message {str} -- The raw text coming from the message.

        Returns:
        ----
        dict -- A Message dictionary.
        """

        message = message.encode(
            'utf-8').replace(
                b'\xef\xbf\xbd',
                bytes('"None"', 'utf-8')
            ).decode('utf-8')
        message = json.loads(message)

        return message

    def set_components(self) -> List[dict]:
        """Converts each response to a StreamingMessageComponent Object.

        Returns:
        ----
        List[dict] -- A list of `StreamingMessageComponents`.
        """

        self.components = []

        if self.is_data_response:

            # Loop through the data responses.
            for component in self.decoded_message['data']:
                
                new_component = StreamingMessageComponent(
                    message_component=component, 
                    response_type='data'
                )

                self.components.append(new_component)

        elif self.is_subscription_response:

            # Loop through each Subscription response.
            for component in self.decoded_message['response']:
                
                new_component = StreamingMessageComponent(
                    message_component=component,
                    response_type='subscription'
                )
                
                self.components.append(new_component)

    @property
    def components_count(self) -> int:
        """Returns the Count of the components.

        Returns:
        ----
        int -- The number of items in the components collection.
        """

        if self.components:
            return len(self.components)
        else:
            return 0

    @property
    def is_data_response(self) -> bool:
        """Specifies whether the message is a data response.

        Returns:
        ----
        bool -- `True` if the message is a data message.
        """

        if 'data' in self.decoded_message:
            return True
        else:
            return False

    @property
    def is_subscription_response(self) -> bool:
        """Specifies whether the message is a subscription response.

        Returns:
        ----
        bool -- `True` if the message is a subscription message.
        """

        if 'response' in self.decoded_message:
            return True
        else:
            return False


class StreamingMessageComponent():

    """
    Represents a single component in the content
    section of a stream message. A stream message
    can contain multiple responses, a component is
    a single response.
    """

    def __init__(self, message_component: dict, response_type: str) -> None:
        """Initalizes the `StreamingMessageComponent`.

        Arguments:
        ----
        message_component {dict} -- The service that belongs to a message
            response.

        response_type {str} -- A type of response the component comes from.
        """
        self.component = message_component
        self.component_type = response_type

    @property
    def service(self) -> str:
        """Returns Service name of the component."""

        return self.component['service']

    @property
    def time_recieved(self, as_datetime: bool = False) -> Union[datetime, int]:
        """Returns the time the component was recieved.

        Keyword Arguments:
        ----
        as_datetime {bool} -- `True` if you want the timestamp converted to a
            python `datetime` object, `False` if you want a timestamp. (default: {False})

        Returns:
        ----
        Union[datetime, int] -- Either a timestamp or a `datetime` object.
        """

        if as_datetime:
            return datetime.fromtimestamp(t=self.component['timestamp'])
        else:
            return self.component['timestamp']

    @property
    def command(self) -> str:
        """Returns the Component Command."""

        return self.component['command']

    @property
    def content(self) -> Union[dict, List]:
        """Returns the Component Content."""

        return self.component['content']

    @property
    def content_count(self) -> int:
        """Returns the number of content dicitonaries in a component."""

        if self.component_type == 'data':
            return len(self.content)
        else:
            return 1

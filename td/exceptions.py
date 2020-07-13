class TknExpError(Exception):
    """Raise exception when refresh or access token is expired.

    Args:
        Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Args:
            message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)

class ExdLmtError(Exception):
    """Raise exception when exceeding query limit of the server.

    Args:
        Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Args:
            message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)

class NotNulError(Exception):
    """Raise exception when a null value is passed into non-null field.

    Args:
        Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Args:
            message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)

class ForbidError(Exception):
    """Raise forbidden exception. This usually occurs when the app does
    not have access to the account.

    Args:
        Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Args:
            message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)

class NotFndError(Exception):
    """Raise exception when criteria is not found.

    Args:
        Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Args:
            message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)

class ServerError(Exception):
    """Raise exception when there is an error with the service or the server
    cannot provide response.

    Args:
        Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Args:
            message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)

class GeneralError(Exception):
    """Raise exception for all other status code >400 errors which are not
    defined above.

    Args:
        Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Args:
            message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)
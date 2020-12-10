class TknExpError(Exception):
    """Raise exception when refresh or access token is expired.

    ### Arguments:
    ----
    Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Arguments:
        ----
        message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)

class ExdLmtError(Exception):
    """Raise exception when exceeding query limit of the server.

    ### Arguments:
    ----
    Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Arguments:
        ----
        message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)

class NotNulError(Exception):
    """Raise exception when a null value is passed into non-null field.

    ### Arguments:
    ----
    Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Arguments:
        ----
        message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)

class ForbidError(Exception):
    """Raise forbidden exception. This usually occurs when the app does
    not have access to the account.

    ### Arguments:
    ----
    Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Arguments:
        ----
        message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)

class NotFndError(Exception):
    """Raise exception when criteria is not found.

    ### Arguments:
    ----
    Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Arguments:
        ----
        message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)

class ServerError(Exception):
    """Raise exception when there is an error with the service or the server
    cannot provide response.

    ### Arguments:
    ----
    Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Arguments:
        ----
        message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)

class GeneralError(Exception):
    """Raise exception for all other status code >400 errors which are not
    defined above.

    ### Arguments:
    ----
    Exception (Exception): The base python exception class
    """
    def __init__(self, message):
        """Print out message for this exception.

        Arguments:
        ----
        message (str): Pass in the message returned by the server.
        """
        self.message = message
        super().__init__(self.message)
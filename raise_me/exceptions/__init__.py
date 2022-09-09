"""Module of exceptions that raise-me may raise."""


class InvalidEvent(SyntaxError):
    """Exception when an event from 'raise-events.yaml' is malformed."""
    pass


class UnrecognizedTargetType(Exception):
    """Exception when EventTarget type is not valid."""
    pass


class UnrecognizedHttpMethod(Exception):
    """Exception when http method is not valid."""
    pass
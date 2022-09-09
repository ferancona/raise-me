"""Module of exceptions that raise-me may raise."""


class InvalidEvent(SyntaxError):
    """Exception when an event from 'raise-events.yaml' is malformed."""
    pass


class UnrecognizedTargetType(Exception):
    """Exceptioni when EventTarget type is unrecognized."""
    pass
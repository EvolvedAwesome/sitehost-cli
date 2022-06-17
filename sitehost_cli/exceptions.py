class API_Exception(Exception):
    """Generic API exception. Can be used to describe any general API
    errors or inherited to describe specific API error cases.
    """
    pass

class NotEnoughArgumentsException(API_Exception):
    """Child class for API commands."""
    pass

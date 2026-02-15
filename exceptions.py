class InvalidBotTokenError(Exception):
    """Raised when missing or invalid Bot Token"""
    pass

class UnpinError(Exception):
    """Raised when unpinning fails"""
    pass

class PinError(Exception):
    """Raised when pinning fails"""
    pass

class BotMessageDeleteError(Exception):
    """Raised when deleting fails"""
    pass
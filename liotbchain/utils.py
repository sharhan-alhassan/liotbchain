# utils.py

import logging
import logging.config
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': 'liotbchain.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': LOG_LEVEL,
            'propagate': True
        }
    }
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)


class Error(Exception):
    """Base class for other exceptions"""
    pass

class InvalidBlockError(Error):
    """Raised when a block's integrity is compromised."""
    pass

class InvalidChainError(Error):
    """Raised when the blockchain is not consistent or has invalid blocks."""
    pass

class BlockchainOperationError(Error):
    """Raised when a blockchain operation fails."""
    pass

class MiningFailedError(Error):
    """Raised when mining a new block fails."""
    pass

class DatabaseConnectionError(Error):
    """Raised when there is an issue connecting to the database."""
    pass

class DatabaseConfigurationError(Error):
    """Raised when the database configuration is incorrect or missing."""
    pass
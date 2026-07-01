"""
Application logging configuration.
"""

import logging # Instead of using print(), professional applications use the logging module.


def setup_logger() -> logging.Logger: # for return type logging.This function returns a Logger object.
    """
    Configure application logger.

    Returns:
        Configured logger instance.
    """

    logging.basicConfig( # Set global logging settings for the entire application
        level=logging.INFO,# show info and higher stuff
        format=("%(asctime)s " "%(levelname)s " "%(name)s " "%(message)s"),# "Whenever a log is printed, display these pieces of information in this order." date,logger level,loggername then the message
    )

    return logging.getLogger("adaptive_rag")


logger = setup_logger() # runs immediately when Python imports logger.py for the first time.

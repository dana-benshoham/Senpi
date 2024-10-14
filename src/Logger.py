import logging
import logging.handlers

def get_logger():
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler that logs messages to a file
    file_handler = logging.handlers.TimedRotatingFileHandler(
        'app.log', when='midnight', interval=1, backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler that logs messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create a formatter that includes the date, time, module name, and log level
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
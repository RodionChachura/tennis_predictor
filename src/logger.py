import os
import logging
import logging.handlers


def setup_logger():
    logger = logging.getLogger(__name__.split('.')[0])
    logger.setLevel(logging.DEBUG)

    fh = logging.handlers.RotatingFileHandler(os.path.join(os.getcwd(), 'ronni.log'), maxBytes=1024, backupCount=1)
    fh_formatter = logging.Formatter('%(asctime)-15s %(levelname)s %(message)s')
    fh.setFormatter(fh_formatter)

    logger.addHandler(fh)
import logging

from rich.logging import RichHandler

logger = logging.getLogger(__name__)


def init_logging(info: bool = True, debug: bool = False) -> None:
    if debug:
        logging.basicConfig(level=logging.DEBUG, handlers=[RichHandler()])
    elif info:
        logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])
    else:
        logging.basicConfig(level=logging.WARNING, handlers=[RichHandler()])

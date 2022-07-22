import re
import os
import logging
from urllib.parse import urlparse
logger = logging.getLogger(__name__)


def changes_the_name(addres, suffix='.html'):
    """Generates the changed address of the resource."""
    path_parse = urlparse(addres)
    path = os.path.splitext(path_parse.netloc + path_parse.path)[0]
    result = re.sub(r'\W', '-', path) + suffix
    logger.debug(f'Convert the path {addres} to a name {result}')
    return result

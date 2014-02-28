import logging
import requests

from information_value.models import Document
from information_value.models import odm_session

log = logging.getLogger('lenin')


def wget(url):
    log.info('Trying to fetch url: %s' % url)
    response = requests.get(url)
    Document(
                url=url,
                name=url,
                text=response.text,
    )
    odm_session.flush()

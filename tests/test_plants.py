import pytest
from flask import g, session

import logging
logging.basicConfig(level=logging.DEBUG)

from botanic_website.views.plants import *


# def test_plants_index(client):
#     response= client.get('/')
#     log = logging.getLogger('test_plants_index')
#     assert response.data is not None
#     log.debug('\n-----------testing index---------')
#
#
# def test_plants_single(client):
#     response = client.get('/plants/single')
#     assert response is not None

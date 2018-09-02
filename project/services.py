# standard library imports...
from urllib.parse import urljoin

# third-party imports...
import requests

#  local imports
from project.constants import BASE_URL

USERS_URL = urljoin(BASE_URL, 'users')


def get_users():
    response = requests.get(USERS_URL)
    if response.ok:
        return send_response
    else:
        return None

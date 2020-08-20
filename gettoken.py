from urllib.parse import urlencode

def get_token(id):
    OAUTH_URL = 'https://oauth.vk.com/authorize'
    OAUTH_PARAMS = {
    'client_id': id,
    'scope': 'friends',
    'display': 'page',
    'response_type': 'token',
    'v': 5.89
        }

    return ('?'.join((OAUTH_URL, urlencode(OAUTH_PARAMS))))

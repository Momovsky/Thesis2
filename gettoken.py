from urllib.parse import urlencode

OAUTH_URL = 'https://oauth.vk.com/authorize'
OAUTH_PARAMS = {
    'client_id': 7489754,
    'scope': 'friends',
    'display': 'page',
    'response_type': 'token',
    'v': 5.89
}

print('?'.join(
    (OAUTH_URL, urlencode(OAUTH_PARAMS))
))
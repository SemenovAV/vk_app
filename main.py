import requests
from urllib.parse import urlencode

APP_ID = '7302199'
TOKEN = ''
API_URL = 'https://api.vk.com/method/'
AUTH_URL = 'https://oauth.vk.com/authorize'
VERSION = 5.52
params = {
    'client_id': APP_ID,
    'display': 'page',
    'scope': 'friends',
    'response_type': 'token',
    'v': VERSION,
}

def get_token():
    print('Ссылка для получения access_token:')
    print('?'.join((AUTH_URL, urlencode(params))))
    return input('TOKEN:')


def get_user(user_id=None, screen_name=None):
    params = {
        'access_token': TOKEN,
        'v': VERSION,
    }
    if user_id:
        params['user_ids'] = str(user_id)
    elif screen_name:
        params['screen_name'] = screen_name
    response = requests.get(
        f'{API_URL}users.get',
        params=params
    )
    data = response.json().get('response', False)
    if data:
        return data[0]
    else:
        return False


class User:

    def __init__(self, user_id=None, screen_name=None):
        self.id = user_id or get_user(user_id or screen_name)['id']
        self.link = f'https://vk.com/id{self.id}'

    def __and__(self, other):
        params = {
            'access_token': TOKEN,
            'v': 5.52,
            'source_uid': self.id,
            'target_uid': other.id
        }
        response = requests.get(
            f'{API_URL}friends.getMutual',
            params=params
        )
        data = response.json().get('response', False)
        if data:
            return [User(user_id=friend) for friend in data]
        else:
            return False

    def __str__(self):
        return self.link


if __name__ == '__main__':
    if not TOKEN:
        TOKEN = get_token()
    i = User()
    friend = User(screen_name='glebse')
    mutual = i & friend
    print(i)
    print(friend)
    print(mutual)

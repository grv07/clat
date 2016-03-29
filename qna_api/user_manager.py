import requests

# ORIGIN_URL = 'http://52.77.85.150/api/'
ORIGIN_URL = 'http://localhost:8000/'

def register_user(username, email, test_key = 'c3vsg3jcp7'):
    url = 'user/data/'
    r = requests.post(ORIGIN_URL+url, data = {'username': username, 'email': email, 'test_key':test_key})
    return r.text

    
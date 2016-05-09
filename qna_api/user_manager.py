import requests
from CLAT.settings import QNA_PATH

#ORIGIN_URL = 'http://localhost:8000/'

def register_user(username, email, test_key = 'c3vsg3jcp7'):
    url = 'user/data/'
    r = requests.post(QNA_PATH+url, data = {'username': username, 'email': email, 'test_key':test_key})
    return r.text

    

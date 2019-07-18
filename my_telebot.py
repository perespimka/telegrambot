import requests
from time import sleep
from kittens import get_random_cat
from my_token import token


prox = {'https' :  '195.122.185.95:3128',
        'SOCKS5' : '139.59.169.246:1080'
 }

class Bot():

    def __init__(self, token):
        self.token = token
        self.url = 'https://api.telegram.org/bot%s/' % self.token

    def last_update(self, offset=None, timeout=2):
        params = {'offset' : offset, 'timeout' : timeout } 
        r = requests.get(self.url + 'getUpdates', params=params, proxies=prox)
        update = r.json()['result']
        if len(update) > 0:
            return update[-1]
        else:
            return None

    
    def send_message(self, chat_id, text):
        params = {'chat_id' : chat_id, 'text' : text}
        meth = 'sendMessage'
        answ = requests.get(self.url + meth, params=params, proxies=prox)
        return answ

    
x = Bot(token)   

offset = None

while True:
    try:
        req = x.last_update(offset)
        if req:
            if req['message']['text'].lower() == 'привет':
                x.send_message(req['message']['chat']['id'], 'Дратути!')
            if req['message']['text'].lower() == 'кисик':
                x.send_message(req['message']['chat']['id'], get_random_cat())
            '''
            else:
                x.send_message(req['message']['chat']['id'], 'Нипанятна')
            '''
            offset = req['update_id'] + 1
            

    except requests.exceptions.ProxyError:
        print('Ошибка Прокси')              
    except requests.exceptions.ConnectionError:
        print('Ошибка соединения')
    sleep(2)

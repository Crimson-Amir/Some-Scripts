import requests
from private import PORT, auth, telegram_bot_token, ADMIN_CHAT_ID, DOMAIN

telegram_bot_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"


class XuiApiClean:
    def __init__(self):
        self.connect = requests.Session()
        get_cookies = ""

        if get_cookies == "":
            self.login = self.connect.post(f'https://{DOMAIN}:{PORT}/login', data=auth)
            get_cookies = self.login.cookies.get('session')
            self.headers = {'Cookie': f'session={get_cookies}'}
            print(self.login.json())

    @staticmethod
    def send_telegram_message(message):
        requests.post(
            telegram_bot_url,
            data={'chat_id': ADMIN_CHAT_ID, "text": message})

    def check_request(self, request):
        if request.status_code == 200:
            print('connect Successful!')
            return True
        else:
            text = f'connection problem! code: {request.status_code} | url: {request.url}'
            print(text)
            self.send_telegram_message(text)
            return False

    def check_json(self, request):
        try:
            test_ = request.json()
            print('connect Successful!')
            return test_
        except Exception as e:
            text = f'connection problem! code: {request.status_code} | url: {request.url}'
            print(text, e)
            self.send_telegram_message(text)
            return False

    def get_all_inbounds(self):
        get_inbounds = self.connect.get(f'https://{DOMAIN}:{PORT}/panel/api/inbounds/list')
        if self.check_request(get_inbounds):
            return get_inbounds

    def get_inbound(self, inbound_id):
        get_inbound = self.connect.get(f'https://{DOMAIN}:{PORT}/panel/api/inbounds/get/{inbound_id}')
        if self.check_request(get_inbound):
            return get_inbound

    def get_client(self, client_email):
        get_client_ = self.connect.get(f'https://{DOMAIN}:{PORT}/panel/api/inbounds/getClientTraffics/{client_email}')
        if self.check_request(get_client_):
            return get_client_

    def add_inbound(self, data):
        add_inb = self.connect.post(f'https://{DOMAIN}:{PORT}/panel/api/inbounds/add', json=data)
        if self.check_json(add_inb):
            return add_inb.json()

    def add_client(self, data):
        ad_client = self.connect.post(f'https://{DOMAIN}:{PORT}/panel/api/inbounds/addClient', json=data)
        if self.check_json(ad_client):
            return ad_client.json()

    def update_inbound(self, inbound_id, data):
        inb = self.connect.post(f'https://{DOMAIN}:{PORT}/panel/api/inbounds/update/{inbound_id}', json=data)
        if self.check_json(inb):
            return inb.json()

    def update_client(self, uuid, data):
        inb = self.connect.post(f'https://{DOMAIN}:{PORT}/panel/api/inbounds/updateClient/{uuid}', json=data)
        if self.check_json(inb):
            return inb.json()

    def del_inbound(self, inbound_id):
        inb = self.connect.post(f'https://{DOMAIN}:{PORT}/panel/api/inbounds/del/{inbound_id}')
        if self.check_json(inb):
            return inb.json()

    def del_client(self, uuid):
        inb = self.connect.post(f'https://{DOMAIN}:{PORT}/panel/api/inbounds/delClient/{uuid}')
        if self.check_json(inb):
            return inb.json()

    def del_depleted_clients(self, inbound_id=""):
        inb = self.connect.post(f'https://{DOMAIN}:{PORT}/panel/api/inbounds/delDepletedClients/{inbound_id}')
        if self.check_json(inb):
            return inb.json()

    def create_backup(self):
        inb = self.connect.post(f'https://{DOMAIN}:{PORT}/panel/api/inbounds/createbackup')
        if self.check_json(inb):
            return inb.json()

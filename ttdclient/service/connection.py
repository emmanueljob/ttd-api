import requests
import json


class Connection:

    authorization_tokens = {}

    def __init__(self, username=None, password=None, url=None):
        self.password = password
        self.username = username
        self.url = url

    def connect(self):
        headers = []
        headers.push(self.get_authorization())

    def get_authorization(self):
        if self.authorization_tokens is None or self.username not in self.authorization_tokens:
            self.authorization_tokens[self.username] = self.authorize()

        return {'TTD-Auth': self.authorization_tokens[self.username]}

    def authorize(self):
        auth_url = "{0}/authentication".format(self.url)
        credentials = {
            "Login": self.username,
            "Password": self.password
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(auth_url, headers=headers, data=json.dumps(credentials), verify=False)

        if response is not None:
            obj = json.loads(response.text)
            if 'Token' in obj:
                self.authorization_tokens[self.username] = obj.get('Token')
            else:
                raise Exception('unable to authenticate: ' + response.text)

        return self.authorization_tokens[self.username]

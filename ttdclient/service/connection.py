import requests
import json


class Connection:

    authorization_token = None

    def __init__(self, username=None, password=None, url=None):
        Connection.password = password
        Connection.username = username
        Connection.url = url

    def connect(self):
        headers = []
        headers.push(Connection.get_authorization())

    def get_authorization(self):
        if Connection.authorization_token is None:
            Connection.authorization_token = self.authorize()

        return {'TTD-Auth': Connection.authorization_token}

    def authorize(self):
        auth_url = "{0}/authentication".format(Connection.url)
        credentials = {
            "Login": Connection.username,
            "Password": Connection.password
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(auth_url, headers=headers, data=json.dumps(credentials))

        if response is not None:
            obj = json.loads(response.text)
            if 'Token' in obj:
                Connection.authorization_token = obj.get('Token')
            else:
                raise Exception('unable to authenticate: ' + response.text)

        return Connection.authorization_token

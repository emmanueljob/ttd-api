import logging
import json
import requests
import datetime


class Base(dict):

    connection = None

    # Needs to be defined in the subclass
    obj_name = None

    def __init__(self, connection=None, data=None):
        self.data = data
        self.logger = logging.getLogger("ttd-api")
        Base.connection = connection
        super(Base, self).__init__()

    def get_url(self):
        return "{0}/{1}".format(Base.connection.url, self.obj_name)

    def get_create_url(self):
        return self.get_url()

    def get_find_url(self, id):
        return "{0}/{1}".format(self.get_url(), id)

    def find(self, id=None):
        if id is None:
            response = self._execute("GET", self.get_url(), None)

            rval = []
            if response:
                rval = self._get_response_objects(response)
            return rval
        else:
            response = self._execute("GET", self.get_find_url(id), None)
            return self._get_response_object(response)

    def create(self):
        response = self._execute("POST", self.get_create_url(), json.dumps(self.export_props()))
        obj = self._get_response_object(response)
        return obj

    def getId(self):
        return self.get('id')

    def save(self, payload):
        response = self._execute("PUT", self.get_url(), json.dumps(payload))
        obj = self._get_response_object(response)
        return obj

    def _execute(self, method, url, payload):
        return self._execute_no_reauth(method, url, payload)

    def _execute_no_reauth(self, method, url, payload):
        headers = Base.connection.get_authorization()

        headers['Content-Type'] = 'application/json'

        start_time = datetime.datetime.now()
        self.curl_command = ""
        rval = None
        if method == "GET":
            self.curl_command = "curl -H 'Content-Type: application/json' -H 'TTD-Auth: {0}' '{2}'".format(headers['TTD-Auth'], payload, url)
            rval = requests.get(url, headers=headers, data=payload, verify=False)
        elif method == "POST":
            self.curl_command = "curl -XPOST -H 'Content-Type: application/json' -H 'TTD-Auth: {0}' -d '{1}' '{2}'".format(headers['TTD-Auth'], payload, url)
            rval = requests.post(url, headers=headers, data=payload, verify=False)
        elif method == "PUT":
            self.curl_command = "curl -XPUT -H 'Content-Type: application/json' -H 'TTD-Auth: {0}' -d '{1}' '{2}'".format(headers['TTD-Auth'], payload, url)
            rval = requests.put(url, headers=headers, data=payload, verify=False)
        elif method == "DELETE":
            self.curl_command = "curl -XDELETE -H 'Content-Type: application/json' -H 'TTD-Auth: {0}' '{2}'".format(headers['TTD-Auth'], payload, url)
            rval = requests.delete(url, headers=headers, verify=False)
        else:
            raise Exception("Unknown method")
        
        end_time = datetime.datetime.now()
        total_time = end_time - start_time
        self.logger.debug("{0}, \"{1}\"".format(str(total_time), self.curl_command.replace('"', '""')))
        return rval

    def _get_response_objects(self, response):
        rval = {}
        rval["response_code"] = response.status_code
        obj = json.loads(response.text)
        if response.status_code == 200:
            data = []
            results = obj.get('Result')
            for result in results:
                data.append(result)

            rval["msg_type"] = "success"
            rval["msg"] = ""
            rval["data"] = obj
            rval["request_body"] = ""
        else:
            rval["msg_type"] = "error"
            rval["msg"] = obj.get("Message")
            rval["data"] = obj.get("ErrorDetails")
            rval["request_body"] = self.curl_command

        return json.dumps(rval)

    def _get_response_object(self, response):
        rval = {}
        rval["response_code"] = response.status_code
        obj = json.loads(response.text)
        if response.status_code == 200:
            rval["msg_type"] = "success"
            rval["msg"] = ""
            rval["data"] = obj
            rval["request_body"] = ""
        else:
            rval["msg_type"] = "error"
            rval["msg"] = obj.get("Message")
            rval["data"] = obj.get("ErrorDetails")
            rval["request_body"] = self.curl_command

        return json.dumps(rval)

    def import_props(self, props):
        for key, value in props.iteritems():
            self[key] = value

    def export_props(self):
        rval = {}
        # do this an obvious way because using __dict__ gives us params we dont need.
        for key, value in self.iteritems():
            rval[key] = value

        return rval

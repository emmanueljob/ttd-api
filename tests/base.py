import unittest

from ttdclient.conf.properties import Properties
from ttdclient.service.connection import Connection


class Base(unittest.TestCase):

    conn = None

    def __init__(self, *args, **kwargs):

        props = Properties("test")
        self.username = props.username
        self.password = props.password
        self.url = props.url
        Base.conn = Connection(username=self.username,
                               password=self.password,
                               url=self.url)

        super(Base, self).__init__(*args, **kwargs)

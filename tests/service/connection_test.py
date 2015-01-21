import unittest

from ttdclient.conf.properties import Properties
from ttdclient.service.connection import Connection
from tests.base import Base


class ConnectionTest(Base):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetProps(self):
        assert self.username == "ttd_test_api@accuen.com"

    def testConnection(self):
        token = ConnectionTest.conn.authorize()
        assert token is not None

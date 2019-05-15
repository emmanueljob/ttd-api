import unittest
import json

from ttdclient.models.advertiser import Advertiser
from tests.base import Base


class AdvertiserTest(Base):

    def testGetByPartner(self):
        adv = Advertiser(AdvertiserTest.conn)
        self.partner_id = 'acjf93j'
        advs = adv.find_by_partner(self.partner_id)
        advs = json.loads(advs).get("data").get("Result")
        for result in advs:
            assert result.get('AdvertiserId') is not None

    def testGetByName(self):
        adv = Advertiser(AdvertiserTest.conn)
        advs = adv.find_by_name(self.partner_id, 'Test SMP Api')
        advs = json.loads(advs).get("data").get("Result")
        for result in advs:
            assert result.get('AdvertiserName') == 'Test SMP Api'

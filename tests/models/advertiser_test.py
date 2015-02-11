import unittest
import json

from ttdclient.models.advertiser import Advertiser
from tests.base import Base


class AdvertiserTest(Base):

    def testCreate(self):
        adv = Advertiser(AdvertiserTest.conn)
        adv['AdvertiserName'] = 'test'
        adv['AttributionClickLookbackWindowInSeconds'] = 3600
        adv['AttributionImpressionLookbackWindowInSeconds'] = 3600
        adv['ClickDedupWindowInSeconds'] = 7
        adv['ConversionDedupWindowInSeconds'] = 60
        adv['DefaultRightMediaOfferTypeId'] = 1  # Adult
        adv['IndustryCategoryId'] = 54  # Entertainment
        adv['PartnerId'] = '73qiy5s'
        adv.create()

        assert adv.get('AdvertiserId') is not None

        loader = Advertiser(AdvertiserTest.conn)
        adv = loader.find(adv.get('AdvertiserId'))
        assert adv.get('AdvertiserName') == 'test'

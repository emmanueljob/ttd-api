import unittest
import json

from ttdclient.models.advertiser import Advertiser
from ttdclient.models.site_list import SiteList
from tests.base import Base


class SiteListTest(Base):

    def testCreate(self):

        # Create an advertiser first.
        adv = Advertiser(SiteListTest.conn)
        adv['AdvertiserName'] = 'site list adv test'
        adv['AttributionClickLookbackWindowInSeconds'] = 3600
        adv['AttributionImpressionLookbackWindowInSeconds'] = 3600
        adv['ClickDedupWindowInSeconds'] = 7
        adv['ConversionDedupWindowInSeconds'] = 60
        adv['DefaultRightMediaOfferTypeId'] = 1  # Adult
        adv['IndustryCategoryId'] = 54  # Entertainment
        adv['PartnerId'] = '73qiy5s'
        adv.create()

        # Create an advertiser first.
        site_list = SiteList(SiteListTest.conn)
        site_list['SiteListName'] = 'testing site list'
        site_list['AdvertiserId'] = adv.get('AdvertiserId')
        site_list['SiteListLines'] = [{'Domain': 'eman.com', 'adjustment': 1.0}, {'Domain': 'espn.com', 'adjustment': 1.0}]
        site_list.create()

        assert site_list.get('SiteListId') is not None

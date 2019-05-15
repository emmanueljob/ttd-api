import unittest
import json
import time

from ttdclient.models.ad_group import AdGroup
from ttdclient.models.advertiser import Advertiser
from ttdclient.models.campaign import Campaign
from ttdclient.models.contract import Contract
from ttdclient.models.site_list import SiteList
from tests.base import Base


class AdGroupTest(Base):


    def testGetAdGroup(self):
        loader = AdGroup(AdGroupTest.conn)
        ad_group = loader.find('gzv3s54')
        ad_group = json.loads(ad_group).get('data')
        assert ad_group.get('AdGroupId') is not None

    def testGetByCampaign(self):
        loader = AdGroup(AdGroupTest.conn)
        ad_groups = loader.get_by_campaign(self.campaign_id)
        ad_groups = json.loads(ad_groups).get("data").get("Result")
        for test_group in ad_groups:
            assert test_group.get('AdGroupId') is not None

        ad_group_name = 'Test SMP API Ad Group'
        ad_groups = loader.get_by_name(self.campaign_id, ad_group_name)
        ad_groups = json.loads(ad_groups).get("data").get("Result")
        for test_group in ad_groups:
            assert test_group.get('AdGroupName') == 'Test SMP API Ad Group'

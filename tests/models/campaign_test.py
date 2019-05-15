import unittest
import json

from ttdclient.models.campaign import Campaign
from ttdclient.models.advertiser import Advertiser
from tests.base import Base


class CampaignTest(Base):
        
        
    def testGetByAdvertiser(self):
        campaign = Campaign(CampaignTest.conn)
        campaigns = campaign.get_by_advertiser(self.adv_id)
        campaigns = json.loads(campaigns).get("data").get("Result")
        for test_campaign in campaigns:
            assert test_campaign.get('CampaignId') is not None

        campaign_name = 'Test SMP Api Campaign'
        campaigns = campaign.get_by_name(test_campaign.get('AdvertiserId'), campaign_name)
        campaigns = json.loads(campaigns).get("data").get("Result")
        for test_campaign in campaigns:
            assert test_campaign.get('CampaignName') == campaign_name

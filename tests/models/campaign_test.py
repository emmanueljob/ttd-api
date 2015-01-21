import unittest
import json

from ttdclient.models.campaign import Campaign
from ttdclient.models.advertiser import Advertiser
from tests.base import Base


class CampaignTest(Base):

    def testCreate(self):

        adv = Advertiser(CampaignTest.conn)
        adv['AdvertiserName'] = 'test'
        adv['AttributionClickLookbackWindowInSeconds'] = 3600
        adv['AttributionImpressionLookbackWindowInSeconds'] = 3600
        adv['ClickDedupWindowInSeconds'] = 7
        adv['ConversionDedupWindowInSeconds'] = 60
        adv['DefaultRightMediaOfferTypeId'] = 1  # Adult
        adv['IndustryCategoryId'] = 54  # Entertainment
        adv['PartnerId'] = '73qiy5s'
        adv.create()

        campaign = Campaign(CampaignTest.conn)
        campaign['AdvertiserId'] = adv.get('AdvertiserId')
        campaign['CampaignName'] = "test campaign"
        campaign['Budget'] = {'Amount': '10000.00', 'CurrencyCode': 'USD'}
        campaign['StartDate'] = '2015-02-01'
        campaign['CampaignConversionReportingColumns'] = []
        result = campaign.create()

        assert campaign.get('CampaignId') is not None

    def testGet(self):
        loader = Campaign(CampaignTest.conn)
        campaign = loader.find('j4ou3aws')
        print campaign
        assert campaign.get('CampaignName') == 'test'

import unittest
import json

from ttdclient.models.ad_group import AdGroup
from ttdclient.models.advertiser import Advertiser
from ttdclient.models.campaign import Campaign
from tests.base import Base


class AdGroupTest(Base):

    def testCreate(self):
        return 
        # Create an advertiser first.
        adv = Advertiser(AdGroupTest.conn)
        adv['AdvertiserName'] = 'ad group adv test eman'
        adv['AttributionClickLookbackWindowInSeconds'] = 3600
        adv['AttributionImpressionLookbackWindowInSeconds'] = 3600
        adv['ClickDedupWindowInSeconds'] = 7
        adv['ConversionDedupWindowInSeconds'] = 60
        adv['DefaultRightMediaOfferTypeId'] = 1  # Adult
        adv['IndustryCategoryId'] = 54  # Entertainment
        adv['PartnerId'] = '73qiy5s'
        adv.create()

        # Create a campaign first.
        campaign = Campaign(AdGroupTest.conn)
        campaign['AdvertiserId'] = adv.get('AdvertiserId')
        campaign['CampaignName'] = "test campaign for ad group"
        campaign['Budget'] = {'Amount': '10000.00', 'CurrencyCode': 'USD'}
        campaign['StartDate'] = '2015-02-01'
        campaign['CampaignConversionReportingColumns'] = []
        result = campaign.create()

        ad_group = AdGroup(AdGroupTest.conn)
        ad_group['CampaignId'] = campaign.get('CampaignId')
        ad_group['AdGroupName'] = 'ad group test'
        ad_group['IndustryCategoryId'] = 54
        ad_group['ContractAdjustments'] = { 'Id': 'ppik844', 'Adjustment': 1.0 }
        attributes = {
            'BudgetSettings': {
                'Budget': {'Amount': 1000.00, 'CurrencyCode': 'USD'},
                'DailyBudget': {'Amount': 100.00, 'CurrencyCode': 'USD'},
                'PacingEnabled': True
                },
            'BaseBidCPM': {'Amount': 1.00, 'CurrencyCode': 'USD'},
            'MaxBidCPM': {'Amount': 2.00, 'CurrencyCode': 'USD'}
        }

        ad_group['RTBAttributes'] = attributes
        ad_group.create()

        assert ad_group.get('AdGroupId') is not None

    def testGetByCampaign(self):
        # Create an advertiser first.
        adv = Advertiser(AdGroupTest.conn)
        adv['AdvertiserName'] = 'ad group adv test'
        adv['AttributionClickLookbackWindowInSeconds'] = 3600
        adv['AttributionImpressionLookbackWindowInSeconds'] = 3600
        adv['ClickDedupWindowInSeconds'] = 7
        adv['ConversionDedupWindowInSeconds'] = 60
        adv['DefaultRightMediaOfferTypeId'] = 1  # Adult
        adv['IndustryCategoryId'] = 54  # Entertainment
        adv['PartnerId'] = '73qiy5s'
        adv.create()
        
        # Create a campaign first.
        campaign = Campaign(AdGroupTest.conn)
        campaign['AdvertiserId'] = adv.get('AdvertiserId')
        campaign['CampaignName'] = "test campaign for ad group"
        campaign['Budget'] = {'Amount': '10000.00', 'CurrencyCode': 'USD'}
        campaign['StartDate'] = '2015-02-01'
        campaign['CampaignConversionReportingColumns'] = []
        result = campaign.create()

        ad_group = AdGroup(AdGroupTest.conn)
        ad_group['CampaignId'] = campaign.get('CampaignId')
        ad_group['AdGroupName'] = 'ad group test'
        ad_group['IndustryCategoryId'] = 54
        attributes = {
            'BudgetSettings': {
                'Budget': {'Amount': 1000.00, 'CurrencyCode': 'USD'},
                'DailyBudget': {'Amount': 100.00, 'CurrencyCode': 'USD'},
                'PacingEnabled': True
                },
            'BaseBidCPM': {'Amount': 1.00, 'CurrencyCode': 'USD'},
            'MaxBidCPM': {'Amount': 2.00, 'CurrencyCode': 'USD'},
            'ContractAdjustments': { 'Id': 'ppik844', 'Adjustment': 1.0 }
        }
        
        ad_group['RTBAttributes'] = attributes
        ad_group.create()

        ad_groups = ad_group.get_by_campaign(campaign.get('CampaignId'))
        for test_group in ad_groups:
            print test_group
            assert test_group.get('id') == ad_group.get('id')
            # assert test_group.get('RTBAttributes', {}).get('ContractAdustments', {}).get('Adjustment', 0) == 1.0


        ad_groups = ad_group.get_by_name(campaign.get('CampaignId'), 'ad group test')
        for test_group in ad_groups:
            assert test_group.get('AdGroupName') == 'ad group test'

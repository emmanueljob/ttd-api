import unittest
import json
import time

from ttdclient.models.ad_group import AdGroup
from ttdclient.models.advertiser import Advertiser
from ttdclient.models.campaign import Campaign
from ttdclient.models.contract import Contract
from tests.base import Base


class AdGroupTest(Base):


    def testCreate(self):
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

        # Create an advertiser first.
        contract = Contract(AdGroupTest.conn)
        contract['Name'] = 'Contract Test'
        contract['OwnerPartnerId'] = '73qiy5s'
        contract["StartDateUtc"] = "2015-04-30T21:21:19.7668268"
        
        code = int(time.time())
        
        deals = [{
                "SupplyVendorId": 7, # AppNexus
                "SupplyVendorDealId": str(code), # AppNexus
                "FloorPriceCPM": {
                    "CurrencyCode": "USD",
                    "Amount": 1.0
                    }
                }]
        contract['Deals'] = deals
    
        contract.create()

        ad_group = AdGroup(AdGroupTest.conn)
        ad_group['CampaignId'] = campaign.get('CampaignId')
        ad_group['AdGroupName'] = 'ad group test'
        ad_group['IndustryCategoryId'] = 54
        ad_group
        attributes = {
            'BudgetSettings': {
                'Budget': {'Amount': 1000.00, 'CurrencyCode': 'USD'},
                'DailyBudget': {'Amount': 100.00, 'CurrencyCode': 'USD'},
                'PacingEnabled': True
                },
            'BaseBidCPM': {'Amount': 1.00, 'CurrencyCode': 'USD'},
            'MaxBidCPM': {'Amount': 2.00, 'CurrencyCode': 'USD'},
        }

        ad_group['RTBAttributes'] = attributes
        ad_group.set_deals([contract.get('ContractId')])
        
        ad_group.create()

        assert ad_group.get('AdGroupId') is not None

        loader = AdGroup(AdGroupTest.conn)
        reloaded = loader.find(ad_group.get('AdGroupId'))
        assert ad_group.get('AdGroupId') == reloaded.get('AdGroupId')

        # test save
        reloaded.save()

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

        # Create an advertiser first.
        contract = Contract(AdGroupTest.conn)
        contract['Name'] = 'Contract Test'
        contract['OwnerPartnerId'] = '73qiy5s'
        contract["StartDateUtc"] = "2015-04-30T21:21:19.7668268"
        
        code = int(time.time())
        
        deals = [{
                "SupplyVendorId": 7, # AppNexus
                "SupplyVendorDealId": str(code), # AppNexus
                "FloorPriceCPM": {
                    "CurrencyCode": "USD",
                    "Amount": 1.0
                    }
                }]
        contract['Deals'] = deals
    
        contract.create()

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
            'ContractTargeting': { 
                'InventoryTargetingType': 'BothMarkets',
                'ContractIds': [contract.get('ContractId')] 
                }
        }
        
        ad_group['RTBAttributes'] = attributes
        ad_group.set_domains(["espn.com", "cnn.com"])
        ad_group.create()

        ad_groups = ad_group.get_by_campaign(campaign.get('CampaignId'))
        for test_group in ad_groups:
            assert test_group.get('id') == ad_group.get('id')


        ad_groups = ad_group.get_by_name(campaign.get('CampaignId'), 'ad group test')
        for test_group in ad_groups:
            assert test_group.get('AdGroupName') == 'ad group test'


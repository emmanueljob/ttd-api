import json

from ttdclient.models.base import Base
from ttdclient.models.site_list import SiteList
from ttdclient.models.campaign import Campaign

class AdGroup(Base):

    obj_name = "adgroup"

    def getId(self):
        return self.get("AdGroupId")

    def get_by_campaign(self, campaign_id):
        payload = { "CampaignId": campaign_id,
                    "PageStartIndex": 0,
                    "PageSize": None }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/campaign')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)


    def get_by_name(self, campaign_id, name):
        payload = { "CampaignId": campaign_id,
                    "SearchTerms": [name],
                    "PageStartIndex": 0,
                    "PageSize": None }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/campaign')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)

    def set_deals(self, deal_ids):

        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}
            
        self['RTBAttributes']['ContractTargeting'] = { 
            'InventoryTargetingType': 'BothMarkets',
            'ContractIds': deal_ids
            }

    def set_exchanges(self, exchange_ids, override=True):

        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}
            
        self['RTBAttributes']['SupplyVendorAdjustments'] = { 
            'InventoryTargetingType': 'BothMarkets',
            'DefaultAdjustment': 1.0
            }
        
        if override:
            self['RTBAttributes']['SupplyVendorAdjustments']['Adjustments'] = []

        for id in exchange_ids:
            self['RTBAttributes']['SupplyVendorAdjustments']['Adjustments'].append({'Id': id, 'Adjustment': 1.0})


    def set_domains(self, domains):

        # get the campaign so we can get the advertiserId
        loader = Campaign(Base.connection)
        campaign = loader.find(self['CampaignId'])
        
        # get the sitelist
        loader = SiteList(Base.connection)
        sitelist = loader.find_by_name(campaign['AdvertiserId'], self['AdGroupName'])
        if sitelist == None:
            sitelist = SiteList(Base.connection)
            sitelist['SiteListName'] = self['AdGroupName']
            sitelist['AdvertiserId'] = campaign['AdvertiserId']

        sitelist.set_domains(domains)
        if sitelist.getId() == 0 or sitelist.getId() is None:
            sitelist.create()
        else:
            sitelist.save()

        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}
            
        self['RTBAttributes']['SiteTargeting'] = { 
            'SiteListIds': [sitelist.getId()],
            'SiteListFallThroughAdjustment': 0
            }

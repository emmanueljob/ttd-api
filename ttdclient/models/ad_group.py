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
            'AllowOpenMarketBiddingWhenTargetingContracts': True,
            'ContractIds': deal_ids
            }

    def target_exchanges(self, target=True):

        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}
            
        if 'ContractTargeting' not in self['RTBAttributes']:
            return None

        if 'ContractIds' not in self['RTBAttributes']['ContractTargeting']:
            return None

        self['RTBAttributes']['ContractTargeting']['AllowOpenMarketBiddingWhenTargetingContracts'] = target

    def get_deals(self):

        if 'RTBAttributes' not in self:
            return None
            
        if 'ContractTargeting' not in self['RTBAttributes']:
            return None

        if 'ContractIds' not in self['RTBAttributes']['ContractTargeting']:
            return None

        return self['RTBAttributes']['ContractTargeting']['ContractIds']

    def get_creatives(self):

        if 'RTBAttributes' not in self:
            return None
            
        return self['RTBAttributes'].get('CreativeIds', None)


    def set_exchanges(self, exchange_ids, override=True):

        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}
            
        self['RTBAttributes']['SupplyVendorAdjustments'] = { 
            'DefaultAdjustment': 0
            }
        
        if override or 'Adjustments' not in self['RTBAttributes']['SupplyVendorAdjustments']:
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

        # sitelist.getId() always exists so set as default list
        if 'SiteTargeting' in self['RTBAttributes']:
            # If Ad Group as a current list, use it and append the new ID.
            if 'SiteListIds' in self['RTBAttributes']['SiteTargeting']:
                currentList = self['RTBAttributes']['SiteTargeting']['SiteListIds']

                # Weird error if duplicate IDs exist
                """
                Exception: Bad response code {"Message":"The request failed validation. Please check your request and try again.","ErrorDetails":[{"Property":"AdGroup.RTBAttributes.SiteTargeting.SiteListIds","Reasons":["The following Site Lists cannot be used for this operation because they are not accessible to Advertiser '9ut3ufp': ."]}]}
                """
                if sitelist.getId() not in currentList:
                    currentList.append(sitelist.getId())
        else:
            currentList = [sitelist.getId()]

        if domain == None and sitelist.getId() in currentList:
            currentList.remove(sitelist.getId())

        self['RTBAttributes']['SiteTargeting'] = { 
            'SiteListIds': currentList,
            'SiteListFallThroughAdjustment': 0
            }

    def set_budget(self, budget):
        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}
            
        if 'BudgetSettings' not in self['RTBAttributes']:
            self['RTBAttributes']['BudgetSettings'] = {}

        if 'Budget' not in self['RTBAttributes']['BudgetSettings']:
            self['RTBAttributes']['BudgetSettings']['Budget'] = {'CurrencyCode': 'USD'}
        
        self['RTBAttributes']['BudgetSettings']['Budget']['Amount'] = budget
        

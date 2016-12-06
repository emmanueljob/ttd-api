import json

from ttdclient.models.base import Base
from ttdclient.models.site_list import SiteList
from ttdclient.models.campaign import Campaign

class AdGroup(Base):

    obj_name = "adgroup"
    updates = {}


    def save(self):
        if self.getId() is None or self.getId() == 0:
            raise Exception("cant update an object with no id")

        # only push changes
        response = self._execute("PUT", self.get_url(), json.dumps(self.updates))
        obj = self._get_response_object(response)
        self.import_props(obj)

        # once updates reset changes to empty
        self.updates = {}

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

    def set_deals(self, deal_ids=None, deal_group_ids=None):

        if 'RTBAttributes' not in self:
            self.updates['RTBAttributes'] = {}

        if deal_ids is None:
            deal_ids = []

        if deal_group_ids is None:
            deal_group_ids = []
            
        self.updates['RTBAttributes']['ContractTargeting'] = { 
            'AllowOpenMarketBiddingWhenTargetingContracts': True,
            'ContractIds': deal_ids,
            'ContractGroupIds': deal_group_ids
            }

    """
    def set_deal_groups(self, deal_group_ids):

        if 'RTBAttributes' not in self.updates:
            self.updates['RTBAttributes'] = {}
            
        self.updates['RTBAttributes']['ContractTargeting'] = { 
            'AllowOpenMarketBiddingWhenTargetingContracts': True,
            'ContractGroupIds': deal_group_ids
            }
    """

    def target_exchanges(self, target=True):

        if 'RTBAttributes' not in self.updates:
            self.updates['RTBAttributes'] = {}
            
        if 'ContractTargeting' not in self.updates['RTBAttributes']:
            self.updates['RTBAttributes']['ContractTargeting'] = {}

        if 'ContractIds' not in self.updates['RTBAttributes']['ContractTargeting']:
            self.updates['RTBAttributes']['ContractTargeting']['ContractIds']

        self.updates['RTBAttributes']['ContractTargeting']['AllowOpenMarketBiddingWhenTargetingContracts'] = target

    def get_deals(self):
        if self._get_deals(self.update):
           return self._get_deals(self.update)
        return self._get_deals(self)

    def _get_deals(dict_to_check):

        if 'RTBAttributes' not in dict_to_check:
            return None
            
        if 'ContractTargeting' not in dict_to_check['RTBAttributes']:
            return None

        if 'ContractIds' not in dict_to_check['RTBAttributes']['ContractTargeting']:
            return None

        return dict_to_check['RTBAttributes']['ContractTargeting']['ContractIds']

    def get_deal_groups(self):
        if self._get_deal_groups(self.update):
           return self._get_deal_groups(self.update)
        return self._get_deal_groups(self)

    def _get_deal_groups(self):

        if 'RTBAttributes' not in dict_to_check:
            return None
            
        if 'ContractTargeting' not in dict_to_check['RTBAttributes']:
            return None

        if 'ContractIds' not in dict_to_check['RTBAttributes']['ContractTargeting']:
            return None

        return dict_to_check['RTBAttributes']['ContractTargeting']['ContractGroupIds']

    def get_creatives(self):
        if self._get_creatives(self.update):
           return self._get_creatives(self.update)
        return self._get_creatives(self)

    def _get_creatives(self):

        if 'RTBAttributes' not in dict_to_check:
            return None
            
        return dict_to_check['RTBAttributes'].get('CreativeIds', None)

    def set_exchanges(self, exchange_ids, override=True):

        if 'RTBAttributes' not in self.updates:
            self.updates['RTBAttributes'] = {}
            
        self.updates['RTBAttributes']['SupplyVendorAdjustments'] = { 
            'DefaultAdjustment': 0.0
            }
        
        if override or 'Adjustments' not in self.updates['RTBAttributes']['SupplyVendorAdjustments']:
            self.updates['RTBAttributes']['SupplyVendorAdjustments']['Adjustments'] = []

        for id in exchange_ids:
            self.updates['RTBAttributes']['SupplyVendorAdjustments']['Adjustments'].append({'Id': id, 'Adjustment': 1.0})


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

        if 'RTBAttributes' not in self.updates:
            self.updates['RTBAttributes'] = {}

        # sitelist.getId() always exists so set as default list
        if 'SiteTargeting' in self.updates['RTBAttributes']:
            # If Ad Group as a current list, use it and append the new ID.
            if 'SiteListIds' in self.updates['RTBAttributes']['SiteTargeting']:
                currentList = self.updates['RTBAttributes']['SiteTargeting']['SiteListIds']

                # Weird error if duplicate IDs exist
                """
                Exception: Bad response code {"Message":"The request failed validation. Please check your request and try again.","ErrorDetails":[{"Property":"AdGroup.RTBAttributes.SiteTargeting.SiteListIds","Reasons":["The following Site Lists cannot be used for this operation because they are not accessible to Advertiser '9ut3ufp': ."]}]}
                """
                if sitelist.getId() not in currentList:
                    currentList.append(sitelist.getId())
        else:
            currentList = [sitelist.getId()]

        if len(domains) == 0 and sitelist.getId() in currentList:
            currentList.remove(sitelist.getId())

        if len(currentList) == 0:
            self.updates['RTBAttributes']['SiteTargeting'] = {
                'SiteListIds': [],
                'SiteListFallThroughAdjustment': 1
                }
        else:
            self.updates['RTBAttributes']['SiteTargeting'] = {
                'SiteListIds': currentList,
                'SiteListFallThroughAdjustment': 0
                }

    def set_budget(self, budget):
        if 'RTBAttributes' not in self.updates:
            self.updates['RTBAttributes'] = {}
            
        if 'BudgetSettings' not in self.updates['RTBAttributes']:
            self.updates['RTBAttributes']['BudgetSettings'] = {}

        if 'Budget' not in self.updates['RTBAttributes']['BudgetSettings']:
            self.updates['RTBAttributes']['BudgetSettings']['Budget'] = {'CurrencyCode': 'USD'}
        
        self.updates['RTBAttributes']['BudgetSettings']['Budget']['Amount'] = budget
        

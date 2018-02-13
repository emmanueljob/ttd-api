import json

from ttdclient.models.base import Base
from ttdclient.models.site_list import SiteList
from ttdclient.models.campaign import Campaign

class AdGroup(Base):

    obj_name = "adgroup"

    def getId(self):
        return self.data.get("AdGroupId")

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

    def set_deals(self, deal_ids=None):

        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}

        if 'ContractTargeting' not in self['RTBAttributes']:
            self['RTBAttributes']['ContractTargeting'] = {}

        if deal_ids is None:
            deal_ids = []

        try:
            adjustments = self.data['RTBAttributes'].get('ContractTargeting', {}).get('ContractAdjustments')
        except:
            adjustments = None

        if adjustments and len(adjustments) > 0:
            new_adjustments = []
            for adjustment in adjustments:
                if adjustment['Id'] in deal_ids:
                    deal_ids.remove(adjustment['Id'])
                    new_adjustments.append(adjustment)

            for deal_id in deal_ids:
                new_adjustments.append({"Adjustment": 1.0, "Id": deal_id})

            self['RTBAttributes']['ContractTargeting']['ContractAdjustments'] = new_adjustments
        else:
            self['RTBAttributes']['ContractTargeting']['ContractIds'] = deal_ids

    def set_contract_groups(self, deal_group_ids=None):

        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}

        if 'ContractTargeting' not in self['RTBAttributes']:
            self['RTBAttributes']['ContractTargeting'] = {}

        if deal_group_ids is None:
            deal_group_ids = []

        self['RTBAttributes']['ContractTargeting']['ContractGroupIds'] = deal_group_ids

    def set_delivery_profile_adjustments(self, deal_ids=None):

        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}

        if 'ContractTargeting' not in self['RTBAttributes']:
            self['RTBAttributes']['ContractTargeting'] = {}

        if deal_ids is None:
            delivery_profile_adjustments = []
        else:
            delivery_profile_adjustments = []
            for deal_id in deal_ids:
                val = {}
                val["Id"] = deal_id
                val["Adjustment"] = 1
                delivery_profile_adjustments.append(val)

        self['RTBAttributes']['ContractTargeting']['DeliveryProfileAdjustments'] = delivery_profile_adjustments

        """
        self['RTBAttributes']['ContractTargeting'] = { 
            'AllowOpenMarketBiddingWhenTargetingContracts': False,
            'ContractIds': [],
            'ContractGroupIds': [],
            'ContractAdjustments': [],
            "DeliveryProfileAdjustments": delivery_profile_adjustments
            }
        """

    def target_exchanges(self, target=False):

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

    def get_deal_groups(self):

        if 'RTBAttributes' not in self:
            return None
            
        if 'ContractTargeting' not in self['RTBAttributes']:
            return None

        if 'ContractGroupIds' not in self['RTBAttributes']['ContractTargeting']:
            return None

        return self['RTBAttributes']['ContractTargeting']['ContractGroupIds']

    def get_creatives(self):

        if 'RTBAttributes' not in self:
            return None
            
        return self['RTBAttributes'].get('CreativeIds', None)

    def set_exchanges(self, exchange_ids, override=True):

        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}

        if 'SupplyVendorAdjustments' not in self['RTBAttributes']:
            self['RTBAttributes']['SupplyVendorAdjustments'] = {
                'DefaultAdjustment': 0.0
                }
    
        if override or 'Adjustments' not in self['RTBAttributes']['SupplyVendorAdjustments']:
            self['RTBAttributes']['SupplyVendorAdjustments']['Adjustments'] = []

        for id in exchange_ids:

            # Default
            adjustment = 1.0

            # If we get a 'Bid Adjustment' from TTD, use it instead of the default
            for x in self.data['RTBAttributes'].get('SupplyVendorAdjustments').get('Adjustments'):
                if int(x.get('Id')) == int(id):
                    adjustment = x.get('Adjustment')

            self['RTBAttributes']['SupplyVendorAdjustments']['Adjustments'].append({'Id': id, 'Adjustment': adjustment})

    def set_domains(self, domains, sitelist_id=None):

        # get the campaign so we can get the advertiserId
        loader = Campaign(Base.connection)
        campaign = json.loads(loader.find(self.data['CampaignId']))

        # get the sitelist
        loader = SiteList(Base.connection)
        if sitelist_id is not None:
            sitelist = json.loads(loader.find(sitelist_id))
        else:
            sitelist = json.loads(loader.find_by_name(campaign.get('data').get('AdvertiserId'), self.data['AdGroupName']))

        if sitelist.get('data').get('ResultCount') == 0:
            sitelist = SiteList(Base.connection)
            sitelist['SiteListName'] = self.data['AdGroupName']
            sitelist['AdvertiserId'] = campaign.get('data').get('AdvertiserId')
        else:
            try:
                sitelist_data = sitelist.get('data').get('Result')[0]
            except:
                sitelist_data = sitelist.get('data')
            sitelist = SiteList(Base.connection, sitelist_data)

        sitelist.set_domains(domains)
        if sitelist.getId() == 0 or sitelist.getId() is None:
            response = json.loads(sitelist.create())
        else:
            sitelist['SiteListId'] = sitelist_id
            sitelist['SiteListName'] = self.data['AdGroupName']
            response = json.loads(sitelist.save(sitelist))

        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}

        # sitelist.getId() always exists so set as default list
        if 'SiteTargeting' in self.data['RTBAttributes']:
            # If Ad Group as a current list, use it and append the new ID.
            if 'SiteListIds' in self.data['RTBAttributes']['SiteTargeting']:
                currentList = self.data['RTBAttributes']['SiteTargeting']['SiteListIds']
                if sitelist.getId() not in currentList:
                    currentList.append(sitelist.getId())
        else:
            currentList = [sitelist.getId()]

        if len(domains) == 0 and sitelist.getId() in currentList:
            currentList.remove(sitelist.getId())

        if len(currentList) == 0:
            self['RTBAttributes']['SiteTargeting'] = {
                'SiteListIds': [],
                'SiteListFallThroughAdjustment': 1
                }
        else:
            self['RTBAttributes']['SiteTargeting'] = {
                'SiteListIds': currentList,
                'SiteListFallThroughAdjustment': 0
                }

        return sitelist.getId()

    def set_site_lists(self, sitelist_ids):
        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}

        self['RTBAttributes']['SiteTargeting'] = {
            'SiteListIds': self.dsp_sitelist_ids,
            'SiteListFallThroughAdjustment': 1
            }

    def set_budget(self, budget, currency_code):
        if 'RTBAttributes' not in self:
            self['RTBAttributes'] = {}
            
        if 'BudgetSettings' not in self['RTBAttributes']:
            self['RTBAttributes']['BudgetSettings'] = {}

        if 'Budget' not in self['RTBAttributes']['BudgetSettings']:
            self['RTBAttributes']['BudgetSettings']['Budget'] = {'CurrencyCode': currency_code}
        
        self['RTBAttributes']['BudgetSettings']['Budget']['Amount'] = budget
        

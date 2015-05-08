import json

from ttdclient.models.base import Base


class AdGroup(Base):

    obj_name = "adgroup"

    def getId(self):
        return self.get("AdGroupId")

    def get_by_campaign(self, campaign_id):
        payload = { "CampaignId": campaign_id,
                    "PageStartIndex": 0,
                    "PageSize": 100 }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/campaign')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)


    def get_by_name(self, campaign_id, name):
        payload = { "CampaignId": campaign_id,
                    "SearchTerms": [name],
                    "PageStartIndex": 0,
                    "PageSize": 100 }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/campaign')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)

    def set_deals(self, deal_ids):

        self['RTBAttributes']['ContractTargeting'] = { 
            'InventoryTargetingType': 'BothMarkets',
            'ContractIds': deal_ids
            }

    def set_domains(self, domains):
        
        # get the sitelist
        loader = SiteList(Base.connection)
        sitelist = loader.find_by_name(self, self['AdvertiserId'], self['AdGroupName'])
        if sitelist == None:
            sitelist = SiteList(Base.connection)
            sitelist['SiteListName'] = self['AdGroupName']
            sitelist['AdvertiserId'] = self['AdvertiserId']

        sitelist.set_domains(domains)
        sitelist.save()
        self['RTBAttributes']['SiteTargeting'] = { 
            'SiteListIds': [sitelist.getId()]
            }

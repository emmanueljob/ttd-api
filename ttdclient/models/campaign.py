import json

from ttdclient.models.base import Base


class Campaign(Base):

    obj_name = "campaign"
    
    def getId(self):
        return self.get('CampaignId')

    def get_by_advertiser(self, advertiser_id):
        payload = { "AdvertiserId": advertiser_id,
                    "PageStartIndex": 0,
                    "PageSize": None }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/advertiser')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)


    def get_by_name(self, advertiser_id, name):
        payload = { "AdvertiserId": advertiser_id,
                    "SearchTerms": [name],
                    "PageStartIndex": 0,
                    "PageSize": None }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/advertiser')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)

    def getBudget(self):
        return self.get('Budget', {}).get('Amount')

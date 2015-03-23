import json

from ttdclient.models.base import Base


class Campaign(Base):

    obj_name = "campaign"

    def get_by_advertiser(self, advertiser_id):
        payload = { "AdvertiserId": advertiser_id,
                    "PageStartIndex": 0,
                    "PageSize": 100 }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/advertiser')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)

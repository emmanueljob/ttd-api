import json

from ttdclient.models.base import Base


class Creative(Base):

    obj_name = "creative"

    def get_by_advertiser(self, advertiser_id):
        payload = { "AdvertiserId": advertiser_id,
                    "PageStartIndex": 0,
                    "PageSize": None }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/advertiser')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)
    
    def get_size(self):
        
        attributes = [
            'ImageAttributes',
            'FacebookAttributes',
            'FacebookPagePostAttributes',
            'FlashAttributes',
            'ThirdPartyTagAttributes',
            'TradeDeskHostedVideoAttributes',
            'ThirdPartyHostedVideoAttributes',
            ]

        width = 0
        height = 0
        for attribute in attributes:
            fields = self.data.get(attribute, None)
            if not fields:
                continue

            width = fields.get('Width')
            height = fields.get('Height')
            
        return [width, height]

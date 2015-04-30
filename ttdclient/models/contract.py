import json

from ttdclient.models.base import Base


class Contract(Base):

    obj_name = "contract"

    def get(self, partnerId):
        payload = { "OwnerPartnerIds": [partnerId],
                    "PageStartIndex": 0,
                    "PageSize": 100 }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)

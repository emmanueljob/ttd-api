import json

from ttdclient.models.base import Base


class SupplySource(Base):

    obj_name = "supplyvendor"

    def get_supply_sources(self, partner_id):
        payload = {
            "PartnerId": partner_id,
            "PageStartIndex": 0,
            "PageSize": None
        }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/partner')
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)
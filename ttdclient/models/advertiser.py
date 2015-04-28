import json

from ttdclient.models.base import Base


class Advertiser(Base):

    obj_name = "advertiser"
    
    def find_by_partner(self, partner_id, offset=0, limit=None):
        url = "{0}/query/partner?PageSize".format(self.get_url())
        data = { 
            "PartnerId": partner_id,
            "PageStartIndex": offset,
            "PageSize": limit,
            }
        response = self._execute("POST", url, json.dumps(data))

        rval = []
        if response:
            rval = self._get_response_objects(response)
        return rval

    
    def find_by_name(self, partner_id, name, offset=0, limit=None):
        url = "{0}/query/partner?PageSize".format(self.get_url())
        data = { 
            "SearchTerms": [name],
            "PartnerId": partner_id,
            "PageStartIndex": offset,
            "PageSize": limit,
            }
        response = self._execute("POST", url, json.dumps(data))

        rval = []
        if response:
            rval = self._get_response_objects(response)
        return rval
        

import json

from ttdclient.models.base import Base


class ContractGroup(Base):

    obj_name = "contractgroup"

    def getId(self):
        return self.get("ContractGroupId")

    def find_by_advertiser(self, advertiserId):
        payload = { "AdvertiserId": advertiserId,
                    "PageStartIndex": 0,
                    "PageSize": None }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/advertiser/available')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)

    """
    def find_by_id(self, contractGroupId):
        payload = {  }
        method = "GET"
        url = '{0}/{1}'.format(self.get_url(), contractGroupId)
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)
    """

    def get_avails(self, contractId, startDate, endDate):
        payload = { "ContractGroupId": contractId,
                    "ReportStartDateUtc": startDate,
                    "ReportEndDateUtc": endDate,
                    "PageStartIndex": 0,
                    "PageSize": None }

        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'report/impressions/available')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_object(response)

    def set_deals(self, deal_ids):
        self['ContractIds'] = deal_ids
        

import json

from ttdclient.models.base import Base


class Contract(Base):

    obj_name = "contract"

    def find_by_partner(self, partnerId):
        payload = { "PartnerId": partnerId,
                    "PageStartIndex": 0,
                    "PageSize": None }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/partner/available')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)

    def find_by_advertiser(self, partnerId, advertiserId):
        payload = { "PartnerId": partnerId,
                    "AdvertiserId": advertiserId,
                    "PageStartIndex": 0,
                    "PageSize": None }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/advertiser/available')
        
        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)

    def get_avails(self, contractId, startDate, endDate):
        payload = { "ContractId": contractId,
                    "ReportStartDateUtc": startDate,
                    "ReportEndDateUtc": endDate,
                    "PageStartIndex": 0,
                    "PageSize": None }

        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'report/impressions/available')
        
        response = self._execute(method, url, json.dumps(payload))
        print response.text
        

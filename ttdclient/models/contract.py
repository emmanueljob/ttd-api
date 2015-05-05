import json

from ttdclient.models.base import Base


class Contract(Base):

    obj_name = "contract"

    def find_by_partner(self, partnerId):
        payload = { "OwnerPartnerIds": [partnerId],
                    "PageStartIndex": 0,
                    "PageSize": 100 }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/available')
        
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
        

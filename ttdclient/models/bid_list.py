import json

from ttdclient.models.base import Base

class BidList(Base):

    obj_name = "bidlist"

    def getId(self):
        return self.get("BidListId")

    def create_bid_list(self, name, target_list='TargetList', resolution_type='SingleMatchOnly'):
        self['BidList'] = { 
            "Name": name,
            "BidListAdjustmentType": target_list,
            "ResolutionType": resolution_type,
            "BidLines": []
            }

    def set_bid_lines(self, lines):
        self['BidLines'] = lines

    def get_by_ad_group(self, dsp_lineitem_id):
        payload = { "AdGroupId": dsp_lineitem_id,
                    "PageStartIndex": 0,
                    "PageSize": None }
        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/adgroup')

        response = self._execute(method, url, json.dumps(payload))
        return self._get_response_objects(response)
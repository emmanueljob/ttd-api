import json

from ttdclient.models.base import Base

class BidList(Base):

    def getId(self):
        return self.get("BidListId")

    def create_bid_list(self, name, target_list='TargetList', resolution_type='SingleMatchOnly'):
        self['BidList'] = { 
            'Name' = name,
            'BidListAdjustmentType' = target_list,
            'ResolutionType' = resolution_type,
            'BidLines' = []
            }

    def set_bid_lines(self, lines):
        self['BidLines'] = [lines]
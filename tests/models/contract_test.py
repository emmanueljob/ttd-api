import unittest
import json

from ttdclient.models.contract import Contract
from tests.base import Base


class ContractTest(Base):

    def testGet(self):
        # Create an advertiser first.
        partnerId = '73qiy5s'
        contract = Contract(ContractTest.conn)
        contracts = contract.get(partnerId)
        for c in contracts:
            print c

    def testCreate(self):
        # Create an advertiser first.
        contract = Contract(ContractTest.conn)
        contract['Name'] = 'Contract Test'
        contract['OwnerPartnerId'] = '73qiy5s'
        contract["StartDateUtc"] = "2015-04-30T21:21:19.7668268"
        
        deals = [{
                "SupplyVendorId": 7, # AppNexus
                "SupplyVendorDealCode": 'TTD-111-1111', # AppNexus
                "FloorPrice": 1.0
                }]
        contract['Deals'] = deals
    
        contract.create()

        assert contract.get('ContractId') is not None

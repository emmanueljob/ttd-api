import unittest
import json
import time

from ttdclient.models.contract import Contract
from tests.base import Base


class ContractTest(Base):

    def testCreate(self):
        # Create an advertiser first.
        contract = Contract(ContractTest.conn)
        contract['Name'] = 'Contract Test'
        contract['OwnerPartnerId'] = '73qiy5s'
        contract["StartDateUtc"] = "2015-04-30T21:21:19.7668268"
        
        code = int(time.time())
        
        deals = [{
                "SupplyVendorId": 7, # AppNexus
                "SupplyVendorDealCode": str(code), # AppNexus
                "FloorPriceCPM": {
                    "CurrencyCode": "USD",
                    "Amount": 1.0
                    }
                }]
        contract['Deals'] = deals
    
        contract.create()

        assert contract.get('ContractId') is not None

    def testReport(self):

        startDate = "2015-04-25T21:21:19.7668268"
        endDate = "2015-05-01T21:21:19.7668268"
        contractId = '84a6cka'

        contract = Contract(ContractTest.conn)
        contract.get_avails(contractId, startDate, endDate)

    def testGetAll(self):
        partnerId = '73qiy5s'
        contract = Contract(ContractTest.conn)
        contracts = contract.find_by_partner(partnerId)
        
        i = 0
        for c in contracts:
            for deal in c['Deals']:
                i = i + 1
                print str(i) + ": " + c['ContractId'] + " == " + deal['SupplyVendorDealCode']
        
        

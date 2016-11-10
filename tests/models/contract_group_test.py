import unittest
import json
import time

from ttdclient.models.contract_group import ContractGroup
from tests.base import Base


class ContractGroupTest(Base):

    def testCreate(self):
        # Create an advertiser first.
        contract_group = ContractGroup(ContractGroupTest.conn)
        contract_group['ContractGroupId'] = 'Contract Group Test'
        contract_group['Description'] = 'Contract Group Test'
        contract_group['Name'] = 'Contract Group Test'
        contract_group['OwnerPartnerId'] = '73qiy5s'
        
        code = int(time.time())
        
        deals = [
            'pmvdsh4',
            'pnegjgvv'
        ]
        contract_group['ContractIds'] = deals
    
        contract_group.create()

        assert contract_group.get('ContractId') is not None


    def testGetAll(self):
        partnerId = '73qiy5s'
        contract_group = ContractGroup(ContractGroupTest.conn)
        contract_groups = contract_group.find_by_partner(partnerId)
        
        i = 0
        for c in contract_groups:
            for deal in c['Deals']:
                i = i + 1
                print str(i) + ": " + c['ContractId'] + " == " + deal['SupplyVendorDealCode']
        
        

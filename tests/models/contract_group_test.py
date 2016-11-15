import unittest
import json
import time

from ttdclient.models.contract_group import ContractGroup
from tests.base import Base


class ContractGroupTest(Base):

    def testCreate(self):
        partnerId = 'acjf93j' # Live TTD
        # Create an advertiser first.
        contract_group = ContractGroup(ContractGroupTest.conn)
        contract_group['ContractGroupId'] = 'Contract Group Test ID'
        contract_group['Description'] = 'Contract Group Test Desc'
        contract_group['Name'] = 'Contract Group Test Name'
        contract_group['OwnerPartnerId'] = partnerId
        
        code = int(time.time())
        
        deals = [
            'pmvdsh4',
            'pnegjgvv'
        ]
        contract_group['ContractIds'] = deals
    
        contract_group.create()

        assert contract_group.get('ContractGroupId') is not None


    def testGetOne(self):
        contractGroupId = '3o6h44l'
        contract_group = ContractGroup(ContractGroupTest.conn)
        contract_group = contract_group.find_by_id(contractGroupId)

        print contract_group.get('ContractGroupId')

        assert contract_group.get('ContractGroupId') is not None


    def testGetAllByAdvertiser(self):
        advertiserId = '?????'
        contract_group = ContractGroup(ContractGroupTest.conn)
        contract_groups = contract_group.find_by_advertiser(advertiserId)
        
        i = 0
        for c in contract_groups:
            for deal in c['ContractIds']:
                i = i + 1
                print str(i) + ": " + c['ContractGroupId'] + " == " + deal
        
        

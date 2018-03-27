import unittest
import json

from ttdclient.models.supply_source import SupplySource
from tests.base import Base

class TestSupplySource(Base):

    def test_get_supply_sources(self):
        supply_source_instance = SupplySource(TestSupplySource.conn)
        # using sandbox partner_id
        supply_sources = supply_source_instance.get_supply_sources("73qiy5s")
        assert json.loads(supply_sources)['msg_type'] == 'success'
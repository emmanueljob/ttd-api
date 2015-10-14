import unittest
import json
import time

from ttdclient.models.creative import Creative
from ttdclient.models.advertiser import Advertiser
from tests.base import Base


class CreativeTest(Base):

    def testCreate(self):
        # Create an advertiser first.
        adv = Advertiser(CreativeTest.conn)
        adv['AdvertiserName'] = 'ad group adv test eman'
        adv['AttributionClickLookbackWindowInSeconds'] = 3600
        adv['AttributionImpressionLookbackWindowInSeconds'] = 3600
        adv['ClickDedupWindowInSeconds'] = 7
        adv['ConversionDedupWindowInSeconds'] = 60
        adv['DefaultRightMediaOfferTypeId'] = 1  # Adult
        adv['IndustryCategoryId'] = 54  # Entertainment
        adv['PartnerId'] = '73qiy5s'
        adv.create()

        adTag = """<script>
 document.write('<scr'+'ipt src=\'http://ad.doubleclick.net/adj/N8017.858336.OXEGENMEDIA.COM/B6940936;abr=!ie;sz=728x90;click=' + ('%%c1;cpdir=').replace(/;/g,'&') + ';ord=' + new Date().getTime() + '?\'></scr'+'ipt>');
</script>"""

        creative = Creative(CreativeTest.conn)
        creative['CreativeName'] = 'Creative Test'
        creative['AdvertiserId'] = adv.get('AdvertiserId')
        creative['ThirdPartyTagAttributes'] = {'AdTag': adTag, 'Width': 300, 'Height': 250, 'LandingPageUrls': ['http://eman.com']}
        id = creative.create()

        loader = Creative(CreativeTest.conn)
        new_loaded = loader.find(creative.get('CreativeId'))
        assert new_loaded.get('CreativeId') == creative.get('CreativeId')

        assert new_loaded.get_size() == [300,250]

import json

from ttdclient.models.base import Base


class SiteList(Base):

    obj_name = "sitelist"

    def getId(self):
        return self.get("SiteListId")

    def find_by_name(self, advertiser_id, name):
        payload = { "AdvertiserId": advertiser_id,
                    "SearchTerms": [name],
                    "PageStartIndex": 0,
                    "PageSize": None }

        method = "POST"
        url = '{0}/{1}'.format(self.get_url(), 'query/advertiser')

        response = self._execute(method, url, json.dumps(payload))
        objects = self._get_response_objects(response)

        if len(objects) > 0:
            return objects[0]
        return None
        
    def set_domains(self, domains):
        to_add = []
        hits = {}
        print "PRINTING SELF"
        print self
        loader = SiteList(Base.connection)
        a = loader.find('bjrc1vj')
        print a
        for ttd_domain in a.get('SiteListLines'):
            hits[ttd_domain['Domain']] = ttd_domain['Adjustment']
        print hits
        print "END PRINTING SELF"
        for domain in list(set(domains)):
            default_adjustment = 1.0
            to_add.append({'Domain': domain, 'adjustment': 1.0})
        self['SiteListLines'] = to_add


'''
	TODO
	1) Modularize apis for services
	2) Have a multiple APIs to single service solution. Python does not support function overloading.
'''
import json
from pybsf.clients.http_tibrv import BSFHTTPTibrvClient

class Caller(object):
    def __init__(self, realm, domain):
        self.realm = realm
        self.domain = domain
    
    def setup(self, host, port, service_name):
        self.caller = BSFHTTPTibrvClient(
            realm = self.realm,
            remoteHostName = host,
            remoteHostPort = port,
            path = '/bsf/',
            serviceName = service_name,
            domain = self.domain,
            appName = 'DigitalSE'
        )

    def __repr__(self):
        pass

class AudiblePriceAggregatorService(Caller):
    def __init__(self, realm='USAmazon', domain='prod'):
        Caller.__init__(self, realm, domain)

    def call(self, customerId, marketplaceId, merchantId, asin):
        assert self.caller is not None 
        results = self.caller.call('getPrices', customerId=customerId, marketplaceId=marketplaceId, merchantId=merchantId, itemList=[dict(asin=asin)])
        print json.dumps(results, default=lambda x: x.__dict__, indent=2, sort_keys=True)
	return json.dumps(results, default=lambda x: x.__dict__, indent=2, sort_keys=True)

class SubscriptionService(Caller):
    def __init__(self, realm='USAmazon', domain='prod'):
        Caller.__init__(self, realm, domain)

    def call(self, **kwargs):
        assert self.caller is not None 
        results = self.caller.call('getDeepPlanSelections', **kwargs)
        print json.dumps(results, default=lambda x: x.__dict__, indent=2, sort_keys=True)
	return json.dumps(results, default=lambda x: x.__dict__, indent=2, sort_keys=True)

class AudibleLibraryService(Caller):
    def __init__(self, realm='USAmazon', domain='prod'):
        Caller.__init__(self, realm, domain)

    def call(self, **kwargs):
        assert self.caller is not None 
        results = self.caller.call('checkItemPurchasability', **kwargs)
        print json.dumps(results, default=lambda x: x.__dict__, indent=2, sort_keys=True)
	return json.dumps(results, default=lambda x: x.__dict__, indent=2, sort_keys=True)

'''
	Required configurations for things to work
'''

service_data = {

	'NA'	:	{
		'SubscriptionService' : {
			'vip'	:	'subscriptionservice-us.amazon.com',
			'port'	:	9910
		},

		'AudiblePriceAggregatorService'	: {
			'vip'	:	'audible-price-aggregator-service.amazon.com',
			'port'	:	7200	
		},

		'AudibleMembershipInformationService' : {
			'vip'	:	'audible-membership-info-service.amazon.com',
			'port'	:	7200
		},

		'AudibleLibraryService' : {
			'vip'	:	'audible-library-service.amazon.com',
			'port'	:	7200
		}
	}
}

api_data = {

	'getDeepPlanSelections'	 :	{
		'service'	:	'SubscriptionService',
		'params'	:	['subscriptionID']
	},

	'getPrices'	:	{
		'service'	:	'AudiblePriceAggregatorService',
		'params'	:	['marketplaceId', 'merchantId', 'asin', 'customerId']
	},

	'checkItemPurchasability'	:	{
		'service'	:	'AudibleLibraryService',
		'params'	:	['customerID', 'marketplaceID', 'asin']
	}
}

keyword_to_api = {
	'Incorrect Pricing'	:	['getPrices', 'checkItemPurchasability'],
	'Subscription Issue'	:	['getDeepPlanSelections']
}

marketplace_merchant = {
	'AF2M0KC94RCEA'		:	'A2ZO8JX97D5MN9',
	'A2I9A3Q2GNFNGQ'	:	'A2YHV2RYTDNFG3',
	'AN7V1F1VY261K'		:	'A3SGISXRF0LJBD',
	'A2728XDNODOQ8T'	:	'A3LA9RF1WEAZDW',
	'AN7EY7DTAW63G'		:	'AN7EY7DTAW63G'
}

marketplace_mapping = {
	'US'	:	'AF2M0KC94RCEA',
	'UK'	:	'A2I9A3Q2GNFNGQ',
	'DE'	:	'AN7V1F1VY261K',
	'AU'	:	'AN7EY7DTAW63G'

}

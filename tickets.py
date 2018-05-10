#!/apollo/sbin/envroot "$ENVROOT/bin/python2.7"

'''
	VIRSE - Virtual SE
	author - barrupal@amazon.com
	
	TODO
	1) Supports only NA - Configure for other realms
	2) Tag the ticket once processed, or it will keep on updating it - then only update if it is untagged
	3) Setup DJS
	4) Supports only BSF atm, add CORAL clients for services
	5) Beautify the json response maybe?
	
	RUN:
	1) command > /apollo/env/DigitalSEDashboard/python2.7/bin/python2.7 tickets.py
	2) Uncomment all update_ticket() calls

'''

import datetime
import time
from fluxo import FluxoClient
from pyodinhttp import odin_retrieve_pair, OdinOperationError,odin_material_retrieve
from time import gmtime, strftime

import difflib

from configurations import marketplace_merchant, keyword_to_api, api_data, service_data, marketplace_mapping
from services import *


SERVER_NAME = 'https://ticket-api.amazon.com'
FLUXO_MATERIAL_SET = 'com.amazon.DigitalSE.Fluxo.Prod'

fluxo_username = odin_material_retrieve(FLUXO_MATERIAL_SET, "Principal")
fluxo_password = odin_material_retrieve(FLUXO_MATERIAL_SET, "Credential")
fluxo = FluxoClient(fluxo_username, fluxo_password, SERVER_NAME)

def poll_tickets(group, week_differential=2):

	start_time = datetime.datetime.today() - datetime.timedelta(weeks=week_differential)
	end_time = datetime.datetime.today()

	results = fluxo.searchTickets(assigned_group=group, case_type='Trouble Ticket', status={'Assigned'}, create_date=(time.strptime(str(start_time.date()) + ' 17:00:00','%Y-%m-%d %H:%M:%S'), time.strptime(str(end_time.date()) + ' 17:00:00','%Y-%m-%d %H:%M:%S') ))

	for ticket in results:
		match, keyword = find_trigger_keywords(ticket.summary)
		if match is True:
			process_ticket(ticket.id, keyword)

def get_data_from_ticket(title, text):
	data = {}
	marketplaces = marketplace_mapping.keys()
	text = text.strip().split('\n')

	data = dict((lambda x: [x[0].strip(), x[1].strip()])(x) for x in [y.split(':') for y in text if ':' in y])
	# get marketplace from title first, if not, go for the body
	for m in marketplaces:
		if m in title:
			data['marketplace'] = marketplace_mapping.get(m)
			break
	if data.get('marketplace') is None:
		for m in marketplaces:
			if any(m in x.strip() for x in text):
				data['marketplace'] = marketplace_mapping.get(m)
				break

	print 'KV pairs from ticket',data
	return data

def get_closest_key(word, keys):
	''' word : str -> generic part of the word that should be there, like 'market' in 'marketplaceId'
	    keys : list of str -> keys
	    return : (found, key)
	'''
	keys = difflib.get_close_matches(word, keys)
	key = keys[0] if len(keys) > 0 else word
	return len(keys) > 0, key

def process_ticket(ticket_id, keyword):
	# preserves new lines and all, fetched text is in raw form. We need new line seperated text with ':' to distinguish key value pairs
	preserve_text_integrity = (lambda x : str(x).replace('\r\n', '\n'))
	# get all key value pairs available in ticket body
	print 'Running for ticket', ticket_id
	ticket_text = get_ticket_details(ticket_id)	
	params = get_data_from_ticket(preserve_text_integrity(ticket_text.short_description), preserve_text_integrity(ticket_text.details))
	validate_and_make_request(ticket_id, keyword, params)

def validate_and_make_request(ticket_id, keyword, found_params):
	for api in keyword_to_api.get(keyword):
		request = {}
		undefined_params = []
		for required_key in api_data.get(api).get('params'):
			
			found_key, closest_matching_key = get_closest_key(required_key, found_params.keys())
			value = None
			if found_key is True:
				value = found_params.get(closest_matching_key)
			else:
				# in case there are required parameters which can be derived from existing parameters, manually find it here, ex. merchantId
				if 'merchant' in required_key:
					_, marketplace_key_in_api = get_closest_key('marketplace', api_data.get(api).get('params'))
					found, marketplace_key_in_ticket = get_closest_key('marketplace', found_params.keys())
					if found is True:
						found_key = True
						value = marketplace_merchant.get(found_params.get(marketplace_key_in_ticket))

				# if fail to find the key manually, put it in undefined params and skip api call
				if found_key is False:
					undefined_params.append(required_key)
					
			if found_key is True:
				request[required_key] = value
			else:
				#update ticket saying that particular API was skipped because it missed some parameters
				#update_ticket(ticket_id, 'VIRSE: API ' + api + ' skipped because it was missing one or more required parameters', 'Missing params are:\n' + ','.join(undefined_params))
				print 'Missing params', api, undefined_params
	
		print 'Request for keyword', keyword, api, request
		if len(undefined_params) == 0:
			service = api_data.get(api).get('service')
			caller = eval(service)() #with default params USAmazon, prod
			caller.setup(service_data['NA'].get(service).get('vip'), service_data['NA'].get(service).get('port'), service)
			response = caller.call(**request)

		#updating ticket
		#update_ticket(ticket_id, 'VIRSE: API matched is ' + api, response)

def get_ticket_details(ticket_id):
	''' ticket_id : str '''
	ticket_details = fluxo.getTicketById(int(ticket_id))
	return ticket_details

def find_trigger_keywords(text):
	print 'summary', text
	for keyword in keyword_to_api.keys():
		if keyword in text:
			return True, keyword
	return False, None

def update_ticket(ticket_id, corrospondence='', work_log=''):
	status = fluxo.updateTicket(int(ticket_id), correspondence=corrospondence, work_log=work_log)
	print 'Updated ', ticket_id, status

if __name__ == '__main__':
	GROUP_NAME = 'Audible OrderFulfill SE'
	poll_tickets(GROUP_NAME)

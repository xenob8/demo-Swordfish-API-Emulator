#
# Copyright (c) 2017-2021, The Storage Networking Industry Association.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# Neither the name of The Storage Networking Industry Association (SNIA) nor
# the names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
#  THE POSSIBILITY OF SUCH DAMAGE.

# Resource implementation for - /redfish/v1/Chassis/{ChassisId}
# Program name - Chassis_api.py

import g
import json, os
import traceback
import logging
import jwt

from flask import Flask, session
from flask_restful import Resource
from .constants import *
from api_emulator.utils import check_authentication, get_sessionValidation_error, update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.Chassis import get_Chassis_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# Chassis Collection API
class ChassisCollectionAPI(Resource):
	def __init__(self, **kwargs):
		logging.info('Chassis Collection init called')
		self.root = PATHS['Root']
		self.auth_mode = kwargs['auth_mode']

	# HTTP GET
	def get(self):
		logging.info('Chassis Collection get called')
		msg, code = check_authentication(self.auth_mode)
		
		if code == 200:
			path = os.path.join(self.root, 'Chassis', 'index.json')
			return get_json_data(path)
		else:
			return msg, code

	# HTTP POST Collection
	def post(self):
		logging.info('Chassis Collection post called')

		path = create_path(self.root, 'Chassis')
		return create_collection (path, 'Chassis')

	# HTTP PUT Collection
	def put(self):
		logging.info('Chassis Collection put called')
		msg, code = check_authentication(self.auth_mode)
		if code == 200:
			path = os.path.join(self.root, 'Chassis', 'index.json')
			put_object (path)
			return self.get(self.root)
		else:
			return msg, code					

# Chassis API
class ChassisAPI(Resource):
	def __init__(self, **kwargs):
		logging.info('Chassis init called')
		self.root = PATHS['Root']
		self.auth_mode = kwargs['auth_mode']

	# HTTP GET
	def get(self, ChassisId):
		logging.info('Chassis get called')
		if session.get('UserName') != None:
			path = create_path(self.root, 'Chassis/{0}', 'index.json').format(ChassisId)

			msg, code = check_authentication(self.auth_mode)
			if code == 200:
				return get_json_data (path)
			else:
				return msg, code
		else:
			return get_sessionValidation_error(), 403

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, ChassisId):
		logging.info('Chassis post called')
		if session.get('UserName') != None:
			path = create_path(self.root, 'Chassis/{0}').format(ChassisId)
			collection_path = os.path.join(self.root, 'Chassis', 'index.json')

			msg, code = check_authentication()
			if code == 200:
				# Check if collection exists:
				if not os.path.exists(collection_path):
					ChassisCollectionAPI.post(self)

				if ChassisId in members:
					resp = 404
					return resp
				try:
					global config
					wildcards = {'ChassisId':ChassisId, 'rb':g.rest_base}
					config=get_Chassis_instance(wildcards)
					config = create_and_patch_object (config, members, member_ids, path, collection_path)
					resp = config, 200

				except Exception:
					traceback.print_exc()
					resp = INTERNAL_ERROR
					logging.info('ChassisAPI POST exit')
				return resp

			else:
				return msg, code
		else:
			return get_sessionValidation_error(), 403

	# HTTP PUT
	def put(self, ChassisId):
		logging.info('Chassis put called')
		if session.get('UserName') != None:
			path = os.path.join(self.root, 'Chassis/{0}', 'index.json').format(ChassisId)

			msg, code = check_authentication()
			if code == 200:			
				put_object(path)
				return self.get(ChassisId)
			else:
				return msg, code
		else:
			return get_sessionValidation_error(), 403

	# HTTP PATCH
	def patch(self, ChassisId):
		logging.info('Chassis patch called')
		if session.get('UserName') != None:
			path = os.path.join(self.root, 'Chassis/{0}', 'index.json').format(ChassisId)

			msg, code = check_authentication()
			if code == 200:
				patch_object(path)
				return self.get(ChassisId)
			else:
				return msg, code
		else:
			return get_sessionValidation_error(), 403


	# HTTP DELETE
	def delete(self, ChassisId):
		logging.info('Chassis delete called')
		if session.get('UserName') != None:
			path = create_path(self.root, 'Chassis/{0}').format(ChassisId)
			base_path = create_path(self.root, 'Chassis')

			msg, code = check_authentication()
			if code == 200:
				return delete_object(path, base_path)
			else:
				return msg, code
		else:
			return get_sessionValidation_error(), 403


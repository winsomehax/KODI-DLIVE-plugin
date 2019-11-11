from requests import get, post, request
import json


class GraphQLClient:
	def __init__(self, endpoint):
		self.endpoint = endpoint
		self.token = None
		self.headername = None

	def execute(self, query, variables=None):
		return self._send(query, variables)

	def inject_token(self, token, headername='Authorization'):
		self.token = token
		self.headername = headername

	def _send(self, query, variables):
		data = {'query': query, 'variables': variables}
		headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

		if self.token is not None:
			headers[self.headername] = '{}'.format(self.token)

		#        response = request("POST", url, data=payload)
		req = post(self.endpoint, data=json.dumps(data).encode('utf-8'), headers=headers)
		j = req.json()
		return j

import requests
import json
from enum import Enum

class Period(Enum):
    LAST_DAY = 0,
    LAST_WEEK = 1,
    LAST_MONTH = 2,
    LAST_THREE_MONTHS = 3,
    LAST_YEAR = 4,
    ALL = 5,



class Trading212:
	def __init__(self, cookie, mode="demo"):

		self.mode = mode
		self.cookie = cookie
		self.headers = {
		   "User-Agent": "PostmanRuntime/7.29.0",
		   'Content-Type': 'application/json',
		   'Cookie': self.cookie,

		}
		self.base_url = f"https://{self.mode}.trading212.com"

	def get_personal_details(self):
		url = f"{self.base_url}/v1/customers/personal-details"
		response = requests.request("GET", url, headers=self.headers)
		return response.text


	def cdf_order(self, order, cfd_name="USDJPY"):
		url = f"{self.base_url}/rest/v2/pending-orders/entry-dep-limit-stop/{cfd_name}"
		payload = json.dumps(order)
		response = requests.request("POST", url, headers=self.headers, data=payload)

		return response.text

	#Used to get the min/max quantiy of a CFD trade
	def get_instrument_settings(self, cfd_name="USDJPY"):
		url = f"{self.base_url}/rest/v2/account/instruments/settings"
		payload = json.dumps([cfd_name])
		response = requests.request("POST", url, headers=self.headers, data=payload)
		if response.status_code == 200:
			data = json.loads(response.text)
			if data:
				return data
			else:
				return "No data found with {}".format(cfd_name)
		else:
			return response.text


	def get_portfolio_performance(self, time_period=Period.LAST_DAY):
		url=f"{self.base_url}/rest/v2/portfolio?period={time_period.name}"
		response = requests.get(url,headers=self.headers)
		return json.loads(response.content.decode("utf-8"))

	def get_orders(self):
		response = requests.get(
			f"{self.base_url}/rest/history/orders", headers=self.headers
		)
		return json.loads(response.content.decode("utf-8"))

	def get_funds(self):
		response = requests.get(
			f"{self.base_url}/rest/customer/accounts/funds", headers=self.headers
		)
		return json.loads(response.content.decode("utf-8"))

	# Not working
	def get_open_positions(self):
		response = requests.get(
			f"{self.base_url}/rest/v2/trading/open-positions", headers=self.headers
		)
		return json.loads(response.content.decode("utf-8"))


import re, os, json
import requests

from . import core


class Ripe():
	"""docstring for Whois"""
	def __init__(self, options):
		self.options = options
		core.print_banner("Starting scraping IP from Ripe")
		self.initial()

	def initial(self):
		real_data = self.get_real_content()

		#get the raw IP as normal
		ips = core.grep_the_IP(real_data, self.options['cidr_regex'])
		core.write_to_output(ips, self.options['output'])

		#get the range of ip
		range_ips = core.grep_the_IP(real_data, self.options['range_ip_regex'])
		if len(range_ips) > 0:
			core.print_good("Range IP detect")
			for item in range_ips:
				#1.2.3.4 - 5.6.7.8
				start = item.split('-')[0].strip()
				end = item.split('-')[1].strip()

				ips2 = core.get_IP_from_range(start, end)
				core.write_to_output(ips2, self.options['output'])



	#doing a logic based on some web site to get the real content
	def get_real_content(self):
		target = self.options['target']

		url = "https://apps.db.ripe.net:443/db-web-ui/api/whois/search?abuse-contact=true&flags=B&ignore404=true&limit=100&managed-attributes=true&offset=0&query-string={0}&resource-holder=true".format(target)
		
		headers = {"User-Agent": "Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36", "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://apps.db.ripe.net/db-web-ui/", "X-Requested-With": "XMLHttpRequest", "DNT": "1", "Connection": "close", "Cache-Control": "max-age=0"}

		r = requests.get(url, headers=headers)

		return r.text




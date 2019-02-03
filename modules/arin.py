import re, os, json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from . import core


class Arin():
	"""docstring for Whois"""
	def __init__(self, options):
		self.options = options
		core.print_banner("Starting scraping IP from Arin")
		try:
			self.initial()
		except:
			core.print_bad("Some thing wrong with Arin module")


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

		url = "https://whois.arin.net:443/ui/query.do"
		core.print_verbose(url, self.options)

		headers = {"User-Agent": "Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "https://whois.arin.net/ui/query.do", "Content-Type": "application/x-www-form-urlencoded", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
		data={"xslt": "https://localhost:8080/whoisrws/servlet/arin.xsl", "flushCache": "false", "queryinput": target, "whoisSubmitButton": " "}
		r = requests.post(url, headers=headers, data=data, verify=False)

		return r.text




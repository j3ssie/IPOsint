import re, os, json
import requests

from . import core


class Whois():
	"""docstring for Whois"""
	def __init__(self, options):
		self.options = options
		core.print_banner("Starting scraping IP from Whois")
		self.initial()

	def initial(self):
		real_data = self.get_real_content()

		ips = core.grep_the_IP(real_data, self.options['cidr_regex'])

		core.write_to_output(ips, self.options['output'])

	#doing a logic based on some web site to get the real content
	def get_real_content(self):
		target = self.options['target']
		url = "http://whois.domaintools.com:80/go/?q={0}&service=whois".format(target)

		headers = {"User-Agent": "Mozilla/5.0 (X11; FreeBSD amd64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "http://whois.domaintools.com/", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

		r = requests.get(url, headers=headers)

		return r.text




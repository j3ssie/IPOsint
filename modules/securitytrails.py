import re, os, json, time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from . import core


class SecurityTrails():
    """docstring for Whois"""
    def __init__(self, options):
        self.options = options
        core.print_banner("Starting scraping IP from SecurityTrails")
        core.install_webdrive()
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
        url = "https://securitytrails.com/domain/{0}/history/a".format(target)
        response = core.open_with_chrome(url)

        return response




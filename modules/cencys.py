import re, os, json, time
import requests
import ssl
import socket
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from . import core


class Censys():
    """docstring for Whois"""
    def __init__(self, options):
        self.options = options
        core.print_banner("Starting scrapping IP from Censys")
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

        cert_fin = self.get_cert_fingerprint(target)
        # print(cert_fin)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")

        # your executable path is wherever you saved the chrome webdriver
        chromedriver = self.options['cwd'] + '/modules/chromedriver'
        browser = webdriver.Chrome(executable_path=chromedriver, options=options)
        

        url = "https://censys.io/ipv4?q={0}".format(cert_fin)
        browser.get(url)

        #wait for get the right response
        time.sleep(5)
        response = browser.page_source
        browser.close()

        return response

    #get cert fingerprint
    def get_cert_fingerprint(self, addr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        wrappedSocket = ssl.wrap_socket(sock)

        try:
            wrappedSocket.connect((addr, 443))
        except:
            response = False
        else:
            der_cert_bin = wrappedSocket.getpeercert(True)
            pem_cert = ssl.DER_cert_to_PEM_cert(wrappedSocket.getpeercert(True))

            #Thumbprint
            thumb_md5 = hashlib.md5(der_cert_bin).hexdigest()
            thumb_sha1 = hashlib.sha1(der_cert_bin).hexdigest()
            thumb_sha256 = hashlib.sha256(der_cert_bin).hexdigest()

        wrappedSocket.close()
        return thumb_sha256





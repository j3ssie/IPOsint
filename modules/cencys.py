import re, os, json, time
import requests
import ssl
import socket
import hashlib
from bs4 import BeautifulSoup

from . import core


class Censys():
    """docstring for Whois"""
    def __init__(self, options):
        self.options = options
        core.print_banner("Starting scraping IP from Censys")
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
        url = "https://censys.io/ipv4?q={0}".format(cert_fin)
        response = core.open_with_chrome(url)

        # print(cert_fin)
        final_res = self.get_all_page(url, response)

        return final_res

    #check if more page or not
    def get_all_page(self, url, response):
        more_response = response

        #parsing
        soup = BeautifulSoup(response, 'lxml')
        divs = soup.find_all('div')

        for div in divs:
            try:
                if 'SearchResultSectionHeader__subheading' in div['class']:
                    raw_data = div.text
            except:
                pass 

        #should return like '1/4'
        num_page = raw_data.split("Page: ")[1].split("\n")[0]
        current = int(num_page.split('/')[0])
        total = int(num_page.split('/')[1])

        if current < total:
            for i in range(current, total):
                page_url = url + "&page=" + str(i + 1)
                # print(page_url)
                more_response += core.open_with_chrome(page_url)

        return more_response


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





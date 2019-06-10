import re
import os
import time
import ipaddress
import platform
import requests
import shutil
import zipfile
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_IP_from_range(start, end):
    ips = []
    start_ip = ipaddress.IPv4Address(start)
    end_ip = ipaddress.IPv4Address(end)
    for ip_int in range(int(start_ip), int(end_ip)):
        ip = str(ipaddress.IPv4Address(ip_int))
        ips.append(ip)
    return ips

#just grep the IP address


def grep_the_IP(data, cird_regex):
    ips = []
    p = re.compile(cird_regex)

    for m in p.finditer(data):
        ips.append(m.group())
        print_info(m.group())
    return ips

#strip out the private IP


def strip_private_ip(data):
    new_data = []
    for item in data:
        try:
            if not ipaddress.ip_address(item).is_private:
                new_data.append(item)
        except:
            new_data.append(item)

    return new_data

#write the list of data to a file


def write_to_output(data, output_file):
    with open(output_file, 'a+') as o:
        for item in set(data):
            o.write(item + "\n")


# just beatiful soup the html
def just_soup(html):
    soup = BeautifulSoup(html, "lxml")
    return soup

# Possible paths for Google Chrome on porpular OS
chrome_paths = [
    "/usr/bin/chromium",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
]


def get_chrome_binary():
    for chrome_binary in chrome_paths:
        if os.path.isfile(chrome_binary):
            return chrome_binary

    print_bad("Not found Chrome binary on your system")


# get version of your chrome
def get_chrome_version():
    chrome_binary = get_chrome_binary()
    chrome_version = os.popen(
        '"{0}" -version'.format(chrome_binary)).read().lower()
    chrome_app = os.path.basename(os.path.normpath(chrome_binary)).lower()
    # just get some main release
    version = chrome_version.split(chrome_app)[1].strip().split(' ')[0] 
    relative_version = '.'.join(version.split('.')[:2])
    return relative_version


def install_webdrive():
    current_path = os.path.dirname(os.path.realpath(__file__))
    chromedrive_check = shutil.which(current_path + "/chromedriver")

    if chromedrive_check:
        return current_path + "/chromedriver"

    print_info("Download chromedriver")
    relative_version = get_chrome_version()

    if float(relative_version) < 73:
        print_info("Unsupport Chromium version support detected: {0}".format(relative_version))
        print_bad("You need to update your Chromium.(e.g: sudo apt install chromium -y)")
        return

    chrome_driver_url = 'https://sites.google.com/a/chromium.org/chromedriver/downloads'
    # predefine download url
    download_url = 'https://chromedriver.storage.googleapis.com/index.html?path=74.0.3729.6/'
    r = requests.get(chrome_driver_url, allow_redirects=True)
    if r.status_code == 200:
        soup = just_soup(r.text)
        lis = soup.find_all("li")
        for li in lis:
            if 'If you are using Chrome version' in li.text:
                if relative_version in li.text:
                    download_url = li.a.get('href')

    parsed_url = urlparse(download_url)
    zip_chromdriver = parsed_url.scheme + "://" + parsed_url.hostname + \
        "/" + parsed_url.query.split('=')[1]
    
    os_check = platform.platform()
    if 'Darwin' in os_check:
        zip_chromdriver += "chromedriver_mac64.zip"
    elif 'Win' in os_check:
        zip_chromdriver += "chromedriver_win32.zip"
    elif 'Linux' in os_check:
        zip_chromdriver += "chromedriver_linux64.zip"
    else:
        zip_chromdriver += "chromedriver_linux64.zip"

    # print_info("Download: {0}".format(zip_chromdriver))
    r3 = requests.get(zip_chromdriver, allow_redirects=True)

    open(current_path + "/chromedriver.zip", 'wb').write(r3.content)

    with open(current_path + '/chromedriver.zip', 'rb') as f:
        z = zipfile.ZipFile(f)
        for name in z.namelist():
            z.extract(name, current_path)

    os.chmod(current_path + "/chromedriver", 0o775)
    if not shutil.which(current_path + "/chromedriver"):
        print_bad("Some thing wrong with chromedriver")
        sys.exit(-1)

##open url with chromedriver


def open_with_chrome(url, delay=5):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")

    current_path = os.path.dirname(os.path.realpath(__file__))
    chromedrive_check = os.path.isfile(current_path + "/chromedriver")
    if not chromedrive_check:
        raise ValueError("Some thing wrong with chromedriver path")

    chromedriver = current_path + '/chromedriver'
    browser = webdriver.Chrome(executable_path=chromedriver, options=options)

    browser.get(url)

    #wait for get the right response
    time.sleep(delay)
    response = browser.page_source
    browser.close()

    return response


def false_positive(ip):
    #some IP are just example on some resouces
    black_list = ['141.212.120.90']
    if ip in black_list:
        return True

    return False


######## print beautify
# Console colors
W = '\033[1;0m'   # white
R = '\033[1;31m'  # red
G = '\033[1;32m'  # green
O = '\033[1;33m'  # orange
B = '\033[1;34m'  # blue
Y = '\033[1;93m'  # yellow
P = '\033[1;35m'  # purple
C = '\033[1;36m'  # cyan
GR = '\033[1;37m'  # gray
colors = [G, R, B, P, C, O, GR]

info = '{0}[*]{1} '.format(B, GR)
ques = '{0}[?]{1} '.format(C, GR)
bad = '{0}[-]{1} '.format(R, GR)
good = '{0}[+]{1} '.format(G, GR)

verbose = '{1}[{0}VERBOSE{1}] '.format(G, GR)


def print_verbose(text, options):
    if options['verbose']:
        print(verbose + text)


def print_banner(text):
    print('{1}--~~~=:>[ {2}{0}{1} ]>'.format(text, G, C))


def print_info(text):
    print(info + text)


def print_ques(text):
    print(ques + text)


def print_good(text):
    print(good + text)


def print_bad(text):
    print(bad + text)


def check_output(output):
    print('{1}--==[ Check the output: {2}{0}'.format(output, G, P))

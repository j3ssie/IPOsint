import re, os, time
import ipaddress
import platform
import requests
import zipfile

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

def install_webdrive():
    current_path = os.path.dirname(os.path.realpath(__file__))
    chromedrive_check = os.path.isfile(current_path + "/chromedriver")

    if chromedrive_check:
        return

    print("Download chrome headless ")
    # print(current_path)
    url = "https://chromedriver.storage.googleapis.com/2.45/"

    os_check = platform.platform()
    if 'Darwin' in os_check:
        url += "chromedriver_mac64.zip"
    elif 'Win' in os_check:
        url += "chromedriver_win32.zip"
    elif 'Linux' in os_check:
        url += "chromedriver_linux64.zip"

    else:
        url += "chromedriver_linux64.zip"

    r = requests.get(url, allow_redirects=True)
    open(current_path + "/chromedriver.zip", 'wb').write(r.content)

    with open(current_path + '/chromedriver.zip', 'rb') as f:
        z = zipfile.ZipFile(f)
        for name in z.namelist():
            z.extract(name, current_path)

    os.chmod(current_path + "/chromedriver", 0o775)

##open url with chromedriver
def open_with_chrome(url, delay=5):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

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
colors = [G,R,B,P,C,O,GR]

info = '{0}[*]{1} '.format(B,W)
ques =  '{0}[?]{1} '.format(C,W)
bad = '{0}[-]{1} '.format(R,W)
good = '{0}[+]{1} '.format(G,W)

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

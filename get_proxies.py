import pymongo
import requests
from bs4 import BeautifulSoup

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
proxies = ganji['proxies']
proxy_kuaidaili_url = 'http://www.kuaidaili.com/proxylist/%s/'
proxy_xicidaili_url = 'http://www.xicidaili.com/nt/%s'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}

def get_proxy_kuaidaili(url, pages):
    list_view = url % pages
    web_response = requests.get(list_view)
    soup = BeautifulSoup(web_response.text, 'lxml')
    proxy_ip_soup = soup.find_all('td', attrs={'data-title': 'IP'})
    proxy_port_soup = soup.find_all('td', attrs={'data-title': 'PORT'})

    for ip_item, port_item in zip(proxy_ip_soup, proxy_port_soup):
        ip = ip_item.get_text()
        port = port_item.get_text()
        proxies_item = {
            'http': 'http://' + ip + ':'+ port,
            'https': 'http://' + ip + ':'+ port
        }
        try:
            code = requests.get('http://www.baidu.com', proxies=proxies_item, timeout=5).status_code
            if code == 200:
                proxies.insert_one({'ip': ip, 'port': port})
                print({'ip': ip, 'port': port})
        except Exception:
            pass

def get_proxy_xicidaili(url, pages):
    list_view = url % pages
    web_response = requests.get(list_view, headers=header)
    soup = BeautifulSoup(web_response.text, 'lxml')
    if soup.find('tr', 'odd'):
        for ip_soup, port_soup in zip(soup.select('tr.odd > td:nth-of-type(2)'), soup.select('tr.odd > td:nth-of-type(3)')):
            ip = ip_soup.get_text()
            port = port_soup.get_text()
            proxies_item = {
                'http': 'http://' + ip + ':' + port,
                'https': 'http://' + ip + ':' + port
            }
            try:
                code = requests.get('http://www.baidu.com', proxies=proxies_item, timeout=5).status_code
                if code == 200:
                    proxies.insert_one({'ip': ip, 'port': port})
                    print({'ip': ip, 'port': port})
            except Exception:
                pass

if __name__ == '__main__':
    proxies.drop()
    for i in range(1, 500):
        get_proxy_xicidaili(proxy_xicidaili_url, i)

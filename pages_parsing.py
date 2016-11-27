from bs4 import BeautifulSoup
import requests
import pymongo
import random
import time

client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
url_list = ganji['url_list']
item_list = ganji['item_list']
proxies = ganji['proxies']
item_info = ganji['item_info']
proxy_list = [item for item in proxies.find()]


def get_links_from(channel, pages):
    proxy_item = random.choice(proxy_list)
    proxy = {
        'http:': 'http://' + proxy_item['ip'] + ':' + proxy_item['port'],
        'https:': 'http://' + proxy_item['ip'] + ':' + proxy_item['port']
    }
    time.sleep(5)
    list_view = '%so%s/' % (channel, pages)
    web_response = requests.get(list_view, proxies=proxy)

    soup = BeautifulSoup(web_response.text, 'lxml')
    if soup.find('td', 't'):
        for link in soup.select('td.t > a'):
            item_link = link.get('href').split('?')[0]
            url_list.insert_one({'url': item_link})
            print(item_link)
    elif soup.find('div', 'ft-db'):
        for link in soup.select('div.ft-db > ul > li > a'):
            item_link = link.get('href').split('?')[0]
            url_list.insert_one({'url': item_link})
            print(item_link)
    elif soup.find('div', 'zz-til'):
        for link in soup.select('div.zz-til > a'):
            item_link = link.get('href').split('?')[0]
            url_list.insert_one({'url': item_link})
            print(item_link)
    elif soup.find('p', 'infor-title'):
        for link in soup.select('p.infor-title > a'):
            item_link = 'http://sz.ganji.com' + link.get('href').split('?')[0]
            url_list.insert_one({'url': item_link})
            print(item_link)
    elif soup.find('div', 'infor01'):
        for link in soup.select('div.infor01 > a'):
            item_link = 'http://sz.ganji.com' + link.get('href').split('?')[0]
            url_list.insert_one({'url': item_link, 'is_crawler': 0})
            print(item_link)

def get_item_info(url):
    # time.sleep(2)
    proxy_item = random.choice(proxy_list)
    proxy = {
        'http:': 'http://' + proxy_item['ip'] + ':' + proxy_item['port'],
        'https:': 'http://' + proxy_item['ip'] + ':' + proxy_item['port']
    }
    web_response = requests.get(url, proxies=proxy)
    soup = BeautifulSoup(web_response.text, 'lxml')
    item = ''
    if soup.find('div', 'box_left_top'):
        title = soup.select('div.box_left_top > h1.info_titile')[0].get_text() if soup.find('div', 'box_left_top') else None
        look_time = soup.select('span.look_time')[0].get_text() if soup.find('span', 'look_time') else None
        price = soup.select('span.price_now > i')[0].get_text() if soup.find('span', 'price_now') else None
        region = soup.select('div.palce_li > span > i')[0].get_text() if soup.find('div', 'palce_li') else None
        tag = list(soup.select('div.quality')[0].stripped_strings) if soup.find('div', 'quality') else None
        item = {
            'title': title,
            'price': price,
            'look_time': look_time,
            'region': region,
            'tag': tag
        }

    elif soup.find('div', 'leftBox'):
        title = soup.select('div.col-cont.title-box > h1.title-name')[0].get_text() if soup.find('h1', 'title-name') else None
        post_time = soup.select('i.pr-5')[0].get_text() if soup.find('i', 'pr-5') else None
        if post_time.strip():
            post_time = post_time.split()[0]
        price = soup.select('i.f22.fc-orange.f-type')[0].get_text() if soup.find('i', 'f22') else None
        region = []
        for item in soup.select('ul.det-infor > li > a'):
            region.append(item.get_text())
        item = {
            'title': title,
            'price': price,
            'post_time': post_time,
            'region': region,
        }
    if item:
        item_info.insert_one(item)
        url_list.update({'url': url}, {'url': url, 'is_crawler': 1})
        print(item)

if __name__ == '__main__':
    # get_links_from('http://sz.ganji.com/xiaofeika/', 1)
    get_item_info('http://sz.ganji.com/bangong/2268633150x.htm')
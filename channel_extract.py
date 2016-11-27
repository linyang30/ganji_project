import requests
from bs4 import BeautifulSoup
from pages_parsing import ganji

second_hand_main_url = 'http://sz.ganji.com/wu/'
host_url = 'http://sz.ganji.com'
channel_list_db = ganji['channel_list_db']

def get_channel_url(url):
    web_response = requests.get(url)
    soup = BeautifulSoup(web_response.text, 'lxml')

    select_list = ['div.main-pop.{}-item > dl > dt > a'.format(i) for i in ['mob', 'baby', 'sport', 'office', 'lipin', 'live']]
    for select_item in select_list:
        for item in soup.select(select_item):
            print(host_url + item.get('href'))

channel_list = '''
        http://sz.ganji.com/shouji/
        http://sz.ganji.com/shoujipeijian/
        http://sz.ganji.com/bijibendiannao/
        http://sz.ganji.com/taishidiannaozhengji/
        http://sz.ganji.com/diannaoyingjian/
        http://sz.ganji.com/wangluoshebei/
        http://sz.ganji.com/shumaxiangji/
        http://sz.ganji.com/youxiji/
        http://sz.ganji.com/xuniwupin/
        http://sz.ganji.com/yingyouyunfu/
        http://sz.ganji.com/fushixiaobaxuemao/
        http://sz.ganji.com/meironghuazhuang/
        http://sz.ganji.com/yundongqicai/
        http://sz.ganji.com/yueqi/
        http://sz.ganji.com/tushu/
        http://sz.ganji.com/bangongjiaju/
        http://sz.ganji.com/wujingongju/
        http://sz.ganji.com/nongyongpin/
        http://sz.ganji.com/xianzhilipin/
        http://sz.ganji.com/shoucangpin/
        http://sz.ganji.com/baojianpin/
        http://sz.ganji.com/laonianyongpin/
        http://sz.ganji.com/gou/
        http://sz.ganji.com/qitaxiaochong/
        http://sz.ganji.com/xiaofeika/
        http://sz.ganji.com/menpiao/
        '''

if __name__ == '__main__':
    channel_list_db.drop()
    for channel_item in channel_list.split():
        channel_list_db.insert_one({'url': channel_item})


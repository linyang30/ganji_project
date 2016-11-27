from multiprocessing import Pool
from pages_parsing import get_links_from, get_item_info
from channel_extract import channel_list_db
from pages_parsing import url_list



def get_all_links_from(channel):
    for i in range(101):
        get_links_from(channel, i)
    channel_list_db.update(
        {'url': channel},
        {'url': channel, 'is_crawler': True}
    )


if __name__ == '__main__':
    pool = Pool()
    # pool.map(get_all_links_from, [item['url'] for item in channel_list_db.find()])
    pool.map(get_item_info, [item['url'] for item in url_list.find({'is_crawler': 0})])
    # print(url_list.find({'is_crawler': 1}).count())
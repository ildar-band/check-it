# coding: utf-8

import logging
import re

import requests
from parsel import Selector
from w3lib.html import remove_tags

logging.basicConfig(format='%(message)s', level=logging.INFO)

LIBRU_URL = 'http://az.lib.ru/d/dostoewskij_f_m/'


# :kekeke: overkill, but why not
def is_link_to_dostoewskiy(link):
    if link and re.match('text_\d+\.shtml', link):
        return True
    else:
        return False


def end_dostoewskiy_links(link):
    if link == 'text_0410.shtml':
        return True
    else:
        return False

if __name__ == '__main__':
    logging.info('Scraping texts:')
    html = requests.get(LIBRU_URL).text

    all_text = ''
    for a in Selector(html).xpath('//a'):
        link = a.xpath('.//@href').extract_first()
        if end_dostoewskiy_links(link):
            break

        if is_link_to_dostoewskiy(link):
            title = a.xpath('.//text()').extract_first()
            logging.info(title)

            url = '{}{}'.format(LIBRU_URL, link)
            html = requests.get(url).text
            text = Selector(html).css('body').extract()[0]
            text = remove_tags(text)
            all_text += text

    with open('dostoewskij.txt', 'w') as f:
        f.write(all_text)

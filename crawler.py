#!/usr/bin/env python3
# coding: utf-8

import requests
import re
from lxml import html
from lxml import etree

# proxies = {"http": "some randon proxy"} 

url = #手动加博客主页URL吧懒得改了

def get_tree(url):
    # r = requests.get(url, proxies = proxies)
    r = requests.get(url)
    tree = html.fromstring(r.content)
    return tree


def get_next_page(this_page_url):
    tree = get_tree(this_page_url)
    next_page = tree.xpath("//html/body/div[3]/div[6]/div[2]/a")
    page_link = next_page[0].get('href')
    next_page_url = url + page_link
    return next_page_url


def get_all_pages(this_page_url, list_pages):
    tree = get_tree(this_page_url)

    if tree.xpath("//div[@class='next active']"):
        new_url = get_next_page(this_page_url)
        list_pages.append(new_url)
        return get_all_pages(new_url, list_pages)

    return list_pages[::-1]


def page_article_content(page_url):
    # r = requests.get(page_url, proxies = proxies)
    r = requests.get(page_url)
    tree = etree.HTML(r.text)

    length = tree.xpath('count(//*[@class="block article"])')
    for i in range(int(length) + 1, 0, -1):
        position = 'string(/html/body/div[3]/div[' + str(i) + ']/div[2]/div[1]/div)'
        content = tree.xpath(position)
        print(content)


def get_all_page_content(url):
    ALL_PAGES = get_all_pages(url, [url])

    for article in ALL_PAGES:
        page_article_content(article)



get_all_page_content(url)



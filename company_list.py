#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import re

corps_base_url = "http://www.wooyun.org/corps/page/"

# 保存到文件里
f = open("corps.txt","w")

# 获取第一页内容并获取总页数
page = 1
response = urllib2.urlopen(corps_base_url + str(page),timeout=10)
html = response.read()
reg = r'条纪录, (\d+) 页'
page_count =  int(re.findall(re.compile(reg),html)[0])

while page <= page_count:
    response = urllib2.urlopen(corps_base_url + str(page),timeout=10)
    html = response.read()
    soup = BeautifulSoup(html,'lxml')
    table = soup.find('table',class_="listTable")
    tr_list = table.find_all("tr")
    for tr in tr_list:
        td_list = tr.find_all("td")
        join_date = td_list[0].text
        corp_name = td_list[1].text
        corp_power_link = td_list[2].a["href"].strip()
        print join_date,corp_name,corp_power_link
        if corp_power_link != "http://":
            f.write("%s\n" % (corp_power_link))
    page = page + 1

f.close()
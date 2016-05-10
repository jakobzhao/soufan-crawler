# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Feb 29, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import urllib

from pymongo import MongoClient, errors
from log import *
import time
from settings import TZCHINA
import datetime
import random
import urllib2
from bs4 import BeautifulSoup
from httplib import BadStatusLine
import platform
from selenium import webdriver
from settings import TIMEOUT, TZCHINA
from utils import get_interval_as_human
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Crawling pages from http://esf.fang.com/house/i31/
def crawler_rent(project, address, port):
    start = datetime.datetime.now()
    log(NOTICE, u'Crawling old ones')

    client = MongoClient(address, port)
    db = client[project]

    if "Linux" in platform.platform():
        pass
    else:
        browser = webdriver.PhantomJS(executable_path=r'C:\Workspace\phantomjs\bin\phantomjs.exe')

    # if "Linux" in platform.platform():
    #     display = Display(visible=0, size=(1024, 768))
    #     display.start()

    # firefox_profile = webdriver.FirefoxProfile()
    # firefox_profile.set_preference('permissions.default.image', 2)
    # firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    #
    # browser = webdriver.Firefox(firefox_profile=firefox_profile)
    #
    # browser.set_window_size(960, 1050)
    # browser.set_window_position(0, 0)

    browser.set_page_load_timeout(TIMEOUT)

    base_url = "http://esf.fang.com/house/i3"
    now = datetime.datetime.now(TZCHINA) - datetime.timedelta(minutes=10)
    i = 0
    while i < 100:
        try:
            browser.get(base_url + str(i+1) + "/")
            time.sleep(get_interval_as_human(8, 12))
            i += 1
        except BadStatusLine:
            log(WARNING, 'Bad Status')
            continue
        except TimeoutException:
            log(WARNING, 'Time out')
            continue

        soup = BeautifulSoup(browser.page_source, 'html5lib')
        items = soup.find_all('dd', class_='info rel floatr')
        for item in items:
            name = item.find("p", class_="mt10").contents[0].text
            url = "http://esf.fang.com/" + item.find("p", class_="title").contents[0].attrs['href']
            features = item.find("p", class_="title").text
            try:
                built_at = int(item.find("p", class_="mt12").contents[-1].strip()[-4:])
            except:
                built_at = 1900

            address = item.find("p", class_="mt10").contents[2].text
            comments_num = -1
            memo = u"二手"
            district = u'北京市'
            # print i, name, comments_num, memo, address, features
            # price
            try:
                price_raw = item.find("p", class_="danjia alignR mt5").contents[0][:-1]
                unit = item.find("p", class_="danjia alignR mt5").text.split(price_raw)[1]
                price = int(price_raw)
            except:
                price = 0
                unit = u"价格待定"

            print i, name, comments_num, memo, district, address, price, unit, built_at, features

            page_json = {
                "city": "bj",
                "name": name,
                "url": url,
                "cmt_count": comments_num,
                "district": district,
                "address": address,
                "price": price,
                "unit": unit,
                "features": features,
                "built_at": built_at,
                "memo": memo
            }
            try:
                db.communities.insert_one(page_json)
            except errors.DuplicateKeyError:
                log(NOTICE, 'This post has already been inserted.')

    log(NOTICE, 'Time: %d sec(s)' % int((datetime.datetime.now() - start).seconds))


# Crawling pages from http://newhouse.fang.com/house/s/b91/
def crawler_old(project, address, port):
    start = datetime.datetime.now()
    log(NOTICE, u'Crawling old ones')

    client = MongoClient(address, port)
    db = client[project]

    if "Linux" in platform.platform():
        pass
    else:
        browser = webdriver.PhantomJS(executable_path=r'C:\Workspace\phantomjs\bin\phantomjs.exe')

    # if "Linux" in platform.platform():
    #     display = Display(visible=0, size=(1024, 768))
    #     display.start()

    # firefox_profile = webdriver.FirefoxProfile()
    # firefox_profile.set_preference('permissions.default.image', 2)
    # firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    #
    # browser = webdriver.Firefox(firefox_profile=firefox_profile)
    #
    # browser.set_window_size(960, 1050)
    # browser.set_window_position(0, 0)

    browser.set_page_load_timeout(TIMEOUT)

    base_url = "http://newhouse.fang.com/house/s/b9"
    now = datetime.datetime.now(TZCHINA) - datetime.timedelta(minutes=10)
    i = 57
    while i < 120:
        try:
            browser.get(base_url + str(i+1) + "/")
            time.sleep(get_interval_as_human(8, 12))
            i += 1
        except BadStatusLine:
            log(WARNING, 'Bad Status')
            continue
        except TimeoutException:
            log(WARNING, 'Time out')
            continue

        soup = BeautifulSoup(browser.page_source, 'html5lib')
        items = soup.find_all('div', class_='sslalone')
        for item in items:
            name = item.find('div', class_="fl").contents[0].contents[0].text
            features = item.find('div', class_="fl").contents[0].contents[1].text[1:-1]
            url = item.find('div', class_="fl").contents[0].contents[0].attrs['href']
            comments_num = -1
            memo = ""

            # address
            address = item.find('div', class_="fl add").contents[1].text
            district = u'北京市'
            # print i, name, comments_num, memo, address, features
            # price
            try:
                price = int(item.find('div', class_="fr").contents[0].contents[0].text)
                unit = unicode(item.find('div', class_="fr").contents[0].contents[1])
            except:
                price = 0
                unit = u"价格待定"

            print i, name, comments_num, memo, address, price, unit, features
            page_json = {
                "city": "bj",
                "name": name,
                "url": url,
                "cmt_count": comments_num,
                "district": district,
                "address": address,
                "price": price,
                "unit": unit,
                "features": features,
                "memo": memo
            }
            try:
                db.communities.insert_one(page_json)
            except errors.DuplicateKeyError:
                log(NOTICE, 'This post has already been inserted.')

    log(NOTICE, 'Time: %d sec(s)' % int((datetime.datetime.now() - start).seconds))


# Crawling pages from http://newhouse.fang.com/house/s/b91/
def crawler(project, address, port):
    start = datetime.datetime.now()
    log(NOTICE, u'Crawling 搜房网 北京房价')

    client = MongoClient(address, port)
    db = client[project]

    # if "Linux" in platform.platform():
    #     pass
    # else:
    #     browser = webdriver.PhantomJS(executable_path=r'C:\Workspace\phantomjs\bin\phantomjs.exe')

    # if "Linux" in platform.platform():
    #     display = Display(visible=0, size=(1024, 768))
    #     display.start()

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    browser = webdriver.Firefox(firefox_profile=firefox_profile)

    browser.set_window_size(960, 1050)
    browser.set_window_position(0, 0)

    browser.set_page_load_timeout(TIMEOUT)

    base_url = "http://newhouse.fang.com/house/s/b9"
    now = datetime.datetime.now(TZCHINA) - datetime.timedelta(minutes=10)
    i = 61
    while i < 68:
        try:
            browser.get(base_url + str(i+1) + "/")
            time.sleep(get_interval_as_human(8, 12))
            i += 1
        except BadStatusLine:
            log(WARNING, 'Bad Status')
            continue
        except TimeoutException:
            log(WARNING, 'Time out')
            continue

        soup = BeautifulSoup(browser.page_source, 'html5lib')
        items = soup.find_all('div', class_='nlc_details')
        for item in items:
            name = item.find('a').text.strip()
            url = item.find('a').attrs['href']
            comments_num_raw = item.find('span', class_='value_num')
            try:
                comments_num = int(comments_num_raw.text[1:-4])
                memo = ''
            except:
                comments_num = 0
                memo = comments_num_raw

            # address
            address_raw = item.find('div', class_='address').text.strip()
            try:
                district = address_raw[1:].split("]")[0].strip()
            except:
                district = address_raw
            try:
                address = address_raw[1:].split("]")[1].strip()
            except:
                address = address_raw

            # stars
            score = 0
            try:
                stars = item.find('ul', class_='star_group').contents
            except AttributeError:
                score = -1
            if score == 0:
                for star in stars:
                    try:
                        if star.attrs['class'][0] == u"orange-star":
                            score += 1
                        if star.attrs['class'][0] == u"half-star":
                            score += 0.5
                    except:
                        pass

            # features
            featurelist = item.find('div', 'fangyuan pr').text.strip().split("\n")
            features = ''
            for f in featurelist:
                features += ' ' + f.strip()
            # price
            price_raw = soup.find('div', class_="nhouse_price")
            if price_raw.text.strip() != u"价格待定":
                try:
                    price = price_raw.contents[1].text.strip()
                    unit = price_raw.contents[2].text.strip()
                except:
                    price = 0
                    unit = u"价格待定"
            else:
                price = 0
                unit = u"价格待定"

            print i, name, score, comments_num, memo, district, address, price, unit, features
            page_json = {
                "city": "bj",
                "name": name,
                "url": url,
                "cmt_count": comments_num,
                "address": address,
                "district": district,
                "price": price,
                "unit": unit,
                "features": features,
                "memo": memo
            }
            try:
                db.communities.insert_one(page_json)
            except errors.DuplicateKeyError:
                log(NOTICE, 'This post has already been inserted.')

    log(NOTICE, 'Time: %d sec(s)' % int((datetime.datetime.now() - start).seconds))

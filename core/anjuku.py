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
def crawler_new(project, address, port):
    start = datetime.datetime.now()
    log(NOTICE, u'Crawling 安居客 新楼盘')
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

    base_url = "http://bj.fang.anjuke.com/loupan/s?p="
    city = "beijing"
    type = "NEW"
    i = 0
    while i < 34:
        try:
            browser.get(base_url + str(i+1))
            time.sleep(get_interval_as_human(3, 7))
            i += 1
        except BadStatusLine:
            log(WARNING, 'Bad Status')
            continue
        except TimeoutException:
            log(WARNING, 'Time out')
            continue

        soup = BeautifulSoup(browser.page_source, 'html5lib')
        items = soup.find_all('div', class_='item-mod')
        for item in items:
            if "data-link" not in item.attrs:
                continue
            name = item.find('a', class_="items-name").text
            url = item.find('a', class_="items-name").attrs['href']
            address_raw = item.find('p', class_='address').text.strip()
            address = address_raw.split(u"]")[1]
            district = address_raw.split(u"]")[0][1:].strip()
            # built_at = item.find('p', class_="date").text.strip().split(u"\uff1a")[1]
            try:
                features = item.find('div', class_="tag-panel").text.replace(" ", "").replace("\n", " ")
            except AttributeError:
                features = ""

            # price
            if item.find('p', class_="price") != None:
                try:
                    price = int(item.find('p', class_="price").contents[1].text)
                    unit = unicode(item.find('p', class_="price").contents[0]) + u" " + unicode(item.find('p', class_="price").contents[2])
                except:
                    price = 0
                    unit = u"售价待定"
            else:
                price = 0
                unit = u"售价待定"

            print i, name, type, district, address, price, unit, features, url
            page_json = {
                "city": city,
                "name": name,
                "type": type,
                "built_at": "",
                "url": url,
                "address": address,
                "district": district,
                "price": price,
                "unit": unit
            }
            try:
                db.communities.insert_one(page_json)
            except errors.DuplicateKeyError:
                log(NOTICE, 'This post has already been inserted.')

    log(NOTICE, 'Time: %d sec(s)' % int((datetime.datetime.now() - start).seconds))


# Crawling pages from http://newhouse.fang.com/house/s/b91/
def crawler(project, address, port):
    start = datetime.datetime.now()
    log(NOTICE, u'Crawling 安居客')

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
    city = "beijing"
    base_url = "http://" + city + ".anjuke.com/community/p"

    type = "SH"
    i = 0
    while i < 1000:
        try:
            browser.get(base_url + str(i+1) + "/")
            time.sleep(get_interval_as_human(3, 7))
            i += 1
        except BadStatusLine:
            log(WARNING, 'Bad Status')
            continue
        except TimeoutException:
            log(WARNING, 'Time out')
            continue

        soup = BeautifulSoup(browser.page_source, 'html5lib')
        items = soup.find_all('div', class_='li-itemmod')
        for item in items:
            name = item.find('h3').text.strip()
            url = "http://" + city + ".anjuke.com" + item.find('a').attrs['href']
            address_raw = item.find('address').text.strip()
            address = address_raw.split(u"\uff3d")[1]
            district = address_raw.split(u"\uff3d")[0][1:]
            built_at = item.find('p', class_="date").text.strip().split(u"\uff1a")[1]

            # price
            try:
                price = int(item.find('div', class_="li-side").contents[1].contents[1].text)
                unit = item.find('div', class_="li-side").contents[1].contents[2].strip()
            except:
                price = 0
                unit = u"价格待定"

            print i, name, type, district, address, price, unit
            page_json = {
                "city": city,
                "name": name,
                "type": type,
                "built_at": built_at,
                "url": url,
                "address": address,
                "district": district,
                "price": price,
                "unit": unit
            }
            try:
                db.communities.insert_one(page_json)
            except errors.DuplicateKeyError:
                log(NOTICE, 'This post has already been inserted.')

    log(NOTICE, 'Time: %d sec(s)' % int((datetime.datetime.now() - start).seconds))


# Crawling pages from http://newhouse.fang.com/house/s/b91/
def crawler_community(project, address, port):
    start = datetime.datetime.now()
    log(NOTICE, u'Crawling 安居客 小区')

    client = MongoClient(address, port)
    db = client[project]

    # Deployment
    if "Linux" in platform.platform():
        pass
        # display = Display(visible=0, size=(1024, 768))
        # display.start()
    else:
        browser = webdriver.PhantomJS(executable_path=r'C:\Workspace\phantomjs\bin\phantomjs.exe')

    # Debugging
    # firefox_profile = webdriver.FirefoxProfile()
    # firefox_profile.set_preference('permissions.default.image', 2)
    # firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    # browser = webdriver.Firefox(firefox_profile=firefox_profile)
    # browser.set_window_size(960, 1050)
    # browser.set_window_position(0, 0)

    # Execution
    browser.set_page_load_timeout(TIMEOUT)
    # search_json = {'type': 'SH'}
    search_json = {"$and": [{'type': 'SH'},{'p_co': {'$exists': False}}]}
    coms = db.communities.find(search_json)
    count = coms.count()
    print count
    i = 0
    communities = []
    for com in coms:
        community = {
            'url': com['url'],
            'name': com['name'],
            'built_at': com['built_at']
        }
        communities.append(community)

    # for community in communities[7001:8000]:
    for community in communities:
        try:
            print community['url']
            browser.get(community['url'])
            time.sleep(get_interval_as_human(2, 3))
            i += 1
        except BadStatusLine:
            log(WARNING, 'Bad Status')
            continue
        except TimeoutException:
            log(WARNING, 'Time out')
            continue
        except errors.CursorNotFound:
            log(WARNING, 'Cursor not found')
            continue
        soup = BeautifulSoup(browser.page_source, 'html5lib')

        r_co, p_type, p_co, p_payment, t_area, t_units, built_at, rental_ratio, far, park, green, desc = "", "", "", "", "", "", "", "", "", "", "", ""

        j = 0
        while True:
            try:
                lines = len(soup.find('dl', class_="comm-l-detail float-l").contents)
                break
            except:
                time.sleep(600)

        while j < lines:
            item = soup.find('dl', class_="comm-l-detail float-l").contents[j]
            if unicode(item).strip() == u"":
                j += 1
                continue
            item = item.text.strip()
            try:
                value = soup.find('dl', class_="comm-l-detail float-l").contents[j+1].text.strip()
            except:
                value = ""
            if item == u"开发商":
                r_co = value

            if item == u"物业类型":
                p_type = value

            if item == u"物业公司":
                p_co = value

            if item == u"物业费用":
                p_payment = value
            j += 1

        j = 0
        while True:
            try:
                lines = len(soup.find('dl', class_="comm-r-detail float-r").contents)
                break
            except:
                time.sleep(600)

        while j < lines:
            item = soup.find('dl', class_="comm-r-detail float-r").contents[j]
            if unicode(item).strip() == u"":
                j += 1
                continue
            item = item.text.strip()
            try:
                value = soup.find('dl', class_="comm-r-detail float-r").contents[j+1].text.strip()
            except:
                value = ""

            if item == u"总建面":
                t_area = value
            if item == u"总户数":
                t_units = value
            if item == u"建造年代":
                built_at = value
            if item == u"容积率":
                if value == u"暂无数据":
                    far = 0
                else:
                    try:
                        far = float("0" + value)
                    except UnicodeEncodeError:
                        far = value
                    except ValueError:
                        far = value
            if item == u"出租率":
                rental_ratio = value
            if item == u"停车位":
                park = value
            if item == u"绿化率":
                green = value
            j += 1
        try:
            desc = soup.find('div', class_="comm-description").text.strip()
        except:
            desc = ""

        if community["built_at"] != u"暂无数据":
            built_at = community["built_at"]

        page_json = {
            "r_co": r_co,
            "p_type": p_type,
            "p_co": p_co,
            "p_payment": p_payment,
            "t_area": t_area,
            "t_units": t_units,
            "built_at": built_at,
            "rental_ratio": rental_ratio,
            "far": far,
            "park": park,
            "green": green,
            "desc": desc
        }

        print i, community['name'], r_co, p_type, p_co, p_payment, t_area, t_units, built_at, rental_ratio, far, park, green
        db.communities.update({'name': community['name']}, {'$set': page_json})

    log(NOTICE, "mission completes.")
    log(NOTICE, 'Time: %d sec(s)' % int((datetime.datetime.now() - start).seconds))

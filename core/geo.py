# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import urllib2
import json
import sys
import time
from settings import BAIDU_AK
from log import *

reload(sys)
sys.setdefaultencoding('utf-8')


def geocode(loc):
    lat, lng = -1, -1
    url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=%s' % (loc, BAIDU_AK)
    others = [u'其他', u'美国', u'英国', u'澳大利亚', u'伊朗', u'台湾', u'沙特阿拉伯',
              u'爱尔兰', u'印度', u'印尼', u'奥地利', u'挪威', u'乌克兰', u'瑞士',
              u'西班牙', u'古巴', u'挪威', u'德国', u'埃及', u'巴西', u'比利时']
    if loc in others:
        pass
    else:
        try:
            response = urllib2.urlopen(url.replace(' ', '%20'))
        except urllib2.HTTPError, e:
            log(WARNING, e, 'geocode')
        try:
            loc_json = json.loads(response.read())
            lat = loc_json[u'result'][u'location'][u'lat']
            lng = loc_json[u'result'][u'location'][u'lng']
        except ValueError:
            log(ERROR, "No JSON object was decoded", 'geocode')
        except KeyError, e:
            log(ERROR, e.message, 'geocode')
        # time.sleep(2)
    return [lat, lng]


def geocode_locational_info(project, address, port):
    from pymongo import MongoClient
    client = MongoClient(address, port)
    db = client[project]
    #search_json = {'$or': [{'latlng': [0, 0]}, {'latlng': [-1, -1]}], 'location': {'$ne': ''}}
    search_json = {'lat': 0}
    communities = db.communities.find(search_json)
    count = communities.count()
    print count
    i = 0
    for community in communities:
        i += 1
        latlng = geocode(u"北京" + community['address'])

        print i, community['name'], latlng
        db.communities.update({'name': community['name']}, {'$set': {'lat': latlng[0], 'lng': latlng[1]}})

    log(NOTICE, "mission completes.")

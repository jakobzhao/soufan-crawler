# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Feb 25, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from core.anjuku import *
from core.log import *

import datetime

from settings import SETTINGS


start = datetime.datetime.now()
log(NOTICE, 'Anjuke Crawler Initializing...')

#crawler(SETTINGS['project'], SETTINGS['address'], SETTINGS['port'])
crawler_community(SETTINGS['project'], SETTINGS['address'], SETTINGS['port'])

log(NOTICE, 'Mission completes. Time: %d sec(s)' % (int((datetime.datetime.now() - start).seconds)))

if __name__ == '__main__':
    pass

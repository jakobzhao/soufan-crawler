# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Feb 25, 2016
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

from core.log import *
from core.geo import *
import datetime

from settings import SETTINGS

start = datetime.datetime.now()
log(NOTICE, 'Geocode Initializing...')

geocode_locational_info(SETTINGS['project'], SETTINGS['address'], SETTINGS['port'])

log(NOTICE, 'Mission completes. Time: %d sec(s)' % (int((datetime.datetime.now() - start).seconds)))

if __name__ == '__main__':
    pass
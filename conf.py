#!/usr/bin/env python
# coding: utf-8

# API request configurations
site_id = "norwich-pear-tree"
base_url = 'https://api.krakenflex.systems/interview-tests-mock-api/v1/'
headers = {'Accept': 'application/json', 
           "x-api-key": "EltgJ5G8m44IzwE6UN2Y4B4NjPW77Zk6FJK3lL23", 
           "Content-Type": "application/json"}

# URL's
outages_url = base_url + "outages"
site_info_url = base_url + "site-info" + "/" + site_id
results_url = base_url + "site-outages" + "/" + site_id

# Filters
date_filter = "2022-01-01T00:00:00.000Z"
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Author: nols

import geoip2.database
def search(ip):
    Geoip2 = r'/Users/nols/Downloads/GeoLite2-City_20200707/GeoLite2-City.mmdb'
    client = geoip2.database.Reader(Geoip2)
    ip_location = client.city(ip)
    country = ip_location.country.names['zh-CN']
    try:
        city = ip_location.city.names['zh-CN']
    except:
        city = ''
        pass

    location = country + ' ' +city
    return location



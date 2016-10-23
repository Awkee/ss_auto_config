#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    Brief:
        根据ss站点提供的免费SS服务配置信息，自动生成config.json配置文件
        通常情况下，我们可以手工配置，但是能自动化岂不是更好。
    Author : zwker <next4nextjob at gmail.com>
    Created: 2016/10/23
    Python Version: 2.7.X
'''

import urllib2
import re
import json

url = 'http://www.ishadowsocks.org'
req = urllib2.Request(url)
con = urllib2.urlopen(req)
doc = doc = ''.join(con.readlines())

#拿网页里的密码
pattern = re.compile(r'C密码(.*)')
match = pattern.search(doc)

if match:
    content = match.group()
    ## 获取密码
    psd = content.split(':')[1].split('<')[0]

else:
    print 'match fail'

file_obj = open('/etc/shadowsocks/config.json.mod')
jsonfile = file_obj.read()
print jsonfile
conf_json = json.loads(jsonfile)
conf_json['password'] = psd
jsonfile = json.dumps(conf_json,sort_keys=True, indent=4)
file_obj.close()
file_obj = open('/etc/shadowsocks/config.json', 'w')
file_obj.write(jsonfile)
file_obj.close()

con.close()

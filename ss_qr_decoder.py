#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    Brief:
        根据ss站点提供的免费SS服务的二维码，自动解码并生成config.json配置文件
        通常情况下，我们可以手工配置，但是能自动化岂不是更好。
    Author : zwker <next4nextjob at gmail.com>
    Created: 2016/10/23
    Python Version: 2.7.X
    依赖包：zbar,wget
    安装方法：
        pip install zbar wget
    说明：安装zbar可能会失败，失败情况下需要安装`libzbar-dev`包，安装方法：以ubuntu为例：sudo apt-get install libzbar-dev
'''
import json
import zbar
import Image
import wget
import base64
import os

ss_url="http://www.shadowsocks8.net/images/server03.png"

ss_filename=wget.download( ss_url );
if os.path.isfile(ss_filename) :
    # create a scanner
    scanner = zbar.ImageScanner()
    # configurue the reader
    scanner.parse_config('enable')
    # obtain the image data
    pil = Image.open( ss_filename ).convert('L')
    width, height = pil.size
    raw = pil.tobytes()

    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)
    # scan the image for barcodes
    scanner.scan(image)
    # extract results
    for symbol in image:
        # do something useful with results
        if symbol.data.startswith("ss://" ) :
            result = base64.decodestring( symbol.data[5:] )
        server_user = result.split(':')[1].split('@')
        print 'decoded', symbol.type, 'symbol', '"%s"'  % symbol.data
        print 'result:',result,"密码:",server_user[0]
    # clean up
    del(image)
os.remove(ss_filename)

file_obj = open('/etc/shadowsocks/config.json.qr')
jsonfile = file_obj.read()
print jsonfile
conf_json = json.loads(jsonfile)
conf_json['password'] = server_user[0]
print conf_json
jsonfile = json.dumps(conf_json,sort_keys=True, indent=4)
print jsonfile
file_obj.close()
file_obj = open('/etc/shadowsocks/config.json', 'w')
file_obj.write(jsonfile)
file_obj.close()

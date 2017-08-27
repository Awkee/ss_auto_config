#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# Author: zwker
# mail: xiaoyu0720@gmail.com
# Created Time: 2017年08月27日 星期日 09时55分19秒
#########################################################################

import urllib2

import sys 
import re
import json
import zbar
import Image
import wget
import base64
import os
import argparse
import atexit
from shadowsocks.local import main 




def get_parser():
    parser = argparse.ArgumentParser(description = u"decode the ss-qrcode-url and generate the config.json file for your shadowsocks client", epilog="this will help set the shadowsocks config.json faster.")
    parser.add_argument("-c", "--config" , nargs = '?' , default = 'config.json' , help = 'set the output filename, default ./config.json' )
    parser.add_argument("-d", "--daemon" , nargs = '?' , metavar = 'start/stop/restart' , choices = [ 'start','stop','restart'] , default = 'start' , help = 'daemon mode')
    parser.add_argument("-p", "--pid-file" , nargs = '?' , default = 'ss.pid' , help = 'pid file for daemon mode')
    parser.add_argument("-l", "--log-file" , nargs = '?' , default = 'ss.log' , help = 'log file for daemon mode')
    parser.add_argument("-q", "--quiet-mode" ,  action = 'store_false' ,  help = 'quiet mode, only show warnings/errors')
    parser.add_argument("ss_qrcode_url", nargs = '?' , default = 'http://ss.ishadowx.com/img/qr/jpa.png', help = 'shadowsocks qrcode png image url' )
    return parser.parse_args()


def decode_qrcode( qrcode_file):
    '''
    decode the qrcode png image file,then return the image object result
    '''
    if  os.path.isfile( qrcode_file ) :
        # create a scanner
        scanner = zbar.ImageScanner()
        # configurue the reader
        scanner.parse_config('enable')
        # obtain the image data
        pil = Image.open( qrcode_file ).convert('L')
        width, height = pil.size
        raw = pil.tobytes()
        # wrap image data
        image = zbar.Image(width, height, 'Y800', raw)
        # scan the image for barcodes
        scanner.scan(image)
    else:
        print "qrcode image file[" + qrcode_file + "] is not a file ."

    return image



def main_task():
    '''
    功能为根据指定的 ss-qrcode-url 获取ss配置信息并输出为config文件

    1. 获取SS-QRCode的png文件
    2. 通过Image获取ss-url信息 
    3. 使用base64解析ss-url信息
    4. 解析解码后的ss配置信息
    5. 根据解析后的配置生成json配置文件config.json
    '''

    args = get_parser()
    print args

    try:
        ss_filename = wget.download( args.ss_qrcode_url )
        print ss_filename
        image = decode_qrcode( ss_filename)

        for symbol in image:
            # do something useful with results
            if symbol.data.startswith("ss://" ) :
                result = base64.decodestring( symbol.data[5:] )
            server_info = result.split(':')
            server_user = server_info[1].split('@')
            method , password , server_ip , server_port  = server_info[0], server_user[0],server_user[1],server_info[2]
            print 'decoded', symbol.type, 'symbol', '"%s"'  % symbol.data
            print 'result:[' + result + "]"
            print method , password , server_ip , server_port 
            server_port = int(server_port)

    finally:
        # clean up
        os.remove(ss_filename)


    ## 5.generate config.json file
    args.config = os.path.realpath(args.config)

    file_obj = open( args.config , 'w')
    #print jsonfile
    conf_json = dict()
    conf_json['fast_open'] = False
    conf_json['local_address'] = '0.0.0.0'
    conf_json['local_port'] = 1080 
    conf_json['method'] = method
    conf_json['password'] = password
    conf_json['server'] = server_ip
    conf_json['server_port'] = server_port
    conf_json['timeout'] = 600
    conf_json['workers'] = 1

    #print conf_json
    jsonfile = json.dumps(conf_json,sort_keys=True, indent=4)
    print jsonfile
    file_obj.write(jsonfile)
    file_obj.close()

    sys.argv = [ sys.argv[0] , "-c" , args.config , '-d', args.daemon , '-q', '--pid-file', args.pid_file , '--log-file', args.log_file ]
    if  args.quiet_mode :
        sys.argv += "-q" 
    print sys.argv
    sys.exit(main())



if __name__ == "__main__" :
    print sys.argv
    main_task()


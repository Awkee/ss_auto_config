# ss_auto_config

This is a tool for shadowsocks client in linux , you can use it to generate config.json file from some ss free website qr-code or ss uri address

This is a auto-configuration demo for shadowsocks client.
If you have any better tools or method , I wish you may email or leave a message to me to share . 

# about SS URI and QR code


Shadowsocks for Android / iOS also accepts BASE64 encoded URI format configs:

    ss://BASE64-ENCODED-STRING-WITHOUT-PADDING

Where the plain URI should be:

    ss://method[-auth]:password@hostname:port

For example, we have a server at 192.168.100.1:8888 using bf-cfb encryption method and password test with onetime authentication enabled. Then, with the plain URI ss://bf-cfb-auth:test@192.168.100.1:8888, we can generate the BASE64 encoded URI:

    ss://YmYtY2ZiLWF1dGg6dGVzdEAxOTIuMTY4LjEwMC4xOjg4ODg

This URI can also be encoded to QR code. Then, just scan it with your Android / iOS devices:


[Click this for More](https://shadowsocks.org/en/config/quick-guide.html)


# about autoss
> if you always use shadowsocks to browser google / duckduckgo or youtube website , may be you will like it.

## Overview

`autoss.py`  can download the ss-qrcode-url image , decode it  and format the config info into the config.json file , which you can use to start the ss client service.

## Requirement

- `zbar` : use to decode qrcode image
- `wget` : use to download the url image file 
- `shadowsocks` : use to start shadowsocks client service,like sslocal script file





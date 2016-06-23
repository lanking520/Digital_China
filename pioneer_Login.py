"""
Name: Pioneer Login System in Python
Date: 2016-06-23
Author: Qing Lan
Copyright: Personal and Test Team in "iQuicker"
License: MIT
"""
import cookielib
import urllib2
import urllib
import json

"""
loginUrl = "http://www.baidu.com/"
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
resp = urllib2.urlopen(loginUrl)
for index, cookie in enumerate(cj):
    print '[',index, ']',cookie
"""
iQuickerUrl = "https://www.iquicker.com.cn/iquicker_web/login"
my_dict={"username":"18146618480","password":"MTIzNDU2Nzg=","rememberMe":True}
encodedjson = json.dumps(my_dict)
#postData = urllib.urlencode({"username":"18146618480","password":"MTIzNDU2Nzg=","rememberMe":True})
#org":"0000000053e5da3f0153e9286ae9000f" try it after first success
print "postData=", encodedjson
req = urllib2.Request(iQuickerUrl, encodedjson)
print req
req.add_header('Content-Type', "application/json")
resp = urllib2.urlopen(req)
print resp.read()
print 'geturl=',resp.geturl()

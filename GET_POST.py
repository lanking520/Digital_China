import cookielib
import urllib2
import urllib
import json

iQuickerUrl = "https://www.iquicker.com.cn/iquicker_web/login"
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
my_dict={"username":"18146618480","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff8080815379364f0153892a6cce00ec"}
scheduleappurl = "https://www.iquicker.com.cn/iquicker_web/schedul/app"

def INITCOOKIES():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

def POST(url, data, header_type = "application/json", encodejson = True):
    if encodejson:
        data = json.dumps(data)
        req = urllib2.Request(url, data)
    else:
        data = urllib.urlencode(data)
        req = urllib2.Request(iQuickerUrl, data)
    req.add_header('Content-Type', header_type)
    resp = urllib2.urlopen(req)
    print resp.read()

def GET(url, header_type = "application/json"):
    req = urllib2.Request(url)
    req.add_header('Content-Type', header_type)
    resp = urllib2.urlopen(req)
    print resp.read()

POST(iQuickerUrl, my_dict)
GET(scheduleappurl)

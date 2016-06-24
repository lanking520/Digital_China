"""
Name: Working Example for the News System
Author: Qing Lan
Copyright: Personal and Test Team in "iQuicker"
Description: Comparing to Milestone two, one News Class is created to regularize the test subjects
"""
import cookielib
import urllib2
import urllib
import json


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
# Let the single cookie system override the current openurl
my_dict={"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}

def INITCOOKIES():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

def COOKIE_TO_FILE(filename):
    cookie = cookielib.MozillaCookieJar(filename)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    response = opener.open("http://www.baidu.com")
    cookie.save(ignore_discard=True, ignore_expires=True)

def FILE_TO_COOKIE(filename):
    cookie = cookielib.MozillaCookieJar()
    #Initiallize the Cookies environment
    cookie.load(filename, ignore_discard=True, ignore_expires=True)
    req = urllib2.Request("http://www.baidu.com")
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    #opener are similar to urlopen and have the equal functionalities
    response = opener.open(req)
    print response.read()

def POST(url, data, header_type = "application/json", encodejson = True):
    if encodejson:
        data = json.dumps(data)
        req = urllib2.Request(url, data)
    else:
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
    req.add_header('Content-Type', header_type)
    source_code = ErrorOut(req)
    print json.loads(source_code)['message']
    return source_code

def GET(url,data = "", header_type = "application/json",encodejson = False):
    if encodejson:
        data = json.dumps(data)
    else:
        data = urllib.urlencode(data)
    geturl = url + "?" + data
    req = urllib2.Request(geturl)
    req.add_header('Content-Type', header_type)
    source_code = ErrorOut(req)
    print json.loads(source_code)['message']
    return source_code

def DELETE(url,data = "", header_type = "application/json",encodejson = True):
    #Without Functionality test
    if encodejson:
        data = json.dumps(data)
    else:
        data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    req.add_header('Content-Type', header_type)
    req.get_method = lambda: 'DELETE'
    source_code = ErrorOut(req)
    print json.loads(source_code)['message']
    return source_code

def PUT(url,data = "", header_type = "application/json",encodejson = True):
    if encodejson:
        data = json.dumps(data)
    else:
        data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    req.add_header('Content-Type', header_type)
    req.get_method = lambda: 'PUT'
    resp = ErrorOut(req)
    source_code = ErrorOut(req)
    print json.loads(source_code)['message']
    return source_code

def ErrorOut(req):
    #Later for using in the test
    try:
        resp = urllib2.urlopen(req)
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
        else:
            print "OK"
    print "Passed Basic Access!"
    return resp.read()

class News:
    def __init__(self):
        self.url_manager = []
        self.iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
        self.newsurl = "http://testwww.iquicker.com.cn/iquicker_web/newstype/datas"
        self.all_news = "http://testwww.iquicker.com.cn/iquicker_web/news/datas"
        self.news_id = "http://testwww.iquicker.com.cn/iquicker_web/news/data/num"
        self.news_root = "http://testwww.iquicker.com.cn/iquicker_web/news/data/"
        self.id_info = ""
        self.data_manager = []
        self.my_dict = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
        self.all_news_data = {"pageNo" : 1, "pageSize" : 20, "sortInfo" : "DESC_isUp_isUpTime_publishTime"}

    def Login_to_system(self):
        print "in Login System..."
        POST(self.iQuickerUrl, self.my_dict)

    def get_news_type(self):
        print "in News Type..."
        GET(self.newsurl)


    def get_news_data(self):
        print "in news Data..."
        Dict = GET(self.all_news, self.all_news_data)
        Dict = json.loads(Dict)
        #print Dict
        Dict = Dict['data']['list'][0]
        self.id_info = Dict['id']

    def get_news_id(self):
        print "in news id..."
        GET(self.news_root + str(self.id_info))

My_news = News()
My_news.Login_to_system()
My_news.get_news_data()
My_news.get_news_id()
My_news.get_news_type()

'''
iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
my_dict = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
POST(iQuickerUrl, my_dict)
newsurl = "http://testwww.iquicker.com.cn/iquicker_web/newstype/datas"
GET(newsurl)
all_news = "http://testwww.iquicker.com.cn/iquicker_web/news/datas"
all_news_data = {"pageNo" : 1, "pageSize" : 20, "sortInfo" : "DESC_isUp_isUpTime_publishTime"}
news_data_dict = GET(all_news, all_news_data)
news_id = "http://testwww.iquicker.com.cn/iquicker_web/news/data/num"
GET(news_id)

news_data_dict = json.loads(news_data_dict)
#print news_data_dict
news_data_dict = news_data_dict['data']['list'][0]
news_data_dict = news_data_dict['id']

news1 = "http://testwww.iquicker.com.cn/iquicker_web/news/data/"+str(news_data_dict)
GET(news1)
'''


#for item in cj:
#    print 'Name = '+item.name
#    print 'Value = '+item.value

'''
Name: Qing Lan
Copyright: Personal and 'iQuicker' Test team
Date: 2016-06-24
Description: The test on the Task functions
'''
import cookielib
import urllib2
import urllib
import json


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
# Let the single cookie system override the current openurl
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
    try:
        print json.loads(source_code)['message']
    except:
        print "Faulty Data Structure!"
    #print source_code
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
    try:
        print json.loads(source_code)['message']
    except:
        print "Faulty Data Structure!"
    #print source_code
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
    try:
        print json.loads(source_code)['message']
    except:
        print "Faulty Data Structure!"
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
    try:
        print json.loads(source_code)['message']
    except:
        print "Faulty Data Structure!"
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

#Login the system
iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
my_dict = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
POST(iQuickerUrl, my_dict)
#personal_info
get_personal = "http://testwww.iquicker.com.cn/iquicker_web/login/user"
GET(get_personal)
#Get_user_data
Get_user_data = "http://testwww.iquicker.com.cn/iquicker_web/mobile/ad_books"
user_data = GET(Get_user_data)
user_data = json.loads(user_data)
id_book = []
name_book = []
for i in range(len(user_data)):
    id_book.append(user_data[i]['uuid'])
    name_book.append(user_data[i]['name'])

#reach to the Tasks Section
Tasks_url = "http://testwww.iquicker.com.cn/iquicker_web/task/tasks"
Data_tasks = {"isOver" : False, "page" : 1, "pageSize" : 20, "sortType" : 1, "type" : 0}
Task_info = GET(Tasks_url,Data_tasks)
Task_id = []
Task_info = json.loads(Task_info)
Task_info = Task_info['data']['content']
for i in range(len(Task_info)):
    Task_id.append(Task_info[i]['id'])

#Start Posting Tasks!
Post_task_url = "http://testwww.iquicker.com.cn/iquicker_web/task/tasks"
Post_kernel = {"subject" : "RobotSend", "principals" : [{"id": id_book[0] , "name": name_book[0]}], "participants":[{"id": id_book[0] , "name": name_book[0]}], "endDate" : "2017-06-24T16:00:00.000Z", "priority" : 3, "detail" : "This is a Test Message" , "shared" : False , "publishScope" : ["company"], "publishScopeName" : ["/u5168/u516C/u53F8"]}
POST(Post_task_url,Post_kernel)


#Start Modifying Tasks!
Post_task_url = "http://testwww.iquicker.com.cn/iquicker_web/task/tasks"
Post_kernel = {"id": Task_id[-1], "subject" : "RobotSendModify", "principals" : [{"id": id_book[0] , "name": name_book[0]}], "participants":[{"id": id_book[0] , "name": name_book[0]}], "endDate" : "2017-06-24T16:00:00.000Z", "priority" : 3, "detail" : "This is a Modified Message" , "shared" : False ,"attList": None, "publishScope" : ["company"], "publishScopeName" : ["/u5168/u516C/u53F8"]}
POST(Post_task_url,Post_kernel)


#Start Delete the Task!
Delete_url = "http://testwww.iquicker.com.cn/iquicker_web/task/tasks/" + str(Task_id[-1])
#go_To_TASK
DELETE(Delete_url)


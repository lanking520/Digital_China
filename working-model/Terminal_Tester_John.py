'''
Name: Terminal Tester For iQuicker
Author: Qing Lan
Date: 2016-08-09
Copyright: Personal
Description: This working model are tested and verified. It improve the outcome of the result
'''
# -*- coding: utf-8 -*-
import cookielib
import urllib2
import urllib
import json
import time
import csv
import codecs

# Default Settings for a system to keep cookies, please add it before testing
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
# Let the single cookie system override the current openurl
# Cookies Info
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
    # Initiallize the Cookies environment
    cookie.load(filename, ignore_discard=True, ignore_expires=True)
    req = urllib2.Request("http://www.baidu.com")
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    # opener are similar to urlopen and have the equal functionalities
    response = opener.open(req)
    print response.read()

# Helper Functions
def get_current_time():
    #获取当前时间(标准格式)
    return time.strftime("%Y-%m-%d %H:%M:%S")

def get_raw_time():
    #获取当前时间(数字串)
    return time.time()

def title_exporter(dictionary):
    #剖析结构,获取标题,并保留原有结构
    my_dict_titles = []
    try:
        my_dict_titles.append(dictionary.keys())
        for key in dictionary:
            if isinstance(dictionary[key], dict):
                my_dict_titles.append(title_exporter(dictionary[key]))
            if isinstance(dictionary[key], list):
                if len(dictionary[key]):
                    if isinstance(dictionary[key][0],dict):
                        my_dict_titles.append(title_exporter(dictionary[key][0]))
    except:
        if isinstance(dictionary, list):
            my_dict_titles.append(title_exporter(dictionary[0]))
    #print my_dict_titles
    return my_dict_titles

def comparator(actual_data, template_data):
    #匹配内容数量是否相同
    actual_data = list_to_dict(name_extractor(actual_data))
    template_data = list_to_dict(name_extractor(template_data))
    missing_list = []
    for key in template_data.keys():
        try:
            key_result = template_data[key] - actual_data[key]
        except:
            missing_list.append(key)
            key_result = 0
        if (key_result < 0):
            missing_list.append(key)

    return missing_list

def list_to_dict(my_list):
    #在一个没有结构体的纯字符串数组中生成哈西图
    my_dict = {}
    for i in my_list:
        if my_dict.has_key(i):
            #dict.has_key 如果有存在的标题,返回值0
            my_dict[i] += 1
        else:
            my_dict[i] = 1
    return my_dict

def name_extractor(my_array):
    #破坏数组结构体,提取所有标题并存在一个数组里
    result_array = []
    for i in range(len(my_array)):
        if isinstance(my_array[i], list):
            result_array.extend(name_extractor(my_array[i]))
        else:
            result_array.append(my_array[i])
        result_array.sort()
    return result_array

def sort_my_array(my_array):
    #给复杂数组排序
    result_array = []
    for i in range(len(my_array)):
        if isinstance(my_array[i], list):
            result_array.append(sort_my_array(my_array[i]))
        else:
            result_array.append(my_array[i])
    result_array.sort()
    return result_array

def remove_duplications(my_array = []):
    # Only applicable to sorted array
    # 去除同类项
    final_array = [my_array[0]]
    for i in range(len(my_array)):
        if (final_array[-1] != my_array[i]):
            final_array.append(my_array[i])
    return final_array

# Major Functions
def POST(url, data, header_type = "application/json",encodejson = True):
    if encodejson:
        data = json.dumps(data)
        #以json格式转换
        req = urllib2.Request(url, data)
        #准备一个发到服务器的包
    else:
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
    req.add_header('Content-Type', header_type)
    #加标题头
    source_code = ErrorOut(req)
    try:
        print json.loads(source_code)['message']
        #json.loads()[标准json方式读取]
    except:
        print "Faulty Data Structure!"
        #没有message的情况
    # print source_code
    return source_code

def GET(url,data = "", header_type = "application/json",encodejson = False):
    if encodejson:
        data = json.dumps(data)
    else:
        data = urllib.urlencode(data)
    geturl = url + "?" + data
    #print geturl
    req = urllib2.Request(geturl)
    req.add_header('Content-Type', header_type)
    source_code = ErrorOut(req)
    try:
        print json.loads(source_code)['message']
    except:
        print "Faulty Data Structure!"
    # print source_code
    return source_code

def DELETE(url,data = "", header_type = "application/json",encodejson = True):
    # Without Functionality test
    if encodejson:
        data = json.dumps(data)
    else:
        data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    req.add_header('Content-Type', header_type)
    req.get_method = lambda: 'DELETE'
    #通过官方文件查的,需要仔细看看
    source_code = ErrorOut(req)
    try:
        print json.loads(source_code)['message']
    except:
        print "Faulty Data Structure!"
    return source_code

def PUT(url, data = "", header_type = "application/json", encodejson = True):
    if encodejson:
        data = json.dumps(data)
    else:
        data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    req.add_header('Content-Type', header_type)
    req.get_method = lambda: 'PUT'
    source_code = ErrorOut(req)
    try:
        print json.loads(source_code)['message']
    except:
        print "Faulty Data Structure!"
    return source_code


def ErrorOut(req):
    #Later for using in the test
    try:
        #发包
        resp = urllib2.urlopen(req)
        #resp=返回值
        #print "Passed Basic Access!"
        return resp.read()
        #resp.read()返回json格式的返回值
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
        else:
            print "OK"
        return None

class News:
    def __init__(self):
        #self.url_manager = []
        #批量导入url的功能没有做,但是加入会更便捷
        self.iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
        self.newsurl = "http://testwww.iquicker.com.cn/iquicker_web/newstype/datas"
        self.all_news = "http://testwww.iquicker.com.cn/iquicker_web/news/datas"
        self.news_id = "http://testwww.iquicker.com.cn/iquicker_web/news/data/num"
        self.news_root = "http://testwww.iquicker.com.cn/iquicker_web/news/data/"
        self.id_info = ""
        self.data_manager = []
        self.function_name = {"login" : 1, "Get News Type" : 2, "Get News data" : 3, "Get News ID" : 4}
        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0

        self.class_name = str(self.__class__).split('__main__.')[1]
        self.result_dict = {self.class_name : []}

    def Login_to_system(self):
        print "in Login System..."
        kernel = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
        template = [[u'status', u'message', u'data', u'success'], [[u'orgs', u'initialised']]]
        self.determine_error(POST(self.iQuickerUrl, kernel), "login",template, self.iQuickerUrl)
        self.times += 1

    def get_news_type(self):
        print "in News Type..."
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'createDate', u'shareUserIds', u'companyName', u'write', u'typeName',
                      u'readRight', u'writeRight', u'createUser', u'org', u'id', u'attList']]]

        self.determine_error(GET(self.newsurl), "Get News Type", template, self.newsurl)
        self.times += 1


    def get_news_data(self):
        print "in news Data..."
        kernel = {"pageNo" : 1, "pageSize" : 20, "sortInfo" : "DESC_isUp_isUpTime_publishTime"}
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'totalpage', u'list'],
                     [[u'stores', u'userId', u'picObj', u'id', u'write', u'title', u'createDate',
                       u'tags', u'content', u'publishScope', u'department', u'type', u'isUpTime',
                       u'companyName', u'circlePicPath', u'contentTitle', u'readRight', u'createUser',
                       u'org', u'userName', u'shareUserIds', u'publishTime', u'isUp', u'writeRight',
                       u'attList', u'mobilePicPath', u'discusses', u'isFile', u'browses', u'isCirclePic'],
                      [[u'src', u'selection', u'thumbnail']],
                      [[u'createDate', u'shareUserIds', u'companyName', u'write', u'typeName', u'readRight',
                        u'writeRight', u'createUser', u'org', u'id', u'attList']]]]]

        Dict = GET(self.all_news, kernel)
        self.determine_error(Dict, "Get News data", template, self.all_news)
        Dict = json.loads(Dict)
        #print Dict
        Dict = Dict['data']['list'][0]
        self.id_info = Dict['id']
        self.times += 1

    def get_news_id(self):
        print "in news id..."
        url = self.news_root + str(self.id_info)
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'stores', u'userId', u'picObj', u'id', u'write', u'title', u'createDate',
                      u'tags', u'content', u'publishScope', u'department', u'type', u'isUpTime',
                      u'companyName', u'circlePicPath', u'contentTitle', u'readRight', u'createUser',
                      u'org', u'userName', u'shareUserIds', u'publishTime', u'isUp', u'writeRight',
                      u'attList', u'mobilePicPath', u'discusses', u'isFile', u'browses', u'isCirclePic'],
                     [[u'src', u'selection', u'thumbnail']],
                     [[u'createDate', u'shareUserIds', u'companyName', u'write', u'typeName', u'readRight',
                       u'writeRight', u'createUser', u'org', u'id', u'attList']]]]
        self.determine_error(GET(url), "Get News ID", template, url)
        self.times += 1

    def determine_error(self,data, name, template=[], url=""):
        #data:服务器返回值,name:method名字,template:用来匹配的标准结构,url
        error = False
        Failure_reason = ""
        try:
            result = json.loads(data)['success']
        except:
            result = "No Result"
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        #第一步:判断结构是否正确,同时判断返回是否为成功
        template = sort_my_array(template)
        to_compare = sort_my_array(title_exporter(json.loads(data)))
        missing_list = comparator(to_compare, template)
        #missing_list 内容存放的东西是丢失的标题
        if (data == None):
            Failure_reason += "/No Data Coming Out"
            error = True
        if (not result):
            Failure_reason += "/Not pass the system test"
            error = True
        if (missing_list != []):
            Failure_reason += "/Kernel Comparison Failed, Missing: " + str(missing_list)
            error = True
        if error:
            print Failure_reason
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        try:
            my_message = json.loads(data)['message']
        except:
            my_message = "No Message"
        kernel = {"Name" : name, "URL" : url, "Success" : result, "Message": my_message, "Failure Reason": Failure_reason}
        self.result_dict[self.class_name].append(kernel)
        return data

    def show_off_all_data(self):
        print "................................................"
        print "...............News Function Summary............"
        print "Function runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Failure Url:"
        for url in self.url_list:
            print url
        print "Please check the dictionary for more information"
        print "...............Thank you........................"


class Tasks:
    def __init__(self):
        self.iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
        self.personal_info = "http://testwww.iquicker.com.cn/iquicker_web/login/user"
        self.get_user_data = "http://testwww.iquicker.com.cn/iquicker_web/mobile/ad_books"
        self.task_info = "http://testwww.iquicker.com.cn/iquicker_web/task/tasks/"
        self.discuss_on_tasks = "http://testwww.iquicker.com.cn/iquicker_web/discuss/data"
        self.discuss_list = "http://testwww.iquicker.com.cn/iquicker_web/discusslist/data/"
        self.function_name = {"login" : 1, "Get Personal Data" : 2, "Get Name List" : 3, "Get Unfinished" : 4, "Get Finished" : 5,
                              "Label Finished" : 6, "Label UnFinished" : 7, "Post Tasks" : 8, "Modify Task" : 9, "Delete Task" : 10,
                              "Comment on Task" : 11, "Discuss List" : 12}

        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0
        self.id_book = []
        self.name_book = []
        self.Task_id = []
        self.Finished_Task_id = []
        self.my_dict = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}

        self.class_name = str(self.__class__).split('__main__.')[1]
        self.result_dict = {self.class_name : []}

    def login(self):
        print "in Login System..."
        template = [[u'status', u'message', u'data', u'success'], [[u'orgs', u'initialised']]]
        self.determine_error(POST(self.iQuickerUrl, self.my_dict), "login",template, self.iQuickerUrl)
        self.times += 1

    def get_personal_data(self):
        print "Fetching personal info..."
        template = [[u'status', u'success', u'orgName', u'orgLogoWhite', u'orgLogoColour',
                     u'orgInnerEmailStatus', u'theme', u'orgCode', u'message', u'data'],
                    [[u'hometown', u'idcard', u'bankCard', u'telephone', u'statusReason',
                      u'sex', u'pinyinPrefix', u'id', u'innerEmail', u'img', u'innerEmailContact',
                      u'joindate', u'department', u'shortname', u'type', u'email', u'status', u'fax',
                      u'isTrialAccount', u'pinyin', u'qualifications', u'birthday', u'address', u'org',
                      u'createTime', u'itcode', u'name', u'mobile', u'prefixId', u'sn', u'signature',
                      u'position', u'joinTime', u'enname'],
                     [[u'org', u'subDept', u'id', u'deptManager', u'parDept', u'flag2', u'shortname',
                       u'status', u'usable', u'flag', u'zfield9', u'zfield8', u'zfield5', u'zfield4',
                       u'zfield7', u'zfield6', u'zfield1', u'zfield3', u'zfield2', u'name', u'zfield10',
                       u'prefixId', u'sn', u'root']]]]
        self.determine_error(GET(self.personal_info), "Get Personal Data",template, self.personal_info)
        self.times += 1

    def get_name_list(self):
        print "Fetching Namelist..."
        user_data = GET(self.get_user_data)
        template = [[[u'tel', u'uuid', u'mobile', u'piny', u'position', u'deptname', u'id', u'name']]]
        self.determine_error(user_data, "Get Name List", template, self.get_user_data)
        user_data = json.loads(user_data)
        for i in range(len(user_data)):
            self.id_book.append(user_data[i]['uuid'])
            self.name_book.append(user_data[i]['name'])
        self.times += 1

    def get_unfinished(self):
        print "Fetching Unfinished task id..."
        self.Task_id = []
        Data_tasks = {"isOver" : False, "page" : 1, "pageSize" : 20, "sortType" : 1, "type" : 0}
        Task_info = GET(self.task_info,Data_tasks)
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'sort', u'last', u'size', u'number', u'content', u'totalPages', u'numberOfElements',
                      u'totalElements', u'first'],
                     [[u'endDate', u'overUserId', u'id', u'publishScopeName', u'subject', u'write',
                       u'overStatus', u'createDate', u'detail', u'priority', u'participants', u'publishScope',
                       u'shared', u'principals', u'overDate', u'readRight', u'createUser', u'org',
                       u'labelObjectList', u'createName', u'shareUserIds', u'writeRight', u'attList'],
                      [[u'id', u'name']], [[u'id', u'name']]]]]
        self.determine_error(Task_info, "Get Unfinished", template, self.task_info)
        Task_info = json.loads(Task_info)
        Task_info = Task_info['data']['content']
        for i in range(len(Task_info)):
            self.Task_id.append(Task_info[i]['id'])
        self.times += 1

    def get_finished(self):
        print "Fetching finished task id..."
        self.Finished_Task_id = []
        Data_tasks = {"isOver" : True, "page" : 1, "pageSize" : 20, "sortType" : 1, "type" : 0}
        Task_info = GET(self.task_info,Data_tasks)
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'sort', u'last', u'size', u'number', u'content', u'totalPages', u'numberOfElements',
                      u'totalElements', u'first'],
                     [[u'endDate', u'overUserId', u'id', u'publishScopeName', u'subject', u'write',
                       u'overStatus', u'createDate', u'detail', u'priority', u'participants', u'publishScope',
                       u'shared', u'principals', u'overDate', u'readRight', u'createUser', u'org',
                       u'labelObjectList', u'createName', u'shareUserIds', u'writeRight', u'attList'],
                      [[u'id', u'name']], [[u'id', u'name']]]]]
        result = self.determine_error(Task_info, "Get Finished", template, self.task_info)
        title_exporter(json.loads(result))
        Task_info = json.loads(Task_info)
        Task_info = Task_info['data']['content']
        for i in range(len(Task_info)):
            self.Finished_Task_id.append(Task_info[i]['id'])
        self.times += 1

    def Label_finished(self):
        print "Label Unfinished Task->Finished"
        self.get_unfinished()
        Label_url = self.task_info + str(self.Task_id[-1]) + "/completion"
        template = [[u'status', u'message', u'success']]
        self.determine_error(PUT(Label_url), "Label Finished", template, Label_url)
        self.times += 1

    def Label_unfinished(self):
        print "Label Finished Task->Unfinished"
        self.get_finished()
        #print self.Finished_Task_id
        Label_url = self.task_info + str(self.Finished_Task_id[-1]) + "/incompletion"
        template = [[u'status', u'message', u'success']]
        self.determine_error(PUT(Label_url), "Label UnFinished", template, Label_url)
        self.times += 1

    def post_task(self):
        print "Posting new task now..."
        Post_kernel = {"subject" : "RobotSend", "principals" : [{"id": self.id_book[0] , "name": self.name_book[0]}], "participants":[{"id": self.id_book[0] , "name": self.name_book[0]}], "endDate" : "2017-06-24T16:00:00.000Z", "priority" : 3, "detail" : "This is a Test Message" , "shared" : False , "publishScope" : ["company"], "publishScopeName" : ["/u5168/u516C/u53F8"]}
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'endDate', u'overUserId', u'id', u'publishScopeName',
                      u'subject', u'write', u'overStatus', u'createDate',
                      u'detail', u'priority', u'participants', u'publishScope',
                      u'shared', u'principals', u'overDate', u'readRight', u'createUser',
                      u'org', u'labelObjectList', u'createName', u'shareUserIds', u'writeRight',
                      u'attList'], [[u'id', u'name']], [[u'id', u'name']]]]
        self.determine_error(POST(self.task_info,Post_kernel), "Post Tasks", template, self.task_info)
        self.times += 1

    def modify_task(self):
        print "Modifying new task now..."
        self.get_unfinished()
        Post_kernel = {"id": self.Task_id[-1], "subject" : "RobotSendModify", "principals" : [{"id": self.id_book[0] , "name": self.name_book[0]}], "participants":[{"id": self.id_book[0] , "name": self.name_book[0]}], "endDate" : "2017-06-24T16:00:00.000Z", "priority" : 3, "detail" : "This is a Modified Message" , "shared" : False ,"attList": None, "publishScope" : ["company"], "publishScopeName" : ["/u5168/u516C/u53F8"]}
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'endDate', u'overUserId', u'id', u'publishScopeName',
                      u'subject', u'write', u'overStatus', u'createDate', u'detail',
                      u'priority', u'participants', u'publishScope', u'shared',
                      u'principals', u'overDate', u'readRight', u'createUser',
                      u'org', u'labelObjectList', u'createName', u'shareUserIds',
                      u'writeRight', u'attList'], [[u'id', u'name']], [[u'id', u'name']]]]
        self.determine_error(POST(self.task_info,Post_kernel), "Modify Task", template, self.task_info)
        self.times += 1

    def delete_task(self):
        print "deleting task now..."
        self.get_unfinished()
        Delete_url = self.task_info + str(self.Task_id[-1])
        template = [[u'status', u'message', u'success']]
        self.determine_error(DELETE(Delete_url), "Delete Task", template, Delete_url)
        self.times += 1

    def commment_on_tasks(self):
        print "Posting discuss on the Tasks..."
        self.get_unfinished()
        kernel = {"discussType":"task","masterId":self.Task_id[-1],"discussedId":"","discussedUserId":"","discussedUserName":"","content":"Looks&nbsp;nice!","isFile":"N","publishTime":get_current_time(),"relay":0,"attList":[],"userIdNames":""}
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'storePeopleId', u'userId', u'relayTimes', u'id', u'publishScopeName',
                      u'write', u'createDate', u'goodPeopleId', u'content', u'publishScope',
                      u'type', u'discussList', u'companyName', u'deleted', u'readRight', u'createUser',
                      u'org', u'userName', u'shareUserIds', u'publishTime', u'writeRight', u'attList']]]
        self.determine_error(POST(self.discuss_on_tasks, kernel), "Comment on Task", template, self.discuss_on_tasks)
        self.times += 1


    def get_disscuss_list(self):
        print "Get all Discuss data for a task..."
        self.get_unfinished()
        url = self.discuss_list + self.Task_id[-1]
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'discussList', u'createDate', u'shareUserIds', u'write',
                      u'masterId', u'readRight', u'writeRight', u'createUser',
                      u'org', u'id', u'attList'],
                     [[u'userName', u'content', u'discussedUserId', u'userIdNames',
                       u'relay', u'createDate', u'isFile', u'shareUserIds',
                       u'publishScope', u'userId', u'publishTime', u'discussedId',
                       u'write', u'masterId', u'readRight', u'writeRight', u'createUser',
                       u'org', u'discussedUserName', u'id', u'attList']]]]

        self.determine_error(GET(url), "Discuss List", template, url)
        self.times += 1

    def determine_error(self,data, name, template=[], url=""):
        error = False
        Failure_reason = ""
        try:
            result = json.loads(data)['success']
        except:
            result = "No Result"
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        template = sort_my_array(template)
        to_compare = sort_my_array(title_exporter(json.loads(data)))
        missing_list = comparator(to_compare, template)
        if (data == None):
            Failure_reason += "/No Data Coming Out"
            error = True
        if (not result):
            Failure_reason += "/Not pass the system test"
            error = True
        if (missing_list != []):
            Failure_reason += "/Kernel Comparison Failed, Missing: " + str(missing_list)
            error = True
        if error:
            print Failure_reason
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        try:
            my_message = json.loads(data)['message']
        except:
            my_message = "No Message"
        kernel = {"Name" : name, "URL" : url, "Success" : result, "Message": my_message, "Failure Reason": Failure_reason}
        self.result_dict[self.class_name].append(kernel)
        return data


    def show_off_all_data(self):
        print "................................................"
        print "...............Task Function Summary............"
        print "Function runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Failure Url:"
        for url in self.url_list:
            print url
        print "Please check the dictionary for more information"
        print "...............Thank you........................"


class calendar:
    def __init__(self):
        self.iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
        self.get_calendar = "http://testwww.iquicker.com.cn/iquicker_web/schedul/app"
        self.get_user_data = "http://testwww.iquicker.com.cn/iquicker_web/mobile/ad_books"
        self.personal_info = "http://testwww.iquicker.com.cn/iquicker_web/login/user"
        self.post_calendar = "http://testwww.iquicker.com.cn/iquicker_web/schedul/"
        self.get_single_url = "http://testwww.iquicker.com.cn/iquicker_web/schedul/schedul/"
        self.function_name = {"login" : 1, "Get Name List" : 2, "Get Schedule" : 3, "Post Event" : 4,
                              "Modify Event" : 5, "Delete Event" : 6, "Get single Schedule" : 7}
        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0
        self.id_book = []
        self.name_book = []
        self.schedule_book = []
        self.schedule_job_id = []
        self.schedule_create_date = []

        self.class_name = str(self.__class__).split('__main__.')[1]
        self.result_dict = {self.class_name : []}

    def login(self):
        print "in Login System..."
        template = [[u'status', u'message', u'data', u'success'], [[u'orgs', u'initialised']]]
        kernel = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
        self.determine_error(POST(self.iQuickerUrl, kernel), "login",template, self.iQuickerUrl)
        self.times += 1

    def get_personal_info(self):
        print "Getting Personal Info..."
        my_data = GET(self.personal_info)
        self.determine_error(my_data, "Get Personal info", [], self.personal_info)
        self.my_id = json.loads(my_data)['data']['id']
        self.my_name = json.loads(my_data)['data']['name']
        self.times += 1

    def get_name_list(self):
        print "Fetching Namelist..."
        user_data = GET(self.get_user_data)
        template = [[[u'tel', u'uuid', u'mobile', u'piny', u'position', u'deptname', u'id', u'name']]]
        self.determine_error(user_data, "Get Name List", template, self.get_user_data)
        user_data = json.loads(user_data)
        for i in range(len(user_data)):
            self.id_book.append(user_data[i]['uuid'])
            self.name_book.append(user_data[i]['name'])
        self.times += 1

    def get_schedule(self):
        print "Getting Schedule..."
        self.schedule_book = []
        self.schedule_job_id = []
        self.schedule_create_date = []
        kernel = {"end" : "2017-06-27 23:59:59", "page" : 1, "pageSize" : 1000, "start" : "2015-06-27 00:00:00",
        "userIds" :self.my_id}
        # After adding new person in the Address book, this part maybe influence
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'sort', u'last', u'size', u'number', u'content', u'totalPages', u'numberOfElements',
                      u'totalElements', u'first'],
                     [[u'attachments', u'share', u'workDay', u'org', u'id', u'publishScopeName', u'content',
                       u'busy', u'end', u'title', u'createDate', u'write', u'start', u'publishScope', u'type',
                       u'schedulerJobId', u'notice', u'repeat', u'readRight', u'createUser', u'endRemindDate',
                       u'allDay', u'createrName', u'shareUserIds', u'remind', u'writeRight', u'place', u'repeatType',
                       u'meeters', u'viewType', u'attList'],
                      [[u'meeters', u'remind', u'vmName', u'title'], [[u'id', u'name']]], [[u'id', u'name']]]]]

        day_schedule = GET(self.get_calendar, kernel)
        self.determine_error(day_schedule, "Get Schedule", template, self.get_calendar)
        day_schedule = json.loads(day_schedule)['data']['content']
        for i in range(len(day_schedule)):
            self.schedule_book.append(day_schedule[i]['id'])
            self.schedule_job_id.append(day_schedule[i]['schedulerJobId'])
            self.schedule_create_date.append(day_schedule[i]['createDate'])
        self.times += 1

    def get_single_schedule(self):
        print "Getting Single Schedule..."
        self.get_schedule()
        url = self.get_single_url + self.schedule_book[0]
        self.determine_error(GET(url), "Get single Schedule", ["no template"], url)
        self.times += 1

    def post_new_event(self):
        print "Posting new event on Calendar..."
        kernel = {"title":"Robot_Create_new","viewType":True,"type":"1","place":"Mountain View","allDay":False,
                  "start":"2016-07-13 00:00:00","end":"2016-07-13 01:00:00",
                  "meeters":[{"id":self.my_id,"name":self.my_name}],"content":"Robot send test message",
                  "repeat":False,"endRemindDate": None,"remind":"5","share":False,"repeatType":0,"workDay":False,
                  "publishScope":["company"],"publishScopeName":["/u5168/u516C/u53F8"]}
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'attachments', u'share', u'workDay', u'org', u'id', u'publishScopeName', u'content',
                      u'busy', u'end', u'title', u'createDate', u'write', u'start', u'publishScope', u'type',
                      u'schedulerJobId', u'notice', u'repeat', u'readRight', u'createUser', u'endRemindDate',
                      u'allDay', u'createrName', u'shareUserIds', u'remind', u'writeRight', u'place', u'repeatType',
                      u'meeters', u'viewType', u'attList'],
                     [[u'meeters', u'remind', u'vmName', u'title'], [[u'id', u'name']]], [[u'id', u'name']]]]
        self.determine_error(POST(self.post_calendar, kernel), "Post Event", template, self.post_calendar)
        self.times += 1

    def modify_event(self):
        print "Modifying Event..."
        self.get_schedule()
        kernel = {"id" : self.schedule_book[-1],"title":"Robot_Create_modify","viewType":True,"type":"1","place":"Mountain View1","allDay":False,
                  "start":"2016-07-13 00:00:00","end":"2016-07-13 01:00:00",
                  "meeters":[{"id":self.id_book[-1],"name":self.name_book[-1]}],"content":"Robot send test message1",
                  "repeat":False,"endRemindDate": None,"remind":"5","share":False,"repeatType":0,"attList": None,"workDay":False,
                  "publishScope":["company"],"publishScopeName":["/u5168/u516C/u53F8"], "schedulerJobId":self.schedule_job_id[-1],
                  "createDate":self.schedule_create_date[-1],"createUser":self.my_id,"createrName":self.my_name,"org":"ff808081557080a6015575e3d9300330"}
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'attachments', u'share', u'workDay', u'org', u'id', u'publishScopeName', u'content',
                      u'busy', u'end', u'title', u'createDate', u'write', u'start', u'publishScope', u'type',
                      u'schedulerJobId', u'notice', u'repeat', u'readRight', u'createUser', u'endRemindDate',
                      u'allDay', u'createrName', u'shareUserIds', u'remind', u'writeRight', u'place', u'repeatType',
                      u'meeters', u'viewType', u'attList'],
                     [[u'meeters', u'remind', u'vmName', u'title'], [[u'id', u'name']]], [[u'id', u'name']]]]
        self.determine_error(POST(self.post_calendar, kernel), "Modify Event", template, self.post_calendar)
        self.times += 1

    def delete_event(self):
        print "Deleting event..."
        self.get_schedule()
        template = [[u'status', u'message', u'success']]
        url = self.post_calendar + self.schedule_book[-1]
        self.determine_error(DELETE(url), "Delete Event", template, url)
        self.times += 1

    def determine_error(self,data, name, template=[], url=""):
        error = False
        Failure_reason = ""
        try:
            result = json.loads(data)['success']
        except:
            result = "No Result"
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        template = sort_my_array(template)
        to_compare = sort_my_array(title_exporter(json.loads(data)))
        missing_list = comparator(to_compare, template)
        if (data == None):
            Failure_reason += "/No Data Coming Out"
            error = True
        if (not result):
            Failure_reason += "/Not pass the system test"
            error = True
        if (missing_list != []):
            Failure_reason += "/Kernel Comparison Failed, Missing: " + str(missing_list)
            error = True
        if error:
            print Failure_reason
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        try:
            my_message = json.loads(data)['message']
        except:
            my_message = "No Message"
        kernel = {"Name" : name, "URL" : url, "Success" : result, "Message": my_message, "Failure Reason": Failure_reason}
        self.result_dict[self.class_name].append(kernel)
        return data

    def show_off_all_data(self):
        print "................................................"
        print "...........Calendar Function Summary............"
        print "Function runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Failure Url:"
        for url in self.url_list:
            print url
        print "Please check the dictionary for more information"
        print "...............Thank you........................"


class Work_comm:
    def __init__(self):
        self.iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
        self.get_user_data = "http://testwww.iquicker.com.cn/iquicker_web/mobile/ad_books"
        self.user_info = "http://testwww.iquicker.com.cn/iquicker_web/login/user"
        self.all_wcomm = "http://testwww.iquicker.com.cn/iquicker_web/wcontact/contact-applys/"
        self.log_data = "http://testwww.iquicker.com.cn/iquicker_web/flow/log/"
        self.function_name = {"login" : 1, "Get Personal Info" : 2, "Get Name List" : 3, "Get all Comm" : 4,
                              "Create New Work" : 5, "Get Single Info" : 6, "Get Process Record" : 7, "Agree" : 8,
                              "Reject" : 9, "Delete Work Contact" : 10}
        self.my_id = ""
        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0
        self.id_book = []
        self.name_book = []
        self.wcomm_id = []

        self.class_name = str(self.__class__).split('__main__.')[1]
        self.result_dict = {self.class_name : []}

    def login(self):
        print "in Login System..."
        template = [[u'status', u'message', u'data', u'success'], [[u'orgs', u'initialised']]]
        kernel = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
        self.determine_error(POST(self.iQuickerUrl, kernel), "login",template, self.iQuickerUrl)
        self.times += 1

    def get_personal_info(self):
        print "Get personal information..."
        template = [[u'status', u'success', u'orgName', u'orgLogoWhite', u'orgLogoColour', u'orgInnerEmailStatus', u'theme',
                     u'orgCode', u'message', u'data'],
                    [[u'hometown', u'idcard', u'bankCard', u'telephone', u'statusReason', u'sex', u'pinyinPrefix', u'id',
                      u'innerEmail', u'img', u'innerEmailContact', u'joindate', u'department', u'shortname', u'type', u'email',
                      u'status', u'fax', u'isTrialAccount', u'pinyin', u'qualifications', u'birthday', u'address', u'org', u'createTime',
                      u'itcode', u'name', u'mobile', u'prefixId', u'sn', u'signature', u'position', u'joinTime', u'enname'],
                     [[u'org', u'subDept', u'id', u'deptManager', u'parDept', u'flag2', u'shortname', u'status', u'usable',
                       u'flag', u'zfield9', u'zfield8', u'zfield5', u'zfield4', u'zfield7', u'zfield6', u'zfield1', u'zfield3',
                       u'zfield2', u'name', u'zfield10', u'prefixId', u'sn', u'root']]]]
        id_getter = GET(self.user_info)
        self.determine_error(id_getter, "Get Personal Info", template, self.user_info)
        self.my_id = json.loads(id_getter)['data']['id']
        self.times += 1

    def get_name_list(self):
        print "Fetching Namelist..."
        user_data = GET(self.get_user_data)
        template = [[[u'tel', u'uuid', u'mobile', u'piny', u'position', u'deptname', u'id', u'name']]]
        self.determine_error(user_data, "Get Name List", template, self.get_user_data)
        user_data = json.loads(user_data)
        for i in range(len(user_data)):
            self.id_book.append(user_data[i]['uuid'])
            self.name_book.append(user_data[i]['name'])
        self.times += 1

    def get_all_work_comm(self):
        print "Get all data in work-communication section..."
        self.wcomm_id = []
        kernel = {"page" : 1, "pageSize" : 20, "scope" : "ALL"}
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'sort', u'last', u'size', u'number', u'content', u'totalPages', u'numberOfElements',
                      u'totalElements', u'first'],
                     [[u'billStatus', u'currApprAuthors', u'detail', u'shareUsers', u'id', u'subject', u'write',
                       u'flowStatus', u'flowCurrNodeName', u'createDate', u'flowCurrNodeId', u'approvalIdList',
                       u'version', u'apprReadors', u'userName', u'readRight', u'createUser', u'org', u'deptId',
                       u'currApprUserIds', u'shareUserIds', u'flowId', u'apprUsers', u'writeRight', u'deptName',
                       u'attList', u'delete'], [[u'shareUserName', u'prefixId', u'shareUserId']],
                      [[u'name', u'level', u'label', u'placeholder', u'id', u'useId']]]]]

        user_info = GET(self.all_wcomm, kernel)
        self.determine_error(user_info, "Get all Comm", template, self.all_wcomm)
        user_info = json.loads(user_info)['data']['content']
        for i in range(len(user_info)):
            self.wcomm_id.append(user_info[i]['id'])
        self.times += 1

    def create_new_work(self):
        print "Create a new Work process..."
        kernel = {"shareUsers":[{"shareUserId":self.id_book[-1],"shareUserName":self.name_book[-1]}],
                  "apprUsers":[{"id":"apprUser_1","label":u"/u4E00/u7EA7/u5BA1/u6279",
                                "placeholder":"/u8BF7/u9009/u62E9/u5BA1/u6279/u4EBA(/u53EF/u9009/u591A/u4EBA/u5E76/u7B7E)","level":1,
                                "useId":self.id_book[1],"name": self.name_book[1]},
                               {"id":"apprUser_2","label":u"/u4E8C/u7EA7/u5BA1/u6279",
                                "placeholder":"/u8BF7/u9009/u62E9/u5BA1/u6279/u4EBA(/u53EF/u9009/u591A/u4EBA/u5E76/u7B7E)","level":2,
                                "useId":self.id_book[1],"name": self.name_book[1]}],"subject":"Robot Send","detail":"LOL",
                  "billStatus":"SUBMIT"}
        # Error Throwout in id_book
        template = [[u'status', u'message', u'success']]
        self.determine_error(POST(self.all_wcomm, kernel), "Create New Work", template, self.all_wcomm)
        self.times += 1

    def get_single_WComm_info(self):
        print "Get single piece of Work communication info..."
        self.get_all_work_comm()
        url = self.all_wcomm + self.wcomm_id[-1]
        kernel = {"id" : self.wcomm_id[-1]}
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'billStatus', u'currApprAuthors', u'detail', u'shareUsers', u'id', u'subject', u'write', u'flowStatus',
                      u'flowCurrNodeName', u'createDate', u'flowCurrNodeId', u'approvalIdList', u'version', u'apprReadors',
                      u'userName', u'readRight', u'createUser', u'org', u'deptId', u'currApprUserIds', u'shareUserIds', u'flowId',
                      u'apprUsers', u'writeRight', u'deptName', u'attList', u'delete'], [[u'shareUserName', u'prefixId', u'shareUserId']],
                     [[u'name', u'level', u'label', u'placeholder', u'id', u'useId']]]]

        flow_data = GET(url, kernel)
        self.determine_error(flow_data, "Get Single Info", template, url)
        flow_data = json.loads(flow_data)['data']['flowId']
        self.times += 1
        return flow_data

    def get_process_record(self):
        print "Getting All processing Record..."
        flow_data = self.get_single_WComm_info()
        url = self.log_data + flow_data
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'nodeType', u'taskEndTime', u'otherOperatorEn', u'operatorId', u'nextTaskName', u'operationName',
                      u'remark', u'operatorCn', u'otherOperatorCn', u'taskId', u'taskStartTime', u'org', u'taskName',
                      u'operatorEn', u'nextTaskId', u'id', u'operationId']]]

        self.determine_error(GET(url), "Get Process Record", template, url)
        self.times += 1

    def agree_on_wcomm(self):
        print "Agreement Established on the WC..."
        self.get_all_work_comm()
        url = self.all_wcomm + self.wcomm_id[0] + "/agreement"
        #print self.wcomm_id[0]
        kernel = {"id":self.wcomm_id[0],"opinion":"Robot Agree",
                  "shareUsers":[{"shareUserId":self.id_book[1],"shareUserName":self.name_book[1]}]}
        template = [[u'status', u'message', u'success']]
        self.determine_error(PUT(url, kernel), "Agree", template, url)
        self.times +=1

    def reject_on_wcomm(self):
        print "Rejection Established on the WC..."
        self.get_all_work_comm()
        url = self.all_wcomm + self.wcomm_id[0] + "/rejection"
        #print self.wcomm_id[0]
        kernel = {"id":self.wcomm_id[0],"opinion":"Robot Disagree",
                  "shareUsers":[{"shareUserId":self.id_book[0],"shareUserName":self.name_book[0]}]}
        template = [[u'status', u'message', u'success']]
        self.determine_error(PUT(url, kernel), "Reject", template, url)
        self.times += 1

    def delete_work_contact(self):
        print "Delete work contact..."
        self.get_all_work_comm()
        url = self.all_wcomm + self.wcomm_id[0]
        kernel = {'id' : self.wcomm_id[0]}
        self.determine_error(DELETE(url, kernel),"Delete Work Contact", ["No template"], url)
        self.times += 1

    def determine_error(self,data, name, template=[], url=""):
        error = False
        Failure_reason = ""
        try:
            result = json.loads(data)['success']
        except:
            result = "No Result"
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        template = sort_my_array(template)
        to_compare = sort_my_array(title_exporter(json.loads(data)))
        missing_list = comparator(to_compare, template)
        if (data == None):
            Failure_reason += "/No Data Coming Out"
            error = True
        if (not result):
            Failure_reason += "/Not pass the system test"
            error = True
        if (missing_list != []):
            Failure_reason += "/Kernel Comparison Failed, Missing: " + str(missing_list)
            error = True
        if error:
            print Failure_reason
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        try:
            my_message = json.loads(data)['message']
        except:
            my_message = "No Message"
        kernel = {"Name" : name, "URL" : url, "Success" : result, "Message": my_message, "Failure Reason": Failure_reason}
        self.result_dict[self.class_name].append(kernel)
        return data

    def show_off_all_data(self):
        print "................................................"
        print "...........Work Communication Function Summary............"
        print "Function runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Failure Url:"
        for url in self.url_list:
            print url
        print "Please check the dictionary for more information"
        print "...............Thank you........................"

class Compnews:
    def __init__(self):
        self.iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
        self.news_type = "http://testwww.iquicker.com.cn/iquicker_web/newstype/datas"
        self.news_data = "http://testwww.iquicker.com.cn/iquicker_web/news/datas"
        self.discuss_list = "http://testwww.iquicker.com.cn/iquicker_web/discusslist/data/"
        self.single_news = "http://testwww.iquicker.com.cn/iquicker_web/news/data/"
        self.user_info = "http://testwww.iquicker.com.cn/iquicker_web/login/user"
        self.news_number = "http://testwww.iquicker.com.cn/iquicker_web/news/data/num"
        self.create_discuss = "http://testwww.iquicker.com.cn/iquicker_web/discuss/data/"
        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0
        self.function_name = {"login" : 1, "Get Personal Info" : 2, "Get News Type" : 3, "Get News Data" : 4,
                              "Get News Threemonth" : 5, "Get Discuss List" : 6, "Get Single List" : 7,
                              "Increase View Number" : 8, "Discuss on News" : 9, "Delete Discuss" : 10}
        self.news_id = []
        self.discuss_id = []
        self.my_id = ""
        self.my_name = ""

        self.class_name = str(self.__class__).split('__main__.')[1]
        self.result_dict = {self.class_name : []}

    def login(self):
        print "in Login System..."
        template = [[u'status', u'message', u'data', u'success'], [[u'orgs', u'initialised']]]
        kernel = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
        self.determine_error(POST(self.iQuickerUrl, kernel), "login",template, self.iQuickerUrl)
        self.times += 1

    def get_personal_info(self):
        print "Get personal information..."
        template = [[u'status', u'success', u'orgName', u'orgLogoWhite', u'orgLogoColour', u'orgInnerEmailStatus', u'theme',
                     u'orgCode', u'message', u'data'],
                    [[u'hometown', u'idcard', u'bankCard', u'telephone', u'statusReason', u'sex', u'pinyinPrefix', u'id',
                      u'innerEmail', u'img', u'innerEmailContact', u'joindate', u'department', u'shortname', u'type', u'email',
                      u'status', u'fax', u'isTrialAccount', u'pinyin', u'qualifications', u'birthday', u'address', u'org', u'createTime',
                      u'itcode', u'name', u'mobile', u'prefixId', u'sn', u'signature', u'position', u'joinTime', u'enname'],
                     [[u'org', u'subDept', u'id', u'deptManager', u'parDept', u'flag2', u'shortname', u'status', u'usable',
                       u'flag', u'zfield9', u'zfield8', u'zfield5', u'zfield4', u'zfield7', u'zfield6', u'zfield1', u'zfield3',
                       u'zfield2', u'name', u'zfield10', u'prefixId', u'sn', u'root']]]]
        id_getter = GET(self.user_info)
        self.determine_error(id_getter, "Get Personal Info", template, self.user_info)
        self.my_id = json.loads(id_getter)['data']['id']
        self.my_name = json.loads(id_getter)['data']['name']
        self.times += 1

    def get_news_type(self):
        print "Getting News type..."
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'createDate', u'shareUserIds', u'companyName', u'write', u'typeName',
                      u'readRight', u'writeRight', u'createUser', u'org', u'id', u'attList']]]
        self.determine_error(GET(self.news_type), "Get News Type", template, self.news_type)
        self.times += 1

    def get_news_data(self):
        print "Getting News Data..."
        self.news_id = []
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'totalpage', u'list'],
                     [[u'stores', u'userId', u'picObj', u'id', u'write', u'title', u'createDate',
                       u'tags', u'content', u'publishScope', u'department', u'type', u'isUpTime',
                       u'companyName', u'circlePicPath', u'contentTitle', u'readRight', u'createUser',
                       u'org', u'userName', u'shareUserIds', u'publishTime', u'isUp', u'writeRight',
                       u'attList', u'mobilePicPath', u'discusses', u'isFile', u'browses',
                       u'isCirclePic'], [[u'src', u'selection', u'thumbnail']],
                      [[u'createDate', u'shareUserIds', u'companyName', u'write', u'typeName',
                        u'readRight', u'writeRight', u'createUser', u'org', u'id', u'attList']]]]]
        kernel = {"pageNo" : 1, "pageSize" : 20, "sortInfo" : "DESC_isUp_isUpTime_publishTime"}
        news_id_list = GET(self.news_data, kernel)
        self.determine_error(news_id_list, "Get News Data", template, self.news_data)
        news_id_list = json.loads(news_id_list)['data']['list']
        for i in range(len(news_id_list)):
            self.news_id.append(news_id_list[i]['id'])
        self.times += 1

    def get_news_threemonth(self):
        print "Getting News in three Month..."
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'totalpage', u'list'],
                     [[u'stores', u'userId', u'picObj', u'id', u'write', u'title', u'createDate',
                       u'tags', u'content', u'publishScope', u'department', u'type', u'isUpTime',
                       u'companyName', u'circlePicPath', u'contentTitle', u'readRight', u'createUser',
                       u'org', u'userName', u'shareUserIds', u'publishTime', u'isUp', u'writeRight',
                       u'attList', u'mobilePicPath', u'discusses', u'isFile', u'browses',
                       u'isCirclePic'], [[u'src', u'selection', u'thumbnail']],
                      [[u'createDate', u'shareUserIds', u'companyName', u'write', u'typeName',
                        u'readRight', u'writeRight', u'createUser', u'org', u'id', u'attList']]]]]
        kernel = {"endTime" : "2016-06-28 23:59:59","pageNo" : 1, "pageSize" : 20,
                  "sortInfo" : "DESC_isUp_isUpTime_publishTime",  "startTime" : "2016-03-31 00:00:00"}
        self.determine_error(GET(self.news_data, kernel), "Get News Threemonth", template, self.news_data)
        self.times += 1

    def get_news_discuss(self):
        print "Get News discussion List..."
        self.discuss_id = []
        url = self.discuss_list + self.news_id[-1]
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'discussList', u'createDate', u'shareUserIds', u'write', u'masterId',
                      u'readRight', u'writeRight', u'createUser', u'org', u'id', u'attList'],
                     [[u'userName', u'content', u'discussedUserId', u'userIdNames', u'relay',
                       u'createDate', u'isFile', u'shareUserIds', u'publishScope', u'userId',
                       u'publishTime', u'discussedId', u'write', u'masterId', u'readRight', u'writeRight',
                       u'createUser', u'org', u'discussedUserName', u'id', u'attList']]]]
        kernel = {"masterId" : self.my_id}
        discuss_id_fetcher = GET(url, kernel)
        self.determine_error(discuss_id_fetcher, "Get Discuss List", template, url)
        # Only taking the discuss id in the first news
        discuss_id_fetcher = json.loads(discuss_id_fetcher)['data'][0]['discussList']
        for i in range(len(discuss_id_fetcher)):
            self.discuss_id.append(discuss_id_fetcher[i]['id'])
        self.times += 1

    def get_single_news(self):
        print "Getting Single News..."
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'stores', u'userId', u'picObj', u'id', u'write', u'title',
                      u'createDate', u'tags', u'content', u'publishScope', u'department',
                      u'type', u'isUpTime', u'companyName', u'circlePicPath', u'contentTitle',
                      u'readRight', u'createUser', u'org', u'userName', u'shareUserIds',
                      u'publishTime', u'isUp', u'writeRight', u'attList', u'mobilePicPath',
                      u'discusses', u'isFile', u'browses', u'isCirclePic'],
                     [[u'src', u'selection', u'thumbnail']],
                     [[u'createDate', u'shareUserIds', u'companyName', u'write', u'typeName',
                       u'readRight', u'writeRight', u'createUser', u'org', u'id', u'attList']]]]
        url = self.single_news + self.news_id[-1]
        self.determine_error(GET(url), "Get Single List", template, url)
        self.times += 1

    def increase_view_number(self):
        print "Increasing views number"
        template = [[u'status', u'message', u'success']]
        kernel = {"newsId" : self.news_id[-1], "type" : "browses"}
        self.determine_error(POST(self.news_number, kernel), "Increase View Number", template, self.news_number)
        self.times += 1

    def discuss_on_news(self):
        print "Creating discuss on News..."
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'storePeopleId', u'userId', u'relayTimes', u'id', u'publishScopeName',
                      u'write', u'createDate', u'goodPeopleId', u'content', u'publishScope',
                      u'type', u'discussList', u'companyName', u'deleted', u'readRight',
                      u'createUser', u'org', u'userName', u'shareUserIds', u'publishTime',
                      u'writeRight', u'attList']]]

        kernel = {"discussType":"","masterId":self.news_id[-1],
                  "discussedId":"","discussedUserId":"","discussedUserName":"",
                  "content":"Robot Send","isFile":"N",
                  "publishTime":get_current_time(),"relay":0,"attList":[],
                  "userIdNames": "",
                  "atConnectTitle":"Click to See"}
        self.determine_error(POST(self.create_discuss, kernel), "Discuss on News", template, self.create_discuss)
        self.times += 1

    def delete_discuss(self):
        print "Deleting discusses on News..."
        self.get_news_discuss()
        template = [[u'status', u'message', u'success']]
        url = self.create_discuss + self.news_id[-1] + "/" + self.discuss_id[-1] +"/xinwen"
        kernel = {"discussId" : self.discuss_id[-1], "discussType" : "xinwen", "masterId" : self.news_id[-1]}
        self.determine_error(DELETE(url, kernel), "Delete Discuss", template, url)
        self.times += 1


    def determine_error(self,data, name, template=[], url=""):
        error = False
        Failure_reason = ""
        try:
            result = json.loads(data)['success']
        except:
            result = "No Result"
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        template = sort_my_array(template)
        to_compare = sort_my_array(title_exporter(json.loads(data)))
        missing_list = comparator(to_compare, template)
        if (data == None):
            Failure_reason += "/No Data Coming Out"
            error = True
        if (not result):
            Failure_reason += "/Not pass the system test"
            error = True
        if (missing_list != []):
            Failure_reason += "/Kernel Comparison Failed, Missing: " + str(missing_list)
            error = True
        if error:
            print Failure_reason
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        try:
            my_message = json.loads(data)['message']
        except:
            my_message = "No Message"
        kernel = {"Name" : name, "URL" : url, "Success" : result, "Message": my_message, "Failure Reason": Failure_reason}
        self.result_dict[self.class_name].append(kernel)
        return data

    def show_off_all_data(self):
        print "................................................"
        print "...........Company News Function Summary............"
        print "Function runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Failure Url:"
        for url in self.url_list:
            print url
        print "Please check the dictionary for more information"
        print "...............Thank you........................"

class address_book:

    def __init__(self):
        self.iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
        self.get_user_data = "http://testwww.iquicker.com.cn/iquicker_web/mobile/ad_books"
        self.label = "http://testwww.iquicker.com.cn/iquicker_web/labelobject/data/"
        self.personal_info = "http://testwww.iquicker.com.cn/iquicker_web/person/"
        self.my_fans_info = "http://testwww.iquicker.com.cn/iquicker_web/blogattention/data/attention/"
        self.fans_me = "http://testwww.iquicker.com.cn/iquicker_web/blogattention/data/fans/"
        self.whats_up = "http://testwww.iquicker.com.cn/iquicker_web/blogall/data/personel"
        self.attention_to = "http://testwww.iquicker.com.cn/iquicker_web/blogattention/data/"
        self.notice_poster = "http://testwww.iquicker.com.cn/iquicker_web/notice/data"
        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0
        self.id_book = []
        self.name_book = []
        self.person_data = {}
        self.function_name = {"login": 1, "Get Name List": 2, "Get Label": 3, "Get Personal info": 4,
                              "Get My Fans": 5, "Get Fans Me": 6, "Get Whatsup": 7, "Label Fans": 8,
                              "Unlabel Fans": 9, "Post New Fans": 10}

        self.class_name = str(self.__class__).split('__main__.')[1]
        self.result_dict = {self.class_name : []}

    def login(self):
        print "in Login System..."
        template = [[u'status', u'message', u'data', u'success'], [[u'orgs', u'initialised']]]
        kernel = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
        self.determine_error(POST(self.iQuickerUrl, kernel), "login",template, self.iQuickerUrl)
        self.times += 1

    def get_name_list(self):
        print "Fetching Namelist..."
        user_data = GET(self.get_user_data)
        template = [[[u'tel', u'uuid', u'mobile', u'piny', u'position', u'deptname', u'id', u'name']]]
        self.determine_error(user_data, "Get Name List", template, self.get_user_data)
        user_data = json.loads(user_data)
        for i in range(len(user_data)):
            self.id_book.append(user_data[i]['uuid'])
            self.name_book.append(user_data[i]['name'])
        self.times += 1

    def get_label(self):
        print "Getting person's Label..."
        url = self.label + self.id_book[0]
        template = [[u'status', u'message', u'data', u'success'], [[u'myId', u'myList'], [[u'userList', u'tag']]]]
        kernel = {"objId" : self.id_book[0]}
        # Fetching the info of Jiqiren->Robot
        self.determine_error(GET(url, kernel), "Get Label", template, url)
        self.times += 1

    def get_personal_info(self):
        print "Gettting personal info..."
        url = self.personal_info + self.id_book[0]
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'hometown', u'idcard', u'bankCard', u'telephone', u'statusReason', u'sex', u'pinyinPrefix',
                      u'id', u'innerEmail', u'img', u'innerEmailContact', u'joindate', u'department', u'shortname',
                      u'type', u'email', u'status', u'fax', u'isTrialAccount', u'pinyin', u'qualifications',
                      u'birthday', u'address', u'org', u'createTime', u'itcode', u'name', u'mobile', u'prefixId',
                      u'sn', u'signature', u'position', u'joinTime', u'enname'],
                     [[u'status', u'usable', u'name', u'deptManager', u'prefixId', u'org', u'shortname', u'id']]]]

        personal_data = GET(url)
        self.determine_error(personal_data, "Get Personal info", template, url)
        self.person_data = json.loads(personal_data)['data']
        self.times += 1

    def get_my_fans(self):
        print "Getting all my fans"
        url = self.my_fans_info + self.id_book[0]
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'userName', u'obj', u'createDate', u'shareUserIds', u'userId', u'write', u'readRight',
                      u'writeRight', u'createUser', u'attentionTime', u'org', u'type', u'id', u'attList'],
                     [[u'status', u'itcode', u'name', u'mobile', u'pinyin', u'id', u'signature', u'pinyinPrefix',
                       u'telephone', u'createTime', u'prefixId', u'focusOrNot', u'org', u'department', u'position',
                       u'joinTime', u'type', u'email'], [[u'status', u'name', u'prefixId', u'org', u'shortname', u'id']]]]]

        kernel = {"id" : self.id_book[0]}
        self.determine_error(GET(url, kernel), "Get My Fans", template, url)
        self.times += 1

    def get_fans_me(self):
        print "Getting who fans me..."
        url = self.fans_me + self.id_book[0]
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'userName', u'obj', u'createDate', u'shareUserIds', u'userId', u'write', u'readRight',
                      u'writeRight', u'createUser', u'attentionTime', u'org', u'type', u'id', u'attList'],
                     [[u'hometown', u'bankCard', u'telephone', u'sex', u'pinyinPrefix', u'id', u'joindate',
                       u'department', u'shortname', u'type', u'email', u'status', u'fax', u'pinyin',
                       u'qualifications', u'org', u'createTime', u'itcode', u'name', u'mobile', u'prefixId',
                       u'focusOrNot', u'position', u'joinTime', u'enname'],
                      [[u'status', u'name', u'prefixId', u'org', u'shortname', u'id']]]]]
        kernel = {"id" : self.id_book[0]}
        self.determine_error(GET(url, kernel), "Get Fans Me", template, url)
        self.times += 1

    def get_whats_up(self):
        print "Getting the whats up!..."
        template = [[u'status', u'message', u'data', u'success'],
                    [[u'department', u'myId', u'totalpage', u'list', u'myName'],
                     [[u'storePeopleId', u'userId', u'relayTimes', u'id', u'publishScopeName', u'write', u'createDate',
                       u'goodPeopleId', u'content', u'publishScope', u'type', u'discussList', u'companyName',
                       u'deleted', u'readRight', u'createUser', u'org', u'userName', u'shareUserIds', u'publishTime',
                       u'writeRight', u'attList'],
                      [[u'userName', u'content', u'discussList', u'relay', u'createDate', u'shareUserIds',
                        u'publishScope', u'userId', u'publishTime', u'write', u'masterId', u'readRight',
                        u'writeRight', u'imgList', u'publishScopeName', u'createUser', u'org', u'isFile', u'id',
                        u'attList', u'userIdNames']]]]]
        kernel = {"pageNo" : 1, "pageSize" : 20, "search_IS_userId" : self.id_book[0], "sortInfo" : "DESC_publishTime"}
        self.determine_error(GET(self.whats_up, kernel), "Get Whatsup", template, self.whats_up)
        self.times += 1

    def label_fans(self):
        print "Become a fans..."
        template = [[u'status', u'message', u'success']]
        kernel = {"attentionTime" : get_current_time(), "modelType" : "AttentionMe", "obj" : self.person_data,"type" : "people"}
        self.determine_error(POST(self.attention_to, kernel), "Label Fans", template, self.attention_to)
        self.times += 1


    def unlabel_fans(self):
        print "Get rid of fans..."
        kernel = {"objId" :self.id_book[0]}
        template = [[u'status', u'message', u'success']]
        url = self.attention_to + self.id_book[0]
        self.determine_error(DELETE(url, kernel), "Unlabel Fans", template, url)
        self.times += 1

    def post_new_fans(self):
        print "Notice the person of the new fans..."
        template = [[u'status', u'message', u'success']]
        kernel = {"connectUrl" : "http://", "content" : "Hossien Find your interests", "modelType" : "AttentionMe",
                  "readState" : "0", "sendTime" : get_current_time(), "type" : "System Notice", "typeId" : "system",
                  "userId" : self.id_book[0], "userName" : self.name_book[0]}
        self.determine_error(POST(self.notice_poster, kernel), "Post New Fans", template, self.notice_poster)
        self.times += 1


    def determine_error(self,data, name, template=[], url=""):
        error = False
        Failure_reason = ""
        try:
            result = json.loads(data)['success']
        except:
            result = "No Result"
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        template = sort_my_array(template)
        to_compare = sort_my_array(title_exporter(json.loads(data)))
        missing_list = comparator(to_compare, template)
        if (data == None):
            Failure_reason += "/No Data Coming Out"
            error = True
        if (not result):
            Failure_reason += "/Not pass the system test"
            error = True
        if (missing_list != []):
            Failure_reason += "/Kernel Comparison Failed, Missing: " + str(missing_list)
            error = True
        if error:
            print Failure_reason
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        try:
            my_message = json.loads(data)['message']
        except:
            my_message = "No Message"
        kernel = {"Name" : name, "URL" : url, "Success" : result, "Message": my_message, "Failure Reason": Failure_reason}
        self.result_dict[self.class_name].append(kernel)
        return data

    def show_off_all_data(self):
        print "................................................"
        print ".......Address Book Function Summary............"
        print "Function runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Failure Url:"
        for url in self.url_list:
            print url
        print "Please check the dictionary for more information"
        print "...............Thank you........................"

class Notice_and_me:

    def __init__(self):
        self.iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
        self.notice_terminal = "http://testwww.iquicker.com.cn/iquicker_web/notice/datas/page"
        self.system_settings = "http://testwww.iquicker.com.cn/iquicker_web/is-permitted/companySetting:systemSetting"
        self.get_companies = "http://testwww.iquicker.com.cn/iquicker_web/login/user/orgs-except-logined/status-filter:1"
        self.invitation = "http://testwww.iquicker.com.cn/iquicker_web/person/invite"
        self.feedback = "http://testwww.iquicker.com.cn/iquicker_web/feedback/feedback"
        self.my_feedback = "http://testwww.iquicker.com.cn/iquicker_web/feedback/feedbacks"
        self.password = "http://testwww.iquicker.com.cn/iquicker_web/register/password/mobile/15611765076"
        # We hereby using the default phone number
        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0
        self.feedback_id = []
        self.function_name = {"login": 1, "Reply Me" : 2, "System Setting" : 3, "Get Company" : 4,
                              "Send Invitation" : 5, "Get All Feedback" : 6, "Get Single Feedback" : 7,
                              "Reply Feedback" : 8, "Change Password" : 9, "Send Feedback" : 10}

        self.class_name = str(self.__class__).split('__main__.')[1]
        self.result_dict = {self.class_name : []}

    def login(self):
        print "in Login System..."
        template = [[u'status', u'message', u'data', u'success'], [[u'orgs', u'initialised']]]
        kernel = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
        self.determine_error(POST(self.iQuickerUrl, kernel), "login",template, self.iQuickerUrl)
        self.times += 1

    def reply_me(self):
        print "Fetching all replys I have..."
        kernel = {"pageNo" : 1, "pageSize" : 20, "search_IS_type" : "评论", "sortInfo" : "DESC_sendTime"}
        self.determine_error(GET(self.notice_terminal, kernel), "Reply Me", [], self.notice_terminal)
        self.times += 1

    def get_system_settings(self):
        print "Getting system Settings..."
        self.determine_error(GET(self.system_settings), "System Setting", ["No Template"], self.system_settings)
        self.times += 1

    def get_all_company(self):
        print "Getting all companies..."
        template = [[[u'createTime', u'displayName', u'domain', u'englishName', u'id', u'logoColour', u'logoWhite', u'name', u'source', u'userStatus']], [u'data', u'message', u'status', u'success']]
        self.determine_error(GET(self.get_companies), "Get Company", template, self.get_companies)
        self.times += 1

    def invite_people(self):
        print "Inviting people..."
        kernel = [{"$$hashKey" : "object:175", "mobile" : "15614413537"}]
        template = [[u'message', u'status', u'success']]
        # Hashkey Problem????
        self.determine_error(POST(self.invitation, kernel), "Send Invitation", template, self.invitation)
        self.times += 1

    def send_feedback(self):
        print "Posting Feedback now..."
        template = [[u'message', u'status', u'success']]
        kernel = {"open":False,"answerAndQuestion":[{"describe":"Robot Send","attList":[]}],"workOrderInformation":{}}
        self.determine_error(POST(self.feedback, kernel), "Send Feedback", template, self.feedback)
        self.times += 1

    def get_my_feedback(self):
        print "Getting my feedback now..."
        self.feedback_id = []
        template = [[[[[u'applicationDate', u'applyNo', u'attList', u'createDate', u'createUser', u'id', u'manageDate', u'org', u'readRight', u'service', u'serviceUpdateDate', u'shareUserIds', u'solveDate', u'status', u'write', u'writeRight']], [[u'applyNo', u'attList', u'createDate', u'createUser', u'date', u'describe', u'id', u'name', u'org', u'readRight', u'shareUserIds', u'write', u'writeRight']], [u'answerAndQuestion', u'applyNo', u'attList', u'createDate', u'createName', u'createUser', u'id', u'open', u'org', u'orgName', u'readRight', u'shareUserIds', u'sortDate', u'status', u'workOrderInformation', u'write', u'writeRight']], [u'content', u'first', u'last', u'number', u'numberOfElements', u'size', u'sort', u'totalElements', u'totalPages']], [u'data', u'message', u'status', u'success']]
        kernel = {"page" : 1, "pageSize": 20, "scope" : "MY_QUESTION"}
        feedback_list = GET(self.my_feedback, kernel)
        self.determine_error(feedback_list, "Get All Feedback", template, self.my_feedback)
        feedback_list = json.loads(feedback_list)['data']['content']
        for i in range(len(feedback_list)):
            self.feedback_id.append(feedback_list[i]['id'])
        self.times += 1

    def get_single_feedback(self):
        print "Getting single feedback..."
        self.get_my_feedback()
        template = [[[[u'applicationDate', u'applyNo', u'attList', u'createDate', u'createUser', u'id', u'manageDate', u'org', u'readRight', u'service', u'serviceUpdateDate', u'shareUserIds', u'solveDate', u'status', u'write', u'writeRight']], [[u'applyNo', u'attList', u'createDate', u'createUser', u'date', u'describe', u'id', u'name', u'org', u'readRight', u'shareUserIds', u'write', u'writeRight']], [u'answerAndQuestion', u'applyNo', u'attList', u'createDate', u'createName', u'createUser', u'id', u'open', u'org', u'orgName', u'readRight', u'shareUserIds', u'sortDate', u'status', u'workOrderInformation', u'write', u'writeRight']], [u'data', u'message', u'status', u'success']]
        kernel = {"id": self.feedback_id[0], "open" : False}
        self.determine_error(GET(self.feedback, kernel), "Get Single Feedback", template, self.feedback)
        self.times += 1

    def reply_feedback(self):
        print "Reply my feedback..."
        self.get_my_feedback()
        template = [[u'message', u'status', u'success']]
        kernel = {"id":self.feedback_id[0],"open":False,"answerAndQuestion":[{"describe":"Robot Okay","attList":[]}]}
        self.determine_error(PUT(self.feedback, kernel), "Reply Feedback", template, self.feedback)
        self.times += 1

    def change_password(self):
        print "Change my password..."
        kernel = {"newPassword" : "MTIzNDU2Nzg=", "oldPassword" : "MTIzNDU2Nzg="}
        template = [[u'message', u'status', u'success']]
        self.determine_error(PUT(self.password, kernel), "Change Password", template, self.password)
        self.times += 1

    def determine_error(self,data, name, template=[], url=""):
        error = False
        Failure_reason = ""
        try:
            result = json.loads(data)['success']
        except:
            result = "No Result"
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        template = sort_my_array(template)
        to_compare = sort_my_array(title_exporter(json.loads(data)))
        missing_list = comparator(to_compare, template)
        if (data == None):
            Failure_reason += "/No Data Coming Out"
            error = True
        if (not result):
            Failure_reason += "/Not pass the system test"
            error = True
        if (missing_list != []):
            Failure_reason += "/Kernel Comparison Failed, Missing: " + str(missing_list)
            error = True
        if error:
            print Failure_reason
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        try:
            my_message = json.loads(data)['message']
        except:
            my_message = "No Message"
        kernel = {"Name" : name, "URL" : url, "Success" : result, "Message": my_message, "Failure Reason": Failure_reason}
        self.result_dict[self.class_name].append(kernel)
        return data

    def show_off_all_data(self):
        print "................................................"
        print ".......Notification Function Summary............"
        print "Function runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Failure Url:"
        for url in self.url_list:
            print url
        print "Please check the dictionary for more information"
        print "...............Thank you........................"


class Whats_up:
    def __init__(self):
        self.iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
        self.whatsupurl = "http://testwww.iquicker.com.cn/iquicker_web/microblog/data/blog"
        self.all_blogs = "http://testwww.iquicker.com.cn/iquicker_web/blogall/data/blogs/"
        self.repost_url = "http://testwww.iquicker.com.cn/iquicker_web/microblog/data/blog"
        self.discuss_url = "http://testwww.iquicker.com.cn/iquicker_web/discuss/data"
        self.like_url =  "http://testwww.iquicker.com.cn/iquicker_web/blogall/data/good/"
        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0
        self.blog_id = []
        self.reply_id = ""
        self.master_id = ""
        self.my_name = ""
        self.my_id = ""
        self.function_name = {"login" : 1, "Post Whats up" : 2, "Get all blogs" : 3, "Get single blog" : 4,
                              "Delete Blog" : 5, "Repost Blog" : 6, "Initial reply" : 7, "Reply blog" : 8,
                              "Like the blog" : 9}

        self.class_name = str(self.__class__).split('__main__.')[1]
        self.result_dict = {self.class_name : []}

    def login(self):
        print "in Login System..."
        template = [[u'status', u'message', u'data', u'success'], [[u'orgs', u'initialised']]]
        kernel = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
        self.determine_error(POST(self.iQuickerUrl, kernel), "login",template, self.iQuickerUrl)
        self.times += 1

    def post_whatsup(self):
        print "Posting What's Up now..."
        template = [[[[[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussList', u'id', u'imgList', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [u'blog']], [u'data', u'message', u'status', u'success']]
        kernel = {"publishScope":["company"],"publishScopeName":["/u5168/u516C/u53F8"],"content":"Robot Send",
                  "isFile":"N","relay":0,"attList":[],"userIdNames":"","imgList":[]}
        name_id = POST(self.whatsupurl, kernel)
        self.determine_error(name_id, "Post Whats up", template, self.whatsupurl)
        name_id = json.loads(name_id)['data']['blog']
        self.my_id = name_id['userId']
        self.my_name = name_id['userName']
        self.times += 1

    def get_all_blogs(self):
        print "Get all blogs..."
        self.blog_id = []
        template = [[[[[[[[[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussList', u'id', u'imgList', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussList', u'id', u'imgList', u'isFile', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussList', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'master', u'relay', u'source']], [[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussedId', u'discussedUserId', u'discussedUserName', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussList', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussedId', u'discussedUserId', u'discussedUserName', u'id', u'isFile', u'masterId', u'org', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'discuss', u'master', u'source']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [u'department', u'list', u'myId', u'myName', u'totalpage']], [u'data', u'message', u'status', u'success']]
        kernel = {"pageNo" : 1, "pageSize" : 10, "sortInfo" : "DESC_publishTime"}
        blogid_list = GET(self.all_blogs, kernel)
        self.determine_error(blogid_list, "Get all blogs", template, self.all_blogs)
        blogid_list = json.loads(blogid_list)['data']['list']
        for i in range(len(blogid_list)):
            self.blog_id.append(blogid_list[i]['id'])
        self.times += 1

    def get_single_blog(self):
        print "Get a single blog..."
        self.get_all_blogs()
        template = [[[[[[[[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussList', u'id', u'imgList', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussList', u'id', u'imgList', u'isFile', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussList', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'master', u'relay', u'source']], [[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussedId', u'discussedUserId', u'discussedUserName', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussList', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussedId', u'discussedUserId', u'discussedUserName', u'id', u'isFile', u'masterId', u'org', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'discuss', u'master', u'source']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [u'data', u'message', u'status', u'success']]
        kernel = {"id" : self.blog_id[0]}
        url = self.all_blogs + self.blog_id[0]
        self.determine_error(GET(url,kernel), "Get single blog", template, url)
        self.times += 1

    def delete_blog(self):
        print "Deleting blog..."
        self.get_all_blogs()
        template = [[u'message', u'status', u'success']]
        kernel = {"id" : self.blog_id[0]}
        url = self.all_blogs + self.blog_id[0]
        self.determine_error(DELETE(url,kernel), "Delete Blog", template, url)
        self.times += 1

    def repost_blog(self):
        print "reposting blogs..."
        self.get_all_blogs()
        template = [[[[[[[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussList', u'id', u'imgList', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussList', u'id', u'imgList', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussList', u'id', u'imgList', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'master', u'relay', u'source']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [u'blog']], [u'data', u'message', u'status', u'success']]
        kernel = {"type":"relay","masterId":self.blog_id[0],
                  "content":"Good","isFile":"N","publishScope":["company"],
                  "publishScopeName":["/u5168/u516C/u53F8"],"relay":0,"attList":[],"userIdNames":""}
        self.determine_error(POST(self.repost_url, kernel), "Repost Blog", template, self.repost_url)
        self.times += 1

    def reply_blog_init(self):
        print "replying blog init..."
        # This function must be placed right after creating the post in case of error
        self.get_all_blogs()
        template = [[[[[[[[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussList', u'id', u'imgList', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussList', u'id', u'imgList', u'isFile', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussList', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'master', u'relay', u'source']], [[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussedId', u'discussedUserId', u'discussedUserName', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussedId', u'discussedUserId', u'discussedUserName', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussList', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'discuss', u'master', u'source']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [u'data', u'message', u'status', u'success']]
        kernel = {"discussType":"weibo","masterId":self.blog_id[0],"discussedId":"",
                  "discussedUserId":"","discussedUserName":"","content":"Robot Initial reply","isFile":"N",
                  "publishTime":get_current_time(),"relay":0,"attList":[],"userIdNames":"","atConnectTitle":"Click to see"}
        get_master_id = POST(self.discuss_url, kernel)
        self.determine_error(get_master_id, "Initial reply", template, self.discuss_url)
        get_master_id = json.loads(get_master_id)['data']['content']['discuss']
        self.reply_id = get_master_id['id']
        self.master_id = get_master_id['masterId']
        self.times += 1

    def reply_blog(self):
        print "replying blog..."
        # This function must be placed right after reply_blog_init
        self.get_all_blogs()
        template = [[[[[[[[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussList', u'id', u'imgList', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussList', u'id', u'imgList', u'isFile', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussList', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'master', u'relay', u'source']], [[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussedId', u'discussedUserId', u'discussedUserName', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussedId', u'discussedUserId', u'discussedUserName', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [[u'attList', u'content', u'discussList', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'discuss', u'master', u'source']], [u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [u'data', u'message', u'status', u'success']]
        kernel = {"discussType":"weibo","masterId":self.master_id,
                  "discussedId":self.reply_id,
                  "discussedUserId":self.my_id,
                  "discussedUserName":self.my_name,"content":"nice","isFile":"N","publishTime":"2016-07-05 10:52:08",
                  "relay":0,"attList":[],"userIdNames":"","atConnectTitle":"Click to see"}
        self.determine_error(POST(self.discuss_url, kernel), "Reply blog", template, self.discuss_url)
        self.times += 1


    def like_this_blog(self):
        print "Like this blog->..."
        self.get_all_blogs()
        template = [[u'message', u'status', u'success']]
        kernel = {"id" : self.blog_id[0]}
        url = self.like_url + self.blog_id[0]
        self.determine_error(POST(url, kernel), "Like the blog", template, url)
        self.times += 1

    def determine_error(self,data, name, template=[], url=""):
        error = False
        Failure_reason = ""
        try:
            result = json.loads(data)['success']
        except:
            result = "No Result"
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        template = sort_my_array(template)
        to_compare = sort_my_array(title_exporter(json.loads(data)))
        missing_list = comparator(to_compare, template)
        if (data == None):
            Failure_reason += "/No Data Coming Out"
            error = True
        if (not result):
            Failure_reason += "/Not pass the system test"
            error = True
        if (missing_list != []):
            Failure_reason += "/Kernel Comparison Failed, Missing: " + str(missing_list)
            error = True
        if error:
            print Failure_reason
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        try:
            my_message = json.loads(data)['message']
        except:
            my_message = "No Message"
        kernel = {"Name" : name, "URL" : url, "Success" : result, "Message": my_message, "Failure Reason": Failure_reason}
        self.result_dict[self.class_name].append(kernel)
        return data

    def show_off_all_data(self):
        print "................................................"
        print "...........Blog Function Summary............"
        print "Function runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Failure Url:"
        for url in self.url_list:
            print url
        print "Please check the dictionary for more information"
        print "...............Thank you........................"

class attendance:
    def __init__(self):
        self.iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
        self.personal_info = "http://testwww.iquicker.com.cn/iquicker_web/login/user"
        self.current_permission = "http://testwww.iquicker.com.cn/iquicker_web//attendance/attendanceSearchController/getCurrentPermissino"
        self.check_new_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/systemInitConfigCtrl/checkNewPersonForMobile"
        self.all_attendance = "http://testwww.iquicker.com.cn/iquicker_web/attendance/outWorkController/findAll"
        self.att_info = "http://testwww.iquicker.com.cn/iquicker_web/attendance/attendMobileCardCtrl/mobileCardConfigFind"
        self.personal_leave = "http://testwww.iquicker.com.cn/iquicker_web/attendance/leaveController/findAttendMobileLeaveForDays"
        self.outwork_url =  "http://testwww.iquicker.com.cn/iquicker_web/attendance/attendMobileCardCtrl/mobileCardFindOutWork"
        self.personal_att_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/attendanceReportController/findPersonDetailData"
        self.spec_att_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/attendanceSearchController/findForAttendMobileByPersonIdDate"
        self.other_att_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/attendanceSearchController/findByPageForMobileDeal"
        self.vacation_type = "http://testwww.iquicker.com.cn/iquicker_web/attendance/vacationTypeController/findAll"
        self.find_last_att_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/attendanceController/findLastAttendanceForMobile"
        self.find_by_leave_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/leaveController/findByLeaveEnable"
        self.post_leave_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/leaveController/continuesLeavesSave"
        self.modify_leave_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/leaveController/save"
        self.find_leave_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/leaveApplyController/findAll"
        self.find_person_leave = "http://testwww.iquicker.com.cn/iquicker_web/attendance/leaveApplyController/findByLeaveApplyIds"
        self.vacation_decision = "http://testwww.iquicker.com.cn/iquicker_web/attendance/leaveApplyController/btSave"
        self.days_leave_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/leaveController/continueLeaveModifyForMobile"
        self.delete_leave_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/leaveController/deleteForMobile"
        self.outwork_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/outWorkController/findByPage"
        self.outwork_post_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/outWorkController/planSave"
        self.outwork_single_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/outWorkController/findOne"
        self.outwork_delete_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/outWorkController/delete"
        self.find_default_check_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/beateCardPlaceController/findDefaultAjaxResult"
        self.find_check_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/beateCardPlaceController/findByPage"
        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0
        self.my_id = ""
        self.my_name = ""
        self.personId = []
        self.vacation_type_id = []
        self.leaveApplyId = []
        self.leave_id = []
        self.outwork_id = []
        self.function_name = {"login" : 1, "Get Personal info" : 2, "Get Current Permission" : 3, "Check new person" : 4,
                              "Get all Attendance" : 5, "Get personal Attendance" : 6, "Get Leave Id" : 7, "Get Outwork Data" : 8,
                              "Get Attendacne List" : 9, "Get others Attendance" : 10, "All vacation types" : 11,
                              "Find Last Attendance" : 12, "Find By Leave" : 13, "Post Leave" : 14, "Modify Leave" : 15,
                              "Delete Leave" : 16, "Find All Leave" : 17, "Get Single Vacation" : 18, "Get single Vacation" : 19,
                              "Approve for Vacation" : 20, "Find Outwork info" : 21, "Post Outwork" : 22, "Get Single Outwork" :23,
                              "Delete Outwork" : 24, "Find Default Location" : 25, "Find all location" : 26, "Get Specific Attendance" : 27}

        self.class_name = str(self.__class__).split('__main__.')[1]
        self.result_dict = {self.class_name : []}

    def login(self):
        print "in Login System..."
        template = [[u'status', u'message', u'data', u'success'], [[u'orgs', u'initialised']]]
        kernel = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
        self.determine_error(POST(self.iQuickerUrl, kernel), "login",template, self.iQuickerUrl)
        self.times += 1

    def get_personal_info(self):
        print "Getting Personal Info..."
        template = [[[[u'deptManager', u'flag', u'flag2', u'id', u'name', u'org', u'parDept', u'prefixId', u'root', u'shortname', u'sn', u'status', u'subDept', u'usable', u'zfield1', u'zfield10', u'zfield2', u'zfield3', u'zfield4', u'zfield5', u'zfield6', u'zfield7', u'zfield8', u'zfield9']], [u'address', u'bankCard', u'birthday', u'createTime', u'department', u'email', u'enname', u'fax', u'hometown', u'id', u'idcard', u'img', u'innerEmail', u'innerEmailContact', u'isTrialAccount', u'itcode', u'joinTime', u'joindate', u'mobile', u'name', u'org', u'pinyin', u'pinyinPrefix', u'position', u'prefixId', u'qualifications', u'sex', u'shortname', u'signature', u'sn', u'status', u'statusReason', u'telephone', u'type']], [u'data', u'message', u'orgCode', u'orgInnerEmailStatus', u'orgLogoColour', u'orgLogoWhite', u'orgName', u'status', u'success', u'theme']]
        my_data = GET(self.personal_info)
        self.determine_error(my_data, "Get Personal info", template, self.personal_info)
        self.my_id = json.loads(my_data)['data']['id']
        self.my_name = json.loads(my_data)['data']['name']
        self.times += 1

    def get_current_permission(self):
        print "Get Current Permission..."
        template = [[u'data', u'message', u'status', u'success']]
        self.determine_error(GET(self.current_permission), "Get Current Permission", template, self.current_permission)
        self.times += 1

    def check_new_person(self):
        print "Check new Person..."
        template = [[[u'isHasAttend', u'isMaster', u'message']], [u'data', u'message', u'status', u'success']]
        self.determine_error(GET(self.check_new_url),"Check new person", template, self.check_new_url)
        self.times += 1

    def get_all_attendance(self):
        print "Get all attendance..."
        template = [[[u'approvalItcode', u'approvalName', u'approvalStateDesc', u'aprovalCommont', u'aprovalDate', u'aprovalId', u'aprovalResult', u'aprovalSate', u'createDate', u'creator', u'creatorItcode', u'creatorName', u'id', u'isNeedCreator', u'mobileBeatList', u'mobileBeats', u'org', u'outDate', u'outEndDate', u'outReason', u'outStartDate', u'outType', u'outTypeDesc', u'remark']], [u'data', u'message', u'status', u'success']]
        kernel = {"aprovalSate" : 1, "outEndDate" : "2017-07-05 23:59:59", "outStartDate" : "2015-07-06 00:00:00", "outType" : ""}
        self.determine_error(POST(self.all_attendance, kernel), "Get all Attendance", template, self.all_attendance)
        self.times += 1

    def get_personal_attendance(self):
        print "Get Personal Attendance..."
        template = [[[[u'attendanceRules', u'circleEndDay', u'circleStartDay', u'circleType', u'createDate', u'creatorId', u'elasticType', u'freeTime', u'freeType', u'id', u'isDefault', u'lateCount', u'lateTime', u'org', u'restTimeEnd', u'restTimeStart', u'restType', u'schedulName', u'sortCode', u'workEnd', u'workMinutes', u'workStart', u'workTime']], [[u'beatPlace', u'beatPlaceRemark', u'buffer', u'createDate', u'creatorId', u'firstBeatCardTime', u'id', u'isDefault', u'lonLat', u'org', u'sortCode', u'workStartTime', u'workdEndTime']], [u'approvalId', u'approvalItCode', u'approvalName', u'attendaceType', u'attendanceEndDate', u'attendanceSchedul', u'attendanceSchedulId', u'attendanceStartDate', u'attendanceTypeDesc', u'beateCardPlace', u'beateCardPlaceId', u'cardInfo', u'cardMachineList', u'createDate', u'creatorId', u'deptName', u'id', u'isOperate', u'itcode', u'org', u'pageNo', u'pageSize', u'personId', u'personType', u'positon', u'proxyId', u'proxyItCode', u'proxyName', u'userName', u'vacationDays', u'vacationDaysList', u'workEnd', u'workStart']], [u'data', u'message', u'status', u'success']]
        self.determine_error(GET(self.att_info), "Get personal Attendance", template, self.att_info)
        self.times += 1

    def get_personal_leave(self):
        print "Get personal leave info..."
        template = [[[[[u'createDate', u'id', u'lackDate', u'lackEndTime', u'lackLength', u'lackStartTime', u'lackType', u'leaveExist', u'org', u'personId', u'sortCode']], [u'applyerId', u'applyerItcode', u'approvalName', u'aprovalId', u'attendCircleEnd', u'attendCircleStart', u'attendDate', u'beatEndTime', u'beatStartTime', u'groupId', u'groupIdTotal', u'id', u'isOperate', u'lackInfo', u'lackTypeDesc', u'leave', u'leaveApplys', u'leaveEndTime', u'leaveIds', u'leaveStartTime', u'leaves', u'userName', u'workEndTime', u'workEndTimeDate', u'workStartTime', u'workTime']], [u'leaveModules', u'operate']], [u'data', u'message', u'status', u'success']]
        self.leave_id = []
        kernel = {"month" : 7, "year" : 2016}
        data_fetcher = GET(self.personal_leave,kernel)
        self.determine_error(data_fetcher, "Get Leave Id", template, self.personal_leave)
        data_fetcher = json.loads(data_fetcher)['data']['leaveModules']
        for i in range(len(data_fetcher)):
            if len(data_fetcher[i]['leaves']):
                if (data_fetcher[i]['leaves'][0]['groupId'] == None):
                    # case: Single Leave
                    self.leave_id.append(data_fetcher[i]['leaves'][0]['id'])
                else:
                    self.leave_id.append([data_fetcher[i]['leaves'][0]['id'],data_fetcher[i]['leaves'][0]['groupId']])
        self.times += 1

    def get_outwork(self):
        print "Getting Outwork data..."
        template = [[[[u'approvalItcode', u'approvalName', u'approvalStateDesc', u'aprovalCommont', u'aprovalDate', u'aprovalId', u'aprovalResult', u'aprovalSate', u'createDate', u'creator', u'creatorItcode', u'creatorName', u'id', u'isNeedCreator', u'mobileBeatList', u'mobileBeats', u'org', u'outDate', u'outEndDate', u'outReason', u'outStartDate', u'outType', u'outTypeDesc', u'remark']], [u'content', u'first', u'last', u'number', u'numberOfElements', u'size', u'sort', u'totalElements', u'totalPages']], [u'data', u'message', u'status', u'success']]
        self.determine_error(GET(self.outwork_url), "Get Outwork Data", template, self.outwork_url)
        self.times += 1

    def get_att_list(self):
        print "Getting all Personal Attendance..."
        template = [[[[u'createDate', u'id', u'lackDate', u'lackEndTime', u'lackLength', u'lackStartTime', u'lackType', u'leaveExist', u'org', u'personId', u'sortCode']], [u'applyerId', u'applyerItcode', u'approvalName', u'aprovalId', u'attendCircleEnd', u'attendCircleStart', u'attendDate', u'beatEndTime', u'beatStartTime', u'groupId', u'groupIdTotal', u'id', u'isOperate', u'lackInfo', u'lackTypeDesc', u'leave', u'leaveApplys', u'leaveEndTime', u'leaveIds', u'leaveStartTime', u'leaves', u'userName', u'workEndTime', u'workEndTimeDate', u'workStartTime', u'workTime']], [u'data', u'message', u'status', u'success']]
        kernel = {"month" : 7, "personId" : self.my_id, "year": 2016}
        self.determine_error(GET(self.personal_att_url, kernel), "Get Attendacne List", template, self.personal_att_url)
        self.times += 1

    def get_spec_att(self):
        print "Get Specific Attendance..."
        kernel = {"personId" : self.my_id, "searchDate" : "2016-07-01"}
        template = [[[u'approvalDate', u'approvalId', u'approvalItcode', u'approvalName', u'beatCardFirsrtTime', u'beatCardLastTime', u'childIndex', u'createDate', u'creatorId', u'groupId', u'id', u'isOperate', u'itCode', u'lackEndTime', u'lackStartTime', u'lackStateDesc', u'lackType', u'leaveApply', u'leaveEndTime', u'leaveExist', u'leaveHours', u'leaveMinutes', u'leaveStartTime', u'leaveState', u'leaveStateDesc', u'machineType', u'month', u'operate', u'org', u'parentIndex', u'personId', u'remark', u'sortCode', u'updateDate', u'userName', u'vacationType', u'vacationTypeId', u'year']], [u'data', u'message', u'status', u'success']]
        self.determine_error(GET(self.spec_att_url, kernel), "Get Specific Attendance", template, self.spec_att_url)
        self.times += 1

    def get_other_att(self):
        print "get other people Attendance..."
        kernel = { "month" : 7, "page" : 1, "pageSize" : 8, "year" : 2016}
        template = [[[[u'approvalId', u'approvalName', u'approvarItcode', u'attendance', u'deptName', u'id', u'itCode', u'leaveTotal', u'name', u'position']], [u'attendLoginInfosResult', u'totalPage']], [u'data', u'message', u'status', u'success']]
        self.determine_error(GET(self.other_att_url, kernel), "Get others Attendance", template, self.other_att_url)
        self.times += 1

    def get_all_vacation_type(self):
        print "Get all vacation type now..."
        self.vacation_type_id = []
        template = [[[u'alculationUnit', u'creartor', u'createDate', u'creatorId', u'creatorItCode', u'creatorName', u'days', u'deduct', u'effect', u'fixType', u'halfDayHours', u'id', u'isDefault', u'noBreak', u'org', u'sortCode', u'vacationName']], [u'data', u'message', u'status', u'success']]
        vacation_type = POST(self.vacation_type, "")
        self.determine_error(vacation_type, "All vacation types", template, self.vacation_type)
        vacation_type = json.loads(vacation_type)['data']
        for i in range(len(vacation_type)):
            self.vacation_type_id.append(vacation_type[i]['id'])
        self.times += 1

    def find_last_attendance(self):
        print "Finding last attendance..."
        template = [[[[u'attendanceRules', u'circleEndDay', u'circleStartDay', u'circleType', u'createDate', u'creatorId', u'elasticType', u'freeTime', u'freeType', u'id', u'isDefault', u'lateCount', u'lateTime', u'org', u'restTimeEnd', u'restTimeStart', u'restType', u'schedulName', u'sortCode', u'workEnd', u'workMinutes', u'workStart', u'workTime']], [[u'beatPlace', u'beatPlaceRemark', u'buffer', u'createDate', u'creatorId', u'firstBeatCardTime', u'id', u'isDefault', u'lonLat', u'org', u'sortCode', u'workStartTime', u'workdEndTime']], [u'approvalId', u'approvalItCode', u'approvalName', u'attendaceType', u'attendanceEndDate', u'attendanceSchedul', u'attendanceSchedulId', u'attendanceStartDate', u'attendanceTypeDesc', u'beateCardPlace', u'beateCardPlaceId', u'cardInfo', u'cardMachineList', u'createDate', u'creatorId', u'deptName', u'id', u'isOperate', u'itcode', u'org', u'pageNo', u'pageSize', u'personId', u'personType', u'positon', u'proxyId', u'proxyItCode', u'proxyName', u'userName', u'vacationDays', u'vacationDaysList', u'workEnd', u'workStart']], [u'data', u'message', u'status', u'success']]
        kernel = {"personId" : self.my_id}
        self.determine_error(GET(self.find_last_att_url, kernel), "Find Last Attendance", template, self.find_last_att_url)
        self.times += 1

    def find_by_leave_enable(self):
        print "Find By leave Enable Terminal..."
        kernel = {"month" : 7, "year" : 2016}
        template = [[u'data', u'message', u'status', u'success']]
        self.determine_error(GET(self.find_by_leave_url, kernel), "Find By Leave", template, self.find_by_leave_url)
        self.times += 1

    def post_leave(self):
        # The date in here can be modified
        print "Ready to leave..."
        self.get_all_vacation_type()
        kernel = {"leaveState":"1","approvalId":self.my_id,"leaveEndTime":"2016-07-08",
                  "leaveStartTime":"2016-07-04","vacationTypeId":self.vacation_type_id[1],
                  "remark":"Robot Test","year":2016,"month":7,"machineType":2}
        self.determine_error(POST(self.post_leave_url, kernel), "Post Leave", ["No Template"], self.post_leave_url)
        self.times += 1

    def modify_leave(self):
        print "Modifying leave applications..."
        self.get_personal_leave()
        if isinstance(self.leave_id[0], list):
            kernel = {"groupId":self.leave_id[0][1],"vacationTypeId": self.vacation_type_id[1],
                  "approvalId":self.my_id,"remark":"Robot Test1","leaveEndTime":"2016-07-08",
                  "leaveStartTime":"2016-07-04","machineType":2}
            url = self.days_leave_url
        else:
            kernel = {"groupId":None, "id" : self.leave_id[0],"vacationTypeId": self.vacation_type_id[1],
                  "approvalId":self.my_id,"remark":"Robot Test1","leaveEndTime":"2016-07-08","leaveState" : 1,
                  "leaveStartTime":"2016-07-04","machineType":2}
            url = self.modify_leave_url
        self.determine_error(POST(url, kernel), "Modify Leave", ["No Template"], url)
        self.times += 1

    def delete_leave_request(self):
        print "Delete leave request now..."
        self.get_personal_leave()
        if isinstance(self.leave_id[0], list):
            kernel = {"groupId" : self.leave_id[0][1], "id" : self.leave_id[0][0]}
        else:
            kernel = {"id" : self.leave_id[0], "groupId" : None}
        print kernel
        print self.delete_leave_url
        print self.determine_error(POST(self.delete_leave_url, kernel), "Delete Leave", ["No Template"], self.delete_leave_url)
        self.times += 1

    def find_all_leave_apply(self):
        print "Find all applications of Leaving..."
        self.personId = []
        kernel ={"applyState" :1 ,"month": "", "year" : 2016}
        template = [[[[u'applyState', u'approvalId', u'approvalItcode', u'aprovaContent', u'aprovalResult', u'groupId', u'isOperate', u'leaveApplyId', u'leaveEndTime', u'leaveStartTime', u'leaveid', u'personId', u'remark', u'userName', u'vacationType', u'vacationTypeName']], [u'attendDate', u'isOperator', u'leaveApplyPends', u'outWorks', u'personId', u'userName']], [u'data', u'message', u'status', u'success']]
        personId_list = GET(self.find_leave_url, kernel)
        self.determine_error(personId_list, "Find All Leave", template, self.find_leave_url)
        personId_list = json.loads(personId_list)['data']
        for i in range(len(personId_list)):
            self.personId.append(personId_list[i]['personId'])
        self.times += 1

    def select_person_vacation(self):
        print "Select a single person's Vacation..."
        self.leaveApplyId = []
        template = [[[[u'applyState', u'approvalId', u'approvalItcode', u'aprovaContent', u'aprovalResult', u'groupId', u'isOperate', u'leaveApplyId', u'leaveEndTime', u'leaveStartTime', u'leaveid', u'personId', u'remark', u'userName', u'vacationType', u'vacationTypeName']], [u'attendDate', u'isOperator', u'leaveApplyPends', u'outWorks', u'personId', u'userName']], [u'data', u'message', u'status', u'success']]
        kernel ={"applyState" :1 ,"personId" : self.personId[0],"month": "", "year" : 2016}
        apply_id_fetcher = GET(self.find_leave_url, kernel)
        self.determine_error(apply_id_fetcher, "Get Single Vacation", template, self.find_leave_url)
        apply_id_fetcher = json.loads(apply_id_fetcher)['data'][0]['leaveApplyPends']
        for i in range(len(apply_id_fetcher)):
            self.leaveApplyId.append(apply_id_fetcher[i]['leaveApplyId'])
        self.times += 1

    def get_person_Vacation_apply(self):
        print "Getting single piece of vacation request..."
        self.select_person_vacation()
        template = [[[u'applyState', u'applyTime', u'applyerId', u'approvalDate', u'approvalName', u'aprovaContent', u'aprovalId', u'aprovalResult', u'aprovalResultDesc', u'beatCardFirsrtTime', u'beatCardLastTime', u'createDate', u'creatorId', u'id', u'isOperate', u'leaveEndTime', u'leaveRemark', u'leaveStartTime', u'org', u'userName', u'vacationType', u'vacationTypeId', u'vacationTypeName']], [u'data', u'message', u'status', u'success']]
        kernel = {"leaveApplyId" : self.leaveApplyId[0]}
        self.determine_error(GET(self.find_person_leave, kernel), "Get single Vacation", template, self.find_person_leave)
        self.times += 1

    def approve_person_vacation(self):
        print "Approval for person's vacation..."
        self.select_person_vacation()
        approval_array = []
        sub_kernel = {"aprovaContent" : "Agree", "aprovalResult" : 1, "isOperate" : True, "leaveAppId":""}
        days_id = self.leaveApplyId[-1].split(',')
        for i in range(len(days_id)):
            sub_kernel['leaveAppId'] = days_id[i]
            approval_array.append(sub_kernel)
        kernel = {"leaveApplyPends" : approval_array}
        self.determine_error(POST(self.vacation_decision, kernel), "Approve for Vacation", ["No Template"], self.vacation_decision)
        self.times += 1

    def find_outwork(self):
        print "Finding all outwork info..."
        self.outwork_id = []
        template = [[[[u'approvalItcode', u'approvalName', u'approvalStateDesc', u'aprovalCommont', u'aprovalDate', u'aprovalId', u'aprovalResult', u'aprovalSate', u'createDate', u'creator', u'creatorItcode', u'creatorName', u'id', u'isNeedCreator', u'mobileBeatList', u'mobileBeats', u'org', u'outDate', u'outEndDate', u'outReason', u'outStartDate', u'outType', u'outTypeDesc', u'remark']], [[u'ascending', u'direction', u'ignoreCase', u'NoneHandling', u'property']], [u'content', u'first', u'last', u'number', u'numberOfElements', u'size', u'sort', u'totalElements', u'totalPages']], [u'data', u'message', u'status', u'success']]
        kernel = {"page" : 1, "pageSize" : 20, "search_GTE_outStartDate" : "2015-07-12 00:00:00", "search_LTE_outEndDate" : "2017-07-11 23:59:59"}
        outwork_id_list = GET(self.outwork_url, kernel)
        self.determine_error(outwork_id_list, "Find Outwork info", template, self.outwork_url)
        outwork_id_list = json.loads(outwork_id_list)['data']['content']
        for i in range(len(outwork_id_list)):
            self.outwork_id.append(outwork_id_list[i]['id'])
        self.times += 1

    def post_outwork(self):
        print "Posting outwork..."
        template = [[[u'approvalItcode', u'approvalName', u'approvalStateDesc', u'aprovalCommont', u'aprovalDate', u'aprovalId', u'aprovalResult', u'aprovalSate', u'createDate', u'creator', u'creatorItcode', u'creatorName', u'id', u'isNeedCreator', u'mobileBeatList', u'mobileBeats', u'org', u'outDate', u'outEndDate', u'outReason', u'outStartDate', u'outType', u'outTypeDesc', u'remark']], [u'data', u'message', u'status', u'success']]
        kernel = {"aprovalId" : self.my_id, "isNeedCreator" : 1, "outEndDate" : "2016-08-15 01:00:00",
                  "outReason" : "Roboto", "outStartDate" : "2016-08-15 00:00:00", "outType" : "2", "remark" : "Sapporo" }
        self.determine_error(POST(self.outwork_post_url, kernel), "Post Outwork", template, self.outwork_post_url)
        self.times += 1

    def get_single_outwork(self):
        print "Getting single Out work..."
        self.find_outwork()
        template = [[[u'approvalItcode', u'approvalName', u'approvalStateDesc', u'aprovalCommont', u'aprovalDate', u'aprovalId', u'aprovalResult', u'aprovalSate', u'createDate', u'creator', u'creatorItcode', u'creatorName', u'id', u'isNeedCreator', u'mobileBeatList', u'mobileBeats', u'org', u'outDate', u'outEndDate', u'outReason', u'outStartDate', u'outType', u'outTypeDesc', u'remark']], [u'data', u'message', u'status', u'success']]
        kernel = {"id" : self.outwork_id[0]}
        self.determine_error(GET(self.outwork_single_url, kernel), "Get Single Outwork", template, self.outwork_single_url)
        self.times += 1

    def delete_outwork(self):
        print "Deleting one outwork..."
        template = [[u'data', u'message', u'status', u'success']]
        self.find_outwork()
        kernel = {"id" : self.outwork_id[0]}
        self.determine_error(GET(self.outwork_delete_url, kernel), "Delete Outwork", template, self.outwork_delete_url)
        self.times += 1

    def find_default_check_location(self):
        print "Finding All default check Locations..."
        template = [[[u'beatPlace', u'beatPlaceRemark', u'buffer', u'createDate', u'creatorId', u'firstBeatCardTime', u'id', u'isDefault', u'lonLat', u'org', u'sortCode', u'workStartTime', u'workdEndTime']], [u'data', u'message', u'status', u'success']]
        self.determine_error(GET(self.find_default_check_url), "Find Default Location", template, self.find_default_check_url)
        self.times += 1

    def find_all_check_location(self):
        print "Finding all Check locations..."
        template = [[[[u'beatPlace', u'beatPlaceRemark', u'buffer', u'createDate', u'creatorId', u'firstBeatCardTime', u'id', u'isDefault', u'lonLat', u'org', u'sortCode', u'workStartTime', u'workdEndTime']], [u'content', u'first', u'last', u'number', u'numberOfElements', u'size', u'sort', u'totalElements', u'totalPages']], [u'data', u'message', u'status', u'success']]
        self.determine_error(GET(self.find_check_url), "Find all location", template, self.find_check_url)
        self.times += 1

    def determine_error(self,data, name, template=[], url=""):
        error = False
        Failure_reason = ""
        try:
            result = json.loads(data)['success']
        except:
            result = "No Result"
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        template = sort_my_array(template)
        to_compare = sort_my_array(title_exporter(json.loads(data)))
        missing_list = comparator(to_compare, template)
        if (data == None):
            Failure_reason += "/No Data Coming Out"
            error = True
        if (not result):
            Failure_reason += "/Not pass the system test"
            error = True
        if (missing_list != []):
            Failure_reason += "/Kernel Comparison Failed, Missing: " + str(missing_list)
            error = True
        if error:
            print Failure_reason
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        try:
            my_message = json.loads(data)['message']
        except:
            my_message = "No Message"
        kernel = {"Name" : name, "URL" : url, "Success" : result, "Message": my_message, "Failure Reason": Failure_reason}
        self.result_dict[self.class_name].append(kernel)
        return data

    def show_off_all_data(self):
        print "................................................"
        print ".........Attendance Function Summary............"
        print "Function runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Failure Url:"
        for url in self.url_list:
            print url
        print "Please check the dictionary for more information"
        print "...............Thank you........................"

class wreport:
    def __init__(self):
        self.iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
        self.personal_info = "http://testwww.iquicker.com.cn/iquicker_web/login/user"
        self.all_wreport_url = "http://testwww.iquicker.com.cn/iquicker_web/wreport/work-reports"
        self.discuss_num_url = "http://testwww.iquicker.com.cn/iquicker_web/discusslist/data/count/"
        self.discuss_data_url = "http://testwww.iquicker.com.cn/iquicker_web/discusslist/data/"
        self.single_report_url = "http://testwww.iquicker.com.cn/iquicker_web/wreport/work-reports/"
        self.discuss_url = "http://testwww.iquicker.com.cn/iquicker_web/discuss/data"
        self.post_work_url = "http://testwww.iquicker.com.cn/iquicker_web/wreport/work-reports/"
        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0
        self.my_id = ""
        self.my_name = ""
        self.report_id = []
        self.discuss_id = []
        self.function_name = {"login" : 1, "Get Personal info" : 2, "Get all report" : 3, "Get Discuss Number" : 4,
                              "Get Single Report" : 5, "Get Report Discuss" : 6, "Post Report" : 7, "Delete Report" : 8,
                              "Comment on Report" : 9, "Reply Report" : 10}
        self.class_name = str(self.__class__).split('__main__.')[1]
        self.result_dict = {self.class_name : []}

    def login(self):
        print "in Login System..."
        template = [[u'status', u'message', u'data', u'success'], [[u'orgs', u'initialised']]]
        kernel = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
        self.determine_error(POST(self.iQuickerUrl, kernel), "login",template, self.iQuickerUrl)
        self.times += 1

    def get_personal_info(self):
        print "Getting Personal Info..."
        template = [[[[u'deptManager', u'flag', u'flag2', u'id', u'name', u'org', u'parDept', u'prefixId', u'root', u'shortname', u'sn', u'status', u'subDept', u'usable', u'zfield1', u'zfield10', u'zfield2', u'zfield3', u'zfield4', u'zfield5', u'zfield6', u'zfield7', u'zfield8', u'zfield9']], [u'address', u'bankCard', u'birthday', u'createTime', u'department', u'email', u'enname', u'fax', u'hometown', u'id', u'idcard', u'img', u'innerEmail', u'innerEmailContact', u'isTrialAccount', u'itcode', u'joinTime', u'joindate', u'mobile', u'name', u'org', u'pinyin', u'pinyinPrefix', u'position', u'prefixId', u'qualifications', u'sex', u'shortname', u'signature', u'sn', u'status', u'statusReason', u'telephone', u'type']], [u'data', u'message', u'orgCode', u'orgInnerEmailStatus', u'orgLogoColour', u'orgLogoWhite', u'orgName', u'status', u'success', u'theme']]
        my_data = GET(self.personal_info)
        self.determine_error(my_data, "Get Personal info", template, self.personal_info)
        self.my_id = json.loads(my_data)['data']['id']
        self.my_name = json.loads(my_data)['data']['name']
        self.times += 1

    def get_all_wreport(self):
        print "Getting all weekly report..."
        self.report_id = []
        template = [[[[[u'prefixId', u'shareUserId', u'shareUserName']], [u'applyNo', u'attList', u'createDate', u'createUser', u'createUserName', u'endDate', u'id', u'org', u'plan', u'readRight', u'reportType', u'shareUserIds', u'shareUsers', u'startDate', u'summary', u'userDept', u'userDeptName', u'write', u'writeRight']], [u'content', u'first', u'last', u'number', u'numberOfElements', u'size', u'sort', u'totalElements', u'totalPages']], [u'data', u'message', u'status', u'success']]
        kernel = {"page" : 1, "pageSize" : 20, "userShared" : "MINE"}
        report_id_list = GET(self.all_wreport_url, kernel)
        self.determine_error(report_id_list, "Get all report", template, self.all_wreport_url)
        report_id_list = json.loads(report_id_list)['data']['content']
        for i in range(len(report_id_list)):
            self.report_id.append((report_id_list[i]['id']))
        self.times += 1

    def get_discuss_num(self):
        print "Get discuss numbers..."
        self.get_all_wreport()
        template = [[u'data', u'message', u'status', u'success']]
        kernel = {"masterId" : self.report_id[-1]}
        self.determine_error(GET(self.discuss_num_url, kernel), "Get Discuss Number", template, self.discuss_num_url)
        self.times += 1

    def get_single_report(self):
        print "Get single report..."
        self.get_all_wreport()
        template = [[[[u'prefixId', u'shareUserId', u'shareUserName']], [u'applyNo', u'attList', u'createDate', u'createUser', u'createUserName', u'endDate', u'id', u'org', u'plan', u'readRight', u'reportType', u'shareUserIds', u'shareUsers', u'startDate', u'summary', u'userDept', u'userDeptName', u'write', u'writeRight']], [u'data', u'message', u'status', u'success']]
        kernel = {"id" : self.report_id[-1]}
        url = self.single_report_url + self.report_id[-1]
        self.determine_error(GET(url, kernel), "Get Single Report", template, url)
        self.times += 1

    def get_report_discuss(self):
        print "Get report discuss..."
        self.discuss_id = []
        self.get_all_wreport()
        template = [[[[u'applyNo', u'attList', u'content', u'createDate', u'createUser', u'discussedId', u'discussedUserId', u'discussedUserName', u'id', u'isFile', u'masterId', u'org', u'publishScope', u'publishTime', u'readRight', u'relay', u'shareUserIds', u'userId', u'userIdNames', u'userName', u'write', u'writeRight']], [u'applyNo', u'attList', u'createDate', u'createUser', u'discussList', u'id', u'masterId', u'org', u'readRight', u'shareUserIds', u'write', u'writeRight']], [u'data', u'message', u'status', u'success']]
        kernel = {"masterId" : self.report_id[0]}
        url = self.discuss_data_url + self.report_id[0]
        my_discuss_id = GET(url, kernel)
        self.determine_error(my_discuss_id, "Get Report Discuss", template, url)
        my_discuss_id = json.loads(my_discuss_id)['data'][0]['discussList']
        for key in my_discuss_id:
            self.discuss_id.append(key['id'])
        self.times += 1

    def post_work_report(self):
        print "Posting work report..."
        kernel = {"reportType":"DAILY","startDate":1468812207832,"endDate":1468812207832,"summary":"Robot send",
                  "plan":"Robot send next","shareUsers":
                      [{"prefixId":"p-" + self.my_id,"shareUserId":self.my_id,
                        "shareUserName":self.my_name}]}
        template = [[u'message', u'status', u'success']]
        self.determine_error(POST(self.post_work_url, kernel), "Post Report", template, self.post_work_url)
        self.times += 1


    def delete_wreport(self):
        print "Deleting Work report"
        self.get_all_wreport()
        template = [[u'message', u'status', u'success']]
        kernel = {"id" : self.report_id[0]}
        url = self.post_work_url + self.report_id[0]
        self.determine_error(DELETE(url, kernel), "Delete Report", template, url)
        self.times += 1

    def comment_on_report(self):
        print "Comment on the report..."
        self.get_all_wreport()
        template = [[[u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [u'data', u'message', u'status', u'success']]
        kernel = {"discussType":"workreprot","masterId":self.report_id[0],"discussedId":"",
                  "discussedUserId":"","discussedUserName":"","content":"heya","isFile":"N",
                  "publishTime":get_current_time(),"relay":0,"attList":[],"userIdNames":""}
        self.determine_error(POST(self.discuss_url, kernel), "Comment on Report", template, self.discuss_url)
        self.times  += 1

    def reply_on_report(self):
        print "Reply on the report..."
        self.get_all_wreport()
        self.get_report_discuss()
        template = [[[u'applyNo', u'attList', u'companyName', u'content', u'createDate', u'createUser', u'deleted', u'discussList', u'goodPeopleId', u'id', u'org', u'publishScope', u'publishScopeName', u'publishTime', u'readRight', u'relayTimes', u'shareUserIds', u'storePeopleId', u'type', u'userId', u'userName', u'write', u'writeRight']], [u'data', u'message', u'status', u'success']]
        kernel = {"discussType":"undefined","masterId":self.report_id[0],
                  "discussedId":self.discuss_id[-1],"discussedUserId":self.my_id,
                  "discussedUserName":self.my_name,"content":"Robot Reply","isFile":"N","publishTime":get_current_time(),"relay":0,
                  "attList":[],"userIdNames":""}
        self.determine_error(POST(self.discuss_url, kernel), "Reply Report", template, self.discuss_url)
        self.times += 1


    def determine_error(self,data, name, template=[], url=""):
        error = False
        Failure_reason = ""
        try:
            result = json.loads(data)['success']
        except:
            result = "No Result"
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        template = sort_my_array(template)
        to_compare = sort_my_array(title_exporter(json.loads(data)))
        missing_list = comparator(to_compare, template)
        if (data == None):
            Failure_reason += "/No Data Coming Out"
            error = True
        if (not result):
            Failure_reason += "/Not pass the system test"
            error = True
        if (missing_list != []):
            Failure_reason += "/Kernel Comparison Failed, Missing: " + str(missing_list)
            error = True
        if error:
            print Failure_reason
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        try:
            my_message = json.loads(data)['message']
        except:
            my_message = "No Message"
        kernel = {"Name" : name, "URL" : url, "Success" : result, "Message": my_message, "Failure Reason": Failure_reason}
        self.result_dict[self.class_name].append(kernel)
        return data

    def show_off_all_data(self):
        print "................................................"
        print ".........Attendance Function Summary............"
        print "Function runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Failure Url:"
        for url in self.url_list:
            print url
        print "Please check the dictionary for more information"
        print "...............Thank you........................"

class amend1:
    def __init__(self):
        self.iQuickerUrl = "http://testwww.iquicker.com.cn/iquicker_web/login"
        self.personal_info = "http://testwww.iquicker.com.cn/iquicker_web/login/user"
        self.find_check_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/beateCardPlaceController/findByPage"
        self.save_location_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/beateCardPlaceController/save"
        self.delete_location_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/beateCardPlaceController/delete"
        self.set_default_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/beateCardPlaceController/setDefaultPos"
        self.punch_card_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/attendMobileCardCtrl/mobileCardSave"
        self.get_icon_url = "http://testwww.iquicker.com.cn/iquicker_web/person/"
        self.beatecard_normal_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/attendMobileCardCtrl/mobileCardSave"
        self.beatecard_out_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/attendMobileCardCtrl/mobileOutWorkCardSave"
        self.beatecard_approve_url = "http://testwww.iquicker.com.cn/iquicker_web/attendance/outWorkController/pendBtSave"
        self.apply_expense_url = "http://testwww.iquicker.com.cn/iquicker_web/reimburse/bill"
        self.get_my_sub_url = "http://testwww.iquicker.com.cn/iquicker_web/wreport/work_report_shared_configs"
        self.set_head_img_url = "http://testwww.iquicker.com.cn/iquicker_web/person/"
        self.logout_url = "http://testwww.iquicker.com.cn/iquicker_web/logout"
        self.get_personal_url = "http://testwww.iquicker.com.cn/iquicker_web/persons"
        self.get_notice_url = "http://testwww.iquicker.com.cn/iquicker_web/notice/datas/page"
        self.get_work_url = "http://testwww.iquicker.com.cn/iquicker_web/flow/allTypes"
        self.wait_my_app_url = "http://testwww.iquicker.com.cn/iquicker_web/task/datas/page"
        self.my_apply_url = "http://testwww.iquicker.com.cn/iquicker_web/apply/datas/page"
        self.related_topic_url = "http://testwww.iquicker.com.cn/iquicker_web/blogall/data/topicses"
        self.my_agenda_url = "http://testwww.iquicker.com.cn/iquicker_web/schedul/agenda"
        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0
        self.my_id = ""
        self.my_name = ""
        self.my_data ={}
        self.beatecard_info = {}
        self.function_name = {"login" : 1, "Get Personal info" : 2, "Get my icon" : 3, "Get Agenda" : 4, "Find all location" : 5}
        self.class_name = str(self.__class__).split('__main__.')[1]
        self.result_dict = {self.class_name : []}

    def login(self):
        print "in Login System..."
        template = [[u'status', u'message', u'data', u'success'], [[u'orgs', u'initialised']]]
        kernel = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
        self.determine_error(POST(self.iQuickerUrl, kernel), "login",template, self.iQuickerUrl)
        self.times += 1

    def get_personal_info(self):
        print "Getting Personal Info..."
        template = [[[[u'deptManager', u'flag', u'flag2', u'id', u'name', u'org', u'parDept', u'prefixId', u'root', u'shortname', u'sn', u'status', u'subDept', u'usable', u'zfield1', u'zfield10', u'zfield2', u'zfield3', u'zfield4', u'zfield5', u'zfield6', u'zfield7', u'zfield8', u'zfield9']], [u'address', u'bankCard', u'birthday', u'createTime', u'department', u'email', u'enname', u'fax', u'hometown', u'id', u'idcard', u'img', u'innerEmail', u'innerEmailContact', u'isTrialAccount', u'itcode', u'joinTime', u'joindate', u'mobile', u'name', u'org', u'pinyin', u'pinyinPrefix', u'position', u'prefixId', u'qualifications', u'sex', u'shortname', u'signature', u'sn', u'status', u'statusReason', u'telephone', u'type']], [u'data', u'message', u'orgCode', u'orgInnerEmailStatus', u'orgLogoColour', u'orgLogoWhite', u'orgName', u'status', u'success', u'theme']]
        my_data = GET(self.personal_info)
        self.determine_error(my_data, "Get Personal info", template, self.personal_info)
        self.my_id = json.loads(my_data)['data']['id']
        self.my_name = json.loads(my_data)['data']['name']
        self.my_data = json.loads(my_data)['data']
        self.times += 1

    def get_my_icon(self):
        print "Getting my icon..."
        url = self.get_icon_url + self.my_id + "/image-base64"
        self.determine_error(json.dumps(GET(url)), "Get my icon", ["Not applicable"],url)
        self.times += 1

    def find_all_check_location(self):
        print "Finding all Check locations..."
        template = [[[[u'beatPlace', u'beatPlaceRemark', u'buffer', u'createDate', u'creatorId', u'firstBeatCardTime', u'id', u'isDefault', u'lonLat', u'org', u'sortCode', u'workStartTime', u'workdEndTime']], [u'content', u'first', u'last', u'number', u'numberOfElements', u'size', u'sort', u'totalElements', u'totalPages']], [u'data', u'message', u'status', u'success']]
        id_list = GET(self.find_check_url)
        self.determine_error(id_list, "Find all location", template, self.find_check_url)
        id_list = json.loads(id_list)['data']['content']
        for key in id_list:
            self.beatecard_info[key['id']] = key['isDefault']
        self.times += 1

    def set_new_location(self):
        print "Setting new location..."
        kernel = {"beatPlace":"Statue of Liberty","beatPlaceRemark":"No 1 Morningheight Manhattan NY","isDefault":"2",
                  "lonLat":{"lng":116.459228,"lat":39.942651},"buffer":"500"}
        POST(self.save_location_url, kernel)
        self.times += 1

    def set_default_location(self):
        print "Setting default location..."
        self.find_all_check_location()
        kernel = {'id': self.beatecard_info.keys()[0]}
        POST(self.set_default_url, kernel)
        self.times += 1

    def delete_location(self):
        print "Deleting Location now..."
        self.find_all_check_location()
        if len(self.beatecard_info.keys()) <= 1:
            input_id = ""
        else:
            # Method to avoid deleting default condition
            card_id = self.beatecard_info.keys()[0]
            if self.beatecard_info[card_id] == 1:
                input_id  = self.beatecard_info.keys()[1]
            else:
                input_id = card_id
        kernel = {'id' : input_id}
        GET(self.delete_location_url, kernel)
        self.times += 1

    def beatecard_normal(self):
        print "Try to Punch card..."
        kernel = {"lonLat":{"lng":116.459228,"lat":39.942651}, "beatType" : 1}
        POST(self.punch_card_url, kernel)
        self.times += 1

    def beatecard_out(self):
        print "Try to Punch Card Out..."
        kernel = {"beatPlace": "tiananmen", "imgList" : None, "outworkId" :"ff80808155bdc8260155bde21f41001f","lonLat": {"lng":116.459228,"lat":39.942651}}
        POST(self.beatecard_out_url, kernel)
        self.times += 1

    def beatecard_approve(self):
        print "Approve Punch Card out..."
        kernel = {"outWorks" : [{"aprovalCommont" : "Agree", "aprovalResult" : "1", "id" : "ff808081560753ce01560b876e560072"}]}
        POST(self.beatecard_approve_url, kernel)
        self.times += 1

    def expense_apply(self):
        print "Apply for Expense on PC..."
        kernel = {"amount" : 12, "deptId" : "ff808081557080a6015575e3d9310333", "billStatus" : "save"}
        print POST(self.apply_expense_url, kernel)
        self.times += 1

    def my_default_subscriber(self):
        print "Getting my default subscriber on W report..."
        GET(self.get_my_sub_url)
        self.times += 1

    def update_my_info(self):
        print "Updating my personal information..."
        kernel = {"map":{"name":"X","position":"X","department":"X","mobile":"X","telephone":"X","email":"X","signature":"X","birthday":"X","sex":"X","img":"X"},"object":{"name":self.my_name,"position": self.my_data['position'],"department":{"id":self.my_data['department']['id']},"mobile":self.my_data['mobile'],"telephone":self.my_data['telephone'],"email":"11883823@qq.com","signature": self.my_data['signature'],"birthday":"2016-02-19T00:00:00.000Z","sex":False,"img":""}}
        url = self.set_head_img_url+ self.my_id + "?&login"
        PUT(url,kernel)
        self.times += 1

    def get_person_data(self):
        print "Getting all persons info..."
        GET(self.get_personal_url)
        self.times += 1

    def logout(self):
        print "Logging out..."
        POST(self.logout_url,"")
        self.times += 1

    def get_system_notice(self):
        print "Getting system notice..."
        kernel = {"pageNo":1, "pageSize":20, "search_IS_type":"系统通知", "sortInfo":"DESC_sendTime"}
        GET(self.get_notice_url, kernel)
        self.times += 1

    def set_system_notice(self):
        print "Setting system notice..."
        kernel = {"pageNo":1, "pageSize":999, "search_IS_readState" : "0", "sortInfo":"DESC_sendTime"}
        GET(self.get_notice_url, kernel)
        self.times += 1

    def get_my_work(self):
        print "Getting my work..."
        GET(self.get_work_url)
        self.times += 1

    def wait_my_approval(self):
        print "Waiting for my approval List..."
        kernel = {"pageNo" : 1, "pageSize" : 10, "search_IS_dealState" : "0", "sortInfo" : "DESC_createTime"}
        GET(self.wait_my_app_url, kernel)
        self.times += 1

    def my_apply(self):
        print "My applications..."
        kernel = {"pageNo" : 1, "pageSize" : 10, "sortInfo" :"DESC_createTime"}
        GET(self.my_apply_url,kernel)
        self.times += 1
        
    def apply_namecard(self):
        print "Applying Namecard..."
        kernel = {"flowStatus":0,"id":"","org":"ff808081557080a6015575e3d9300330","readRight":["ff808081557080a6015575e3d9310336"],"writeRight":["ff808081557080a6015575e3d9310336"],"write":False,"applyNo":None,"attList":None,"shareUserIds":[],"createUser":"ff808081557080a6015575e3d9310336","createDate":None,"tmplName":None,"companyZh":"接口测试公司","companyEn":None,"addressZh":"西二旗","addressEn":None,"postCode":None,"website":"digitalchina.com","cardFacade":"5795c81fe4b0861bc80ae0bd","cardBack":None,"priceCommon":25,"priceUrgent":100,"printDaysCommon":10,"printDaysUrgent":3,"cardNum":100,"contactInfos":"[{\"id\":\"1\",\"fieldName\":\"姓名\",\"cname\":\"name\",\"order\":1,\"del\":False,\"hasEn\":true,\"inputType\":\"text\",\"value\":\"胡欣\",\"validate\":\"请填写姓名\"},{\"cname\":\"nameEn\",\"fieldName\":\"姓名(英文)\"},{\"id\":\"2\",\"fieldName\":\"部门\",\"cname\":\"department\",\"order\":2,\"del\":False,\"hasEn\":true,\"isSelect\":true,\"inputType\":\"text\",\"value\":\"ff808081557080a6015575e3d9310335\",\"cvalue\":\"一级部门\"},{\"cname\":\"departmentEn\",\"fieldName\":\"部门(英文)\"},{\"id\":\"3\",\"fieldName\":\"职位\",\"cname\":\"position\",\"order\":3,\"del\":False,\"hasEn\":true,\"inputType\":\"text\",\"value\":\"tester\"},{\"cname\":\"positionEn\",\"fieldName\":\"职位(英文)\"},{\"id\":\"4\",\"fieldName\":\"电话\",\"cname\":\"tel\",\"order\":4,\"del\":False,\"inputType\":\"text\",\"validate\":\"电话格式不正确,如010-71805768\"},{\"id\":\"5\",\"fieldName\":\"手机\",\"cname\":\"phone\",\"order\":5,\"del\":False,\"inputType\":\"text\",\"value\":\"15611765076\",\"validate\":\"手机格式不正确,如18801285678\"},{\"id\":\"6\",\"fieldName\":\"邮箱\",\"cname\":\"mail\",\"order\":6,\"del\":False,\"inputType\":\"text\",\"value\":\"11883823@qq.com\",\"validate\":\"邮箱格式不正确,如lily@digitalchina.com\"}]","urgentStat":"COMMON","cardBoxNum":"1","userName":"胡欣","deptId":"ff808081557080a6015575e3d9310335","deptName":"一级部门","leaderApprIds":"ff808081557080a6015575e3d9310336","leaderApprNames":"胡欣","adminApprIds":"ff808081557080a6015575e3d9310336","adminApprNames":"胡欣","tmplId":"5795c821e4b0861bc80ae0c3","cardStatus":"SUBMIT"}
        url = "http://testwww.iquicker.com.cn/iquicker_web/card/business-card-applys"
        print POST(url, kernel)
        self.times += 1

    def get_related_topic(self):
        print "Get related topics..."
        print "Posting a topic..."
        kernel1 = {"publishScope":["company"],"publishScopeName":["/u5168/u516C/u53F8"],"content":"Robot Send&nbsp;#robot#&nbsp;",
                  "isFile":"N","relay":0,"attList":[],"userIdNames":"","imgList":[]}
        url1 = "http://testwww.iquicker.com.cn/iquicker_web/microblog/data/blog"
        POST(url1, kernel1)
        kernel = {"pageNo" : 1, "pageSize" : 20, "sortInfo" : "DESC_publishTime", "topicName" :"#robot#"}
        GET(self.related_topic_url, kernel)
        self.times += 1

    def get_agenda(self):
        print "Get swipe agenda..."
        kernel = {"end" : "2017-07-13 23:59:59", "page" : 1, "pageSize" : 1000, "start" : "2015-07-13 00:00:00",
        "userIds" :self.my_id}
        self.determine_error(GET(self.my_agenda_url, kernel), "Get Agenda", [], self.my_agenda_url)
        self.times += 1


    def determine_error(self,data, name, template=[], url=""):
        error = False
        Failure_reason = ""
        try:
            result = json.loads(data)['success']
        except:
            result = "No Result"
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        template = sort_my_array(template)
        to_compare = sort_my_array(title_exporter(json.loads(data)))
        if (data == None):
            Failure_reason += "/No Data Coming Out"
            error = True
        if (not result):
            Failure_reason += "/Not pass the system test"
            error = True
        if (template != to_compare):
            Failure_reason += "/Kernel Comparison Failed"
            error = True
            print to_compare
            print template
        if error:
            print Failure_reason
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        try:
            my_message = json.loads(data)['message']
        except:
            my_message = "No Message"

        kernel = {"Name" : name, "URL" : url, "Success" : result, "Message": my_message, "Failure Reason": Failure_reason}
        self.result_dict[self.class_name].append(kernel)
        return data

    def show_off_all_data(self):
        print "................................................"
        print ".........Attendance Function Summary............"
        print "Function runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Failure Url:"
        for url in self.url_list:
            print url
        print "Please check the dictionary for more information"
        print "...............Thank you........................"


My_amend1 = amend1()
My_amend1.login()
My_amend1.get_personal_info()
My_amend1.my_default_subscriber()
My_amend1.update_my_info()
My_amend1.get_person_data()
My_amend1.set_system_notice()
My_amend1.get_system_notice()
My_amend1.get_my_work()
My_amend1.wait_my_approval()
My_amend1.my_apply()
My_amend1.get_related_topic()
My_amend1.get_agenda()
#My_amend1.apply_namecard()
My_amend1.logout()
#My_amend1.expense_apply()
My_amend1.login()
My_amend1.get_my_icon()
My_amend1.set_new_location()
My_amend1.set_default_location()
My_amend1.beatecard_normal()
#My_amend1.beatecard_out()
My_amend1.beatecard_approve()
My_amend1.delete_location()


My_wreport = wreport()
My_wreport.login()
My_wreport.get_personal_info()
My_wreport.get_discuss_num()
My_wreport.get_report_discuss()
My_wreport.get_single_report()
My_wreport.get_all_wreport()
My_wreport.post_work_report()
My_wreport.comment_on_report()
My_wreport.reply_on_report()
My_wreport.delete_wreport()

My_attendance = attendance()
My_attendance.login()
My_attendance.get_personal_info()
My_attendance.get_current_permission()
My_attendance.check_new_person()
My_attendance.get_all_attendance()
My_attendance.get_personal_attendance()
My_attendance.get_personal_leave()
My_attendance.get_outwork()
My_attendance.get_att_list()
My_attendance.get_spec_att()
My_attendance.get_other_att()
My_attendance.get_all_vacation_type()
My_attendance.find_last_attendance()
My_attendance.find_by_leave_enable()
My_attendance.post_leave()
My_attendance.modify_leave()
My_attendance.delete_leave_request()
My_attendance.find_all_leave_apply()
My_attendance.select_person_vacation()
My_attendance.get_person_Vacation_apply()
My_attendance.approve_person_vacation()
My_attendance.find_outwork()
My_attendance.post_outwork()
My_attendance.get_single_outwork()
My_attendance.delete_outwork()
My_attendance.find_default_check_location()
My_attendance.find_all_check_location()
# My_whatsup.upload()


My_whatsup = Whats_up()
My_whatsup.login()
My_whatsup.post_whatsup()
My_whatsup.repost_blog()
My_whatsup.like_this_blog()
My_whatsup.reply_blog_init()
My_whatsup.reply_blog()
My_whatsup.get_all_blogs()
My_whatsup.get_single_blog()
My_whatsup.delete_blog()

Notice_settings = Notice_and_me()
Notice_settings.login()
#Notice_settings.reply_me()
Notice_settings.get_system_settings()
Notice_settings.get_all_company()
Notice_settings.send_feedback()
Notice_settings.invite_people()
Notice_settings.get_my_feedback()
Notice_settings.get_single_feedback()
Notice_settings.reply_feedback()
Notice_settings.change_password()


My_news = News()
My_news.Login_to_system()
My_news.get_news_data()
My_news.get_news_id()
My_news.get_news_type()

My_task = Tasks()
My_task.login()
My_task.get_personal_data()
My_task.get_name_list()
My_task.post_task()
My_task.commment_on_tasks()
My_task.modify_task()
My_task.Label_finished()
My_task.Label_unfinished()
My_task.delete_task()
My_task.get_disscuss_list()

My_calendar = calendar()
My_calendar.login()
My_calendar.get_personal_info()
My_calendar.get_name_list()
My_calendar.post_new_event()
My_calendar.get_schedule()
My_calendar.get_single_schedule()
My_calendar.modify_event()
My_calendar.delete_event()

My_Work_Comm = Work_comm()
My_Work_Comm.login()
My_Work_Comm.get_name_list()
My_Work_Comm.get_personal_info()
My_Work_Comm.get_all_work_comm()
My_Work_Comm.get_single_WComm_info()
My_Work_Comm.get_process_record()
My_Work_Comm.create_new_work()
My_Work_Comm.agree_on_wcomm()
My_Work_Comm.reject_on_wcomm()
My_Work_Comm.delete_work_contact()

My_Work_News = Compnews()
My_Work_News.login()
My_Work_News.get_personal_info()
My_Work_News.get_news_type()
My_Work_News.get_news_data()
My_Work_News.get_news_threemonth()
My_Work_News.get_news_discuss()
My_Work_News.get_single_news()
My_Work_News.increase_view_number()
My_Work_News.discuss_on_news()
My_Work_News.delete_discuss()

My_ad_book = address_book()
My_ad_book.login()
My_ad_book.get_name_list()
My_ad_book.get_label()
My_ad_book.get_personal_info()
My_ad_book.get_my_fans()
My_ad_book.get_fans_me()
My_ad_book.get_whats_up()
My_ad_book.label_fans()
My_ad_book.post_new_fans()
My_ad_book.unlabel_fans()

My_wreport.show_off_all_data()
My_attendance.show_off_all_data()
My_news.show_off_all_data()
My_task.show_off_all_data()
My_calendar.show_off_all_data()
My_Work_Comm.show_off_all_data()
My_Work_News.show_off_all_data()
My_ad_book.show_off_all_data()
Notice_settings.show_off_all_data()
My_whatsup.show_off_all_data()

def store_to_csv():
    data_set = []
    data_set.append(My_attendance.result_dict)
    data_set.append(My_calendar.result_dict)
    data_set.append(My_news.result_dict)
    data_set.append(My_task.result_dict)
    data_set.append(My_Work_Comm.result_dict)
    data_set.append(My_Work_News.result_dict)
    data_set.append(My_ad_book.result_dict)
    data_set.append(Notice_settings.result_dict)
    data_set.append(My_whatsup.result_dict)
    data_set.append(My_wreport.result_dict)
    my_time = time.strftime("%Y_%m_%d %H_%M_%S")
    file_name = 'Terminal_test '+my_time+'.csv'
    csvfile = file(file_name, 'wb')
    csvfile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvfile)
    writer.writerow(['Section','Name', 'URL', 'Success', 'Message', 'Failure Reason'])
    kernel = ["", "", "", "", "", ""]
    for my_data in data_set:
        section_name = my_data.keys()[0]
        kernel[0] = section_name
        for line_data in my_data[section_name]:
            kernel[1] = line_data['Name']
            kernel[2] = line_data['URL']
            kernel[3] = line_data['Success']
            message_data = line_data['Message']
            if isinstance(message_data, int):
                message_data = str(message_data)
            else:
                message_data = message_data.encode("utf8")
            kernel[4] = message_data
            kernel[5] = line_data['Failure Reason']
            writer.writerow(kernel)
    # writer.writerow()
    csvfile.close()

store_to_csv()

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

'''
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

#Get Unfinished Task List
Tasks_url = "http://testwww.iquicker.com.cn/iquicker_web/task/tasks"
Data_tasks = {"isOver" : False, "page" : 1, "pageSize" : 20, "sortType" : 1, "type" : 0}
Task_info = GET(Tasks_url,Data_tasks)
Task_id = []
Task_info = json.loads(Task_info)
Task_info = Task_info['data']['content']
for i in range(len(Task_info)):
    Task_id.append(Task_info[i]['id'])

#Get Finished Task List
Tasks_url = "http://testwww.iquicker.com.cn/iquicker_web/task/tasks"
Data_tasks = {"isOver" : True, "page" : 1, "pageSize" : 20, "sortType" : 1, "type" : 0}
Task_info = GET(Tasks_url,Data_tasks)
Finished_Task_id = []
Task_info = json.loads(Task_info)
Task_info = Task_info['data']['content']
for i in range(len(Task_info)):
    Finished_Task_id.append(Task_info[i]['id'])

#Start Posting Tasks!
Post_task_url = "http://testwww.iquicker.com.cn/iquicker_web/task/tasks"
Post_kernel = {"subject" : "RobotSend", "principals" : [{"id": id_book[0] , "name": name_book[0]}], "participants":[{"id": id_book[0] , "name": name_book[0]}], "endDate" : "2017-06-24T16:00:00.000Z", "priority" : 3, "detail" : "This is a Test Message" , "shared" : False , "publishScope" : ["company"], "publishScopeName" : ["/u5168/u516C/u53F8"]}
POST(Post_task_url,Post_kernel)


#Start Modifying Tasks!
Post_task_url = "http://testwww.iquicker.com.cn/iquicker_web/task/tasks"
Post_kernel = {"id": Task_id[-1], "subject" : "RobotSendModify", "principals" : [{"id": id_book[0] , "name": name_book[0]}], "participants":[{"id": id_book[0] , "name": name_book[0]}], "endDate" : "2017-06-24T16:00:00.000Z", "priority" : 3, "detail" : "This is a Modified Message" , "shared" : False ,"attList": None, "publishScope" : ["company"], "publishScopeName" : ["/u5168/u516C/u53F8"]}
POST(Post_task_url,Post_kernel)

#Label_finished
Label_url = "http://testwww.iquicker.com.cn/iquicker_web/task/tasks/" + str(Task_id[-1]) + "/completion"
PUT(Label_url)

#Label_Unfinished
UnLabel_url = "http://testwww.iquicker.com.cn/iquicker_web/task/tasks/" + str(Finished_Task_id[-1]) + "/incompletion"
PUT(Label_url)

#Start Delete the Task!
Delete_url = "http://testwww.iquicker.com.cn/iquicker_web/task/tasks/" + str(Task_id[-1])
#go_To_TASK
DELETE(Delete_url)
'''
'''
template = [[u'status', u'message', u'data', u'success'],
            [[u'department', u'myId', u'totalpage', u'list', u'myName'],
             [[u'storePeopleId', u'userId', u'relayTimes', u'id', u'publishScopeName', u'write', u'createDate',
               u'goodPeopleId', u'content', u'publishScope', u'type', u'discussList', u'companyName', u'deleted',
               u'readRight', u'createUser', u'org', u'userName', u'shareUserIds', u'applyNumber', u'publishTime',
               u'writeRight', u'attList'],
              [[u'source', u'master', u'discuss'],
               [[u'storePeopleId', u'userId', u'relayTimes', u'id', u'publishScopeName', u'write', u'createDate',
                 u'goodPeopleId', u'content', u'publishScope', u'type', u'discussList', u'companyName', u'deleted',
                 u'readRight', u'createUser', u'org', u'userName', u'shareUserIds', u'applyNumber', u'publishTime',
                 u'writeRight', u'attList'],
                [[u'source', u'master', u'relay'],
                 [[u'storePeopleId', u'userId', u'relayTimes', u'id', u'publishScopeName', u'write',
                   u'createDate', u'goodPeopleId', u'content', u'publishScope', u'type', u'discussList',
                   u'companyName', u'deleted', u'readRight', u'createUser', u'org', u'userName', u'shareUserIds',
                   u'applyNumber', u'publishTime', u'writeRight', u'attList'],
                  [[u'userIdNames', u'userId', u'id', u'publishScopeName', u'write', u'createDate', u'content',
                    u'masterId', u'publishScope', u'discussList', u'relay', u'readRight', u'createUser', u'org',
                    u'userName', u'shareUserIds', u'applyNumber', u'publishTime', u'writeRight', u'isFile',
                    u'imgList', u'attList']]],
                 [[u'userName', u'write', u'userIdNames', u'relay', u'shareUserIds', u'userId', u'publishTime',
                   u'content', u'readRight', u'writeRight', u'imgList', u'publishScopeName', u'publishScope',
                   u'org', u'isFile', u'id', u'attList', u'discussList']],
                 [[u'userName', u'write', u'userIdNames', u'relay', u'shareUserIds', u'userId', u'publishTime',
                   u'content', u'masterId', u'readRight', u'writeRight', u'publishScopeName', u'publishScope',
                   u'org', u'isFile', u'id', u'attList', u'discussList']]],
                [[u'discussedUserId', u'userIdNames', u'userId', u'discussedUserName', u'discussedId', u'write',
                  u'createDate', u'id', u'content', u'masterId', u'publishScope', u'relay', u'readRight',
                  u'createUser', u'org', u'userName', u'shareUserIds', u'applyNumber', u'publishTime', u'writeRight',
                  u'isFile', u'attList']]],
               [[u'userName', u'write', u'discussList', u'relay', u'shareUserIds', u'userId', u'publishTime',
                 u'content', u'masterId', u'readRight', u'writeRight', u'publishScopeName', u'publishScope',
                 u'org', u'isFile', u'id', u'attList', u'userIdNames']],
               [[u'userName', u'content', u'discussedUserId', u'userIdNames', u'relay', u'isFile', u'shareUserIds',
                 u'userId', u'publishTime', u'discussedId', u'write', u'masterId', u'readRight', u'writeRight', u'org',
                 u'discussedUserName', u'id', u'attList']]]]]]
'''
'''
template1 = [[[[[u'applyNo', u'attList', u'companyName', u'createDate', u'createUser', u'id', u'org', u'readRight', u'shareUserIds', u'typeName', u'write', u'writeRight']], [[u'selection', u'src', u'thumbnail']], [u'applyNo', u'attList', u'browses', u'circlePicPath', u'companyName', u'content', u'contentTitle', u'createDate', u'createUser', u'department', u'discusses', u'id', u'isCirclePic', u'isFile', u'isUp', u'isUpTime', u'mobilePicPath', u'org', u'picObj', u'publishScope', u'publishTime', u'readRight', u'shareUserIds', u'stores', u'tags', u'title', u'type', u'userId', u'userName', u'write', u'writeRight']], [u'list', u'totalpage']], [u'data', u'message', u'status', u'success']]
template2 = [[[[[u'attList', u'companyName', u'createDate', u'createUser', u'id', u'org', u'readRight', u'shareUserIds', u'typeName', u'write', u'writeRight']], [[u'selection', u'src', u'thumbnail']], [u'attList', u'browses', u'circlePicPath', u'companyName', u'content', u'contentTitle', u'createDate', u'createUser', u'department', u'discusses', u'id', u'isCirclePic', u'isFile', u'isUp', u'isUpTime', u'mobilePicPath', u'org', u'picObj', u'publishScope', u'publishTime', u'readRight', u'shareUserIds', u'stores', u'tags', u'title', u'type', u'userId', u'userName', u'write', u'writeRight']], [u'list', u'totalpage']], [u'data', u'message', u'status', u'success']]
comparator(template2, template1)
'''

'''
# Strict Version: Apllies to the strict comparison between data
def determine_error(self,data, name, template=[], url=""):
        error = False
        Failure_reason = ""
        try:
            result = json.loads(data)['success']
        except:
            result = "No Result"
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        template = sort_my_array(template)
        to_compare = sort_my_array(title_exporter(json.loads(data)))
        if (data == None):
            Failure_reason += "/No Data Coming Out"
            error = True
        if (not result):
            Failure_reason += "/Not pass the system test"
            error = True
        if (template != to_compare):
            Failure_reason += "/Kernel Comparison Failed"
            error = True
            print to_compare
            print template
        if error:
            print Failure_reason
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        kernel = {"Name" : name, "URL" : url, "Success" : result, "Failure Reason": Failure_reason}
        self.result_dict[self.class_name].append(kernel)
        return data
'''

# print remove_duplications(name_extractor(sort_my_array(template)))
#for item in cj:
#    print 'Name = '+item.name
#    print 'Value = '+item.value

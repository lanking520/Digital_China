import cookielib
import urllib2
import urllib
import json
import time

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
    return time.strftime("%F %T" , time.localtime() )

def get_raw_time():
    return time.time()

def title_exporter(dictionary):
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

# Major Functions
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
    # print source_code
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
        #print "Passed Basic Access!"
        return resp.read()
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
        self.url_manager = []
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
        result = True
        try:
            result = json.loads(data)['success']
        except:
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        if (data == None or not result or template != title_exporter(json.loads(data))):
            print title_exporter(json.loads(data))
            print template
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
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
        result = True
        try:
            result = json.loads(data)['success']
        except:
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        if (data == None or not result or template != title_exporter(json.loads(data))):
            print title_exporter(json.loads(data))
            print template
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
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
        self.post_calendar = "http://testwww.iquicker.com.cn/iquicker_web/schedul/"
        self.function_name = {"login" : 1, "Get Name List" : 2, "Get Schedule" : 3, "Post Event" : 4,
                              "Modify Event" : 5, "Delete Event" : 6}
        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0
        self.id_book = []
        self.name_book = []
        self.schedule_book = []
        self.schedule_job_id = []
        self.schedule_create_date = []

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

    def get_schedule(self):
        print "Getting Schedule..."
        self.schedule_book = []
        self.schedule_job_id = []
        self.schedule_create_date = []
        kernel = { "end" : "2017-06-27 23:59:59", "page" : 1, "pageSize" : 1000, "start" : "2015-06-27 00:00:00",
        "userIds" :self.id_book[0]}
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

    def post_new_event(self):
        print "Posting new event on Calendar..."
        kernel = {"title":"Robot_Create_new","viewType":True,"type":"1","place":"Mountain View","allDay":False,
                  "start":"2016-06-27 00:00:00","end":"2016-06-27 01:00:00",
                  "meeters":[{"id":self.id_book[-1],"name":self.name_book[-1]}],"content":"Robot send test message",
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
                  "start":"2016-06-27 00:00:00","end":"2016-06-27 01:00:00",
                  "meeters":[{"id":self.id_book[-1],"name":self.name_book[-1]}],"content":"Robot send test message1",
                  "repeat":False,"endRemindDate": None,"remind":"5","share":False,"repeatType":0,"attList": None,"workDay":False,
                  "publishScope":["company"],"publishScopeName":["/u5168/u516C/u53F8"], "schedulerJobId":self.schedule_job_id[-1],
                  "createDate":self.schedule_create_date[-1],"createUser":self.id_book[0],"createrName":self.name_book[0],"org":"ff808081557080a6015575e3d9300330"}
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
        result = True
        try:
            result = json.loads(data)['success']
        except:
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        if (data == None or not result or template != title_exporter(json.loads(data))):
            print title_exporter(json.loads(data))
            print template
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
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
                              "Reject" : 9}
        self.my_id = ""
        self.error_count = []
        self.url_list = []
        self.port_type_warning = []
        self.times = 0
        self.id_book = []
        self.name_book = []
        self.wcomm_id = []

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
                                "useId":self.id_book[0],"name": self.name_book[0]},
                               {"id":"apprUser_2","label":u"/u4E8C/u7EA7/u5BA1/u6279",
                                "placeholder":"/u8BF7/u9009/u62E9/u5BA1/u6279/u4EBA(/u53EF/u9009/u591A/u4EBA/u5E76/u7B7E)","level":2,
                                "useId":self.id_book[0],"name": self.name_book[0]}],"subject":"Robot Send","detail":"LOL",
                  "billStatus":"SUBMIT"}
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
        print self.wcomm_id[0]
        kernel = {"id":self.wcomm_id[0],"opinion":"Robot Agree",
                  "shareUsers":[{"shareUserId":self.id_book[0],"shareUserName":self.name_book[0]}]}
        template = [[u'status', u'message', u'success']]
        self.determine_error(PUT(url, kernel), "Agree", template, url)
        self.times +=1

    def reject_on_wcomm(self):
        print "Rejection Established on the WC..."
        self.get_all_work_comm()
        url = self.all_wcomm + self.wcomm_id[0] + "/rejection"
        print self.wcomm_id[0]
        kernel = {"id":self.wcomm_id[0],"opinion":"Robot Disagree",
                  "shareUsers":[{"shareUserId":self.id_book[0],"shareUserName":self.name_book[0]}]}
        template = [[u'status', u'message', u'success']]
        self.determine_error(PUT(url, kernel), "Reject", template, url)
        self.times +=1

    def determine_error(self,data, name, template=[], url=""):
        result = True
        try:
            result = json.loads(data)['success']
        except:
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        if (data == None or not result or template != title_exporter(json.loads(data))):
            print title_exporter(json.loads(data))
            print template
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
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
        result = True
        try:
            result = json.loads(data)['success']
        except:
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        if (data == None or not result or template != title_exporter(json.loads(data))):
            print title_exporter(json.loads(data))
            print template
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
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


'''
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
My_calendar.get_name_list()
My_calendar.get_schedule()
My_calendar.post_new_event()
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

My_news.show_off_all_data()
My_task.show_off_all_data()
My_calendar.show_off_all_data()
My_Work_Comm.show_off_all_data()
My_Work_News.show_off_all_data()
'''
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

#for item in cj:
#    print 'Name = '+item.name
#    print 'Value = '+item.value

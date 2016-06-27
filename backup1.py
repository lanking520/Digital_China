import cookielib
import urllib2
import urllib
import json
import time

#Default Settings for a system to keep cookies, please add it before testing
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
# Let the single cookie system override the current openurl
#Cookies Info
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

#Helper Functions
def get_current_time():
    return time.strftime("%F %T" , time.localtime() )

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

#Major Functions
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
'''
My_news = News()
My_news.Login_to_system()
My_news.get_news_data()
My_news.get_news_id()
My_news.get_news_type()
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

        self.basic_struct = ['status', 'message', 'data', 'success']

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
                    [[u'sort', u'last', u'size', u'number', u'content', u'totalPages', u'first',
                      u'totalElements', u'numberOfElements'],
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
                    [[u'sort', u'last', u'size', u'number', u'content', u'totalPages', u'first',
                      u'totalElements', u'numberOfElements'],
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
            self.error_count.append(self.function_name[name])
            self.url_list.append(url)
        return data

    def show_off_all_data(self):
        print "................................................"
        print "Function runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Failure Url:"
        for url in self.url_list:
            print url
        print "Please check the dictionary for more information"

My_task = Tasks()
My_task.login() == None
My_task.get_personal_data()
My_task.get_name_list()
My_task.post_task()
My_task.commment_on_tasks()
My_task.modify_task()
My_task.Label_finished()
My_task.Label_unfinished()
My_task.delete_task()
My_task.get_disscuss_list()
My_task.show_off_all_data()

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

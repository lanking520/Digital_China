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
        print "Passed Basic Access!"
        return resp.read()
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
        else:
            print "OK"
        return None

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
        self.port_type_warning = []
        self.times = 0
        self.id_book = []
        self.name_book = []
        self.Task_id = []
        self.Finished_Task_id = []
        self.my_dict = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}

    def login(self):
        print "in Login System..."
        self.determine_error(POST(self.iQuickerUrl, self.my_dict), "login")
        self.times += 1

    def get_personal_data(self):
        print "Fetching personal info..."
        self.determine_error(GET(self.personal_info), "Get Personal Data")
        self.times += 1

    def get_name_list(self):
        print "Fetching Namelist..."
        user_data = GET(self.get_user_data)
        self.determine_error(user_data, "Get Name List")
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
        self.determine_error(Task_info, "Get Unfinished")
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
        self.determine_error(Task_info, "Get Finished")
        Task_info = json.loads(Task_info)
        Task_info = Task_info['data']['content']
        for i in range(len(Task_info)):
            self.Finished_Task_id.append(Task_info[i]['id'])
        self.times += 1

    def Label_finished(self):
        print "Label Unfinished Task->Finished"
        self.get_unfinished()
        Label_url = self.task_info + str(self.Task_id[-1]) + "/completion"
        self.determine_error(PUT(Label_url), "Label Finished")
        self.times += 1

    def Label_unfinished(self):
        print "Label Finished Task->Unfinished"
        self.get_finished()
        #print self.Finished_Task_id
        Label_url = self.task_info + str(self.Finished_Task_id[-1]) + "/incompletion"
        self.determine_error(PUT(Label_url), "Label UnFinished")
        self.times += 1

    def post_task(self):
        print "Posting new task now..."
        Post_kernel = {"subject" : "RobotSend", "principals" : [{"id": self.id_book[0] , "name": self.name_book[0]}], "participants":[{"id": self.id_book[0] , "name": self.name_book[0]}], "endDate" : "2017-06-24T16:00:00.000Z", "priority" : 3, "detail" : "This is a Test Message" , "shared" : False , "publishScope" : ["company"], "publishScopeName" : ["/u5168/u516C/u53F8"]}
        self.determine_error(POST(self.task_info,Post_kernel), "Post Tasks")
        self.times += 1

    def modify_task(self):
        print "Modifying new task now..."
        self.get_unfinished()
        Post_kernel = {"id": self.Task_id[-1], "subject" : "RobotSendModify", "principals" : [{"id": self.id_book[0] , "name": self.name_book[0]}], "participants":[{"id": self.id_book[0] , "name": self.name_book[0]}], "endDate" : "2017-06-24T16:00:00.000Z", "priority" : 3, "detail" : "This is a Modified Message" , "shared" : False ,"attList": None, "publishScope" : ["company"], "publishScopeName" : ["/u5168/u516C/u53F8"]}
        self.determine_error(POST(self.task_info,Post_kernel), "Modify Task")
        self.times += 1

    def delete_task(self):
        print "deleting task now..."
        self.get_unfinished()
        Delete_url = self.task_info + str(self.Task_id[-1])
        self.determine_error(DELETE(Delete_url), "Delete Task")
        self.times += 1

    def commment_on_tasks(self):
        print "Posting discuss on the Tasks..."
        self.get_unfinished()
        kernel = {"discussType":"task","masterId":self.Task_id[-1],"discussedId":"","discussedUserId":"","discussedUserName":"","content":"Looks&nbsp;nice!","isFile":"N","publishTime":get_current_time(),"relay":0,"attList":[],"userIdNames":""}
        self.determine_error(POST(self.discuss_on_tasks, kernel), "Comment on Task")
        self.times += 1


    def get_disscuss_list(self):
        print "Get all Discuss data for a task..."
        self.get_unfinished()
        url = self.discuss_list + self.Task_id[-1]
        self.determine_error(GET(url), "Discuss List")
        self.times += 1

    def determine_error(self,data, name):
        result = True
        try:
            result = json.loads(data)['success']
        except:
            print "There is no success options"
            self.port_type_warning.append(self.function_name[name])
        if (data == None or not result):
            self.error_count.append(self.function_name[name])

    def show_off_all_data(self):
        print "................................................"
        print "System runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Please check the dictionary for more information"

counter  =  0
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

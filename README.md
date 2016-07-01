# Digital China 2016
Software Testing Intern (Team iQuicker)

Company Structure: HYBRID

Test Team Lead: Xin Hu

Team Lead: Yuyang Nie

Workflow: Customer-->Supplier-->UI Designer-->Programmer(Front)/Programmer(Back)-->Testers-->Programmer-->Tester....-->Supplier-->Customer

No income, Refreshment Inclusive

Flexible workloads: 9:00-18:00

Period: 21st of June to the 22th of August

## Project Description
iQuicker is a innovative Internet Service to enable modern Company and Goverment Department to work cooperately in a single network. The services includes Financial and Administrative support to most of the users. Focused on the File Storage and Data Transfer, the abunant Extension Apps create the endless possiblities in the future development. This Apps is aimed to be sale with authorization to Num_of_Empolyees as well as the inclusive development plan. It is belived that, the company needs the efficient management system and the cloud services to achieve the overall performance increment supporting from individuals' performance increment

## Job descriptions
-  Testing the Supporting of Multiple platform
-  Internet test on the applications in the Cloud
-  Hand_on testing (Black box) the Beta Apps
-  Attention on Data import, file correction, format....
-  Assist on Auto Terminal Programs' Development [6.21]

## 2016-06-21 Bot Terminal Test
Previous Job: Resize matter not in the full zoom mode

Keep on Going: Test the program to see if any problem throw out

Target:
- Create Java application to test the terminal if available
To get it worked:

1. JUnit should be known

2. Platform language (json?)

[Update]
- SoapUI needed
- Requirement of Soap: Java Script?
Problem Found:
1. The iQuick does not support resizing
2. System Notice Error
3. Public Uploading error, not supporting public fileshare
4. [Functional Dev]The search result will not set to default after delete the previous searching criteria
5. [Functional Dev]User cannot see his/her personal message
6. Personal Note: Uploading file error (Undefined Undefined B)
7. [Functional Dev] Import ics (General Format) of calendar event
8. apply for reimbursement Error, cannot update data

## 2016-06-22 More than a Terminal Test
Things has changed. The test is focused more on the humanoid test -> Auto test on with the proxy server. The requirement has also been changed to test the functionalities. Will update this afternoon

To get the Source Code, this line will do
```python
import urllib2
def grabSC(url):
  resp = urllib2.urlopen(url)
  source_code = resp.read()
  #print "Source Code:", Source_code
  return source_code
  #return_type: String
```
To get Cookies (Help you find what is returned)
```python
import cookielib
import urllib2
def getCookies(url):
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  urllib2.install_opener(opener)
  resp = urllib2.urlopen(url)    
  for index, cookie in enumerate(cj)
      print '[',index, ']',cookie
```
Today's Summary

1. Cookies and Source Code are good to have now

2. POST Function are still under developing

3. How to get the next page's data if passed?

4. How to make the system flexible to be modified to be used everytime?
```
https://www.iquicker.com.cn/iquicker_web/
```
How to apply the Datatype:json to my posting dataset????
```
<urllib2.Request instance at 0x10251f5f0>
{
  "success" : false,
  "message" : "运行出错",
  "status" : 500
}
geturl= https://www.iquicker.com.cn/iquicker_web/login
```
## 2016-06-23 Go to a step further
After solving the major problem of data type into json:
```python
my_dict={"username":"18146618480","password":"MTIzNDU2Nzg=","rememberMe":True}
encodedjson = json.dumps(my_dict)
req.add_header('Content-Type', "application/json")
```
The problem is solved!! LoL... Let's go a step further, here comes the problem (first terminal test completed):
```
{"success":false,"message":"请选择您所要登录的公司","status":2001,"data":{"initialised":true,"orgs":[{"id":"ff808081520bd453015214e146ea0016","name":"神州云科","displayName":"","englishName":"","domain":"fohp","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1454256000000},{"id":"ff8080815379364f0153892a6cce00ec","name":"科科","displayName":null,"englishName":null,"domain":"nglj","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1454256000000},{"id":"ff8080815379364f0153892e007700f1","name":"peng","displayName":null,"englishName":null,"domain":"rygt","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1454256000000},{"id":"0000000052108757015239e6dc52002e","name":"dctest","displayName":null,"englishName":null,"domain":"jftb","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1454256000000},{"id":"ff80808153c68bf50153d12ae5d6021c","name":"张三疯","displayName":null,"englishName":null,"domain":"b9r9","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1459503163000},{"id":"ff8080815267c11901527678c1cc020f","name":"我是他","displayName":"我是他","englishName":"haha","domain":"y9is","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1454256000000},{"id":"ff80808153c68bf50154c7daf1720dbf","name":"aaabbb","displayName":null,"englishName":null,"domain":"qil5","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1463641895000},{"id":"ff808081542c093f0154e66371a10365","name":"公司","displayName":null,"englishName":null,"domain":"gd5l","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1464154157000},{"id":"ff808081542c093f0154ff5490a20b16","name":"aaaa","displayName":null,"englishName":null,"domain":"r1u9","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":false,"createTime":1464572613000},{"id":"ff80808155170cbf0155191afff60031","name":"NewWork","displayName":null,"englishName":null,"domain":"5ao9","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1465005048000},{"id":"ff808081551729dd015519001d010011","name":"生产","displayName":"生产1","englishName":null,"domain":"gfe8","userStatus":0,"theme":"green","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1465003286000},{"id":"ff80808155170cbf0155194be8ec0052","name":"周六测试","displayName":null,"englishName":null,"domain":"iug4","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1465008253000},{"id":"ff80808155170cbf015519b26ace0103","name":"粽子","displayName":"小粽子","englishName":null,"domain":"pl8o","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1465014971000},{"id":"ff80808153c68bf501546ffd3b7b09e4","name":"xugqtest134","displayName":null,"englishName":null,"domain":"8ts3","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1462167747000},{"id":"ff808081551c36aa015523b367460054","name":"小苹果","displayName":null,"englishName":null,"domain":"3mp7","userStatus":0,"theme":"blue","logoColour":null,"logoWhite":null,"initialised":true,"createTime":1465182808000}]}}
```
With one of the "Org" chosen to the dictionary passed, we received this:
```
{"success":true,"message":"登录成功","status":200,"data":{"initialised":true,"orgs":[]}}
```
[update] Victory! News part finished!
```
Passed Basic Access!
登录成功
Passed Basic Access!
success
Passed Basic Access!
success
Passed Basic Access!
success
Passed Basic Access!
success
```
## 2016-06-24 Data structure...
Today's job is to finish the Tasks section. Similiar to the previous Calendar, this section will only requires GET, POST and DELETE commands. However, the problem might occurs in adding/ modifying/ delecting subjects. Let's see what will happened then. The major obstacles LoL.

[update]

The hardest part in this section, is to fetch the id and name out from this huge list
```
{u'sort': None, u'last': True, u'size': 20, u'number': 0, u'content': [{u'endDate': 1466784000000, u'overUserId': None, u'id': u'e417d457-8bb3-4a11-922f-6bc98a83d651', u'publishScopeName': [u'\u5168\u516c\u53f8'], u'subject': u'lanking', u'write': True, u'overStatus': 0, u'createDate': 1466733319573, u'detail': u'Hello World', u'priority': 3, u'participants': [{u'id': u'ff808081557080a6015575e3d9310336', u'name': u'\u80e1\u6b23'}], u'publishScope': [u'company'], u'shared': False, u'principals': [{u'id': u'ff808081557080a6015575e3d9310336', u'name': u'\u80e1\u6b23'}], u'overDate': None, u'readRight': [u'ff808081557080a6015575e3d9310336'], u'createUser': u'ff808081557080a6015575e3d9310336', u'org': u'ff808081557080a6015575e3d9300330', u'labelObjectList': None, u'createName': u'\u80e1\u6b23', u'shareUserIds': [], u'writeRight': [u'ff808081557080a6015575e3d9310336'], u'attList': None}, {u'endDate': 1466784000000, u'overUserId': None, u'id': u'20f23d22-db2c-4973-93d7-1e22aa88ea8a', u'publishScopeName': [u'\u5168\u516c\u53f8'], u'subject': u'Lanking', u'write': True, u'overStatus': 0, u'createDate': 1466737765378, u'detail': u'LOLOLOLOLOL', u'priority': 3, u'participants': [{u'id': u'ff808081557080a6015575e3d9310336', u'name': u'\u80e1\u6b23'}], u'publishScope': [u'company'], u'shared': False, u'principals': [{u'id': u'ff808081557bd00701558027a33a021b', u'name': u'\u6768\u5229\u5e73'}], u'overDate': None, u'readRight': [u'ff808081557bd00701558027a33a021b', u'ff808081557080a6015575e3d9310336'], u'createUser': u'ff808081557080a6015575e3d9310336', u'org': u'ff808081557080a6015575e3d9300330', u'labelObjectList': None, u'createName': u'\u80e1\u6b23', u'shareUserIds': [], u'writeRight': [u'ff808081557bd00701558027a33a021b', u'ff808081557080a6015575e3d9310336'], u'attList': None}, {u'endDate': 1466870400000, u'overUserId': None, u'id': u'd1138eee-2675-4719-86f7-8a125a85168c', u'publishScopeName': [u'\u5168\u516c\u53f8'], u'subject': u'test2', u'write': True, u'overStatus': 0, u'createDate': 1466733882984, u'detail': u'Testing', u'priority': 3, u'participants': [{u'id': u'ff808081557080a6015575e3d9310336', u'name': u'\u80e1\u6b23'}], u'publishScope': [u'company'], u'shared': False, u'principals': [{u'id': u'ff808081557080a6015575e3d9310336', u'name': u'\u80e1\u6b23'}], u'overDate': None, u'readRight': [u'ff808081557080a6015575e3d9310336'], u'createUser': u'ff808081557080a6015575e3d9310336', u'org': u'ff808081557080a6015575e3d9300330', u'labelObjectList': None, u'createName': u'\u80e1\u6b23', u'shareUserIds': [], u'writeRight': [u'ff808081557080a6015575e3d9310336'], u'attList': None}, {u'endDate': 1498320000000, u'overUserId': None, u'id': u'8b803b0e-c589-4624-9b59-08d2d3044d9c', u'publishScopeName': [u'WholeComany'], u'subject': u'RobotSend', u'write': True, u'overStatus': 0, u'createDate': 1466748949422, u'detail': u'This is a Test Message', u'priority': 3, u'participants': [{u'id': u'ff808081557080a6015575e3d9310336', u'name': u'\u80e1\u6b23'}], u'publishScope': [u'company'], u'shared': False, u'principals': [{u'id': u'ff808081557080a6015575e3d9310336', u'name': u'\u80e1\u6b23'}], u'overDate': None, u'readRight': [u'ff808081557080a6015575e3d9310336'], u'createUser': u'ff808081557080a6015575e3d9310336', u'org': u'ff808081557080a6015575e3d9300330', u'labelObjectList': None, u'createName': u'\u80e1\u6b23', u'shareUserIds': [], u'writeRight': [u'ff808081557080a6015575e3d9310336'], u'attList': None}, {u'endDate': 1498320000000, u'overUserId': None, u'id': u'0a28b7d3-a4e9-4e3a-9616-dd74d0fc8a5b', u'publishScopeName': [u'/u5168/u516C/u53F8'], u'subject': u'RobotSend', u'write': True, u'overStatus': 0, u'createDate': 1466750049835, u'detail': u'This is a Test Message', u'priority': 3, u'participants': [{u'id': u'ff808081557080a6015575e3d9310336', u'name': u'\u80e1\u6b23'}], u'publishScope': [u'company'], u'shared': False, u'principals': [{u'id': u'ff808081557080a6015575e3d9310336', u'name': u'\u80e1\u6b23'}], u'overDate': None, u'readRight': [u'ff808081557080a6015575e3d9310336'], u'createUser': u'ff808081557080a6015575e3d9310336', u'org': u'ff808081557080a6015575e3d9300330', u'labelObjectList': None, u'createName': u'\u80e1\u6b23', u'shareUserIds': [], u'writeRight': [u'ff808081557080a6015575e3d9310336'], u'attList': None}, {u'endDate': 1498320000000, u'overUserId': None, u'id': u'bfe631d9-5e23-420f-b426-c45271112605', u'publishScopeName': [u'/u5168/u516C/u53F8'], u'subject': u'RobotSend', u'write': True, u'overStatus': 0, u'createDate': 1466750270053, u'detail': u'This is a Test Message', u'priority': 3, u'participants': [{u'id': u'ff808081557080a6015575e3d9310336', u'name': u'\u80e1\u6b23'}], u'publishScope': [u'company'], u'shared': False, u'principals': [{u'id': u'ff808081557080a6015575e3d9310336', u'name': u'\u80e1\u6b23'}], u'overDate': None, u'readRight': [u'ff808081557080a6015575e3d9310336'], u'createUser': u'ff808081557080a6015575e3d9310336', u'org': u'ff808081557080a6015575e3d9300330', u'labelObjectList': None, u'createName': u'\u80e1\u6b23', u'shareUserIds': [], u'writeRight': [u'ff808081557080a6015575e3d9310336'], u'attList': None}], u'totalPages': 1, u'first': True, u'totalElements': 6, u'numberOfElements': 6}
```
Hence, by the end of Friday, the Class of Tasks has been done. Hopefully, all of the automated test module could be finished by the end of next week.

## 2016-06-27 As quick as possible!

In this week, the total project should be done as quick as possible in order to reach to the next step. Feeling a liitle sad today, I am not sure what I am about to next.
```
TypeError: not a valid non-string sequence or mapping object
```
The solution for previous error is to delete the data... not good.

[update]
Error Function added, however, the test system structure need to be redesigned
```python
def show_off_all_data(self):
        print "................................................"
        print "System runs: " + str(self.times) + " times"
        print "Error Counts: " + str(len(self.error_count)) + " times"
        print "Failure in: " + str(self.error_count)
        print "Not supported port: " + str(self.port_type_warning)
        print "Please check the dictionary for more information"
```
Core Function:
```python
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
```
After several days' practice, now let's make a summary of the Terminal Test class creation procedure:

### WORKING METHODS
- Step 1: Access All information in draft
- Step 2: Pack them into Class
- Step 3: Adding Test environment
- Step 4: Adding Template and finish the program

## 2016-06-28 Maintain the entire system

Several new feature were added to the new system on the testing part. The core function could identify and export the data structure of List + Dictionary. Please Call Function to test this feature.
```python
title_exporter(dictionary)
```
Today, we will move on to some new tasks to maintain all of the features. Let's see what happened.

[update]

Now the developing speed doubles, the expected finish time is day after tomorrow. Speed it up!
Currently, the life is a little bit boring, hope there will be some difference during the next day... Do insanity Max 30 Tonight!

## 2016-06-29 WorkComm and Company News

The programming speed are increasing in the recent days. Currently, the job are more focused on the whole, how will the test being conducted? How to ensure the reduction of error?

## 2016-06-30 Address Book Failure
Some error occurred which was caused by the self.id_book[-1]. As a new person is added to the system, the previous self.id_book[0] changed to self.id_book[-1] or whatsoever.
```
................................................
...............News Function Summary............
Function runs: 4 times
Error Counts: 0 times
Failure in: []
Not supported port: []
Failure Url:
Please check the dictionary for more information
...............Thank you........................
................................................
...............Task Function Summary............
Function runs: 16 times
Error Counts: 6 times
Failure in: [4, 4, 4, 5, 4, 4]
Not supported port: [3]
Failure Url:
http://testwww.iquicker.com.cn/iquicker_web/task/tasks/
http://testwww.iquicker.com.cn/iquicker_web/task/tasks/
http://testwww.iquicker.com.cn/iquicker_web/task/tasks/
http://testwww.iquicker.com.cn/iquicker_web/task/tasks/
http://testwww.iquicker.com.cn/iquicker_web/task/tasks/
http://testwww.iquicker.com.cn/iquicker_web/task/tasks/
Please check the dictionary for more information
...............Thank you........................
................................................
...........Calendar Function Summary............
Function runs: 8 times
Error Counts: 3 times
Failure in: [3, 3, 3]
Not supported port: [2]
Failure Url:
http://testwww.iquicker.com.cn/iquicker_web/schedul/app
http://testwww.iquicker.com.cn/iquicker_web/schedul/app
http://testwww.iquicker.com.cn/iquicker_web/schedul/app
Please check the dictionary for more information
...............Thank you........................
................................................
...........Work Communication Function Summary............
Function runs: 14 times
Error Counts: 7 times
Failure in: [4, 4, 4, 4, 8, 4, 9]
Not supported port: [3]
Failure Url:
http://testwww.iquicker.com.cn/iquicker_web/wcontact/contact-applys/
http://testwww.iquicker.com.cn/iquicker_web/wcontact/contact-applys/
http://testwww.iquicker.com.cn/iquicker_web/wcontact/contact-applys/
http://testwww.iquicker.com.cn/iquicker_web/wcontact/contact-applys/
http://testwww.iquicker.com.cn/iquicker_web/wcontact/contact-applys/5774c04ae4b0aef4ea1d659c/agreement
http://testwww.iquicker.com.cn/iquicker_web/wcontact/contact-applys/
http://testwww.iquicker.com.cn/iquicker_web/wcontact/contact-applys/5774c04ae4b0aef4ea1d659c/rejection
Please check the dictionary for more information
...............Thank you........................
................................................
...........Company News Function Summary............
Function runs: 11 times
Error Counts: 0 times
Failure in: []
Not supported port: []
Failure Url:
Please check the dictionary for more information
...............Thank you........................
................................................
...........Company News Function Summary............
Function runs: 10 times
Error Counts: 0 times
Failure in: []
Not supported port: [2]
Failure Url:
Please check the dictionary for more information
...............Thank you........................
```
[update]

New requirement: create csv/xls formatted list with the following settings:

Num--Name--URL--Type--Result--Failure_reason

### CSV Stored Data Structure
```python
My_data_set = {"News" : [{"Name":"Get News", "URL" : "Http://News", "Success" : True, "Failure Reason" : "URL Fault"}]}
```
## 2016-07-01 New Month and the end of the weekdays

Been here for two weeks now. Hopefully most of the functions will be done by today. The data structure output will be solved as soon as possible.
```python
def name_extractor(my_array):
    result_array = []
    for i in range(len(my_array)):
        if isinstance(my_array[i], list):
            result_array.extend(name_extractor(my_array[i]))
        else:
            result_array.append(my_array[i])
    return result_array
```
The function written above will extract all cascaded array into a single array. The final decision on the comparison is to compare the Strings in Alphabetical order.

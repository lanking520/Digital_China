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

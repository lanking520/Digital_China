# Functionality test Project

## Project Description
This project is aimed to help the software testers to test all of the functionalities of the apps in a few seconds. The current thinking is using JAVA to simulate GET, POST and DELETE commands in the HTTP protocol. Still under thinking stages. See what happened.
## Steps to solve the problems
1. Create a simple robot that could auto login with data access
2. Manipulate it with more access to more data and pages
### Safe Decision:
On Windows:
```
chrome.exe --disable-web-security
```
On Mac:
```
open /Applications/Google\ Chrome.app/ --args --disable-web-security
```
### Danger Decision:

On Windows:
```
chrome.exe --allow-file-access-from-files
```
On Mac:
```
open /Applications/Google\ Chrome.app/ --args --allow-file-access-from-files
```
Solution to the other problem:
```
--user-data-dir
```
### Login Package (POST)
```
{"username":"18146618480","password":"MTIzNDU2Nzg=","rememberMe":true}
header format: "application/json"
```
Tried and worked functions
```python
    print cookie.name
    print cookie.value
    print cookie.expires
    print cookie.path
    print cookie.comment
    print cookie.domain
    print cookie.secure
    print cookie.version
```
Rough Working example
```python
iQuickerUrl = "https://www.iquicker.com.cn/iquicker_web/login"
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
my_dict={"username":"18146618480","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff8080815379364f0153892a6cce00ec"}
encodedjson = json.dumps(my_dict)
#postData = urllib.urlencode({"username":"18146618480","password":"MTIzNDU2Nzg=","rememberMe":True})
#org":"0000000053e5da3f0153e9286ae9000f" try it after first success
#print "postData=", encodedjson
req = urllib2.Request(iQuickerUrl, encodedjson)
#print req
req.add_header('Content-Type', "application/json")
resp = urllib2.urlopen(req)
print resp.read()
#print 'geturl=',resp.geturl()
for index, cookie in enumerate(cj):
    print '[',index, ']',cookie
scheduleappurl = "https://www.iquicker.com.cn/iquicker_web/schedul/app"
req = urllib2.Request(scheduleappurl)
req.add_header('Content-Type', "application/json")
resp = urllib2.urlopen(req)
print resp.read()
```

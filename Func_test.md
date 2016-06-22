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
{"username":"18146618482","password":"MTIzNDU2Nzg=","rememberMe":true}
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

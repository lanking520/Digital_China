# Functionality test Project

## Project Description
This project is aimed to help the software testers to test all of the functionalities of the apps in a few seconds. The current thinking is using JAVA to simulate GET, POST and DELETE commands in the HTTP protocol. Still under thinking stages. See what happened.
## Steps to solve the problems

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

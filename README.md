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

import urllib2
import cookielib
import urllib
import json
import multipart
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


def encode_multipart_formdata():
    boundary = "+++++"
    upload_data = []
    #upload_data.append("3ff8")
    upload_data.append('--' + boundary)
    upload_data.append('Content-Disposition: form-data; name="file"; filename="Mapping.jpg"')
    upload_data.append('Content-Type: image/jpeg\n')
    fr =open(r'/Users/lanking/Desktop/Mapping.png','rb')
    data = fr.read()
    fr.close()
    upload_data.append(data)
    upload_data.append('--' + boundary + '--')
    http_body='\r\n'.join(upload_data)
    #print http_body
    content_type = 'multipart/form-data; boundary=' +boundary
    return content_type, http_body

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)


iQuickerUrl1 = "http://testwww.iquicker.com.cn/iquicker_web/login"
iQuickerUrl = "http://10.1.158.225:8080/iquicker_web/login"
my_dict1 = {"username":"15611765076","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff808081557080a6015575e3d9300330"}
my_dict = {"username":"13370172510","password":"MTIzNDU2Nzg=","rememberMe":True,"org":"ff8080815208befa01520aa4617b0018"}


url = "http://10.1.158.225:8080/iquicker_web/common/file/upload/blog"
url1 = "http://testwww.iquicker.com.cn/iquicker_web/note/file/upload"
url2 = "http://testwww.iquicker.com.cn/iquicker_web/common/file/upload/blog"
upload_data = []

POST(iQuickerUrl, my_dict1)
content_type, data = encode_multipart_formdata()
# data = json.dumps(data)
'''
data = {"mappings1": open(r'/Users/lanking/Desktop/Mapping.png','rb')}
datagen= multipart.encode(data)
print datagen.get_boundary()
'''
req = urllib2.Request(url, data)

req.add_header( "Content-Type", content_type)
# req.add_header("Transfer-Encoding", "chunked")
req.add_header("User-Agent","Dalvik/1.6.0 (Linux; U; Android 4.4.2; 2014011 MIUI/V7.2.1.0.KHFCNDA)")
req.add_header("Host", "testwww.iquicker.com.cn")
req.add_header( "Accept", "*/*" )
#req.add_header("Content-Length","433357")
req.add_header( "Accept-Language", "zh-CN,zh;q=0.8" )

req.add_header( "Connection", "keep-alive" )

req.add_header( "Accept-Encoding", "gzip, deflate" )


#req.add_header("Accept", "application/json")
# req.add_header("Referer", "https://testwww.iquicker.com.cn/home/note")
# req.add_header(XMLHttp request)

print req.headers

sourcecode = ErrorOut(req)
print sourcecode

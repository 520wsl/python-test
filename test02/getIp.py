import urllib, urllib2, sys
import ssl


host = 'https://iphighproxyv2.haoservice.com'
path = '/devtoolservice/ipagency'
method = 'GET'
appcode = '46b52bc7440642f7bc744c4243b886b8'
querys = 'foreigntype=1'
bodys = {}
url = host + path + '?' + querys

request = urllib.Request(url)
request.add_header('Authorization', 'APPCODE ' + appcode)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
response = urllib.urlopen(request, context=ctx)
content = response.read()
if (content):
    print(content)
"""import httplib, urllib
params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
conn = httplib.HTTPConnection("musi-cal.mojam.com:80")
conn.request("POST", "/cgi-bin/query", params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
conn.close()"""

"""conn = httplib.HTTPConnection("192.168.1.253:80")
conn.request("GET", "/nphControlCamera?Direction=PanRight")
response = conn.getresponse()
print response.status, response.reason
data = response.read()
conn.close()"""

import urllib2
import sys

dx=dy=0
width=320
height=240
if(len(sys.argv))==3:
    dx = int(sys.argv[1])
    dy = int(sys.argv[2])

url = "http://192.168.1.253/nphControlCamera?Width={0}&Height={1}&Direction=Direct&NewPosition.x={2}&NewPosition.y={3}".format(width,height,width/2+dx,height/2+dy)


# Create an OpenerDirector with support for Basic HTTP Authentication...
auth_handler = urllib2.HTTPBasicAuthHandler()
auth_handler.add_password(realm='PTZ Cam',
                          uri='http://192.168.1.253/nphControlCamera?Direction=PanRight',
                          user='hackers',
                          passwd='ghywbp@12;f')
opener = urllib2.build_opener(auth_handler)
# ...and install it globally so it can be used with urlopen.
urllib2.install_opener(opener)
urllib2.urlopen(url)

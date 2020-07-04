import requests
import json
import datetime
data = {
    'cameraIndexCode': '516c070a92fb4a48a151c63d0323201b',
    'captureDate': '20200518'
}

# headers中添加上content-type这个参数，指定为json格式
headers = {'Content-Type': 'application/json'}
url = "http://153.35.93.113:33333/getCapturePictures"
# post的时候，将data字典形式的参数用json包转换成json格式。
response = requests.post(url=url, headers=headers, data=json.dumps(data))

# print(response.text)

js = json.loads(response.text)
# print(js['data'])
# sorted(list_file_name, key=lambda x: x.split("_")[2])
sorted = sorted(js['data'],key=lambda x: x['dateTime'],reverse=True)
print(sorted)

print(datetime.datetime.now().strftime('%Y%m%d'))

import urllib.request

response = urllib.request.urlopen('http://59.83.214.5:6027/image/pic?6dd554zac-=s8001477deb4a--3bb1a3b084d78i8b8*=sd*=3dpi*=1d*i1i9t=pe8m581a-9591fa0*e94ei38id1=')
pic = response.read()

with open('liuhui.jpg', 'wb') as f:
    f.write(pic)
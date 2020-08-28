#!/usr/bin/python3
# -*- coding:utf-8 -*-

import requests, urllib
from urllib import request, parse
from html.parser import HTMLParser

__author__ = 'shuttlelin'

url = 'http://httpbin.org/post'
file = {'file': open('req.xlsx', 'rb')}
# 1. 上传文件
r1 = requests.post(url, files=file)
print('上传文件：', r1.text)
# 2. 查看相应的headers，HTTP 头部是大小写不敏感的
print('查看相应的headers信息：', r1.headers['Content-Type'], '；', r1.headers.get('content-type'))
# 3. 设置请求的超时时间
# r2 = requests.get('http://gihub.com', timeout=0.01)
# 4. 发送请求
r3 = requests.get('https://api.github.com/events')
r4 = requests.post('https://api.github.com/events', data={'key':'vlaue'})
r5 = requests.put('http://httpbin.org/put', data={'key':'vlaue'})
r6 = requests.delete('http://httpbin.org/delete')
r7 = requests.head('http://httpbin.org/get')
r8 = requests.options('http://httpbin.org/get')
print('获取发送get请求的信息：', r3.text)
print('获取发送post请求的信息：', r4.text)
print('获取发送put请求的信息：', r5.text)
print('获取发送delete请求的信息：', r6.text)
print('获取发送head请求的信息：', r7.text)
print('获取发送options请求的信息：', r8.text)
'''
也可以使用requests统一的request方法来发送各种请求：
requests.request('get', 'https://api.github.com/events')
requests.request('post', 'http://httpbin.org/post', data = {'key': 'value'})
requests.request('put', 'http://httpbin.org/put', data = {'key': 'value'})
requests.request('delete', 'http://httpbin.org/delete')
requests.request('head', 'http://httpbin.org/get')
requests.request('options', 'http://httpbin.org/get')
'''
# 5. 在url中传递参数
payload = {'key1': 'value1', 'key2': 'value2'}
r9 = requests.get('http://httpbin.org/get', params=payload)
print('在url中传递参数：', r9.url)


# get-无参
response1 = requests.get(url='http://ws.webxml.com.cn/WebServices/WeatherWs.asmx/getRegionProvince')
print(type(response1)) # 响应对象的类型
print(response1.text) # 响应的内容
# get-有参
url1 = 'http://ws.webxml.com.cn/WebServices/WeatherWs.asmx/getSupportCityString'
params = {'theRegionCode': 31131}
response2 = requests.get(url=url1, params=params)
print(response2.text)

# post
response3 = requests.post(url=url1, data=params, headers={'Content-Type': 'application/x-www-form-urlencoded'})
print(response3.text)

# sop
url2 = 'http://ws.webxml.com.cn/WebServices/WeatherWs.asmx'
data1 = '''<?xml version="1.0" encoding="utf-8">
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLScheam-instance" xmlns:xsd="http://www.w3.org/2001/XMLScheam" xmlns:soap="http:schemas.xmlsoap.org/soap/envelope/">
	<soap:Body>
		<getSupportCityString xmlns="http://webxml.com.cn/">
			#<theRegionCode>string</theRegionCode>
			<theRegionCode>31131</theRegionCode>
		</getSupportCityString>
	</soap:Body>
</soap:Envelope>
'''
response4 = requests.post(url=url2, data=data1, headers={'Content-Type': 'text/xml'})
print(response4.text)

# json
url3 = 'http://139.199.132.220:8000/event/weather/getWeather/'
data2 = '{"theCityCode": 1}'  # 或者 {"theCityCode": 1} 1 or 2
response5 = requests.post(url=url3, data=data2, headers={'Content-Type': 'application/json'})
print(response5.text)
print(response5.status_code)  # 响应 状态码
print(response5.headers)  # 响应 请求头
print(response5.cookies)  # 响应 cookies
print(response5.json())  #  把响应里的json字符串转换成字典格式，方便解析和取值【response.json().get('name') 或者 response.json()['name']，使用get取值,如果该值不存在会返回none而不会报错】
try:
	print(response5.json()).get('name')
except:
	pass


# 对豆瓣的一个URLhttps://api.douban.com/v2/book/2129650进行抓取，并返回响应
with request.urlopen('https://api.douban.com/v2/book/2129650') as f:
	data = f.read()
	print('Status', f.status, f.reason)
	for k, v in f.getheaders():
		print('%s: %s' %(k, v))
	print('Data：', data.decode('utf-8'))
# 模拟浏览器发送GET请求,就需要使用Request对象,通过往Request对象添加HTTP头,就可以把请求伪装成浏览器 【User-Agent：用来标识浏览器】
req = request.Request('http://www.douban.com/')	 # 模拟iPhone 6去请求豆瓣首页
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
with request.urlopen(req) as f:
	print('Status', f.status, f.reason)
	for k, v in f.getheaders():
		print('%s: %s' %(k, v))
	print('Data：', data.decode('utf-8'))

# urllib	request模块可以非常方便地抓取URL内容，也就是发送一个GET请求到指定的页面，然后返回HTTP的响应
	# GET
with request.urlopen('https://api.douban.com/v2/book/2129650') as f:	# 对豆瓣的一个URLhttps://api.douban.com/v2/book/2129650进行抓取，并返回响应
	data = f.read()
	print('Status', f.status, f.reason)
	for k, v in f.getheaders():
		print('%s: %s' %(k, v))
	print('Data：', data.decode('utf-8'))
# 模拟浏览器发送GET请求,就需要使用Request对象,通过往Request对象添加HTTP头,就可以把请求伪装成浏览器 【User-Agent：用来标识浏览器】
req = request.Requst('http://www.douban.com/')	# 模拟iPhone 6去请求豆瓣首页
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
with request.urlopen(req) as f:
	print('Status', f.status, f.reason)
	for k, v in f.getheaders():
		print('%s: %s' %(k, v))
	print('Data：', data.decode('utf-8'))

	# PSOT	以POST发送一个请求，只需要把参数data以bytes形式传入
# 模拟一个微博登录，先读取登录的邮箱和口令，然后按照weibo.cn的登录页的格式以username=xxx&password=xxx的编码传入
print('Login to weibo.cn.....')
email = input('Email：')
passwd = input('Password：')
login_data = parse.urlencode([
	('usernaem',email),
	('password',passwd),
	('entry','mweibo'),
	('client_id',''),
	('savestate','1'),
	('ec',''),
	('pagerefer','https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F')
	])
req = request.Request('https://passport.weibo.cn/sso/login')
req.add_header('Origin', 'https://passport.weibo.cn')
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
req.add_header('Referer', 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F')
with request.urlopen(req, data = login_data.encode('utf-8')) as f:
	print('Status', f.status, f.reason)
	for k, v in f.getheaders():
		print('%s: %s' %(k, v))
	print('Data：', data.decode('utf-8'))

# Handler 通过一个Proxy去访问网站，我们需要利用ProxyHandler来处理
proxy_handler = urllib.request.ProxyHandler({'http':'http://www.example.com:3128/'})
proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
proxy_auth_handler.add_password('realm', 'host', 'username', 'password')
opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
with opener.open('http://www.example.com/login.html') as f:
	pass

# XML(操作XML有两种方法：DOM vs SAX 	优先考虑SAX，因为DOM实在太占内存)
	# SAX：流模式,边读边解析,占用内存小,解析快,缺点是我们需要自己处理事件
		# 当SAX解析器读到一个节点时:<a href="/">python</a>，会产生3个事件：start_element事件，在读取<a href="/">时；char_data事件，在读取python时；end_element事件，在读取</a>时
from xml.parsers.expat import ParserCreate
class DefaultSaxHandler(object):
	"""docstring for DefaultSaxHandler"""
	def start_element(self, name, attrs):
		print('sax:start_element：%s，attrs：%s' %(name, str(attrs)))
	def end_element(self, name):
		print('sax:end_element：%s' %name)
	def char_data(self, text):
		print('sax:char_data：%s' %text)
xml = r'''<?xml version="1.0"?>
<ol>
	<li><a href = "/python">Python</a></li>
	<li><a href = "/ruby">Ruby</a></li>
</ol>
'''
handler = DefaultSaxHandler()
parser = ParserCreate()
parser.StartElementHandler = handler.start_element
parser.EndElementHandler = handler.end_element	# 读取一大段字符串时，CharacterDataHandler可能被多次调用，所以需要自己保存起来，在EndElementHandler里面再合并
parser.CharacterDataHanlder = handler.char_data
parser.Parse(xml)
	# 生成XML
L = []
L.append(r'<?xml version="1.0"?>')
L.append(r'<root>')
# L.append(encode('some & data'))
L.append(r'</root>')
# return ''.join(L)
	# DOM：把整个XML读入内存,解析为树,因此占用内存大,解析慢;优点是可以任意遍历树的节点

# HTMLParser

class MyHTMLParser(HTMLParser):
	"""docstring for MyHTMLParser"""
	def handle_starttag(self, tag, attrs):
		print('<%s>' % tag)
	def handle_endtag(self, tag):
		print('</%s>' % tag)
	def handle_startendtag(self, tag, attrs):
		print('<%s/>' % tag)
	def handle_data(self, data):
		print(data)
	def handle_comment(self, data):
		print('<!--',data,'-->')
	def handle_entityref(self, name):
		print('&%s;' %name)
	def handle_charref(self, name):
		print('&#%s;' %name)
parser = MyHTMLParser()
parser.feed('''<html>
	<head></head>
	<body>
		<p>Some <a href = \"#\">html</a>HTML&nbsp;tutorial...<br>END</p>
	</body>
	''')	# feed()方法可以多次调用，也就是不一定一次把整个HTML字符串都塞进去，可以一部分一部分塞进去
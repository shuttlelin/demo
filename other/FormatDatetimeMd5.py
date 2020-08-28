# 正则表达式
'''
\d		匹配一个数字
\w		匹配一个字母或数字
.		匹配任意字符
*		任意个字符（包括0个）
+		至少一个字符
?		0个或1个字符
\s		匹配一个空格（也包括Tab等空白符）
\s+		至少有一个空格
{n}		n个字符
{n,m}	n-m个字符
[]		范围
^		行的开头
$		行的结束
'-'是特殊字符，在正则表达式中，要用'\'转义，或者用r'-',r前缀就不用考虑转义的问题了
邮箱：someone@gmail.com	bill.gates@microsoft.com
'''

# re.match(r'[a-zA-Z0-9\.\_]+@[0-9a-zA-z\_]+\.\w+',adr)

# datetime 			如果要存储datetime，最佳方法是将其转换为timestamp再存储，因为timestamp的值与时区完全无关

from datetime import datetime

	# 获取当前日期和时间
now = datetime.now() # 获取当前datetime
	# 获取指定日期和时间
dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
	# datetime转换为timestamp	把1970年1月1日 00:00:00 UTC+00:00时区的时刻称为epoch time，记为0（1970年以前的时间timestamp为负数）
		#timestamp = 0 = 1970-1-1 00:00:00 UTC+0:00		timestamp = 0 = 1970-1-1 08:00:00 UTC+8:00	# 北京时间
dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
dt.timestamp() # 把datetime转换为timestamp	【timestamp是一个浮点数。如果有小数位，小数位表示毫秒数】
	# timestamp转换为datetime
t = 1429417200.0
print(datetime.fromtimestamp(t))	# 本地时间	格林威治标准时间与北京时间差了8小时，
print(datetime.utcfromtimestamp(t)) # UTC时间	也就是UTC+0:00时区的时间
	# str转换为datetime
cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print(cday)
	# datetime转换为str
now = datetime.now()
print(now.strftime('%a, %b %d %H:%M'))
	# datetime加减
from datetime import datetime, timedelta
now + timedelta(hours=10)
now - timedelta(days=1)
now + timedelta(days=2, hours=12)
	# 本地时间转换为UTC时间(一个datetime类型有一个时区属性tzinfo，但是默认为None，所以无法区分这个datetime到底是哪个时区，除非强行给datetime设置一个时区)
from datetime import datetime, timedelta, timezone
tz_utc_8 = timezone(timedelta(hours=8)) # 创建时区UTC+8:00
now = datetime.now()
dt = now.replace(tzinfo=tz_utc_8) # 强制设置为UTC+8:00
print(now,dt)
	# 时区转换(通过utcnow()拿到当前的UTC时间，再转换为任意时区的时间)
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)	# 拿到UTC时间，并强制设置时区为UTC+0:00
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))	# astimezone()将转换时区为北京时间
tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))	# astimezone()将转换时区为东京时间
tokyo_dt2 = bj_dt.astimezone(timezone(timedelta(hours=9)))	# astimezone()将bj_dt转换时区为东京时间
print(utc_dt,bj_dt,tokyo_dt,tokyo_dt2)

# base64	用\x00字节在末尾补足后，再在编码的末尾加上1个或2个=号，表示补了多少字节
import base64
base64.b64encode(b'binary\x00string')
base64.b64decode(b'YmluYXJ5AHN0cmluZw==')
s = base64.b64encode('在Python中使用BASE 64编码'.encode('utf-8'))
d = base64.b64decode(s).decode('utf-8')
	# 出现字符+和/，在URL中就不能直接作为参数，所以又有一种"url safe"的base64编码，其实就是把字符+和/分别变成-和_
base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff')
base64.urlsafe_b64decode('abcd--__')
s = base64.urlsafe_b64encode('在Python中使用BASE 64编码'.encode('utf-8'))
d = base64.urlsafe_b64decode(s).decode('utf-8')
	# =用在URL、Cookie里面会造成歧义，所以，很多Base64编码后会把=去掉
#'abcd' -> 'YWJjZA=='	# 标准Base64
#'abcd' -> 'YWJjZA'		# 自动去掉=

# MD5
import hashlib
md5 = hashlib.md5()		or 		hashlib.sha1()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
md5.update('python hashlib?'.encode('utf-8'))
print(md5.hexdigest())

import hmac
message = b'Hello, world!'
key = b'secret'
h = hmac.new(key, message, digestmod='MD5')
h.hexdigest()

# -*- coding: utf-8 -*-
import hmac, random


def hmac_md5(key, s):
	return hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()


class User(object):
	"""docstring for User"""
	def __init__(self, username, password):
		self.username = username
		self.key = ''.join([chr(random.randint(48, 122)) for i in range(20)])
		self.password = hmac_md5(self.key, password)

db = {
	#'michael': USer('michael', '123456'),
	'bob': User('bob', 'abc999'),
	'alice': User('alice', 'alice2008')
}


def login(username, password):
	user = db[username]
	return user.password == hmac_md5(user.key, password)

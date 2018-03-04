#coding=utf-8
import re
import urllib
import requests
import Queue
import time
from bs4 import BeautifulSoup

class ver9000():
	def get_cookie(self,url,headers,count):
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
					login_data=requests.get(url+'/login/LoginForm.jsp',timeout=10)
					cookie_buff=login_data.headers['Set-Cookie']
					cookie_search=re.search(r'([A-za-z0-9]{5,}[!-]+[0-9]*)+',cookie_buff)
					cookie=cookie_search.group()
					self.cookies=dict(ADMINCONSOLESESSION=cookie,path='/')
					print 'Cookie:%s'%cookie
					return True
				except:
					print 'Get cookie Error!\n'
					if ctest == 3:
						f=open('error.txt', 'a')
						f.write('Get cookie Error! '+url+'\n')
						f.close()
		
	def do_login(self,url,usr,pwd,headers,count):
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
					data = {'j_username':usr,'j_password':pwd}
					login_data=requests.post(url+'/j_security_check',data =data,headers=headers,cookies=self.cookies,timeout=10)
					if login_data.content.count('console.portal') !=0:
						print "\r\nLogin Successful!\r\n"
						return 	True
					else:
						print "\r\nLogin Failed!\r\n"
						f=open('bad.txt', 'a')
						f.write('Login Failed: '+url+'\tWebLogic Server 10.x\n')
						f.close()
						return False
				except:
					print 'Login Error!\n'
					if ctest == 3:
						f=open('error.txt', 'a')
						f.write('Login Error! '+url+'\n')
						f.close()


	def get_server_name(self,url,headers,count):
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
					server_data=requests.get(url+'/console.portal?_nfpb=true&_pageLabel=CoreServerServerTablePage',headers=headers,cookies=self.cookies,timeout=10)
					server_soup=BeautifulSoup(server_data.text)
					for name in server_soup.find_all('a'):
						if name.get('href') != None:
							name=re.search(r'\:Name=[\w]*\,Type\=Server',urllib.unquote(name.get('href')))
							if name :
								self.server_name=name.group()
								break
					self.server_name=re.search(r'Name=[a-zA-Z0-9]*',self.server_name)
					self.server_name=self.server_name.group()[5:]
					print 'ServerName:%s\r\n' %self.server_name
					return True
				except:
					print 'get_server_name Error!\n'
					if ctest == 3:
						f=open('error.txt', 'a')
						f.write('get_server_name Error! '+url+'\n')
						f.close()

	def get_domain_name(self,url,headers,count):
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
					domain_data=requests.get(url+'/console.portal?_nfpb=true&_pageLabel=CoreServerServerTablePage',headers=headers,cookies=self.cookies,timeout=10)
					domain_soup=BeautifulSoup(domain_data.text)
					for name in domain_soup.find_all('a'):
						if name.get('href') != None:
							name=re.search(r'\:Name=[\w]*\,Type\=Domain',urllib.unquote(name.get('href')))
							if name :
								self.domain_name=name.group()
								break
					self.domain_name=re.search(r'Name=[\w]*',self.domain_name)
					self.domain_name=self.domain_name.group()[5:]
					print 'DomainName:%s\r\n' %self.domain_name
					return True
				except:
					print 'get_domain_name Error!\n'
					if ctest == 3:
						f=open('error.txt', 'a')
						f.write('get_domain_name Error! '+url+'\n')
						f.close()


	def get_path(self,url,headers,warname,count):
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
					path_exp=warname+' [^ -~]*[ -~]*'
					path_sea=re.search(path_exp,self.path_data.text)
					if path_sea:
						path=re.search(r'[a-zA-Z]:(\\[\w .]+)+',path_sea.group()) #Windows
						if path:
							self.path=path.group()
							self.system=1
							print 'Target system: Windows\n'
						else:
							path=re.search(r'(/[\w .]+)+',path_sea.group()) #Linux
							if path:
								self.path=path.group()
								self.system=2
								print 'Target system: Linux\n'
					time.sleep(1)
					print 'Upload Path:%s\n' %self.path
					return True
				except:
					print 'get_path Error!\n'
					if ctest == 3:
						f=open('error.txt', 'a')
						f.write('get_path Error! '+url+'\n')
						f.close()


	def uploader(self,url,warname,headers,count):
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
					upload_file = {'AppApplicationInstallPortletuploadAppPath': (warname, open(warname, 'rb'), 'application/octet-stream')}
					upload_url=url+'/console.portal?AppApplicationInstallPortlet_actionOverride=/com/bea/console/actions/app/install/uploadApp'
					print 'Uploading...',
					self.path_data=requests.post(upload_url,cookies=self.cookies,headers=headers,files=upload_file,timeout=20)
					print 'OK!\n'
					return True
				except:
					print 'upload Error!\n'
					if ctest == 3:
						f=open('error.txt', 'a')
						f.write('upload Error! '+url+'\n')
						f.close()

	
	def unlock(self,url,headers,count):
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
					unlock_data={'ChangeManagerPortlet_actionOverride':'/MakeChangesAction',
					'changeCenter':'ChangeCenterClicked',
					'_nfpb':'true',
					'_pageLabel':'HomeReserved'
					}
					requests.post(url+'/console.portal',data=unlock_data,headers=headers,cookies=self.cookies,timeout=10)
					print 'Unlock OK!\n'
					return True
				except:
					print 'Unlock Error!\n'
					if ctest == 3:
						f=open('error.txt', 'a')
						f.write('Unlock Error! '+url+'\n')
						f.close()


	def active(self,url,headers,count):
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
					active_data={'ChangeManagerPortlet_actionOverride':'/ActivateChangesAction',
					'changeCenter':'ChangeCenterClicked',
					'_nfpb':'true',
					'_pageLabel':'HomeReserved'
					}
					requests.post(url+'/console.portal',data=active_data,headers=headers,cookies=self.cookies,timeout=10)
					print 'Active OK!\n'
					return True
				except:
					print 'Active Error!\n'
					if ctest == 3:
						f=open('error.txt', 'a')
						f.write('Active Error! '+url+'\n')
						f.close()

	
	def start_instance(self,url,headers,depolyname,count):
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
					start_data1={
					'AppGlobalStartPortletchosenContents':'com.bea.console.handles.AppDeploymentHandle("com.bea:Name='+depolyname+',Type=AppDeployment")',
					'_pageLabel':'AppGlobalStartPage',
					'_nfpb':'true'
					}
					start_data2={'AppGlobalStartPortlet_actionOverride':'/com/bea/console/actions/app/globalstart/finish'}
					print 'Starting instance...\n'
					print 'Stage one....',
					requests.post(url+'/console.portal?AppGlobalStartPortletreturnTo=AppDeploymentsControlPage&AppDeploymentsControlPortlethandle=com.bea.console.handles.JMXHandle%28%22com.bea%3AName%3D'+self.domain_name+'%2CType%3DDomain%22%29',data=start_data1,headers=headers,cookies=self.cookies)
					print 'OK!\tStage two....',
					requests.post(url+'/console.portal',data=start_data2,headers=headers,cookies=self.cookies)
					print 'OK!\n'
					print '%s Started!\n' %depolyname
					return True
				except:
					print 'Start Error!\n'
					if ctest == 3:
						f=open('error.txt', 'a')
						f.write('Start Error! '+url+'\n')
						f.close()

			
	def depoly(self,url,warname,depolyname,headers,count):
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
					if self.system == 1:
						depoly_data1={'AppApplicationInstallPortletselectedAppPath': self.path+'\\'+warname}
						depoly_data2={'AppApplicationInstallPortlettargetStyle': 'Application'}
						depoly_data3={
							'AppApplicationInstallPortletname': depolyname,
							'AppApplicationInstallPortletsecurityModel': 'DDOnly',
							'AppApplicationInstallPortletstagingStyle': 'Default',
							'AppApplicationInstallPortletnoStageSourcePath': self.path+'\\'+warname
							}
					else:
						depoly_data1={'AppApplicationInstallPortletselectedAppPath': self.path+'/'+warname}
						depoly_data2={'AppApplicationInstallPortlettargetStyle': 'Application'}
						depoly_data3={
							'AppApplicationInstallPortletname': depolyname,
							'AppApplicationInstallPortletsecurityModel': 'DDOnly',
							'AppApplicationInstallPortletstagingStyle': 'Default',
							'AppApplicationInstallPortletnoStageSourcePath': self.path+'/'+warname
							}
					print 'Depolying....',
					requests.post(url+'/console.portal?AppApplicationInstallPortlet_actionOverride=/com/bea/console/actions/app/install/appSelected',cookies=self.cookies,headers=headers,data=depoly_data1,timeout=20)
					requests.post(url+'/console.portal?AppApplicationInstallPortlet_actionOverride=/com/bea/console/actions/app/install/targetStyleSelected',cookies=self.cookies,headers=headers,data=depoly_data2,timeout=20)
					requests.post(url+'/console.portal?AppApplicationInstallPortlet_actionOverride=/com/bea/console/actions/app/install/finish',cookies=self.cookies,headers=headers,data=depoly_data3,timeout=20)				
					print 'OK!\n'
					return True
				except:
					print 'depoly Error!\n'
					if ctest == 3:
						f=open('error.txt', 'a')
						f.write('depoly Error! '+url+'\n')
						f.close()


	def test(self,url,depolyname,testpage,count):
		ctest=0
		if len(self.domain_name) < 8:
			t='\t\t\t'
		elif len(self.domain_name) > 15:
			t='\t'
		else:
			t='\t\t'
		while True:
			if ctest == count:
				return False
			else:
				if ctest != 0:
					ctest+=1
					print "Retry %s times" %ctest
				else:
					ctest+=1
				test_url=url.split('/console')[0]+'/'+depolyname+'/'+testpage
				test_data=requests.get(test_url)
				if len(test_url) < 40:
					t2='\t\t'
				else:
					t2='\t'
				if test_data.status_code == 200:
					print 'Test OK!\t'+test_url+'\n'
					f=open('good.txt', 'a')
					if self.system == 1:
						f.write(test_url+t2+'WebLogic 9\t\t'+self.domain_name+t+'Windows\t'+time.strftime("%Y-%m-%d[%H.%M.%S]")+'\n')
						f.close()
						return
					else:
						f.write(test_url+t2+'WebLogic 9\t\t'+self.domain_name+t+'Linux\t'+time.strftime("%Y-%m-%d[%H.%M.%S]")+'\n')
						f.close()
						return
				else:
					print 'Test Failed!'
					f=open('bad.txt', 'a')
					if self.system == 1:
						f.write('Test Failed:'+test_url+t2+'WebLogic 9\t\t'+self.domain_name+t+'Windows\t'+time.strftime("%Y-%m-%d[%H.%M.%S]")+'\n')
						f.close()
						return
					else:
						f.write('Test Failed:'+test_url+t2+'WebLogic 9\t'+self.domain_name+t+'Linux\t'+time.strftime("%Y-%m-%d[%H.%M.%S]")+'\n')
						f.close()
						return

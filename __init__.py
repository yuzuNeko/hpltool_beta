import requests
import json
import time
import pymysql
import os
import tushare as ts
from datetime import datetime,timedelta
import pickle
#迭代打印


class tools:
	@staticmethod
	def sl(li,num,remove=False):
		l=[li[i:i+num] for i in range(0,len(li),num)]
		if not remove:
			return l
		if remove:
			if len(l[-1])!=num:
				l.pop()
			return l
	@staticmethod
	def get_today_string():
		st=datetime.now().__str__()
		l=st.split(' ')
		return l[0]
	@staticmethod
	def get_yestoday_string():
		st=(datetime.now()-timedelta(days=1)).__str__()
		l=st.split(' ')
		return l[0]
	@staticmethod
	def get_someday_string(day,fmt=None):
		#fmt可以格式化输出不同类型的时间数据
		#目前只有两个 一个是普通型默认为None 格式为2019-11-10
		#space型，以空格为间隔 2019 11 10 
		#nospace型 无空格类型 20191110

		#有空可以把下面代码复用一下
		if day>0:
			days=abs(day)
			st=(datetime.now()+timedelta(days=days)).__str__()
			l=st.split(' ')
			result=l[0]
			if fmt=='space':
				result=result.replace('-',' ')
			if fmt=='nospace':
				result=result.replace('-','')
			return result
		if day<0:
			days=abs(day)
			st=(datetime.now()-timedelta(days=days)).__str__()
			l=st.split(' ')
			result=l[0]
			if fmt=='space':
				result=result.replace('-',' ')
			if fmt=='nospace':
				result=result.replace('-','')
			return result
	@staticmethod
	def return_datetime_string_list(start_string,end_string):
		#用途：返回一个两个格式化日期之间的时间序列的列表

		#可以格式化这两个字符，变成可以操作的东西，不限于单一格式
		#普通格式 如2018-10-11
		print('ready')
		fmt={}
		fmt['normal']='%Y-%m-%d'
		start=datetime.strptime(start_string,fmt['normal'])
		result_list=[]
		count=0
		while 1:
			item=start.__str__().split(' ')[0]
			result_list.append(item)
			if item==end_string or count==10000:
				break
			start=start+timedelta(days=1)
			count+=1
		return result_list



	#简化一些常用的方法，舍弃了别人的可读性，以下分别为，将字符串写入
	#读取，序列化等操作，都是在脚本所处的同级文件下进行
	#这里只能用实例方法
	def w(self,filename,string,path=None):
		if path!=None:
			with open(os.path.join(path,filename),'w') as f:
				f.write(string)
		current_module=self.__module__
		if current_module!='__main__':
			import os
			print(os.getcwd())
			current_path=os.getcwd()
			file=os.path.join(current_path,filename)
			with open(file,'w') as f:
				f.write(string)
	def r(self,filename,path=None):
		if path!=None:
			with open(os.path.join(path,filename),'r') as f:
				read=f.read()
				print(read)
				return read
		current_module=self.__module__
		if current_module!='__main__':
			import os
			print(os.getcwd())
			current_path=os.getcwd()
			file=os.path.join(current_path,filename)
			with open(file,'r') as f:
				read=f.read()
				print(read)
				return read
	def pic_r(self,filename,path=None):
		if path!=None:
			with open(os.path.join(path,filename),'rb') as f:
				read=f.read()
				read=pickle.loads(read)
				return read
		current_module=self.__module__
		if current_module!='__main__':
			import os
			import pickle
			print(os.getcwd())
			current_path=os.getcwd()
			file=os.path.join(current_path,filename)
			with open(file,'rb') as f:
				read=f.read()
				read=pickle.loads(read)
				return read
	def pic_w(self,filename,string,path=None):
		if path!=None:
			with open(os.path.join(path,filename),'wb') as f:
				string=pickle.dumps(string)
				f.write(string)
		current_module=self.__module__
		if current_module!='__main__':
			import os
			import pickle
			print(os.getcwd())
			current_path=os.getcwd()
			file=os.path.join(current_path,filename)
			with open(file,'wb') as f:
				string=pickle.dumps(string)
				f.write(string)




def iter_print(items):
	for i in items:
		print(i)

class hplrequests:
	def __init__(self,url='',headers=None):

		if headers==None:
			self.headers={
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'

	}
		else:
			self.headers=headers
		self.url=url
		self.request_text=None
	def get(self):
		res=requests.get(headers=self.headers,url=self.url)
		print(res.text)
		self.request_text=res.text
		return self.request_text
	def get_json(self):
		j=json.loads(self.get())
		print(j)
		return j
	def save_txt(self,filename='default.txt'):
		try:
			res=requests.get(headers=self.headers,url=self.url)
			with open('{}'.format(filename),'w',encoding='utf-8') as f:
				f.write(res.text)
		except:
			print('发生错误')
	def js_get_in_brackets(self):
		import re
		regex='\((.*)\)'
		regex=re.compile(regex,re.S)
		l=regex.findall(self.request_text)
		try:
			self.in_brackets_json=json.loads(l[0])
		except:
			print('不能直接获取为json格式')
		return l[0]

class hplpymysql:

	def __init__(self,host='127.0.0.1',
		user='root',password='123456',
		port=3306,database='sp01',charset='utf8'):
		self.host=host
		self.user=user 
		self.password=password
		self.port=port 
		self.database=database
		conn=pymysql.connect(
			host=host,
			user=user,
			password=password,
			port=port,
			database=database,
			charset=charset

			)
		cur=conn.cursor()
		self.conn=conn
		self.cur=cur
		self.show()
		self.table_list=self.result
		self.current_table=self.table_list[0][0]
		#获取第一个为当前的表
	def __del__(self):
		print('close.....')
		self.conn.close()
		self.cur.close()
	#主要执行函数，其他简易方法基本从这里派生
	def sql(self,sql):
		try:
			self.cur.execute(sql)
			self.conn.commit()
			self.result=self.cur.fetchall()
			print(self.result)
		except Exception as e:
			print('失败。。。')
			print(e)
	def choose(self,table):
		if isinstance(table,int):
			self.current_table=self.table_list[table][0]
			self.cur.execute('desc {}'.format(self.current_table))
			self.conn.commit()
			return 

		self.current_table=table
		self.current_table_field=[]
		self.cur.execute('desc {}'.format(table))
		self.conn.commit()
		result=self.cur.fetchall()
		for i in result:
			print(i)
			self.current_table_field.append(i[0])

	def add(self,*arg,**kw):
		if not self.current_table:
			return
		if kw:
			print(kw)
		if arg:
			print(arg)
			self.sql("insert into {} values {}".format(str(self.current_table),
				str(arg)))
	def show(self):
		print('显示全部的表')
		self.sql('show tables')
	def see(self):
		self.sql('select * from {}'.format(self.current_table))
	def d(self):
		#desc 的简单写法
		self.sql('desc {}'.format(self.current_table))
		iter_print(self.result)
	def all(self):
		self.sql('select * from {}'.format(self.current_table))
		iter_print(self.result)
	def drop(self):
		self.sql(f'drop table {self.current_table}')
		print(f'删除了表{self.current_table}')
	def delall(self):
		self.sql(f'truncate table {self.current_table}')
		print('清除了表中的所有数据')
	def sql_c(self,field,condition):
		#这个地方需要加判断，因为格式化的原因
		self.sql(f'select * from {self.current_table} where {field}="{condition}"')
	def db(self):
		self.sql('show databases')
		for i in self.result:
			print(i)







class stock_handler:
	def __init__(self,data_dir='./',stock_table='',
				split_cycle=480,second_dir='data'):
		#原来命名的不规范，导致写成类的时候也很不规范。。。
		self.data_dir=data_dir
		self.stock_table=stock_table
		self.split_cycle=split_cycle
		self.second_dir=second_dir
		self.today_all='today_all.json'

	def get_new_high(self):
		a=os.listdir(self.data_dir)
		aname=self.stock_table
		cycle=self.split_cycle
		#外层参数
		# print(a)
		#获取当天所有股票涨跌信息的json
		with open('{}'.format(self.today_all),'r') as f:
			today_json=json.loads(f.read())
		with open('{}'.format(aname),'r',encoding='utf-8') as f:
			stock_name=json.loads(f.read())['name']

		result_list=[]
		for i in a:
			with open('./{}/{}'.format(self.second_dir,i),'r') as f:
				read=json.loads(f.read())
			try:
				f=[(key,val)for key,val in read['high'].items()]
				#这里有改动啊
				#不知道会不会有影响，看明天
				q=f[:]
				#可变参数
				#把这里面的硬编码去掉，实现更多的功能和代码重用
				current=q[len(q)-1][1]
				current2=q[len(q)-2][1]
				current3=q[len(q)-3][1]
				current4=q[len(q)-4][1]

				q.sort(key=lambda x :x[1],reverse=True)
				#计算，最后一天的最高值大于半年统计的最高值
				if current>=q[0][1] or current2>=q[0][1] or current3>=q[0][1] or current4>=q[0][1] :
					stockcode=i[0:6]
					for i1 in today_json['code']:
						if today_json['code'][i1]==stockcode:
							#获取涨跌值，这个地方耦合得有点严重了，不舒服
							per=today_json['changepercent'][i1]
							break

					result_list.append((i[0:6],stock_name[i[0:6]],per))
					
			except Exception as e:
				print(e)
				print('error  {}'.format(i))

		for i in result_list:
			print(i)
		return result_list
	def get_data(self,save_dir='',save_suffix='_60min.json',
	json_column='name',ktype='60'):

		with open('{}'.format(str(self.stock_table)),'r',encoding='utf-8') as f:
			a=json.loads(f.read())
		for key,val in a[json_column].items():
			print(key)
			print(val)
			try:
				res=ts.get_k_data(str(key),ktype=ktype)
				res.to_json('{}/{}{}'.format(save_dir,str(key),save_suffix))
			except:
				print('报错！{}'.format(str(val)))
				

	def get_textjson_keyval(self,filename='data.json',column_name='some',encoding='utf-8',
	return_column=False,return_all=False,return_dict=False,ldir=''):
		a=None
		try:
			with open('{}'.format(filename),'r',encoding=encoding) as f:
				a=json.loads(f.read())
		except:
			# print('这里报错')
			pass
		# print(a)
		if not a :
			try:
				with open('{}/{}'.format(ldir,filename),'r',encoding=encoding) as f:
					a=json.loads(f.read())
			except Exception as e:
				print(e)
		
		if return_all:
			return a
		if return_dict:
			return a[column_name]
		# for key,val in a[column_name].items():
		# 	li.append((key,val))
		#再次化简

		li=[(key,val) for key,val in a[column_name].items()]
		return li
	def get_today_all(self,savename='today_all.json'):
		df=ts.get_today_all()
		df.to_json('{}'.format(savename))
	def get_vol_high_of_one(self,filename,col='volume',sep=4,ldir=''):
		try:
			l=self.get_textjson_keyval(filename=filename,column_name=col,ldir=ldir)
		except:
			# print('报错')
			return None
		val_list=[]
		for i in l:
			val_list.append(i[1])
		l=[val_list[i:i+sep] for i in range(0,len(val_list),sep)]
		temp=0
		for i in l:
			if sum(i)>=temp:
				temp=sum(i)
		today=val_list[-sep:]

		if sum(today)>=temp:
			return filename
	#获得文件夹下所有文件符合要求的，返回一个code列表
	def get_vol_high_all(self,ldir='/root/beta/data'):
		l=os.listdir(ldir)
		result_list=[]
		for i in l:
			resu=self.get_vol_high_of_one(i,ldir=ldir)
			if resu:
				result_list.append(self.split_filename(resu))
		return result_list


	def code_for_today(self):
		pass
	def split_filename(self,filename,num=6):
		return filename[:num]
	#获取一个json数据的列







class hpldir:
	def dirobj(self,obj):
		'''
		to see a object's attribute,
		sometimes would not work will return ****

		'''
		a=dir(obj)
		dic={}
		for i in a:
			o='*******************'
			dic[i]='*********************'
			try:
				ob=compile('obj.{}'.format(i),'','eval')
			except :
				pass
			try:
				o=eval(ob)
			except :
				pass
			if o:
				dic[i]=o
			try:
				if o==False:
					dic[i]=o
			except:
				pass
			if not o:
				try:
					dic[i]=o.__str__()
				except:
					pass

		for i in dic:
			print(i+'-------------',dic[i])

#一个斐波那契额数列的类
class fib:
	def __init__(self,max):
		self.start=0
		self.end=1
		self.max=max
		self.count=0
	def __iter__(self):
		#这句话没必要，不够特化
		return self
	def __next__(self):
		index=self.start
		if self.count>self.max:
			raise StopIteration
		self.start,self.end=self.end,self.start+self.end
		
		self.count+=1
		return index




def import_ml_packages():
	#作用域问题，并不能直接弄到本来的作用域
	try:
		import numpy as np
		import pandas as pd
		from pandas import Series,DataFrame
		from sklearn.model_selection import train_test_split
		from sklearn.neighbors import KNeighborsClassifier
		from sklearn.neighbors import KNeighborsRegressor
		from sklearn.linear_model import LinearRegression
		from sklearn.linear_model import LogisticRegression
		from sklearn.linear_model import Ridge
		from sklearn.linear_model import Lasso
		from sklearn.tree import DecisionTreeClassifier
		from sklearn.tree import DecisionTreeRegressor
		from sklearn.ensemble import RandomForestClassifier
		from sklearn.naive_bayes import GaussianNB
		from sklearn.naive_bayes import MultinomialNB
		from sklearn.naive_bayes import BernoulliNB
		import matplotlib.pyplot as plt

	except:
		print('导入失败')

##############################观察者模式#################################################
class observer:
	def __init__(self):
		self.ob=set()

	def sub(self,ob):
		self.ob.add(ob)
	def unsub(self,ob):
		self.ob.discard(ob)

	def notify(self,*arg,**kw):
		for o in self.ob:
			o.recv(*arg,**kw)

class magazine(observer):
	def __init__(self):
		observer.__init__(self)

	def publish(self,msg):
		print('发布')
		self.notify(msg)

class stu:
	def recv(self,data):
		print(data,'学生收到')

class te:
	def recv(self,data):
		print(data,'老师收到')


class manager:
	def __init__(self):
		self.mz=magazine()
		self._list=[]
	def sub(self,*arg,**kw):
		print(arg)
		[self.mz.sub(i) for i in arg]
	def register(self,inst):
		self._list.append(inst)
	def pub(self,msg):
		self.mz.publish(msg)


#########################################################################################



#####################工厂模式###########################################################

import abc

class car(metaclass=abc.ABCMeta):
	def __init__(self,name,tyre,engine,face):
		self.name=name
		self.tyre=tyre
		self.engine=engine
		self.face=face

	def __str__(self):
		return self.name
	@abc.abstractmethod
	def fire(self):
		raise NotImplementedError

	@abc.abstractmethod
	def run(self):
		raise NotImplementedError



class jcar(car):
	def __init__(self,name,tyre,engine,face):
		car.__init__(self,name,tyre,engine,face)
	def fire(self):
		print('点火')
	def run(self):
		print('启动')

car_type_dict={
	
}
class factory:
	def __init__(self,name):
		self.name=name
		self.carlist=[]
	def create_car(self,name,tyre,engine,face,type):
		car=car_type_dict[type](name,tyre,engine,face)
		self.carlist.append(car)





# f=factory()

class cacheBase(metaclass=abc.ABCMeta):
	cached={}

	@abc.abstractmethod
	def get(self,key):
		raise NotImplementedError

	@abc.abstractmethod
	def set(self,key):
		raise NotImplementedError


class redis_cache(cacheBase):
	def get(self,key):
		return print(self.cached[key])

	def set(self,key,val):
		self.cached[key]=val
		print(f'set key:{key} values:{val}')

###################################################################################################






import os
from datetime import datetime
from datetime import timedelta
import time
from threading import Thread

class task_list(list):
	#先添加元素，然后手动进入loop
	#初步做成，完善日志，传参，周期等功能
	#还是有bug主要是在当日启动后的时间去启动，会有问题
	def __init__(self,task_list,*arg):
		for i in task_list:
			self.append(i)



	def get_time(self):
		t=datetime.now()
		self.today=datetime.strftime(t,'%Y-%m-%d')
		# print(t)
		return t
	
	def go_sleep(self,t):
		print(f'进入睡眠，距离下个任务还有{t}秒')
		time.sleep(t)

	def get_seconds(self,now):
		#这段代码，怎么改会比较好？
		#计算启动时间和下一次任务执行的时间，为正数则加入队列
		order_list=[]
		order_list1=[]
		for i in self:
			try:
				t=int((i.first_execute-now).total_seconds())
			except:
				t=int((i.next_execute-now).total_seconds())
			#不得不又硬编码。。
			print(t)
			# print(i.time_before_format)
			if t<0 :
				# print(' here?')
				#这个地方还是悬而未决，要向更好的方法
				t=int((i.first_execute-now+timedelta(seconds=i.time_interval)).total_seconds())
			print(t)
			print('over?')
			print(self.today)
			print(i.time_before_format)

			if t>0:
				order_list.append((t,i))
				order_list1.append(t)
		task=order_list[order_list1.index(min(order_list1))][1]
		sleeptime=min(order_list1)
		return (sleeptime,task)
	def run_threading(self,fnc):
		print(f'开启线程{fnc}')
		t=Thread(target=fnc)
		t.start()


	def loop(self):
		while 1:
			
			now=self.get_time()
			task=self.get_seconds(now)[1]
			t=self.get_seconds(now)[0]
			self.go_sleep(t)
			self.run_threading(task.run_task)



class task:
	#时间格式暂时严格遵守%Y-%m-%d %H:%M:%S
	#这样传入计算会比较方便
	#time interval暂时固定为秒，这样好循环
	#之后再加上一些天数 日期的判断
	#实例化first——execute的时候，传入前面三项可以使用当前时间进行格式化
	#然后再拼起来
	#传参时不传递前面的年月日，默认得到当日的时间
	def __init__(self,os_statement='',recycle=True,
		cycle_times=None,log='task.log',first_execute='',
		time_interval=''):
		self.os_statement=os_statement
		self.recycle=recycle
		self.cycle_times=cycle_times
		self.log=log
		self.time_before_format=first_execute
		self.first_execute=datetime.strptime(first_execute,'%Y-%m-%d  %H:%M:%S')
		self.time_interval=time_interval
		self.modify_old_time()

	def next_call_time(self):
		if self.first_execute:
			self.next_execute=self.first_execute+timedelta(seconds=self.time_interval)
			self.first_execute=None
		else:
			self.next_execute+=timedelta(seconds=self.time_interval)
		return self.next_execute

	def run_task(self):
		print(self.os_statement)
		os.system(self.os_statement)
		self.next_call_time()
		print(f'task结束  {datetime.now()}')
		if not self.recycle:
			return self.count_alive()

	def count_alive(self):
		self.cycle_times-=1
		if self.cycle_times==0:
			return False
		else:
			return True

	def modify_old_time(self):
		self.join_today_time()
		sub=int((self.first_execute-datetime.now()).total_seconds())
		if sub<0:
			prefix=datetime.strftime(datetime.now(),'%Y-%m-%d')
			new=prefix+'  '+self.time_before_format.split('  ')[1]
			self.first_execute=datetime.strptime(new,'%Y-%m-%d  %H:%M:%S')
		print(self.first_execute)
	def join_today_time(self):
		if len(self.time_before_format.split('  '))==1:
			prefix=datetime.strftime(datetime.now(),'%Y-%m-%d')
			new=prefix+'  '+self.time_before_format
			self.first_execute=datetime.strptime(new,'%Y-%m-%d  %H:%M:%S')







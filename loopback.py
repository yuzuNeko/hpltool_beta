import os

'''
数据格式
基本格式，存储为txt的编码为ansi的数据
可以用pandas直接读取，所以这里围绕pandas进行展开
读取完后市dataframe格式的数据
通过df.loc[]进行索引，得到series，但是是没有列索引的
df.values[:-1]获得掐头去尾的数据，里面都是列表，但是在索引的时候难免要硬编码。。
'''

'''
日志
0718
没有考虑跌停等等情况，可操纵性没有考虑，之后要处理每次交易的信息，要带上金额
'''
class loopback:
	'''
	参数设置,data为目标数据流，cycle为组合基数，即将元data
	按照周期进行组合，元data为5分钟数据，那么cycle为3说明是在15分钟维度
	上进行回测。
	ma,制定维度后的均线，不言自明
	止盈止损，设置为3位的浮点数
	contp consl 条件触发偏离价位，触发后改变模式。
	mode,有多重实现。详见mode文档
	cold,冷却期，是在强制冷却期后加上的。数量为组合后的时间，整数类型
	冷却期均在组合后时间里讨论，组合时间=data/cycle
	均线=组合时间/ma

	几个概念：
	组合基数，基本数据流（5min）乘上cycle得到，比如15分钟，20分钟，必须是5分钟的倍数
	均线是基于组合基数计算的
	'''
	def __init__(self,
		data='',cycle=3,ma=60,target_profit='',stop_loss='',con_tp='',con_sl='',
		mode='simple',up_p=0,down_p=0,cold='',):
		#这个初始化赋值能不能写得简单一点，比如用个字典什么的？
		#这样感觉非常繁琐
		self.data=data
		self.cycle=cycle
		self.ma=ma 
		self.target_profit=target_profit
		self.stop_loss=stop_loss
		self.con_tp=con_tp
		self.con_sl=con_sl
		self.mode=mode
		self.up_p=up_p
		self.down_p=down_p
		self.cold=cold
		#其他一些参数
		self.ma_list=[]
		#记录买入卖出的时间和一些参数
		self.log={'trade':[]}

	def setup(self,*arg,**kw):
		#再次设定初始化参数
		self.__init__(*arg,**kw)
		print('再次设定完毕')
	def readdir(self,dir=''):
		#最好要绝对路径
		result_list=[]
		for i in os.listdir(dir):
			result_list.append(os.path.join(dir,i))
		return result_list
	#暂时硬编码，之后要从这里取
	#深深的思考，感觉一直是在写重复的代码，主要是数据格式不一样
	#有没有什么方法能减少我的代码量
	def file_handler(self,filename):
		l=[]
		#获取时间，收盘价
		with open(filename,'r') as f:
			for i in f:
				a=i.split(' ')
				if len(a)!=1:
					l.append((a[0]+'-'+a[1],a[5]))
		return l
	def make_tuple_list(self,df,num=4):
		#从dataframe形成时间+开盘价的元组，并形成这样元组组成的列表，
		#1=开盘价，2=最高，3=最低，4=收盘
		#很多硬编码，不知道怎么去。。
		self.t_list=[]
		self.p_list=[]
		result_list=[]
		for i in df.values[:-1]:
			st=i[0].split(' ')
			t=st[0]+'-'+st[1]
			#开盘价位于第三项
			price=st[num+1]
			self.t_list.append(t)
			self.p_list.append(price)
			result_list.append((t,price))
		self.tuple_list=result_list
		return result_list
	def make_ma(self,ma=None):
		if ma==None:
			ma=self.ma
		for i in self.init_list:
			self.ma_list.append((i[0],self.return_prev(i,self.init_list,ma)))
		return self.ma_list


	def make_init(self,cycle=None):
		if cycle==None:
			cycle=self.cycle
		if not self.tuple_list:
			pritn('请先生成')
			return
		new=[self.tuple_list[i:i+cycle] for i in range(0,len(self.tuple_list),cycle)]
		# print(new)
		new_list=[]
		for i in new:
			sum_=0
			for ii in i:
				sum_+=float(ii[1])
				time=ii[0]
			new_list.append((time,round(sum_/cycle,2)))
		self.init_list=new_list
		return new_list
	def return_prev(self,item,li,ma):
		sum_=0
		index=li.index(item)
		if index<ma-1:
			return None
		sep=li[index+1-ma:index+1]
		for i in sep:
			sum_+=float(i[1])
		return round(sum_/ma,2)
	def status_init(self):
		self.hold_status='等待买入'
		self.is_cold=0
	def comp(self,i):
		if self.init_list[i][1]>=self.ma_list[i][1]:
			return True
		else:
			return False
	def calc_cold(self,i):
		#各种硬编码
		print('*********************************')
		date=self.init_list[i][0][:-5]
		# print(date)
		# print(type(date))
		for q in range(i,len(self.init_list)):
			# print(self.init_list[q][0][:-5])
			if self.init_list[q][0][:-5]!=date:
				cold=q-i
				return cold
		return 0

		#这个函数写得还是不太满意，这个状态机怎么弄会更好
		#呢？
	def check_status(self,i):
		# print(self.is_cold,self.hold_status)
		if self.is_cold!=0:
			self.is_cold-=1
			return None
		#下面这里可以抽象出去。。
		if self.hold_status=='等待买入':
			a=self.comp(i)
			if not a:
				return None
			if a:
				#大于，买入，变更标志为买入持有
				#计算冷却期，赋值
				self.hold_status='买入持有'
				self.is_cold=self.calc_cold(i)
				print(f'{self.init_list[i][0]}进行买入')
				self.every_handler(i,bs='buy')
		if self.hold_status=='买入持有':
			a=self.comp(i)
			if a:
				return None
			if not a :
				self.hold_status='等待买入'
				self.is_cold=self.cold
				#这里可以加个模糊项
				print(f'{self.init_list[i][0]}进行卖出')
				self.every_handler(i,bs='sale')


		


	def init_train(self):
		for i in range(len(self.ma_list)):
			# print(self.ma_list[i][0],self.ma_list[i][1])
			if self.ma_list[i][1]==None:
				continue
			if self.init_list[i][1]>=self.ma_list[i][1]:
				continue
			else:
				self.status_init()
				return i
	def train(self):
		start=self.init_train()
		#这里写得有点乱，但是我也不知道怎么设计比较好

		for i in range(start,len(self.ma_list)):
			self.check_status(i)
	#为了精度，这个df还是要处理一下，把第一行拿下来
	def fit(self,df):
		self.make_tuple_list(df)
		self.make_init()
		self.make_ma()
		self.train()
		# self.evaluate()
		
	def every_handler(self,i,bs):
		self.log['trade'].append((self.init_list[i],bs))
	def evaluate(self):
		#这里直接硬编码，把列表拆分成两个一组
		l=[self.log['trade'][i:i+2] for i in range(0,len(self.log['trade']),2)]
		if len(l[-1])!=2:
			l.pop()
		#每一笔交易需要评估的，收益率，持有时间
		hold_time=[]
		hold_profit=[]
		for i in l:
			# print(i)
			dic={}
			buy=i[0][0][1]
			sale=i[1][0][1]
			result=round((sale-buy)/buy,3)
			#处理收益率
			dic['profit']=result
			dic['per_profit']=str(round(result*100,2))+'%'
			#处理时间
			start=i[0][0][0]
			end=i[1][0][0]
			st=self.t_list.index(start)
			et=self.t_list.index(end)
			hold_t=(et-st)*5/(5*12*4)
			hold_t=str(round(hold_t,2))+'个交易日'
			dic['hold_t']=hold_t
			i.append(dic)
		for i in l:
			print(i)
		return l




		












	








'''
############# mode 模式###############
simple：简单模式，交易策略为，从均线下方触及均线买入，从均线上方跌破均线进行卖出为一次交易。
可选参数有，up_p down_p，即微调上穿均线多少买入，跌破多少卖出。拥有强制冷却期和可选冷却期



'''

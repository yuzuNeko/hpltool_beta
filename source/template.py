'''
	定义一个常用的文本模板，适用于喝多python脚本的写作，可以集成到hpltools里
'''

#内置模块导入区
import sys



#外部库导入区



#自定义库导入区




#全局变量，配置定义


#万用接口类，用于传递一些实现
class Interface():
	def main():
		pass





#选择入口字典
module_set={
	'default':Interface,
}
#可以省略加入字典的步骤
module_set_inject=globals()


def switch(mode=None):
	if mode!=None:
		select_mode=mode
	try:
		if sys.argv[1]:
			select_mode=sys.argv[1]
	except:
		select_mode=None
		#其他在测试时直接定义
	#实例化当前模组
	entry=module_set[select_mode]()
	# entry=module_set_inject[select_mode]()
	#执行本次的脚本入口
	entry.main()


def main():
	switch()




if __name__=='__main__':
	main()
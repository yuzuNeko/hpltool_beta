


"""将我曾经使用过的类型，文件都转换为可以操作的，熟悉的python数据结构

"""
def convert_dict(obj,obj_type=None,interface=None):
	"""将一切可能的类型，转换为字典
	"""
	if obj_type==None:
		print('没有指定类型')
		return 
import numpy as np


class hplnumpy:


	def arithmetic(self,startpoint=1,endpoint=100,step=1):
		ap=np.linspace(startpoint,endpoint,num=int(endpoint/step))
		return ap
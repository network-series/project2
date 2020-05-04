import zipfile
import os
def zipDir(dirpath, outFullName):

	#压缩指定文件夹
	#:param dirpath: 目标文件夹路径
	#:param outFullName:  压缩文件保存路径+XXXX.zip
	#:return: 无
	zip = zipfile.ZipFile(outFullName, 'w', zipfile.ZIP_DEFLATED)
	for path, dirnames, filenames in os.walk(dirpath):
		#去掉目标和路径，只对目标文件夹下边的文件及文件夹进行压缩（包括父文件夹本身）
		this_path = os.path.abspath('.')
		fpath = path.replace(this_path, '')
		for filename in filenames:
			zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
	zip.close()
	'''
	项目二的压缩算法主要参考了以上代码
	'''

import zipfile  
z =zipfile.ZipFile(filename, 'r') 
# 这里的第二个参数用r表示是读取zip文件，w是创建一个zip文件  
for f in z.namelist(): 
print f

import zipfile, os  
 z = zipfile.ZipFile(filename, 'w') 
# 注意这里的第二个参数是w，这里的filename是压缩包的名字

import zipfile, os  
 z = zipfile.ZipFile(filename, 'w') 
# 注意这里的第二个参数是w，这里的filename是压缩包的名字
	'''
	以上代码用于熟悉zipfile的用法
	'''

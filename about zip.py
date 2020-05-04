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
	项目二使用的压缩算法主要参考了以上代码
	'''

import zipfile  
z =zipfile.ZipFile(filename, 'r') 
# 这里的第二个参数用r表示是读取zip文件
for f in z.namelist(): 
print f

import zipfile 
import os  
 z = zipfile.ZipFile(filename, 'w') 
# 注意这里的第二个参数是w，这里的filename是压缩包的名字

import zipfile
# zipfile压缩
z = zipfile.ZipFile('ss.zip', 'w', zipfile.ZIP_STORED) #打包，zipfile.ZIP_STORED是默认参数
# z = zipfile.ZipFile('ss.zip', 'w', zipfile.ZIP_DEFLATED) #压缩
z.write('ss2')
z.write('ss1')
z.close()
#zipfile解压
z = zipfile.ZipFile('ss.zip', 'r')
z.extractall(path=r"C:\Users\Administrator\Desktop")
z.close()

#zip压缩模块
import zipfile
import os

def Compress(dirs, path):
    kZip = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)
    for dir in dirs:
        for dirpath, dirnames, filenames in os.walk(dir):
            for file in filenames:
                kZip.write(os.path.join(dirpath,file))    #绝对路径
    kZip.close()
    print('compress finished')
	'''
	以上代码在csdn和博客园找到，用于熟悉zipfile的用法
	'''

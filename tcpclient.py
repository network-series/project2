import socket
import struct
import pickle
import time
import os
import zipfile
import sys

file_dir = os.path.dirname(os.path.abspath(__file__))
header_struct = struct.Struct('i1024s')
data_struct = struct.Struct('1024s')


def print_file(header):
    file_size = header['file_size']
    file_ctime = header['file_ctime']
    file_atime = header['file_atime']
    file_mtime = header['file_mtime']
    print('文件大小：%s' % file_size)
    print('文件创建时间：%s' % time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(file_ctime)))
    print('文件最近访问时间：%s' % time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(file_atime)))
    print('文件最近修改时间：%s' % time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(file_mtime)))


def send(file_name, client):
    file_path = os.path.join(file_dir, file_name)
    if os.path.isfile(file_path) == 0:
        client.send(header_struct.pack(*(0, b'0')))
    else:
        # 文件头
        header = {
            'file_name': file_name,
            'file_size': os.path.getsize(file_path),
            'file_ctime': os.path.getctime(file_path),
            'file_atime': os.path.getatime(file_path),
            'file_mtime': os.path.getmtime(file_path)
        }
        file_size = header['file_size']
        if file_size == 0:
            return False
        else:
            # 序列化header
            header_str = pickle.dumps(header)
            # 把序列化的header长度和header正文打包发送
            client.send(header_struct.pack(*(len(header_str), header_str)))
            print_file(header)
            with open(file_path, 'rb') as f:
                for line in f:
                    client.send(line)
            return True


def zipDir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


def run(file_name, server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    while True:
        # file_name = input("你想传输的文件叫什么名字呢[输入end断开连接]: ").strip()
        if file_name == 'end':
            break
        zipDir(file_name, file_name + '.zip')
        # client.send(file_name.encode('utf-8'))
        start = time.time()
        print('-' * 80)
        file = file_name + '.zip'
        if not send(file_name, client):
            print('文件名错误')
        else:
            end = time.time()
            print('\n传输完成')
            print('传输时间：', end - start)
        print('-' * 80)
        os.remove(file_name + '.zip')
        break
    client.close()


if __name__ == '__main__':
    run(sys.argv[1],sys.argv[2],int(sys.argv[3]))

import socket
import struct
import pickle
import time
import os
import zipfile
import sys

# file_dir = os.path.dirname(os.path.abspath(__file__))
header_struct = struct.Struct('i1024s')
data_struct = struct.Struct('1024s')


def print_progress(percent, width=50):
    if percent >= 100:
        percent = 100
    # 字符串拼接的嵌套使用
    show_str = ('[%%-%ds]' % width) % (int(width * percent / 100) * '>')
    print('\r%s %d%%' % (show_str, percent), end='')


def get(file_dir, client):
    # 接受序列化的header数据包
    packed_header = client.recv(1024 + 4)
    # 解包得到序列化的header的长度和header正文
    header_size, header_s = header_struct.unpack(packed_header)
    # 反序列化得到header正文
    header = pickle.loads(header_s)
    file_name = header['file_name']
    file_size = header['file_size']
    folder_path, name = os.path.split(file_name)
    with open('%s\\%s' % (file_dir, name), 'wb') as f:
        recv_size = 0
        while recv_size < file_size:
            res = client.recv(1024)
            f.write(res)
            recv_size += len(res)
            recv_per = int(recv_size / file_size * 100)
            print_progress(recv_per)
    return name


def unzip_file(zip_src, dst_dir):
    zipfile.is_zipfile(zip_src)
    fz = zipfile.ZipFile(zip_src, 'r')

    for file in fz.namelist():
        fz.extract(file, dst_dir)


def run(path, server_ip, server_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    print('Server start on')
    print('-> ip: %s port: %d' % (server_ip, server_port))
    while True:
        client, client_addr = server.accept()
        print('A new connection from %s' % client_addr[0])
        while True:
            try:
                # print('Send %s to %s' % (request, client_addr[0]))
                name = get(path, client)
                unzip_file(path+'\\'+name, path)
                os.remove(path+'\\'+name)
            except ConnectionResetError:
                break
        client.close()
    server.close()


if __name__ == '__main__':
    run(sys.argv[1],sys.argv[2],int(sys.argv[3]))

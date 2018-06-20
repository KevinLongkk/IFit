###########################################################################
#*- 				 													-*#
#*- 	coding		: UTF-8 											-*#
#*-		function	: as a servicer to send and receiver file	 		-*#
#*- 	localhost	: 192.168.1.8 										-*#
#*- 	port		: 4518 												-*#
#*-		author		: pwn_w							 					-*#
#*-			 															-*#
###########################################################################

import socket,time,socketserver,struct,os,_thread

host='192.168.1.8'
port=4518
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 		#定义socket类型
s.bind((host,port))										#绑定需要监听的Ip和端口号，tuple格式
s.listen(1)


#--------------------------------接收文件---------------------------------#
def receiverFile(connection,address):				
        try:
            filename = str(conn.recv(1024),encoding="utf8")
            print('Get filename',filename)
            conn.sendall(bytes(filename,encoding="utf8"))
            connection.settimeout(600)
            fileinfo_size=struct.calcsize('128sl') 
            buf = connection.recv(fileinfo_size)
            if buf:
                filename,filesize =struct.unpack('128sl',buf) 
                filename=filename.decode('utf-8')
                filename_f = filename.strip('\00')
                filenewname = os.path.join('/home/pwn_w/',(filename_f))
                print ('file new name is %s, filesize is %s' %(filenewname,filesize))	

                recvd_size = 0 #定义接收了的文件大小
                file = open(filenewname,'wb')
	
                print ('start receiving...')
                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        rdata = connection.recv(1024)
                        recvd_size += len(rdata)
                    else:
                        rdata = connection.recv(filesize - recvd_size) 
                        recvd_size = filesize
                    file.write(rdata)
                file.close()
                print ('receive done')
        except socket.timeout:
            connection.close()		
#-------------------------------------------------------------------------#


#--------------------------------发送文件---------------------------------#
def sendFile(connection,address):
    filepath = str(conn.recv(1024),encoding="utf8")
    print('Get filename',filepath)
    if os.path.isfile(filepath):
        fileinfo_size=struct.calcsize('128sl') #定义打包规则

        #定义文件头信息，包含文件名和文件大小
        fhead = struct.pack('128sl',os.path.basename(filepath).encode('utf-8'),os.stat(filepath).st_size)
        connection.send(fhead) 
        print ('client filepath: ',filepath)
        fo = open(filepath,'rb')
        while True:
            filedata = fo.read(1024)
            if not filedata:
                break
            connection.send(filedata)
        fo.close()
        print ('send over...')
        #s.close()
    else:
        print ('no such file')

#-------------------------------------------------------------------------#



#--------------------------------浏览文件---------------------------------#

def scanFile(connection,address):
    filepath = str(conn.recv(1024),encoding="utf8")
    result = []
    for maindir,subdir,file_name_list in os.walk(filepath):
        for filename in file_name_list:
            apath = os.path.join(maindir,filename)
            result.append(apath)
        connection.sendall(bytes(str(result),encoding="utf8"))

#-------------------------------------------------------------------------#


#--------------------------------执行函数---------------------------------#

def work():
    mode = str(conn.recv(1024),encoding="utf8")			#获取工作模式
    if (mode=='D'):										#进入发送函数
        sendFile(conn,addr)
    elif(mode=='U'):									#进入接收函数
        receiverFile(conn,addr)
    elif(mode=='S'):
        scanFile(conn,addr)	
    elif(mode=='Q'):									#退出
        exit(0)
    else:												#输入其他则提示重新输入
        print('Get an invalid value, waiting next data...')    

#-------------------------------------------------------------------------#




while True:
    conn,addr = s.accept()									#创建套接字
    print('Connected by ',addr)								#打印套接字信息
    while True:
        work()												
    conn.close()	

###########################################################################
#*- 									-*#
#*- 	coding		: UTF-8 					-*#
#*-	function	: as a client to send and receiver file 	-*#
#*- 	connectHost	: 192.168.1.8 					-*#
#*- 	connectPort	: 4518 						-*#
#*-	author		: pwn_w						-*#
#*-			 						-*#
###########################################################################

import os,struct
from socket import *
s = socket(AF_INET,SOCK_STREAM)							#定义socket类型
s.connect(('192.168.1.8',4518))							#创建连接

#--------------------------------发送文件---------------------------------#
def sendFile():															
    filepath = input('Input the video you want to send:\r\n')
    s.sendall(bytes(filepath,encoding="utf8"))
    filepath = str(s.recv(1024), encoding="utf8")
    if os.path.isfile(filepath):
        fileinfo_size=struct.calcsize('128sl') 
        fhead = struct.pack('128sl',os.path.basename(filepath).encode('utf-8'),os.stat(filepath).st_size)
        s.send(fhead) 
        print ('client filepath: ',filepath)
        fo = open(filepath,'rb')
        while True:
            filedata = fo.read(1024)
            if not filedata:
                break
            s.send(filedata)
        fo.close()
        print ('send over...')
    else:
        print ('no such file')
#-------------------------------------------------------------------------#

#--------------------------------接收文件---------------------------------#
def receiverFile():
        try:
            filename = input('Which file you want to download:\r\n')		#输入要下载的文件
            s.sendall(bytes(filename,encoding="utf8"))
            s.settimeout(600)
            fileinfo_size=struct.calcsize('128sl')							#打包规则
            buf = s.recv(fileinfo_size)
            if buf:
                filename,filesize =struct.unpack('128sl',buf) 
                filename=filename.decode('utf-8')
                filename_f = filename.strip('\00')
                filenewname = os.path.join('/home/aston/',(filename_f))
                print ('file new name is %s, filesize is %s' %(filenewname,filesize))	

                recvd_size = 0 #定义接收了的文件大小
                file = open(filenewname,'wb')
	
                print ('stat receiving...')
                while not recvd_size == filesize:
                    if filesize - recvd_size > 1024:
                        rdata = s.recv(1024)
                        recvd_size += len(rdata)
                    else:
                        rdata = s.recv(filesize - recvd_size) 
                        recvd_size = filesize
                    file.write(rdata)
                file.close()
                print ('receive done')
        except socket.timeout:
                print('timeout')
#-------------------------------------------------------------------------#



#--------------------------------浏览文件---------------------------------#

def scanFile():
    directory = input('Which directory you want to scan:\r\n')	#发送要浏览的目录
    s.sendall(bytes(directory,encoding="utf8"))	
    acceptFile = str(s.recv(1024),encoding = "utf8")
    print("".join(("List:",acceptFile)))

#-------------------------------------------------------------------------#



	
#--------------------------------执行函数---------------------------------#

def work():
    Mode = input('Upload(U)、Download(D)、Scan(S) or Quit(Q):\r\n')	#输入工作模式
    s.sendall(bytes(Mode,encoding="utf8"))							#发送至工作模式至服务器
	
    if  (Mode=='D'):												#下载文件
        receiverFile()
		
    elif(Mode=='U'):												#上传文件
        sendFile()
		
    elif(Mode=='S'):												#浏览目录文件
        scanFile()
		
    elif(Mode=='Q'):												#退出服务器
        exit(0)
		
    else:															#提示输入错误工作模式
        print('Invalid value, please input again...')


#-------------------------------------------------------------------------#

				
while True:		
    work()
s.close()


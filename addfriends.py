import os
import sys
import time
import datetime
import subprocess
from auto_adb import auto_adb
import random
import numpy as np
import pandas as pd
from aip import AipOcr
import threading
import re
adb=auto_adb()

APP_ID='15328030'
API_KEY='zeG5KrZDZwXrv32VQtZSQlSu'
SECRET_KEY='zv2AdRGKGnKBE5pFCIFvr7ilyhrAqU7Q'
client=AipOcr(APP_ID,API_KEY,SECRET_KEY)

def Read(device_name):
	pass

#读取连接的手机的序列号，开启多线程
out=os.popen("adb devices").read()
device_list=re.sub('\tdevice','',out[25:]).strip().split('\n')
print(device_list)
for device in device_list:
	if device:
		threading.Thread(target=Read,args=(device,)).start()

#截图操作
class ScreenShot():
	def Screen(self,cmd):
		screenExecute=subprocess.Popen(str(cmd),stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
		stdout, stderr = screenExecute.communicate()
		stdout = stdout.decode("utf-8")
		stderr = stderr.decode("utf-8")
		
	def SaveComputer(self,cmd):
		screenExecute = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
		stdout, stderr = screenExecute.communicate()
		stdout = stdout.decode("utf-8")
		stderr = stderr.decode("utf-8")
#点击手机的坐标
def Change_Position(x,y):
	cmd='shell input tap {0} {1}'.format(x,y)
	print(cmd)
	adb.run(cmd)

def Get_File_Content(FilePath):
	with open(FilePath,'rb') as fp:
		return fp.read()

#对截图进行OCR识别
def Get_Image_Text():
	with open('screenshot.png','rb') as fp:
		image=fp.read()
	result=client.basicGeneral(image)
	return result
	
def Input_Mobile(Mobile):
	cmd='-s 0cd6bd760c3e shell am broadcast -a ADB_INPUT_TEXT --es msg {0}'.format(Mobile)
	adb.run(cmd)
	print('Mobile:'+Mobile)

#填写验证申请	
def Input_Verify_Inf(LastName):
	LastName=LastName+'总，朋友介绍，找您档案项目合作'
	cmd='shell am broadcast -a ADB_INPUT_TEXT --es msg {0}'.format(LastName)
	adb.run(cmd)
	print('LastName')

#填写备注	
def Input_Remark_Inf(Name):
	cmd='shell am broadcast -a ADB_INPUT_TEXT --es msg {0}'.format(Name)
	adb.run(cmd)
	print('Name')

#执行添加好友操作,坐标需根据不同手机自行调整
def Add_Friend(Mobile,Name,LastName):
	print('Adding.............')
	Change_Position(983,157)
	time.sleep(random.randint(2,5))
	Change_Position(751,442)
	time.sleep(random.randint(2,5))
	Change_Position(313,361)
	time.sleep(random.randint(2,5))
	print('Searching mobile number:{0}'.format(Mobile))
	Input_Mobile(Mobile)
	time.sleep(random.randint(2,5))
	Change_Position(340,320)
	time.sleep(random.randint(2,5))
	Cmd_Push='adb shell /system/bin/screencap -p /sdcard/screenshot.png' 
	Cmd_Pull='adb pull /sdcard/screenshot.png'
	screen=ScreenShot()
	screen.Screen(Cmd_Push)
	screen.SaveComputer(Cmd_Pull)
	ResultWord=Get_Image_Text()['words_result']
	
	Word=ResultWord[-3]['words']
	if Word=='该用户不存在':
		print('---该用户不存在---')
		Change_Position(36,150)
		time.sleep(random.randint(0,1))
		Change_Position(36,150)
		time.sleep(random.randint(0,1))
		return Word
	
	Word=ResultWord[-2]['words']
	if Word=='发消息':
		print("---该用户已添加---")
		Change_Position(36, 150)
		time.sleep(random.randint(0, 1))
		Change_Position(36, 150)
		time.sleep(random.randint(0, 1))
		Change_Position(36, 150)
		time.sleep(random.randint(0, 1))	
		return '该用户已添加'
		
	Word=ResultWord[-1]['words']
	if Word=='添加到通讯录':
		print('---发送添加消息---')
		Change_Position(535,1025)
		time.sleep(random.randint(2,5))
		Change_Position(538,922)
		time.sleep(random.randint(2, 5))
		Change_Position(986, 1218)
		time.sleep(random.randint(2, 5))
		Change_Position(540,380)
		time.sleep(random.randint(2,5))
		Change_Position(977,393)
		Input_Verify_Inf(LastName)
		Change_Position(510,711)
		time.sleep(random.randint(2,5))
		Change_Position(975,709)
		time.sleep(random.randint(2,5))
		Input_Remark_Inf(Name)
		Change_Position(967,150)
		time.sleep(random.randint(2,5))
		print('发送成功')
		Change_Position(36, 150)
		time.sleep(random.randint(0, 1))
		Change_Position(36, 150)
		time.sleep(random.randint(0, 1))
		Change_Position(36, 150)
		time.sleep(random.randint(0, 1))
		Change_Position(36, 150)
		return '发送成功'
		
	word=ResultWord[-3]['words']
	print("---添加失败,失败原因："+word+"---")
	Change_Position(36, 150)
	time.sleep(random.randint(0, 1))
	Change_Position(36, 150)
	time.sleep(random.randint(0, 1))
	Change_Position(36, 150)
	return 'Failed'
	
if __name__=='__main__':
	List_Name=[]
	List_Number=[]
	#读取需要添加的手机号和名字
	file_name=open('name.txt')
	file_number=open('number.txt')
	#
	while True:
		namestr=file_name.readline()
		if not namestr:
			break
		List_Name.append(namestr)
	while True:
		numberstr=file_number.readline()
		if not numberstr:
			break
		List_Number.append(numberstr)
	Num=0
	while True:
		file_count=open('count.txt')				#直接打开一个文件，如果文件不存在则创建文件，count.txt内容：0
		count=file_count.read()
		file_count.close()
		now=datetime.datetime.now()
		#每天早上9-晚上8点之间执行操作
		if now.hour>=9 and Num<20:
			Count=int(count)
			Name=List_Name[Count]
			Number=List_Number[Count]
			LastName=Name[0]
			inf=Add_Friend(Number,Name,LastName)
			if inf=='发送成功':
				Num=Num+1
			Count=Count+1					#记录添加个数，防止操作意外停止，可读取当前数继续添加
			file_count=open('count.txt','w+')
			file_count.write(str(Count))
			file_count.close()
			
			timestr=time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
			#记录添加过的信息
			file_info=open('info.txt','a')
			file_info.write(Number+Name+inf+"\n"+timestr+"\n"+"-------------------"+"\n")
			file_info.close()
			#休眠20分钟，防止操作频繁微信后台拒绝添加
			time.sleep(1200)
		else:
			break
			

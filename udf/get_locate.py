#!/usr/bin/env python
# -*- coding:utf8 -*-
from deepdive import *
import re
import handle_string
system = ["mục","Mục","chương","Chương","điều","Điều","khoản","Khoản","phần","Phần"]
def info_locate(string):
	result = []
	lenght = 0
	if(string.find("Sửa đổi, bổ sung các")):
		result.append("Sửa đổi, bổ sung các")
		locate = len(string)-21
		result.append(string[locate:(len(string)-1)])
	elif(string.find("Sửa đổi, bổ sung")):
		result.append("Sửa đổi, bổ sung")
		locate = len(string)-17
		result.append(string[locate:(len(string)-1)])
	elif(string.find("Bổ sung các")):
		result.append("Bổ sung các")
		locate = len(string)-11
		result.append(string[locate:len(string)-1])
	elif(string.find("Bổ sung")):
		result.append("Bổ sung")
		locate = len(string)-7
		result.append(string[locate:len(string)-1])
	elif(string.find("Sửa đổi các")):
		result.append("Sửa đổi các")
		locate = len(string)-11
		result.append(string[locate:len(string)-1])
	elif(string.find("Sửa đổi")):
		result.append("Sửa đổi")
		locate = len(string)-7
		result.append(string[locate:len(string)-1])
	

	elif(string.find("sửa đổi, bổ sung")):
		result.append("sửa đổi, bổ sung")
		locate = len(string)-17
		result.append(string[0:(locate-1)])
	elif(string.find("bổ sung")):
		result.append("bổ sung")
		locate = len(string)-7
		result.append(string[0:(locate-1)])
	elif(string.find("sửa đổi")):
		result.append("sửa đổi")
		locate = len(string)-7
		result.append(string[0:(locate-1)])
#return locate
def locate(list[]):
	data = list[1].split(" ")
	if(list[0]=="Sửa đổi, bổ sung các"):
		if(system[9]in data || system[8] in data ):
			
			if(string.find("Điều") || string.find("điều")):
				locate +=100











# -*- coding:utf8 -*-

import re


#chia doan van thanh list cac text dua tren cac chi so bat dau cua cac doan trong array
def split(string,array):
	result = []
	for i in range(0,len(array)) :
		if(i != (len(array)-1)) :
			result.append(string[array[i]:array[i+1]])
		else:
			result.append(string[array[i]:(len(string)-1)])
	return result	
#sua lai gia tri bat dau cho cac index trong array
def check(string,array):
	for i in range(0,len(array)) :
		if(string[(array[i]-2):array[i]] == "**"):
			array[i] = array[i]-2
	return array
#check xem trong dong chua tu do co in dam hay ko (**xxx**)
def reFind(string,array):
	for i in range(0,len(array)):
		count = 0;
		tempInt = array[i] - 2
		tempC = string[tempInt]
		while tempC != '\n':
			if (tempC == '*'):
				count += 1
			tempInt += 1
			tempC = string[tempInt]
		if count < 2 :
			del array[i]
	return array
#do dai cua list
def lenIterator(list):
	sum = 0
	for i in list :
		sum += 1
	return sum
def itemInQuote(string, index) :
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	for i in quotes :
		if index >= i.span()[0] and index < i.span()[1] :
			return True
	return False
#Chia theo phan
def divPart(string):
	limitText = len(string)
	partIndex = []
	it = re.finditer(r"(\n\*\*Phần thứ\s)", string)
	sum = 0
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	sumQoutes = lenIterator(quotes)
	if lenIterator(it) > 0 :
		it = re.finditer(r"(\n\*\*Phần thứ\s)", string)
		for match in it:
			if sumQoutes > 0 :
				if itemInQuote(string, match.span()[0]) == False :
					partIndex.append(match.span()[0]+2)
			else :
				partIndex.append(match.span()[0]+2)
		sum = len(partIndex)
	if sum > 0 :
		result = {
			"totalPart": len(partIndex),
			"parts" : ""
		}
		listParts = []
		for i in range(0,len(partIndex)):
			if i!=(len(partIndex)-1):
				part = {
					"start":partIndex[i],
					"end": (partIndex[i+1]),
					"totalChap": "",
					"chaps": ""
				}
				res = divChapter(string[partIndex[i]:partIndex[i+1]],partIndex[i])
				part['chaps'] = res[0]
				part['totalChap'] = res[1]
				listParts.append(part)
			else :
				part = {
					"start":partIndex[i],
					"end": limitText,
					"totalChap": "",
					"chaps": ""
				}
				res = divChapter(string[partIndex[i]:limitText],partIndex[i])
				part['chaps'] = res[0]
				part['totalChap'] = res[1]
				listParts.append(part)
		result['[parts'] = listParts
	else :
		result = {
			"totalPart": 0,
			"parts" : ""
		}
		listParts = []
		part = {
					"start": 0,
					"end": len(string),
					"totalChap": "",
					"chaps": ""
				}
		res = divChapter(string,0)
		part['chaps'] = res[0]
		part['totalChap'] = res[1]
		listParts.append(part)
	result['parts'] = listParts
	return result

#Chia theo chuong
def divChapter(string, startIndex) :
	it = re.finditer(r"(\*\*(\_|)*(Chương|CHƯƠNG)\s(\w|[0-9])+(\:|\s|\.|\_|)*)", string)
	chapterIndex = [] #chuoi cac index bat dau cua cac chapter
	listChaps = []
	sum =  0
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	sumQoutes = lenIterator(quotes)
	a = lenIterator(it)
	if  a >0:
		it = re.finditer(r"\*\*(\_|)*(Chương|CHƯƠNG)\s(\w|[0-9])+(\:|\s|\.|\_|)*", string)
		for match in it:
			if sumQoutes > 0 :
				if itemInQuote(string, match.span()[0]) == False :
					chapterIndex.append(match.span()[0])
			else :
				chapterIndex.append(match.span()[0])
		sum = len(chapterIndex)
	if sum > 0 :
		for match in it:
		    chapterIndex.append(match.span()[0])
		for j in range(0,len(chapterIndex)):
			if j!=(len(chapterIndex)-1):
				chap = {
					"start":(chapterIndex[j]+startIndex),
					"end": (chapterIndex[j+1]+startIndex),
					"totalSec": "",
					"secs": ""
				}
				res = divSection(string[chapterIndex[j]:chapterIndex[j+1]],chapterIndex[j]+startIndex)
				chap['secs'] = res[0]
				chap['totalSec'] = res[1]
				listChaps.append(chap)
			else :
				chap = {
					"start":chapterIndex[j]+startIndex,
					"end": len(string)+startIndex,
					"totalSec": "",
					"secs": ""
				}
				res = divSection(string[chapterIndex[j]:len(string)],chapterIndex[j]+startIndex)
				chap['secs'] = res[0]
				chap['totalSec'] = res[1]
				listChaps.append(chap)
	else :
		chap = {
					"start": startIndex ,
					"end": startIndex+len(string),
					"totalSec": "",
					"secs": ""
				}
		res = divSection(string,startIndex)
		chap['secs'] = res[0]
		chap['totalSec'] = res[1]
		listChaps.append(chap)
	resultlist = []
	resultlist.append(listChaps)
	resultlist.append(sum)
	return resultlist	

#Chia theo muc
def divSection(string, startIndex):
	it = re.finditer(r"(\*\*(\_|)*(Mục|MỤC)\s(\w|[0-9])+(\_|\.|\s)*)", string)
	sectionIndex = []
	listSecs = []
	sum = 0
	a = lenIterator(it)
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	sumQoutes = lenIterator(quotes)
	if a>0:
		it = re.finditer(r"(\*\*(\_|)*(Mục|MỤC)\s(\w|[0-9])+(\_|\.|\s)*)", string)
		for match in it:
			if sumQoutes > 0:
				if itemInQuote(string, match.span()[0]) == False :
					sectionIndex.append(match.span()[0])
			else:
				sectionIndex.append(match.span()[0])
		sum = lenIterator(sectionIndex)
	if sum > 0 :
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex),
					"end": (sectionIndex[j+1]+startIndex),
					"totalLaw": "",
					"laws": ""
				}
				res = divLaw(string[sectionIndex[j]:sectionIndex[j+1]],sectionIndex[j]+startIndex)
				sec['laws'] = res[0]
				sec['totalLaw'] = res[1]
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex,
					"end": len(string) +startIndex,
					"totalLaw": "",
					"laws": ""
				}
				res = divLaw(string[sectionIndex[j]:len(string)],sectionIndex[j]+startIndex)
				sec['laws'] = res[0]
				sec['totalLaw'] = res[1]
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"totalLaw": "",
					"laws": ""
				}
		res = divLaw(string,startIndex)
		sec['laws'] = res[0]
		sec['totalLaw'] = res[1]
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(sum)
	return resultlist

#chia theo dieu
#dont need change name variable
def divLaw(string,startIndex):
	it = re.finditer(r"((\\n\s*(\*\*\s*)*)|(\*\*\s*)){1}Điều [0-9]+\w*", string)
	sectionIndex = []
	listSecs = []
	sum = 0
	a = lenIterator(it)
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	sumQoutes = lenIterator(quotes)
	if a>0:
		it = re.finditer(r"((\\n\s*(\*\*\s*)*)|(\*\*\s*)){1}Điều [0-9]+\w*", string)
		for match in it:
			if sumQoutes > 0 :
				if itemInQuote(string, match.span()[0]) == False :
					sectionIndex.append(match.span()[0]+2)
			else :
				sectionIndex.append(match.span()[0]+2)
		sum = len(sectionIndex)
	if sum > 0 :
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex),
					"end": (sectionIndex[j+1]+startIndex),
					"totalItem": "",
					"items":"",
					"name": ""
				}
				findName = re.finditer(r"Điều [0-9]+\w*",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"Điều [0-9]+\w*",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				res = divItem(string[sectionIndex[j]:sectionIndex[j+1]],sectionIndex[j]+startIndex)
				sec['items'] = res[0]
				sec['totalItem'] = res[1]
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex,
					"end": len(string) +startIndex,
					"totalItem": "",
					"items":"",
					"name":""
				}
				findName = re.finditer(r"Điều [0-9]+\w*",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"Điều [0-9]+\w*",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				res = divItem(string[sectionIndex[j]:len(string)],sectionIndex[j]+startIndex)
				sec['items'] = res[0]
				sec['totalItem'] = res[1]
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"totalItem": "",
					"items":"",
					"name": ""
				}
		res = divItem(string,startIndex)
		sec['items'] = res[0]
		sec['totalItem'] = res[1]
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(sum)
	return resultlist

def divItem(string,startIndex) :
	it = re.finditer(r"\\n(\s|\*|\_)*[0-9]+", string)
	sectionIndex = []
	listSecs = []
	sum = 0
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	sumQoutes = lenIterator(quotes)
	a = lenIterator(it)

	if a>0:
		it = re.finditer(r"\\n(\s|\*|\_)*[0-9]+", string)
		for match in it:
			if sumQoutes > 0 :
				if itemInQuote(string, match.span()[0]) == False :
					sectionIndex.append(match.span()[0])
			else :
				sectionIndex.append(match.span()[0])
		sum = len(sectionIndex)
	if sum > 0 :
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex)+2,
					"end": (sectionIndex[j+1]+startIndex)+2,
					"name": "",
					"totalPoint": "",
					"points": ""
				}
				findName = re.finditer(r"[0-9]+",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"[0-9]+",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				res = divPoint(string[sectionIndex[j]:sectionIndex[j+1]],sectionIndex[j]+startIndex)
				sec['points'] = res[0]
				sec['totalPoint'] = res[1]
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex+2,
					"end": len(string) + startIndex,
					"name": "",
					"totalPoint": "",
					"points": ""
				}
				findName = re.finditer(r"[0-9]+",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"[0-9]+",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				res = divPoint(string[sectionIndex[j]:len(string)],sectionIndex[j]+startIndex)
				sec['points'] = res[0]
				sec['totalPoint'] = res[1]
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"name": "",
					"totalPoint": "0",
					"points": ""
				}
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(sum)
	return resultlist
def divPoint(string,startIndex) :
	it = re.finditer(r"\\n(\s|\*|\_)*(\w|đ)+\)", string)
	sectionIndex = []
	listSecs = []
	sum = 0
	quotes = re.finditer(r"\\n(\s|\*|\_)*(\"|\“)([^\"\“]|\–|\’)*(\"|\”)(\.)*(?=\\n)", string)
	sumQoutes = lenIterator(quotes)
	a = lenIterator(it)

	if a>0:
		it = re.finditer(r"\\n(\s|\*|\_)*(\w|đ)+\)", string)
		for match in it:
			if sumQoutes > 0 :
				if itemInQuote(string, match.span()[0]) == False :
					sectionIndex.append(match.span()[0])
			else :
				sectionIndex.append(match.span()[0])
		sum = len(sectionIndex)
	if sum > 0 :
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex)+2,
					"end": (sectionIndex[j+1]+startIndex),
					"name": ""
				}
				findName = re.finditer(r"\\n(\w|đ)+",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"\\n(\w|đ)+",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]+2:sectionIndex[j]+fN.span()[1]]
						break
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex+2,
					"end": len(string) +startIndex,
					"name":""
				}
				findName = re.finditer(r"\\n(\w|đ)+",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"\\n(\w|đ)+",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]+2:sectionIndex[j]+fN.span()[1]]
						break
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"name": ""
				}
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(sum)
	return resultlist

def getHeader(content) :
	result = divPart(content)
	id_firstPart = result['parts'][0]['start']
	id_firstChapter = result['parts'][0]['chaps'][0]['start']
	id_firstSec = result['parts'][0]['chaps'][0]['secs'][0]['start']
	id_firstLaw = result['parts'][0]['chaps'][0]['secs'][0]['laws'][0]['start']
	alist = []
	if id_firstPart > 0 :
		alist.append(id_firstPart)
	if id_firstChapter > 0 :
		alist.append(id_firstChapter)
	if id_firstSec > 0	:
		alist.append(id_firstSec)
	if id_firstLaw > 0 :
		alist.append(id_firstLaw)
	if not alist:
		return len(content)
	return min(alist)

def getTotalPart(result) :
	return result['totalPart']

def getTotalChapter(result, indexPart) :
	return result['parts'][indexPart]['totalChap']

def getTotalSection(result, indexPart, indexChapter) :
	return result['parts'][indexPart]['chaps'][indexChapter]['totalSec']

def getTotalLaw(result,indexPart,indexChapter,indexSec) :
	return result['parts'][indexPart]['chaps'][indexChapter]['secs'][indexSec]['totalLaw']

def getTotalItem(result,indexPart,indexChapter,indexSec,indexLaw) :
	return result['parts'][indexPart]['chaps'][indexChapter]['secs'][indexSec]['laws'][indexLaw]['totalItem']

def getPart(result,index):
	return result['parts'][index]

def getChapter(result,indexPart,index):
	return result['parts'][indexPart]['chaps'][index]

def getSection(result, indexPart, indexChapter, index):
	return result['parts'][indexPart]['chaps'][indexChapter]['secs'][index]

def getLaw(result, indexPart, indexChapter, indexSec, index):
	return result['parts'][indexPart]['chaps'][indexChapter]['secs'][indexSec]['laws'][index]

def getItem(result, indexPart, indexChapter, indexSec, indexLaw, index):
	return result['parts'][indexPart]['chaps'][indexChapter]['secs'][indexSec]['laws'][indexLaw]['items'][index]

#problem with iterator -> generator
#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import divlaw
import handle_string

def getFirst(o):
	a = None
	for i in o:
		a = i
		break
	return a
def rewriteString(string):
	numberft = re.finditer(r"((\,\s)|(và\s))((\d+[a-zđ]{0,1})|([a-zđ]{1}))(?=(\s|\,|\.|\;))",string, re.U)
	a = divlaw.lenIterator(numberft)
	####################################
	while a > 0:
		numberft = re.finditer(r"((\,\s)|(và\s))((\d+[a-zđ]{0,1})|([a-zđ]{1}))(?=(\s|\,|\.|\;))",string, re.U)
		i = getFirst(numberft)
		startIndex = i.start()
		cutIndex = 0
		if string[startIndex] == ',' :
			cutIndex = startIndex + 2
			startIndex -= 1
		else :
			cutIndex = startIndex + 4
			startIndex -=2
		lastW = startIndex
		firstW = 0
		findLast = True
		while startIndex > 0:
			if string[startIndex] == ' ':
				if findLast :
					findLast = False
					lastW = startIndex
				else :
					firstW = startIndex + 1
					break
			startIndex -= 1
		string = string[:cutIndex] + string[firstW:lastW] + ' ' + string[cutIndex:]
		numberft = re.finditer(r"((\,\s)|(và\s))((\d+[a-zđ]{0,1})|([a-zđ]{1}))(?=(\s|\,|\.|\;))",string, re.U)
		a = divlaw.lenIterator(numberft)
	return writeDetail(string)
def writeDetail(string):
	numberft = re.finditer(r"điểm\s[a-zđ]{1}(?!\skhoản)",string, re.U)
	if divlaw.lenIterator(numberft) > 0:
		numberft = re.finditer(r"điểm\s[a-zđ]{1}(?!\skhoản)",string, re.U)
		addLen = 0
		for i in numberft:
			findItem = re.finditer(r"khoản\s\d+[a-zđ]?",string[i.end()+addLen:len(string)],re.U)
			if divlaw.lenIterator(findItem) > 0:
				findItem = re.finditer(r"khoản\s\d+[a-zđ]?",string[i.end()+addLen:len(string)],re.U)
				j = getFirst(findItem)
				if ' đ' in string[i.start():i.end()+1]:
					string = string[:i.end()+addLen+1] + " " + string[i.end()+j.start()+addLen:i.end()+j.end()+addLen] + string[1+i.end()+addLen:]
				else :
					string = string[:i.end()+addLen] + " " + string[i.end()+j.start()+addLen:i.end()+j.end()+addLen] + string[i.end()+addLen:]
				addLen += j.end() - j.start() + 1
			else :
				break
	numberft = re.finditer(r"khoản\s\d+[a-zđ]?(?!\sđiều)",string, re.U)
	if divlaw.lenIterator(numberft) > 0:
		numberft = re.finditer(r"khoản\s\d+[a-zđ]?(?!\sđiều)",string, re.U)
		addLen = 0
		for i in numberft:
			findItem = re.finditer(r"điều\s\d+[a-zđ]?",string[i.end()+addLen:len(string)],re.U)
			if divlaw.lenIterator(findItem) > 0:
				findItem = re.finditer(r"điều\s\d+[a-zđ]?",string[i.end()+addLen:len(string)],re.U)
				j = getFirst(findItem)
				string = string[:i.end()+addLen] + " " + string[i.end()+j.start()+addLen:i.end()+j.end()+addLen] + string[i.end()+addLen:]
				addLen += j.end() - j.start() + 1
			else :
				break
	return string
def divTitle(string):
	result = []
	findAddition = re.finditer(r"bổ\ssung\s.+vào",string,re.U)
	if divlaw.lenIterator(findAddition) > 0 :
		if ";" in string :
			findSemicomma = re.finditer(r"(bổ\ssung|sửa\sđổi).+\;",string,re.U)
			for i in findSemicomma:
				result.append(string[:i.end()])
				result.append(string[i.end():])
				break
		else :
			result.append(string)
	else :
		result.append(string)
	return result
@tsv_extractor
@returns(lambda    
    law_id ="text",
    part_index ="int",
    chap_index ="int",
    sec_index ="int",
    law_index ="int",
    item_index ="int",
    point_index ="int",
    part_modify_name ="text",
    chap_modify_name ="text",
    sec_modify_name ="text",
    law_modify_name ="text",
    item_modify_name ="text",
    point_modify_name ="text",
    type_modify = "int"
    :[])
def extract(
    law_id ="text",
    part_index ="int",
    chap_index ="int",
    sec_index ="int",
    law_index ="int",
    item_index ="int",
    point_index ="int",
    numerical_symbol = "text",
    titles  ="text",
    content ="text",
    location_content ="int",
    count ="int"
    ):
	titles = handle_string.toLowerCase(titles)
	titles = rewriteString(titles)
	a = divTitle(titles)
	for title in a:
		findType = re.finditer(r"(.+vào.+)|(.+(sau|trước).{7,})",title,re.U)
		if divlaw.lenIterator(findType) > 0: 
			type_modify = 2
		else :
			type_modify = 1
        match = re.finditer(r"(\\n(\s|\_|\.|\*|\#)*\“(.(?!\“|\”))+.{2})|(\\n(\s|\_|\.|\*|\#)*\"(.(?!\"))+.{2})", content,re.DOTALL)
        quotesIndex = []
        for i in match:
        	quotesIndex.append(i.start())
        for j in range(len(quotesIndex)) :
			if type_modify == 1:
				divModify = divlaw.divPartModifyLaw(content)
				if j != (len(quotesIndex) - 1):
					divModify = divlaw.divPartModifyLaw(content[quotesIndex[j]:quotesIndex[j+1]])
				else :
					divModify = divlaw.divPartModifyLaw(content[quotesIndex[j]:])
				totalPart = divlaw.getTotalPart(divModify)
				if (totalPart == 0):
					totalPart = 1
				for part_id in range(0,totalPart):
					part = divlaw.getPart(divModify,part_id)
					if part['name'] != "":
						part_name = handle_string.toLowerCase(part['name'])
						if part_name in title:
							yield[
								law_id ,
								part_index ,
								chap_index ,
								sec_index ,
								law_index ,
								item_index ,
								point_index,
								part_name,
								None,
								None,
								None,
								None,
								None,
								type_modify
								]
							continue
					totalChap = divlaw.getTotalChapter(divModify,part_id)
					if totalChap == 0:
						totalChap = 1
					for chap_id in range(0,totalChap):
						chap = divlaw.getChapter(divModify,part_id,chap_id)
						if chap['name'] != "":
							chap_name = handle_string.toLowerCase(chap['name'])
							if chap_name in title:
								part_name = None
								findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title)
								if divlaw.lenIterator(findName)>0 :
									findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title)
									for fN in findName:
										part_name = title[fN.span()[0]:fN.span()[1]]
										break
								yield[
								law_id ,
							    part_index ,
							    chap_index ,
							    sec_index ,
							    law_index ,
							    item_index ,
							    point_index,
							    part_name,
							    chap_name,
							    None,
							    None,
							    None,
							    None,
							    type_modify
								]
								continue
						totalSec = divlaw.getTotalSection(divModify,part_id,chap_id)
						if totalSec == 0:
							totalSec = 1
						for sec_id in range(0,totalSec):
							sec = divlaw.getSection(divModify, part_id, chap_id,sec_id)
							if sec['name'] != "":
								sec_name = handle_string.toLowerCase(sec['name'])
								if sec_name in title:
									part_name = None
									findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title)
									if divlaw.lenIterator(findName)>0 :
										findName = re.finditer(r"phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title)
										for fN in findName:
											part_name = title[fN.span()[0]:fN.span()[1]]
											break
									chap_name = None
									findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title)
									if divlaw.lenIterator(findName)>0 :
										findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title)
										for fN in findName:
											chap['name'] = title[fN.span()[0]:fN.span()[1]]
											break
									yield[
									law_id ,
								    part_index ,
								    chap_index ,
								    sec_index ,
								    law_index ,
								    item_index ,
								    point_index,
								    part_name,
								    chap_name,
								    sec_name,
								    None,
								    None,
								    None,
								    type_modify
									]
									continue
							totalLaw = divlaw.getTotalLaw(divModify,part_id,chap_id,sec_id)
							if totalLaw == 0:
								totalLaw = 1
							for law_index in range(0,totalSec):
								law = divlaw.getLaw(divModify,part_id,chap_id,sec_id,law_index)
								if law['name'] != "":
									law_name = handle_string.toLowerCase(law['name'])
									if law_name in title:
										part_name = None
										findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title)
										if divlaw.lenIterator(findName)>0 :
											findName = re.finditer(r"phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title)
											for fN in findName:
												part_name = title[fN.span()[0]:fN.span()[1]]
												break
										chap_name = None
										findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title)
										if divlaw.lenIterator(findName)>0 :
											findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title)
											for fN in findName:
												chap_name = title[fN.span()[0]:fN.span()[1]]
												break
										sec_name = None
										findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title)
										if divlaw.lenIterator(findName)>0 :
											findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title)
											for fN in findName:
												sec_name = title[fN.span()[0]:fN.span()[1]]
												break
										yield[
										law_id ,
									    part_index ,
									    chap_index ,
									    sec_index ,
									    law_index ,
									    item_index ,
									    point_index,
									    part_name,
									    chap_name,
									    sec_name,
									    law_name,
									    None,
									    None,
									    type_modify
										]
										continue
								totalItem = divlaw.getTotalItem(divModify,part_id,chap_id,sec_id,law_index)
								if totalItem == 0:
									totalItem = 1
								for item_id in range(0,totalItem):
									item = divlaw.getItem(divModify,part_id,chap_id,sec_id,law_index,item_id)
									if item['name'] != "":
										item_name = 'khoản ' + item['name']
										if item_name in title:
											find_item_name = re.finditer(r"khoản\s"+item['name'],title,re.U)
											ex = getFirst(find_item_name)
											index_start = ex.end()
											part_name = None
											findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title[index_start:])
											if divlaw.lenIterator(findName)>0 :
												findName = re.finditer(r"phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title[index_start:])
												for fN in findName:
													part_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
													break
											chap_name = None
											findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title[index_start:])
											if divlaw.lenIterator(findName)>0 :
												findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title[index_start:])
												for fN in findName:
													chap_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
													break
											sec_name = None
											findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title[index_start:])
											if divlaw.lenIterator(findName)>0 :
												findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title[index_start:])
												for fN in findName:
													sec_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
													break
											law_name = None
											findName = re.finditer(r"điều [0-9]+\w*",title[index_start:])
											if divlaw.lenIterator(findName)>0 :
												findName = re.finditer(r"điều [0-9]+\w*",title[index_start:])
												for fN in findName:
													law_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
													break
											yield[
											law_id ,
										    part_index ,
										    chap_index ,
										    sec_index ,
										    law_index ,
										    item_index ,
										    point_index,
										    part_name,
										    chap_name,
										    sec_name,
										    law_name,
										    item['name'],
										    None,
										    type_modify
											]
											continue
									totalPoint = divlaw.getTotalPoint(divModify,part_id,chap_id,sec_id,law_index,item_id)
									if totalPoint == 0:
										totalPoint = 1
									for point_id in range(0,totalPoint):
										point = divlaw.getPoint(divModify,part_id,chap_id,sec_id,law_index,item_id,point_id)
										if point['name'] != "":
											point_name = 'điểm ' + point['name']
											if point_name in title:
												find_point_name = re.finditer(r"điểm "+point['name'],title,re.U)
												index_start = getFirst(find_point_name).end()
												part_name = None
												findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title[index_start:])
												if divlaw.lenIterator(findName)>0 :
													findName = re.finditer(r"phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title[index_start:])
													for fN in findName:
														part_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
														break
												chap_name = None
												findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title[index_start:])
												if divlaw.lenIterator(findName)>0 :
													findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title[index_start:])
													for fN in findName:
														chap_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
														break
												sec_name = None
												findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title[index_start:])
												if divlaw.lenIterator(findName)>0 :
													findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title[index_start:])
													for fN in findName:
														sec_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
														break
												law_name = None
												findName = re.finditer(r"điều [0-9]+\w*",title[index_start:])
												if divlaw.lenIterator(findName)>0 :
													findName = re.finditer(r"điều [0-9]+\w*",title[index_start:])
													for fN in findName:
														law_name = title[index_start+fN.span()[0]:index_start+fN.span()[1]]
														break
												item_name = None
												findName = re.finditer(r"(?:khoản\s)[0-9]+\w*",title[index_start:])
												if divlaw.lenIterator(findName)>0 :
													findName = re.finditer(r"(?:khoản\s)[0-9]+\w*",title[index_start:])
													for fN in findName:
														item_name = title[index_start+8+fN.span()[0]:index_start+fN.span()[1]]
														break
												yield[
												law_id ,
											    part_index ,
											    chap_index ,
											    sec_index ,
											    law_index ,
											    item_index ,
											    point_index,
											    part_name,
											    chap_name,
											    sec_name,
											    law_name,
											    item_name,
											    point['name'],
											    type_modify
												]
												continue
			if type_modify == 2:
				start_index = 0
				ft = re.finditer(r"bổ\ssung\s.+(vào).{5}",title,re.U)
				for i in ft :
					start_index = i.end() - 5
					break
				ft = re.finditer(r"bổ\ssung\s.+(sau|trước).{5}",title,re.U)
				for i in ft :
					start_index = i.end() - 5
					break
				part_name = None
				findName = re.finditer(r"(phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title[start_index:])
				if divlaw.lenIterator(findName)>0 :
					findName = re.finditer(r"phần thứ)\s([A-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",title[start_index:])
					for fN in findName:
						part_name = title[start_index+fN.span()[0]:start_index+fN.span()[1]]
						break
				chap_name = None
				findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title[start_index:])
				if divlaw.lenIterator(findName)>0 :
					findName = re.finditer(r"(chương)\s([A-Z]|[0-9])+",title[start_index:])
					for fN in findName:
						chap_name = title[start_index+fN.span()[0]:start_index+fN.span()[1]]
						break
				sec_name = None
				findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title[start_index:])
				if divlaw.lenIterator(findName)>0 :
					findName = re.finditer(r"(mục)\s([A-Z]|[0-9])+",title[start_index:])
					for fN in findName:
						sec_name = title[start_index+fN.span()[0]:start_index+fN.span()[1]]
						break
				law_name = None
				findName = re.finditer(r"điều [0-9]+[A-zĐđ]*",title[start_index:])
				if divlaw.lenIterator(findName)>0 :
					findName = re.finditer(r"điều [0-9]+[A-zĐđ]*",title[start_index:])
					for fN in findName:
						law_name = title[start_index+fN.span()[0]:start_index+fN.span()[1]]
						break
				item_name = None
				findName = re.finditer(r"(khoản\s)[0-9]+",title[start_index:])
				if divlaw.lenIterator(findName)>0 :
					findName = re.finditer(r"(khoản\s)[0-9]+",title[start_index:])
					for fN in findName:
						item_name = title[start_index+fN.span()[0] + 8:start_index+fN.span()[1]]
						break
				point_name = None
				temp = title
				findName = re.finditer(r"(điểm\s)[A-z]+",title[start_index:],re.U)
				if divlaw.lenIterator(findName) > 0 :
					findName = re.finditer(r"(điểm\s)[A-zđ]+",temp[start_index:],re.U)
					for fN in findName:
						point_name = temp[start_index+fN.span()[0]:start_index+fN.span()[0]]
						break
				if 'sau' in title[:start_index]:
					type_modify = 3
				elif 'trước' in title[:start_index]:
					type_modify = 4
				yield[
					law_id ,
				    part_index ,
				    chap_index ,
				    sec_index ,
				    law_index ,
				    item_index ,
				    point_index,
				    part_name,
				    chap_name,
				    sec_name,
				    law_name,
				    item_name,
				    point_name,
				    type_modify
				]
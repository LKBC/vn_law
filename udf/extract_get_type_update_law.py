#!/usr/bin/env python
# -*- coding:utf8 -*-
from deepdive import *
import re
import ddlib
##lấy ra loại update từ point
def extract_update_point(totalpoint,point_content):
	if(totalpoint == 0):
		return 0
	elif(totalpoint > 0) :
		# get_type_modify_update = re.search(r'([S|s]ửa đổi)*(\,\s)*([b|B]ổ sung\s)*',point_content)
		# get_type_modify_update1 = re.search(r'[^đã]+\s*(được sửa đổi)',point_content)
		get_type_modify_update = re.search(r'[^đã được]+\s([S|s]ửa đổi)',point_content)
		get_type_modify_update1 = re.search(r'[^đã]+\s*(được sửa đổi)',point_content)
		get_type_modify_update2 = re.search(r'[b|B]ổ sung',point_content)
		get_type_modify_update3 = re.search(r'[s|S]ửa thành',point_content)		
		if(get_type_modify_update is not none || get_type_modify_update1 is not none|| get_type_modify_update2 is not none||get_type_modify_update2 is not none||get_type_modify_update3 is not none):
			return 1
		get_type_reject_update = re.search(r'([b|B]ãi bỏ))',point_content)
		if(get_type_reject_update is not none):
			return 2
		get_type_add_update = re.search(r'[b|B]ổ sung cụm từ',point_content):
		if(get_type_add_update is not none):
			return 3 
		get_type_replace_phrase_update = re.search(r'[t|T]hay\s.*cụm từ',point_content)
		get_type_replace_phrase_update1 = re.search(r'[t|T]hay\s.*từ',point_content)
		if(get_type_replace_phrase_update is not none ||  get_type_replace_phrase_update1 is not none):
			return 4
		get_type_delete_phrase_update = re.search(r'[b|B]ỏ cụm từ',point_content)
		if(get_type_delete_phrase_update is not none):
			return 5
		get_type_modify_phrase_update = re.search(r'([s|S]ửa đổi\s)*(\,\s)*([b|B]ổ sung\s)*(một số\s)(từ ngữ\s)*(chữ\s)*của',law_content)
		if(get_type_modify_phrase_update is not none):
			return 6
		# get_type_modify_phrase_update = re.search(r'[s|S]ửa đổi\s.*các chữ',point_content)
		# if(get_type_modify_update is not none ):
		# 	return 6
		get_type_modify_name_update = re.search(r'([t|T]ên của\s).+(([s|S]ửa đổi\s)*(\,\s)*([b|B]ổ sung\s)*)(thành)',point_content)
		if(get_type_modify_name_update is not none):
			return 7
		## trường hợp sửa đổi, bổ sung Điều ... 
		# get_type_modify_true_update = re.search(r'')
	else:
		return 0
##lấy ra loại update từ item
def extract_update_item(totalItem,item_content):
	if(totalItem == 0 ):
		return 0
	elif(totalItem > 0):
		get_type_modify_update = re.search(r'[^đã được]+\s([S|s]ửa đổi)',item_content)
		get_type_modify_update1 = re.search(r'[^đã]+\s*(được sửa đổi)',item_content)
		get_type_modify_update2 = re.search(r'[b|B]ổ sung',item_content)		
		get_type_modify_update3 = re.search(r'[s|S]ửa thành',item_content)		
		if(get_type_modify_update is not none || get_type_modify_update1 is not none|| get_type_modify_update2 is not none||get_type_modify_update2 is not none||get_type_modify_update3 is not none):
			return 1
		get_type_reject_update = re.search(r'([b|B]ãi bỏ))',item_content)
		if(get_type_reject_update is not none):
			return 2
		get_type_add_update = re.search(r'[b|B]ổ sung cụm từ',item_content):
		if(get_type_add_update is not none):
			return 3
		get_type_replace_phrase_update = re.search(r'[t|T]hay\s.*cụm từ',point_content)
		get_type_replace_phrase_update1 = re.search(r'[t|T]hay\s.*từ',point_content)
		if(get_type_replace_phrase_update is not none ||  get_type_replace_phrase_update1 is not none):
			return 4
		get_type_delete_phrase_update = re.search(r'[b|B]ỏ cụm từ',item_content)
		if(get_type_delete_phrase_update is not none):
			return 5
		get_type_modify_phrase_update = re.search(r'([s|S]ửa đổi\s)*(\,\s)*([b|B]ổ sung\s)*(một số\s)(từ ngữ\s)*(chữ\s)*của',law_content)
		if(get_type_modify_phrase_update is not none):
			return 6
		# get_type_modify_phrase_update = re.search(r'[s|S]ửa đổi\s.*các chữ',item_content)
		# if(get_type_modify_update is not none ):
		# 	return 6
		get_type_modify_name_update = re.search(r'([t|T]ên của\s).+(([s|S]ửa đổi\s)*(\,\s)*([b|B]ổ sung\s)*)(thành)',item_content)
		if(get_type_modify_name_update is not none):
			return 7

	else : 
		return 0
##lấy ra loại update từ law
def extract_update_law(totalLaw,law_content):
	if(totalLaw == 0 ):
		return 0
	elif(totalLaw >0):
		get_type_modify_update = re.search(r'[^đã được]+\s([S|s]ửa đổi)',law_content)
		get_type_modify_update1 = re.search(r'[^đã]+\s*(được sửa đổi)',law_content)
		get_type_modify_update2 = re.search(r'[b|B]ổ sung',law_content)		
		get_type_modify_update3 = re.search(r'[s|S]ửa thành',law_content)		
		if(get_type_modify_update is not none || get_type_modify_update1 is not none|| get_type_modify_update2 is not none||get_type_modify_update2 is not none||get_type_modify_update3 is not none):
			return 1
		get_type_reject_update = re.search(r'([b|B]ãi bỏ))',law_content)
		if(get_type_reject_update is not none):
			return 2
		get_type_add_update = re.search(r'[b|B]ổ sung cụm từ',law_content):
		if(get_type_add_update is not none):
			return 3 
		get_type_replace_phrase_update = re.search(r'[t|T]hay\s.*cụm từ',point_content)
		get_type_replace_phrase_update1 = re.search(r'[t|T]hay\s.*từ',point_content)
		if(get_type_replace_phrase_update is not none ||  get_type_replace_phrase_update1 is not none):
		if(get_type_replace_phrase_update is not none):
			return 4
		get_type_delete_phrase_update = re.search(r'[b|B]ỏ cụm từ',law_content)
		if(get_type_delete_phrase_update is not none):
			return 5
		# get_type_modify_phrase_update = re.search(r'[s|S]ửa đổi\s.*các chữ',law_content)
		# if(get_type_modify_update is not none ):
		# 	return 6
		get_type_modify_phrase_update = re.search(r'([s|S]ửa đổi\s)*(\,\s)*([b|B]ổ sung\s)*(một số\s)(từ ngữ\s)*(chữ\s)*của',law_content)
		if(get_type_modify_phrase_update is not none):
			return 6
		get_type_modify_name_update = re.search(r'([t|T]ên của\s).+(([s|S]ửa đổi\s)*(\,\s)*([b|B]ổ sung\s)*)(thành)',law_content)
		if(get_type_modify_name_update is not none):
			return 7
	else : 
		return 0
def extract_location(content):
	locate = re.search(r'([Đ|đ]iểm\s[\w|\d]+.*)*(của)*([k|K]hoản\s[\w|\d]+.*)*(của)*([Đ|đ]iều\s[\w|\d]+.*)*(của)*([C|c]hương\s[\w|\d]+.*)*vào',content)
	if(locate is not None):
		if(len(locate.group())>4):
			return locate.group()
	locate = re.search(r'([Đ|đ]iểm\s[\w|\d]+.*)*(của)*([k|K]hoản\s[\w|\d]+.*)*(của)*([Đ|đ]iều\s[\w|\d]+.*)*(của)*([C|c]hương\s[\w|\d]+.*)*được',content)
	if(locate is not None):
		if(len(locate.group()>5)):
			return locate.group()
def extract_update(type,content,doc_id,totalLaw,law_content,totalItem,item_content,totalpoint,point_content):
	type_update = 0
	##lấy loại update
	## lấy loại update trong điểm
	type_update = extract_update_point(totalpoint,point_content)
	if(type_update == 1):
		location_update = extract_location(point_content)
	## lấy loại update trong khoản
	if(type_update == 0) :
		type_update = extract_update_item(totalItem,item_content)
		if(type_update == 1):
			location_update = extract_location(item_content)
	##lấy loại update trong điều
	if(type_update==0):
		type_update = extract_update_item(totalLaw,law_content)
		if(type_update == 1):
			location_update = extract_location(law_content)


	##lấy vị trí update
	##lấy vị trí update từ point


@tsv_extractor
@returns(lambda
    doc_id = "text",
    type = "text",
    doc_content_update = "text",
    location_update ="text"
    :[])
def extract(
	doc_id ="text",
	totalLaw = "int",
	law_content = "text",
	totalItem = "int",
	item_content = "text",
	totalpoint = "int",
	point_content = "text"
    ):	
	type = 0 
	if(totalLaw >0 && totalItem > 0 && totalpoint > 0 ):
	else(totalLaw >0  && totalItem == 0):	
	elif(totalLaw == 0 && totalItem == 0):
		yield[
			doc_id,
			"null",
			"null",
			"null"
		]
	elif(totalLaw == 0 && totalItem >0):

		

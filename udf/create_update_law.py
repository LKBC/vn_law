#!/usr/bin/env python
# -*- coding:utf8 -*-
from deepdive import * 
import re
import handle_string
@tsv_extractor
@returns(lambda
		id 				= 	"text",
	:[])
def extract(
		id 				=	"text",
		content 		= 	"text",
		signature		=	"text",
		title           = 	"text",
	):
#num_types = len(type)
	if(re.search("Sửa đổi",title)):
		# id = re.match(r'[0-9]*(/[0-9]*)*((/|-)[A-ZĐ]*[0-9]*)+\W+\nĐiều 1.',content,0)
		yield [
			id,	
		]
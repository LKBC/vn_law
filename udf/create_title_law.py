#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import * 
import re
import handle_string
@tsv_extractor
@returns(lambda
		law_id 			=	"text",
		law_title 		= 	"text",
	:[])
def extract(
		id 			=	"text",
		title    	=	"text",
		type        =	"text",
	):
	if(title.find(type)):
		law_title = type + ' '+ title
		yield[
			id,
			law_title,
		]
	else :
		yield [
			id,
			title,
			]
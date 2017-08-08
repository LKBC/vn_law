#!/usr/bin/env python
# -*- coding:utf8 -*-
from deepdive import *
import re
import ddlib

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
	item_content = "text"
    ):
	if(totalLaw == 0 && totalItem == 0):
		yield[
			doc_id,
			"null",
			"null",
			"null"
		]

#!/urs/bin/env pythong
# -*- coding:utf8 -*-



from deepdive import *
import re
import handle_string
import divlaw

@tsv_extractor
@returns(lambda 
    	part_id = "text",
    	part_content = "text[]",
    	part_name   = "text[]",
    	start_part  = "int[]",
    	end_part    = "int[]",
	:[])
def extract(
		id			=	"text",
		content		=	"text[]",
		):
	data_json = divPart(content)
	data = json.loads(data_json)

	
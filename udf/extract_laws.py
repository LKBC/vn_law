#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import divlaw

@tsv_extractor
@returns(lambda
    law_id         ="text",
    part_index      ="int",
    chap_index     ="int",
    sec_index		="int",
    totalLaw       ="int",
    law_index      ="int",
    law_start      ="int",
    law_end        ="int",
    law_name		="text",
    law_content			="text"
    :[])
def extract(
    id 			="text",
    content 	="text",
    part_index  ="int",
    chap_index 	="int",
    sec_index 	="int",
    sec_start 	="int",
    sec_end 	="int"

    ):

	rs = divlaw.divPart(content)
	sec = divlaw.getSection(rs,part_index, chap_index, sec_index)
	totalLaw = sec['totalLaw']
	if totalLaw > 0:
		for i in range(0,totalLaw):
			start = sec['laws'][i]['start']
			end = sec['laws'][i]['end']
			yield [
				id,
				part_index,
				chap_index,
				sec_index,
				totalLaw,
				i,
				start,
				end,
				sec['laws'][i]['name'],
				content[start:end],
			]
	else :
		yield [
			id,
			part_index,
			chap_index,
			sec_index,
			0,
			0,
			sec_start,
			sec_end,
			"",
			"",
		]
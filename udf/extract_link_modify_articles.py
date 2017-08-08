#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string
import divlaw

@tsv_extractor
@returns(lambda
    doc_id = "text",
    modify_doc_id = "text"  
    :[])
def extract(
    doc_id =  "text",
    modify_title = "text",
    doc_id_resources = "text[]",
    doc_title_resources = "text[]",
    doc_symbol_resources = "text[]",
    type_doc = "text[]" 
    ):
    
    pattern = re.compile(r"[0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)+")
    m = pattern.match(modify_title)
    s = "1"
    if (m is not None):
        s = s + "1"
        symbol = m.group(0)
        available = False
        for i in range(0,len(doc_symbol_resources)):
            if doc_symbol_resources[i] == symbol :
                available = True
                yield [
                    doc_id,
                    doc_id_resources[i],
                ]
        if available == False :
            yield [
                doc_id,
                s + "a",
            ]
    else :
        s = s + "1"
        for i in range(0,len(doc_title_resources)):
            temp = type_doc[i] + " " + doc_title_resources[i]
            tempU = handle_string.to_unicode(temp)
            tempReal = handle_string.to_unicode(modify_title)
            available1 = False
            if (re.search(tempU,tempReal,re.I|re.U) is not None) and len(temp) == len(modify_title) :
                available1 = True
                yield [
                    doc_id,
                    doc_id_resources[i],
                ]
        if available1 == False :
            yield [
                doc_id,
                s + "b",
            ]



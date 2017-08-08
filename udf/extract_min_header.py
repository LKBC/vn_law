#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string

@tsv_extractor
@returns(lambda
        doc_id      = "text",
        sentence_end_index   = "int"
    :[])
def extract(
        doc_id         = "text",
        sentence_end_index = "int[]" 
    ):
    a = min(sentence_end_index)
    yield[
    doc_id,
    a,
    ]


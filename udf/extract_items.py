#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string
import divlaw

@tsv_extractor
@returns(lambda
        law_id         ="text",
        part_index     ="int",
        chap_index     ="int",
        sec_index      ="int",
        law_index      ="int",
        totalItem      ="int",
        item_index     ="int",
        item_start     ="int",
        item_end       ="int",
        item_name      ="text",
        item_content   ="text",
    :[])
def extract(
        id          ="text",
        content     ="text",
        part_index  ="int",
        chap_index  ="int",
        sec_index   ="int",
        law_index   ="int",
        law_start   ="int",
        law_end     ="int",
    ):

    result = divlaw.divPart(content)
    law = divlaw.getLaw(result, part_index, chap_index, sec_index, law_index)
    totalItem = law['totalItem']
    if totalItem > 0:
        for i in range(0, totalItem):
            start = law['items'][i]['start']
            end = law['items'][i]['end']
            yield [
                id,
                part_index,
                chap_index,
                sec_index,
                law_index,
                totalItem,
                i,
                start,
                end,
                law['items'][i]['name'],
                content[start:end]
            ]
    else :
        yield [
            id,
            part_index,
            chap_index,
            sec_index,
            law_index,
            0,
            0,
            law_start,
            law_end,
            None,
            None
        ]

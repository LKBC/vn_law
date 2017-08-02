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
        point_index     ="int",
        point_start     ="int",
        point_end       ="int",
        point_name      ="text",
        point_content   ="text",
    :[])
def extract(
        id          ="text",
        content     ="text",
        part_index  ="int",
        chap_index  ="int",
        sec_index   ="int",
        law_index   ="int",
        item_index  ="int",
        item_start   ="int",
        item_end     ="int",
    ):

    result = divlaw.divPart(content)
    item = divlaw.getItem(result, part_index, chap_index, sec_index, law_index,item_index)
    totalPoint = item['totalPoint']
    if totalPoint > 0:
        for i in range(0, totalPoint):
            start = item['points'][i]['start']
            end = item['points'][i]['end']
            yield [
                id,
                part_index,
                chap_index,
                sec_index,
                law_index,
                item_index,
                totalPoint,
                i,
                start,
                end,
                item['points'][i]['name'],
                content[start:end]
            ]
    else :
        yield [
            id,
            part_index,
            chap_index,
            sec_index,
            law_index,
            item_index,
            0,
            0,
            item_start,
            item_end,
            None,
            None
        ]

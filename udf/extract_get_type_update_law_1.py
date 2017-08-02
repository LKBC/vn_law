#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string
import divlaw
def lenIterator(list):
    sum = 0
    for i in list :
        sum += 1
    return sum
def get_numerical_symbol(title):
    get_title1 = re.search(r'(của\s.*)\s(đã được|được)',title)
    get_title  = re.search(r'([0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*))',title,re.M|re.I)
    # get_id = re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)+',get_content.group())
    # get_title1 = re.search(r'([0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)\s(đã được))|([0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)\s(được))',title)
    if(get_title1 is not None):
        number = re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)',get_title1.group())
        if(number is not None):
            return number.group()
    elif ((get_title is not None) and (get_title1 is None)):
        return get_title.group()
    else :
        return None
@tsv_extractor
@returns(lambda
    law_id ="text",
    type =  "int", 
    doc_content_update = "text",
    numerical_symbol = "text",
    :[])
def extract(
    law_id = "text",
    totalLaw = "int",
    law_content = "text",
    totalItem  = "int",
    item_content  = "text",
    totalpoint = "int",
    point_content = "text",
    name_title = "text"
    ):
    ## type = 1 : sửa đổi bổ sung,type = 2 : loại bỏ
    get_type_title = re.search(r'((((s|S)ửa đổi)(\s|\,)*((b|B)ổ sung)*)|((b|B)ổ sung))',name_title)
    if(get_type_title is not None):
        number = None
        if(totalpoint > 0):
            number = get_numerical_symbol(point_content)
        if(number is not None):
            numerical_symbol = number
        elif(number is None):
            if(totalItem > 0):
                number = get_numerical_symbol(item_content)
            if(number is not None):
                numerical_symbol = number
            elif(number is None):
                if(totalLaw > 0):
                    number = get_numerical_symbol(law_id)
                if(number is not None):
                    numerical_symbol = number
                elif(number is None):
                    numerical_symbol = None
        point = 0 
        p = re.compile(r'((((S|s)ửa đổi)(\s|\,)*((b|B)ổ sung)*)|((b|B)ổ sung))')
        p1= re.compile(r'(đã\s|đã được\s)((((S|s)ửa đổi)(\s|\,)*((b|B)ổ sung)*)|((b|B)ổ sung))')
        if(totalpoint > 0):
            type_modify = re.search(r'(((b|B)ổ sung cụm từ)|((b|B)ổ sung từ))',point_content)
            if(type_modify is not None):
                type = 3
                doc_content_update = point_content
                point = 1
            else :
                type_change_name = re.search(r'(S|s)ửa đổi tên',point_content) 
                if(type_change_name is not None):
                    type = 6
                    doc_content_update = point_content
                    point = 1
                else:
                    type_delete = re.search(r'(b|B)ãi bỏ',point_content)
                    if(type_delete is not None):
                        type = 2
                        doc_content_update = point_content
                        point = 1
                    else:
                        type_delete_text = re.search(r'(((b|B)ỏ cụm từ)|((b|B)ỏ từ))',point_content)
                        if(type_delete_text is not None):
                            type = 7
                            doc_content_update = point_content
                            point =1
                        else: 
                            # type_add_text = re.search(r'((((S|s)ửa đổi)(\s|\,)*((b|B)ổ sung)*)|((b|B)ổ sung))',point_content)
                            # type_add_text1 = re.search(r'(đã\s|đã được\s)((((S|s)ửa đổi)(\s|\,)*((b|B)ổ sung)*)|((b|B)ổ sung))',point_content)
                            # if(type_add_text is not None and (len(type_add_text)!=len(type_add_text1))):
                            # type_add_text = re.search(r'((((S|s)ửa đổi)(\s|\,)*((b|B)ổ sung)*)|((b|B)ổ sung))',point_content)
                            # if(type_add_text is not None):
                            type_add_text = p.finditer(point_content)
                            type_add_text1 = p1.finditer(point_content)
                            if(lenIterator(type_add_text) != lenIterator(type_add_text1)):
                                type = 1
                                doc_content_update = point_content
                                point = 1
                            else : 
                                # type_change_text = re.search(r'(t|T)hay\s.*cụm từ',point_content)
                                type_change_text = re.search(r'((t|T)hay\s)*(cụm\s)*từ\s.*(được\s)*(thay\s)*bằng\s(cụm\s)*từ',point_content)
                                if(type_change_text is not None):
                                    type = 4
                                    doc_content_update = point_content
                                    point = 1
                                else : 
                                    type_name_to_name = re.search(r'((t|T)ên của\s).+(((S|s)ửa đổi\s)*(\,\s)*((b|B)ổ sung\s)*)(thành)',item_content)
                                    if(type_name_to_name is not None):
                                        type = 5
                                        doc_content_update =point_content
                                        point = 1
                                    else : 
                                        point = 0
        if(totalItem > 0 and point == 0):
            type = re.search(r'(b|B)ổ sung cụm từ',item_content)
            if(type is not None):
                type = 3
                doc_content_update = item_content
                point = 1
            else:
                type_change_name = re.search(r'(S|s)ửa đổi tên',item_content) 
                if(type_change_name is not None):
                    type = 6
                    doc_content_update = item_content
                    point = 1
                else:
                    type_delete = re.search(r'(b|B)ãi bỏ',item_content)
                    if(type_delete is not None):
                        type = 2
                        doc_content_update = item_content
                        point = 1
                    else:
                        type_delete_text = re.search(r'(((b|B)ỏ cụm từ)|((b|B)ỏ từ))',item_content)
                        if(type_delete_text is not None):
                            type = 7
                            doc_content_update = item_content
                            point = 1
                        else: 
                            # type_add_text = re.search(r'((((S|s)ửa đổi)(\s|\,)*((b|B)ổ sung)*)|((b|B)ổ sung))',item_content)
                            # if(type_add_text is not None):
                            type_add_text = p.finditer(item_content)
                            type_add_text1 = p1.finditer(item_content)
                            if(lenIterator(type_add_text) != lenIterator(type_add_text1)):    
                                type = 1
                                doc_content_update = item_content
                                point=1
                            else:
                                # type_change_text = re.search(r'(t|T)hay\s.*cụm từ',item_content)
                                type_change_text = re.search(r'((t|T)hay\s)*(cụm\s)*từ\s.*(được\s)*(thay\s)*bằng\s(cụm\s)*từ',item_content)
                                if(type_change_text is not None):
                                    type = 4
                                    doc_content_update = item_content
                                    point = 1
                                else : 
                                    type_name_to_name = re.search(r'((t|T)ên của\s).+(((S|s)ửa đổi\s)*(\,\s)*((b|B)ổ sung\s)*)(thành)',item_content)
                                    if(type_name_to_name is not None):
                                        type = 5
                                        doc_content_update = item_content
                                        point = 1
                                    else : 
                                        point = 0
            if(totalpoint > 0 and point == 1 ):
                doc_content_update = point_content
        if(totalLaw >0 and point == 0 ):
            type = re.search(r'(b|B)ổ sung cụm từ',law_content)
            if(type is not None):
                type = 3
                doc_content_update = law_content
                point = 1  
            else:
                type_change_name = re.search(r'(S|s)ửa đổi tên',law_content) 
                if(type_change_name is not None):
                    type = 6
                    doc_content_update = law_content
                    point = 1
                else:
                    type_delete = re.search(r'(b|B)ãi bỏ',law_content)
                    if(type_delete is not None):
                        type = 2
                        doc_content_update = law_content
                        point = 1
                    else:
                        type_delete_text = re.search(r'(((b|B)ỏ cụm từ)|((b|B)ỏ từ))',law_content)
                        if(type_delete_text is not None):
                            type = 7
                            doc_content_update = law_content
                            point = 1
                        else: 
                            # type_add_text = re.search(r'((((S|s)ửa đổi)(\s|\,)*((b|B)ổ sung)*)|((b|B)ổ sung))',law_content)
                            # if(type_add_text is not None):
                            type_add_text = p.finditer(law_content)
                            type_add_text1 = p1.finditer(law_content)
                            if(lenIterator(type_add_text) != lenIterator(type_add_text1)):
                            
                                type = 1
                                doc_content_update = law_content
                                point = 1
                            else:
                                # type_change_text = re.search(r'(((t|T)hay\s.*cụm từ)|((t|T)hay\s.*từ))',law_content)
                                type_change_text = re.search(r'((t|T)hay\s)*(cụm\s)*từ\s.*(được\s)*(thay\s)*bằng\s(cụm\s)*từ',law_content)
                                if(type_change_text is not None):
                                    type = 4
                                    doc_content_update = law_content
                                    point = 1
                                else : 
                                    type_name_to_name = re.search(r'((t|T)ên của\s).+(((S|s)ửa đổi\s)*(\,\s)*((b|B)ổ sung\s)*)(thành)',law_content)
                                    if(type_name_to_name is not None):
                                        type = 5
                                        doc_content_update = law_content
                                        point = 1
                                    else : 
                                        point = 0
            if(totalItem > 0):
                doc_content_update = item_content
        if(point == 1):
            yield[
                law_id,
                type,
                doc_content_update,
                numerical_symbol
            ]

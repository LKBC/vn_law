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
@tsv_extractor
@returns(lambda
    law_id = "text",
    numerical_symbol = "text",
    text_delete = "text", ## cụm từ cần bãi bỏ// nội dung sửa đổi update // sub_content sửa đổi update
    from_text = "text",
    to_text = "text",
    chapter = "text",
    law = "text",
    item = "text",
    point = "text",
    type = "int"
    :[])
def extract(
    law_id = "text",
    type = "int",
    content = "text",
    numerical_symbol = "text"
    ):
    if(type == 2):
        t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
        extract = t.finditer(content)
        if(lenIterator(extract)>0):
            for extract in t.finditer(content):
                temp_law = re.search(r'(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))',content[extract.span()[0]:extract.span()[1]])
                if(temp_law is not None):
                    law = temp_law.group()
                else :
                    law = None
                temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
                if(temp_item is not None):
                    item = temp_item.group()
                else :
                    item = None
                temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
                if(temp_point is not None):
                    point = temp_point.group()
                else :
                    point = None
                yield[
                    law_id,
                    numerical_symbol,
                    content,
                    None,
                    None,
                    None,
                    law,
                    item,
                    point,
                    2
                ]
        else :
            yield[
                law_id,
                numerical_symbol,
                content,
                None,
                None,
                None,
                None,
                None,
                None,
                2
            ]
        # numerical_symbol = get_numerical_symbol(content)
        # p = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(Khoản|khoản)\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))')
        # location = p.finditer(content)
        # if(lenIterator(location)>0):
        #     for location in p.finditer(content):
        #         law = re.search(r'(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))',content[location.span()[0]:location.span()[1]])
        #         item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',content[location.span()[0]:location.span()[1]])
        #         point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',content[location.span()[0]:location.span()[1]])
        #         yield[
        #             law_id,
        #             numerical_symbol,
        #             None,
        #             None,
        #             None,
        #             law.group(),
        #             item.group(),
        #             point.group(),
        #             2
        #         ]
        # else:
        #     p = re.compile(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))')
        #     location = p.finditer(content)
        #     if(lenIterator(location)>0):
        #         for location in p.finditer(content):
        #             law = re.search(r'(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))',content[location.span()[0]:location.span()[1]])
        #             item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',content[location.span()[0]:location.span()[1]])
        #             yield[
        #                 law_id,
        #                 numerical_symbol,
        #                 None,
        #                 None,
        #                 None,
        #                 law.group(),
        #                 item.group(),
        #                 None,
        #                 2
        #             ]
        #     # elif(lenIterator(location)<0):
        #     else:
        #         p = re.compile(r'(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
        #         location = p.finditer(content)
        #         if(lenIterator(location)>0):
        #             for location in p.finditer(content):
        #                 law = re.search(r'(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))',content[location.span()[0]:location.span()[1]])
        #                 yield[
        #                     law_id,
        #                     numerical_symbol,
        #                     None,
        #                     None,
        #                     None,
        #                     law.group(),
        #                     None,
        #                     None,
        #                     2
        #                 ]
    if(type == 3 ):
        p =re.compile(r'(B|b)ổ\ssung\s(cụm\s)*từ\s')
        for location in p.finditer(content):
            sub_content = content[location.span()[1]:len(content)]
            temp = p.finditer(sub_content)
            if(lenIterator(temp)>0):
                for temp in p.finditer(sub_content):
                    sub_content = sub_content[0:temp.span()[0]]
                    break
            temp_replace = re.search(r'(\“|\")(\s)*.+(\s)*(\”|\")\s.*sau\s(cụm\s)*từ\s',sub_content)
            if(temp_replace is not None):
                temp_from_replace = re.search(r'(\“|\")(\s)*.+(\s)*(\”|\")',temp_replace.group())
                from_replace = temp_from_replace.group()
                temp_replace = re.search(r'sau\s(cụm\s)*từ\s(\“|\")(\s)*.+(\s)*(\”|\")',sub_content)
                temp_to_replace = re.search(r'(\“|\")(\s)*.+(\s)*(\”|\")',temp_replace.group())
                to_replace = temp_to_replace.group()
                t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
                extract = t.finditer(sub_content,re.DOTALL)
                if(lenIterator(extract)>0):
                    for extract in t.finditer(sub_content):
                        temp_law = re.search(r'(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))',sub_content[extract.span()[0]:extract.span()[1]])
                        if(temp_law is not None):
                            law = temp_law.group()
                        else :
                            law = None
                        temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
                        if(temp_item is not None):
                            item = temp_item.group()
                        else :
                            item = None
                        temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
                        if(temp_point is not None):
                            point = temp_point.group()
                        else :
                            point = None
                        yield[
                            law_id,
                            numerical_symbol,
                            sub_content,
                            from_replace,
                            to_replace,
                            None,
                            law,
                            item,
                            point,
                            3
                        ]
            else :
                yield[
                    law_id,
                    numerical_symbol,
                    content,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    3
                ]
    if(type == 4 ):
        p =re.compile(r'((t|T)hay\s)*(cụm\s)*từ\s')
        for location in p.finditer(content):
            sub_content = content[location.span()[1]:len(content)]
            temp = p.finditer(sub_content)
            if(lenIterator(temp)>0):
                for temp in p.finditer(sub_content):
                    sub_content = sub_content[0:temp.span()[0]]
                    break

            temp_replace = re.search(r'(\“|\")(\s)*.+(\s)*(\”|\")\s.*(được\s)*(thay\s)*bằng\s(cụm\s)*từ',sub_content)
            if(temp_replace is not None):
                temp_from_replace = re.search(r'(\“|\")(\s)*.+(\s)*(\”|\")',temp_replace.group())
                from_replace = temp_from_replace.group()
                temp_replace = re.search(r'(được\s)*(thay\s)*bằng\s(cụm\s)*từ\s(\“|\")(\s)*.+(\s)*(\”|\")',sub_content)
                temp_to_replace = re.search(r'(\“|\")(\s)*.+(\s)*(\”|\")',temp_replace.group())
                to_replace = temp_to_replace.group()
                t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
                extract = t.finditer(sub_content,re.DOTALL)
                if(lenIterator(extract)>0):
                    for extract in t.finditer(sub_content):
                        temp_law = re.search(r'(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))',sub_content[extract.span()[0]:extract.span()[1]])
                        if(temp_law is not None):
                            law = temp_law.group()
                        else :
                            law = None
                        temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
                        if(temp_item is not None):
                            item = temp_item.group()
                        else :
                            item = None
                        temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
                        if(temp_point is not None):
                            point = temp_point.group()
                        else :
                            point = None
                        yield[
                            law_id,
                            numerical_symbol,
                            sub_content,
                            from_replace,
                            to_replace,
                            None,
                            law,
                            item,
                            point,
                            4
                        ]
            else :
                yield[
                    law_id,
                    numerical_symbol,
                    content,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    4
                ]


    if(type == 7):
        text_delete = re.search(r'\“.+\”',content,re.M|re.I)
        if(text_delete is not None):
            # numerical_symbol = get_numerical_symbol(content)
            t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
            extract = t.finditer(content)
            if(lenIterator(extract)>0):
                for extract in t.finditer(content):
                    temp_chapter = re.search(r'(c|C)hương\s(\w{1,10}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
                    if(temp_chapter is not None):
                        chapter = temp_chapter.group()
                    else:
                        chapter = None
                    temp_law = re.search(r'(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))',content[extract.span()[0]:extract.span()[1]])
                    if(temp_law is not None):
                        law = temp_law.group()
                    else :
                        law = None
                    temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
                    if(temp_item is not None):
                        item = temp_item.group()
                    else :
                        item = None
                    temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
                    if(temp_point is not None):
                        point = temp_point.group()
                    else :
                        point = None
                    yield[
                        law_id,
                        numerical_symbol,
                        content,
                        None,
                        text_delete.group(),
                        chapter,
                        law,
                        item,
                        point,
                        7
                    ]
            # p = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))')
            # location = p.finditer(content)
            # if(lenIterator(location)>0):
            #     for location in p.finditer(content):
            #         law = re.search(r'(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))',content[location.span()[0]:location.span()[1]])
            #         item = re.search(r'(k|K)hoản\s(\w{1,5}|\d{1,5})',content[location.span()[0]:location.span()[1]])
            #         point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',content[location.span()[0]:location.span()[1]])
            #         yield[
            #             law_id,
            #             numerical_symbol,
            #             text_delete.group(),
            #             None,
            #             None,
            #             None,
            #             law.group(),
            #             item.group(),
            #             point.group(),
            #             7
            #         ]
            # else : 
            #     p = re.compile(r'(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))')
            #     location = p.finditer(content)
            #     if(lenIterator(location)>0):
            #         for location in p.finditer(content):
            #             law = re.search(r'(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))',content[location.span()[0]:location.span()[1]])
            #             item = re.search(r'(k|K)hoản\s(\w{1,5}|\d{1,5})',content[location.span()[0]:location.span()[1]])
            #             yield[
            #                 law_id,
            #                 numerical_symbol,
            #                 text_delete.group(),
            #                 None,
            #                 None,
            #                 None,
            #                 law.group(),
            #                 item.group(),
            #                 None,
            #                 7
            #             ]
            #     else:
            #         p = re.compile(r'(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
            #         location = p.finditer(content)
            #         if(lenIterator(location)>0):
            #             for location in p.finditer(content):
            #                 law = re.search(r'(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))',content[location.span()[0]:location.span()[1]])
            #                 yield[
            #                     law_id,
            #                     numerical_symbol,
            #                     text_delete.group(),
            #                     None,
            #                     None,
            #                     None,
            #                     law.group(),
            #                     None,
            #                     None,
            #                     7
            #                 ]
        else :
            yield[
                law_id,
                numerical_symbol,
                content,
                None,
                None,
                None,
                None,
                None,
                None,
                7
            ]
    if(type == 5):
        location = re.search('(t|T)ên của\s.*\sđược\s((s|S)ửa đổi\,\s)*((b|B)ổ sung\s)*',content)
        if(location is not None):
            sub_content = location.group()
            text = re.search('(\"|\").*(\"|\")',content)
            t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
            extract = t.finditer(sub_content)
            if(lenIterator(extract)>0):
                for extract in t.finditer(sub_content):
                    temp_chapter = re.search(r'(c|C)hương\s(\w{1,10}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
                    if(temp_chapter is not None):
                        chapter = temp_chapter.group()
                    else:
                        chapter = None
                    temp_law = re.search(r'(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))',sub_content[extract.span()[0]:extract.span()[1]])
                    if(temp_law is not None):
                        law = temp_law.group()
                    else :
                        law = None
                    temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
                    if(temp_item is not None):
                        item = temp_item.group()
                    else :
                        item = None
                    temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',sub_content[extract.span()[0]:extract.span()[1]])
                    if(temp_point is not None):
                        point = temp_point.group()
                    else :
                        point = None
                    yield[
                        law_id,
                        numerical_symbol,
                        sub_content,
                        None,
                        text.group(),
                        chapter,
                        law,
                        item,
                        point,
                        5
                    ]
        else :
            yield[
                law_id,
                numerical_symbol,
                content,
                None,
                None,
                None,
                None,
                None,
                None,
                5
            ]
    if(type == 6):
        text = re.search('(\“|\"|\").*(\”|\"|\")',content)
        if(text is not None):
            t = re.compile(r'(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))\s(c|C)hương\s(\w{1,10}|\d{1,5})\s|(c|C)hương\s(\w{1,10}|\d{1,5})\s|(Đ|đ)iểm\s(\w{1,5}|\d{1,5})\s(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(k|K)hoản\s(\w{1,5}|\d{1,5})\s(Đ|đ)iều\s((\w{1,5})|(\d{1,5}))|(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))')
            extract = t.finditer(content)
            if(lenIterator(extract)>0):
                for extract in t.finditer(content):
                    temp_chapter = re.search(r'(c|C)hương\s(\w{1,10}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
                    if(temp_chapter is not None):
                        chapter = temp_chapter.group()
                    else:
                        chapter = None
                    temp_law = re.search(r'(đ|Đ)iều\s((\w{1,5})|(\d{1,5}))',content[extract.span()[0]:extract.span()[1]])
                    if(temp_law is not None):
                        law = temp_law.group()
                    else :
                        law = None
                    temp_item = re.search(r'(Khoản|khoản)\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
                    if(temp_item is not None):
                        item = temp_item.group()
                    else :
                        item = None
                    temp_point = re.search(r'(đ|Đ)iểm\s(\w{1,5}|\d{1,5})',content[extract.span()[0]:extract.span()[1]])
                    if(temp_point is not None):
                        point = temp_point.group()
                    else :
                        point = None
                    yield[
                        law_id,
                        numerical_symbol,
                        content,
                        None,
                        text.group(),
                        chapter,
                        law,
                        item,
                        point,
                        6
                    ]
        else :
            yield[
                law_id,
                numerical_symbol,
                content,
                None,
                None,
                None,
                None,
                None,
                None,
                6
            ]

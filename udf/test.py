# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# from util.processer import *
# from itertools import chain
# import psycopg2
# import codecs
# import re
#
# """
# Test processor
# """
#
#
# # tokens = ["toi", "la", "ai", "vay", "troi", "met", "khong", "ta"]
# # # print get_left_window(1, tokens, 4)
# # # print get_right_window(6, tokens, 2)
# # for phrase in get_all_phrases_in_sentence(tokens, 3):
# #     print phrase
#
#
# """
# Test extract M N
# """
# def extract_mn_phrase(begin_index, pos_tags, tokens):
#     num_tokens = len(pos_tags)
#     # find end of the M phrase
#     end_index = begin_index + 1
#     while end_index < num_tokens and pos_tags[end_index] == "M" and tokens[end_index] != "\\":
#         end_index += 1
#     end_index -= 1
#     # find end of the M N(Nu) phrase
#     if (end_index + 1) < num_tokens and (pos_tags[end_index + 1] == "N" or pos_tags[end_index + 1] == "Nu" and tokens[end_index + 1] != "\\"):
#         end_index += 1
#         return end_index
#     return -1
#
# # tokens = ["toi", "la", "ai", "vay", "\\", "\\", "khong", "ta"]
# # pos_tags = ["N", "A", "B", "C", "M", "N", "K", "H"]
# # end_inx = extract_mn_phrase(4, pos_tags, tokens)
# # if end_inx:
# #     print end_inx
# # else: print 'no found'
# # REGEX_MONEY_RANGE = r'^(?:\d+(?:\.0{3})+|[\w\s]+)\s+\u0111\u1ed3ng\s+\u0111\u1ebfn\s+(?:\d+(?:\.0{3})+|[\w\s]+)\s+\u0111\u1ed3ng'
# # REGEX_MONEY = r'^(?:\d+(?:\.0{3})+|[\w\s]+)\s+đồng'
# # line = '3.000.000 đồng đến 5.000.000 đồng'
# # line1 = '25.000.000 đồng'
# # TEST = r'^(?:\d+(?:\.0{3})+|[\p{L}\s_]+)\s+đồng\sđến\s(?:\d+(?:\.0{3})+|[\p{L}\s_]+)\s+đồng$'
# # obj = re.compile(REGEX_MONEY_RANGE, re.UNICODE)
# # print obj.match(line.decode('utf8'))
# # obj2 = re.compile(r'^\s+\w+\s+$', re.UNICODE)
# # print obj2.match(' đến '.decode('utf8')).group()
# # obj3 = re.compile(REGEX_MONEY, re.UNICODE)
# # print obj3.match(line1)
#
#
# # REGEX_MONEY_RANGE = r'^(?:\d+(?:\.0{3})+|[\w\s]+)\s+đồng(?:\s+\w+\s+)(?:\d+(?:\.0{3})+|[\w\s]+)\s+đồng$'
# # line = '3.000.000 đồng đến 5.000.000 đồng'
# # obj = re.compile(REGEX_MONEY_RANGE, re.UNICODE)
# # print obj.match(line)
# #
# # TEST = r'(?:\d+(?:\.0{3})+|[\w\s]+)\s+đồng(?:\s+[^\W\d_]+\s+)'
# # print re.compile(TEST, re.UNICODE).search('25.000 đồng đến '.decode('utf8'))
# #
# # p = re.compile(ur'(?:\d+(?:\.0{3})+|[\w\s]+)\s+đồng(?:\s+[^\W\d_]+\s+)', re.UNICODE)
# # test_str = u'3.000.000 đồng đến '
# #
# # print re.findall(p, test_str)
#
# # def extract_mn_phrase(begin_index, pos_tags, tokens, max_distance):
# #     num_tokens = len(pos_tags)
# #     # find end of the M phrase
# #     end_index = begin_index + 1
# #     while end_index < num_tokens and pos_tags[end_index] == "M":
# #         end_index += 1
# #     end_index -= 1
# #     # find end of the M N(Nu) phrase
# #     end_index += 1
# #     if not (end_index < num_tokens and (pos_tags[end_index] == "N" or pos_tags[end_index] == "Nu")):
# #         end_index = -1
# #
# #     if end_index >= 0:
# #         # Check whether have M N(Nu) - M N(Nu) or not
# #         for distance in range(1, max_distance + 1):
# #             if (end_index + distance + 1) < num_tokens and pos_tags[end_index + distance + 1] == "M":
# #                 temp = extract_mn_phrase(end_index + distance + 1, pos_tags, tokens, max_distance)
# #                 if temp >= 0:
# #                     end_index = temp
# #     return end_index
# #
# # pos_tags=['M','V','E','M','N']
# # tokens = ['06','tháng','đến','12','tháng']
# # print extract_mn_phrase(0,pos_tags,tokens, 4)
#
#
#
# # tokens = ['Phạt', 'tiền', 'từ', '200.000', 'đồng', 'đến', '300.000', 'đồng']
# # tokens1 = ['Gây', "thiệt_hại", 'về' ,"tài_sản", "1.500.000.000", "đồng", "trở_lên"]
# # MAX_PHRASE_LENGTH = 5
# # low_tokens = map(lambda token: token.lower(), tokens1)
# # left_window =  get_left_window(4, low_tokens, 10)
# # print '[DEBUG]: LEFT WINDOW:'
# # for i in left_window: print i
# # print '[DEBUG]: GENERATOR: '
# # for i in get_all_phrases_in_sentence(left_window, MAX_PHRASE_LENGTH): print i
# # phrases_in_sentence_left = list(get_all_phrases_in_sentence(left_window, MAX_PHRASE_LENGTH))
# # print 'Phrase in sentence lef:'
# # for i in phrases_in_sentence_left:
# #     print i
# #
# # APP_HOME = '/Users/anhbientuan/GoogleDrive/Learning/Hoc_Ki/Thesis/SourceCode/vnlaw-deepdive'
# # kw_non_legal_penalty = map(lambda word: word.strip(), open(APP_HOME + "/udf/dicts/kw_non_legal_penalty.txt", 'r').readlines())
# # kw_legal_penalty = map(lambda word: word.strip(), open(APP_HOME + "/udf/dicts/kw_legal_penalty.txt", 'r').readlines())
# #
# # # Non penalty signals on the left of candidate mention
# # NON_PENAL_SIGNALS_LEFT = frozenset(kw_non_legal_penalty)
# # # Penalty signals on the right of candidate mention
# # PENAL_SIGNALS_LEFT = frozenset(kw_legal_penalty)
# # print '### PENAL_SIGNALS_LEFT:'
# # for i in PENAL_SIGNALS_LEFT: print i
# #
# # if len(NON_PENAL_SIGNALS_LEFT.intersection(phrases_in_sentence_left)) > 0:
# #     print 'FOUND NON_PENAL_SIGNALS_LEFT'
# # else: print 'NOT FOUND NON_PENAL_SIGNALS_LEFT'
# #
# # if len(PENAL_SIGNALS_LEFT.intersection(phrases_in_sentence_left)) > 0:
# #     print 'FOUND NON_PENAL_SIGNALS_LEFT'
# # else: print 'NOT FOUND NON_PENAL_SIGNALS_LEFT'
tokens = ["e", ")", "Đối_với", "nhiều", "người", ";", "g", ")", "Phạm_tội", "nhiều", "lần", ";", "3", "."]
# tokens1 = ["e", ")", "Đối_với", "nhiều", "người", ";", "g", ")", "Phạm_tội", "nhiều", ".","lan", ";", "ke", "ho", "he", "ha", "oa", "."]
# tokens2 = ["Phat", "tien", "100.000", "dong", "đối_với", "di", "trai", "phep", "Phạm_tội", "nhiều", ".","lan", "ho", "he", "ha", "oa" "."]
# def extract_phrase_list(tokens, begin_list):
#     num_tokens = len(tokens)
#     i = begin_list
#     while i < num_tokens:
#         if i + 3 < num_tokens: begin_phrase = i + 2
#         else: break
#         j = begin_phrase + 1
#         while j < num_tokens:
#             if (tokens[j] == ";" and (j + 2) < num_tokens and re.search("\w", tokens[j + 1]) and tokens[j + 2] == ")") or j == num_tokens - 1:
#                 end_phrase = j - 1
#                 i = end_phrase + 2
#                 print " ".join(word for word in tokens[begin_phrase: end_phrase + 1])
#                 mention_text = " ".join(map(lambda k: tokens[k].replace('\\', '\\\\'), range(begin_phrase, end_phrase + 1)))
#                 print mention_text
#                 yield (begin_phrase, end_phrase)
#                 break
#             else: j += 1
#
#
# def extract_sentence(tokens, penalty_end_index):
#     num_tokens = len(tokens)
#     i = penalty_end_index + 1
#     while i < num_tokens:
#         if (i + 1) < num_tokens and tokens[i] == "đối_với" and (tokens[i + 1] == "hành_vi" or tokens[i + 1] == "trường_hợp") or ((i + 1) < num_tokens and tokens[i] == "trong" and tokens[i + 1] == "trường_hợp"):
#             begin_phrase = i + 2
#             if tokens[num_tokens - 1] == ".": end_phrase = num_tokens - 2
#             else: end_phrase = num_tokens -1
#             break
#         elif tokens[i] == "đối_với" or tokens[i] == "nếu":
#             begin_phrase = i + 1
#             if tokens[num_tokens - 1] == ".": end_phrase = num_tokens - 2
#             else: end_phrase = num_tokens -1
#             break
#         else: i += 1
#     # print " ".join(word for word in tokens[begin_phrase: end_phrase + 1])
#     return (begin_phrase, end_phrase)
#
# for result in extract_phrase_list(tokens3, 0): print result
# # for result in extract_sentence(tokens3, 0): print result



def find_character(tokens, start, character):
    i = start + 1
    num_tokens = len(tokens)
    while i < num_tokens:
        if tokens[i] == character: return i
        else: i += 1

print find_character(tokens, 2, ")")
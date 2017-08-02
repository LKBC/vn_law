#!/usr/bin/env python
# coding=utf-8
from deepdive import *
import sys, re


def extract_phrase_list(tokens, begin_list):
    num_tokens = len(tokens)
    i = begin_list
    while i < num_tokens:
        if i + 3 < num_tokens: begin_phrase = i + 2
        else: break
        j = begin_phrase + 1
        while j < num_tokens:
            if (tokens[j] == ";" and (j + 2) < num_tokens and re.search("\w", tokens[j + 1]) and tokens[j + 2] == ")") or j == num_tokens - 1:
                end_phrase = j - 1
                i = end_phrase + 2
                yield (begin_phrase, end_phrase)
                break
            else: j += 1

def is_phrase_list_block(tokens):
    num_tokens = len(tokens)
    i = 0
    while i < num_tokens:
        if (i + 2) < num_tokens and tokens[i] == ":" and re.search("\w", tokens[i + 1]) and tokens[i + 2] == ")":
            return True
        else: i += 1
    return False

def get_string(tokens, start, length):
    if (start + length) < len(tokens):
        return " ".join(word for word in tokens[start + 1: start + length + 1])

def find_character(tokens, start, character):
    i = start + 1
    num_tokens = len(tokens)
    while i < num_tokens:
        if tokens[i] == character: return i
        else: i += 1

@tsv_extractor
@returns(lambda
                 mention_id="text",
                 mention_text="text",
                 mention_type="text",
                 doc_id="text",
                 sentence_index="int",
                 begin_index="int",
                 end_index="int",
                 associated_penalty_id="text"

         : [])
def extract(
        doc_id="text",
        sentence_index="int",
        tokens="text[]",
        pos_tags="text[]",
        penalty_id="text",
        penalty_begin_index="int",
        penalty_end_index="int"
):
    num_tokens = len(tokens)
    is_passed = True

    # [PENALTY] ... : a ) ...
    i = penalty_end_index + 1
    phrase_list = None
    if is_phrase_list_block(tokens):
        phrase_list = extract_phrase_list(tokens, i + 1)
        is_passed = False

    if phrase_list:
        for begin, end in phrase_list:
            begin_index = begin
            end_index = end
            # generate a mention identifier
            mention_id = "{}_{}_{}_{}".format(doc_id, sentence_index, begin_index, end_index)
            mention_text = " ".join(map(lambda k: tokens[k].replace('\\', '\\\\'), range(begin_index, end_index + 1)))
            mention_type = "PHRASE_LIST"
            associated_penalty_id = penalty_id
            # print >> sys.stderr, "MENTION TYPE: {} AND MENTION ID: {} AND MENTION_TEXT: {}".format(mention_type, mention_id, mention_text)
            # Output a tuple for each founded phrase
            yield [
                mention_id,
                mention_text,
                mention_type,
                doc_id,
                sentence_index,
                begin_index,
                end_index,
                associated_penalty_id
            ]

    # [PENALTY] ... (nếu | đối_với hành_vi | đối_với trường_hợp | đối_với | trong trường_hợp)
    KW1 = ["nếu", "đối_với"]
    KW2 = ["đối_với hành_vi", "đối_với trường_hợp", "trong trường_hợp"]
    if is_passed:
        begin_phrase = None
        end_phrase = None
        if get_string(tokens, penalty_end_index, 2) in KW2:
            begin_phrase = penalty_end_index + 3
        elif get_string(tokens, penalty_end_index, 1) in KW1:
            begin_phrase = penalty_end_index + 2
        if begin_phrase:
            if is_phrase_list_block(tokens): end_phrase = find_character(tokens, begin_phrase, ";") - 1
            else:
                if tokens[num_tokens - 1] == ".": end_phrase = num_tokens - 2
                else: end_phrase = num_tokens -1

        if begin_phrase and end_phrase:
            begin_index = begin_phrase
            end_index = end_phrase
            # generate a mention identifier
            mention_id = "{}_{}_{}_{}".format(doc_id, sentence_index, begin_index, end_index)
            mention_text = " ".join(map(lambda k: tokens[k].replace('\\', '\\\\'), range(begin_index, end_index + 1)))
            mention_type = "IN_ONE_SENTENCE"
            associated_penalty_id = penalty_id
            # print >> sys.stderr, "MENTION TYPE: {} AND MENTION ID: {}".format(mention_type, mention_id)
            # Output a tuple for each founded phrase
            yield [
                mention_id,
                mention_text,
                mention_type,
                doc_id,
                sentence_index,
                begin_index,
                end_index,
                associated_penalty_id
            ]
#!/usr/bin/env python
# coding=utf-8
from deepdive import *
import re
from collections import namedtuple
from util.processer import *
import os, sys

CrimeLabel = namedtuple('CrimeLabel', 'p_id, label, type')


@tsv_extractor
@returns(lambda
                 p_id="text",
                 label="int",
                 rule_id="text",
         : [])
# heuristic rules for finding positive/negative examples of spouse relationship mentions
def supervise(
        p_id="text", p_begin="int", p_end="int",
        doc_id="text", sentence_index="int", sentence_text="text",
        tokens="text[]", pos_tags="text[]", ner_tags="text[]",
        dep_types="text[]", dep_heads="int[]", label="int"
):
    # # Read keywords from file
    # APP_HOME = os.environ['APP_HOME']
    # kw_non_legal_penalty = map(lambda word: word.strip(), open(APP_HOME + "/udf/dicts/kw_non_crime.txt", 'r').readlines())
    # kw_legal_penalty = map(lambda word: word.strip(), open(APP_HOME + "/udf/dicts/kw_crime.txt", 'r').readlines())

    # Non penalty signals on the left of candidate mention
    # NON_PENAL_SIGNALS_LEFT = frozenset(kw_non_legal_penalty)
    # Penalty signals on the left of candidate mention
    # PENAL_SIGNALS_LEFT = frozenset(kw_legal_penalty)

    crime = CrimeLabel(p_id=p_id, label=None, type=None)

    # Negative rules
    if label < 0:
        yield crime._replace(label=1, type="neg:legal_penalty_false")



    # Positive rules
    # Ruile 1:
    if label > 0:
        yield crime._replace(label=1, type="pos:legal_penalty_true")
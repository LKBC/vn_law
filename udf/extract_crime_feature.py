#!/usr/bin/env python
# coding=utf-8
from deepdive import *
import ddlib
import os,sys
from util.processer import  *

@tsv_extractor
@returns(lambda
                 p_id   = "text",
                 feature = "text",
         :[])
def extract(
        p_id          = "text",
        p_begin_index = "int",
        p_end_index   = "int",
        doc_id         = "text",
        sent_index     = "int",
        tokens         = "text[]",
        pos_tags       = "text[]",
        ner_tags       = "text[]",
        dep_types      = "text[]",
        dep_parents    = "int[]",
):
    """
    Uses DDLIB to generate features for the legal penalty mention
    """
    # Constant
    # WINDOW_SIZE = 10

    # Load keyword dictionaries using ddlib, for domain-specific features
    # Words in "legal_penalty" dictionary are indicative of marriage
    # Words in "non_legal_penalty" dictionary are indicative of non_marriage
    APP_HOME = os.environ['APP_HOME']
    ddlib.load_dictionary(APP_HOME + "/udf/dicts/kw_crime.txt", dict_id="crime")
    ddlib.load_dictionary(APP_HOME + "/udf/dicts/kw_non_crime.txt", dict_id="non_crime")

    # kw_non_legal_penalty = map(lambda word: word.strip(), open(APP_HOME + "/udf/dicts/kw_non_legal_penalty.txt", 'r').readlines())
    # kw_legal_penalty = map(lambda word: word.strip(), open(APP_HOME + "/udf/dicts/kw_legal_penalty.txt", 'r').readlines())
    # Non penalty signals on the left of candidate mention
    # NON_PENAL_SIGNALS_LEFT = frozenset(kw_non_legal_penalty)
    # Penalty signals on the right of candidate mention
    # PENAL_SIGNALS_LEFT = frozenset(kw_legal_penalty)

    WINDOW_SIZE = 10
    MAX_PHRASE_LENGTH = 5

    # Get all subsequences of left sentence with WINDOW_SIZE = 10
    low_tokens = map(lambda token: token.lower(), tokens)
    left_window = get_left_window(p_begin_index, low_tokens, WINDOW_SIZE)
    phrases_in_sentence_left = list(get_all_phrases_in_sentence(left_window, MAX_PHRASE_LENGTH))

    # Create a DDLIB sentence object, which is just a list of DDLIB Word objects
    sent = []
    for i, t in enumerate(tokens):
        sent.append(ddlib.Word(
            begin_char_offset=None,
            end_char_offset=None,
            word=t,
            lemma=t.lower(),  # lemma for vietnamese: lowercase
            pos=pos_tags[i],
            ner=ner_tags[i],
            dep_par=dep_parents[i] - 1,  # Note that as stored from CoreNLP 0 is ROOT, but for DDLIB -1 is ROOT
            dep_label=dep_types[i]))

    # Create DDLIB Span for penalty candidate
    penalty_span = ddlib.Span(begin_word_id=p_begin_index, length=(p_end_index - p_begin_index + 1))

    # Generate the generic features using DDLIB on left and right window
    for feature in ddlib.get_generic_features_mention(sent, penalty_span):
        yield [p_id, feature]

    # # Keywords represent non-legal_penalty appears on the left
    # if len(NON_PENAL_SIGNALS_LEFT.intersection(phrases_in_sentence_left)) > 0:
    #     yield [p_id, 'APPEAR_LEFT_KW_NON_LEGAL_PENALTY']
    #
    # # "phạt tù" appear on the left of mention
    # if "phạt tù" in phrases_in_sentence_left:
    #     yield [p_id, 'APPEAR_LEFT_PHAT_TU']

    # # Keywords represent legal_penalty appears on the left
    # if len(PENAL_SIGNALS_LEFT.intersection(phrases_in_sentence_left)) > 0:
    #     yield [p_id, 'APPEAR_LEFT_KW_LEGAL_PENALTY']

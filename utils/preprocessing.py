# -*- coding: utf-8 -*-

import string
import re
from nltk.tokenize import TweetTokenizer
from time import time
import unicodedata

regexes = {
    'QUOTES': r'(\"(\\.|[^\"]){2,}\")|(\“(\\.|[^\”]){2,}\”)',
    'URL': r'(?:https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})|(https?:[\S]*…)',
    'EMAIL': r'(?:^|(?<=[^\w@.)]))(?:[\w+-](?:\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(?:\.(?:[a-z]{2,})){1,3}(?:$|(?=\b))',
    'PHONE': r'(?<![0-9])(?:\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?![0-9])',
    'T_HEAD': r'^(RT|HT|MT) @\w+: ',
    'UNAME': r'\@\w+',
    'NOO': r'(9\.11)|(9/11)|(11/9)|((?<= )911)',
    'KKK': r'(KKK)|(kkk)',
    'MONEY': r'(?:[$€£¢]\d+(?:[\.,\']\d+)?(?:[MmKkBb](?:n|(?:il(?:lion)?))?)?)|(?:\d+(?:[\.,\']\d+)?[$€£¢])',
    'PERCENT': r"\b\d+(?:[\.,']\d+)?\b",
    'NUMBER': r'\b\d+(?:[\.,\']\d+)?\b',
    'TIME': r'(?:(?:\d+)?\.?\d+(?:AM|PM|am|pm|a\.m\.|p\.m\.))|(?:(?:[0-2]?[0-9]|[2][0-3]):(?:[0-5][0-9])(?::(?:[0-5][0-9]))?(?: ?(?:AM|PM|am|pm|a\.m\.|p\.m\.))?)',
    'DATE': r'',
    
    'EMPHASIS': r'(?:\*\b\w+\b\*)',
    'HASHTAG': r'\#+\b[\w\-\_]+\b',
    'INVALID_HASHTAG': r'(\#+\s+)|(\#+[^\w\s]+)',
    'REPEAT_PUNCTS': r'([!?.*]){2,}',
    'CENSORED': r'(?:\b\w+\*+\w+\b)',
    
    'CAMEL_SPLIT': r'((?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])|[0-9]+|(?<=[0-9\-\_])[A-Za-z]|[\-\_])'
}

tokenizer = TweetTokenizer()

to_tag = ['URL', 'EMAIL', 'PHONE', 'T_HEAD', 'UNAME', 'NOO', 'KKK', 'MONEY', 'PERCENT', 'TIME', 'NUMBER', 'CENSORED']

def unpack_contractions(text):
    """
    Replace *English* contractions in the text str with their unshortened forms.
    N.B. The "'d" and "'s" forms are ambiguous (had/would, is/has/possessive),
    so are left as-is.
    ---------
    ---------
    Important Note: The function is taken from textacy (https://github.com/chartbeat-labs/textacy).
    See textacy.preprocess.unpack_contractions(text)
    -> http://textacy.readthedocs.io/en/latest/api_reference.html#textacy.preprocess.unpack_contractions
    The reason that textacy is not added as a dependency is to avoid having the user to install it's dependencies (such as SpaCy),
    in order to just use this function.
    """
    # standard
    text = re.sub(
        r"(\b)([Aa]re|[Cc]ould|[Dd]id|[Dd]oes|[Dd]o|[Hh]ad|[Hh]as|[Hh]ave|[Ii]s|[Mm]ight|[Mm]ust|[Ss]hould|[Ww]ere|[Ww]ould)n't",
        r"\1\2 not", text)
    text = re.sub(
        r"(\b)([Hh]e|[Ii]|[Ss]he|[Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Yy]ou)'ll",
        r"\1\2 will", text)
    text = re.sub(r"(\b)([Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Yy]ou)'re", r"\1\2 are",
                  text)
    text = re.sub(
        r"(\b)([Ii]|[Ss]hould|[Tt]hey|[Ww]e|[Ww]hat|[Ww]ho|[Ww]ould|[Yy]ou)'ve",
        r"\1\2 have", text)
    # non-standard
    text = re.sub(r"(\b)([Cc]a)n't", r"\1\2n not", text)
    text = re.sub(r"(\b)([Ii])'m", r"\1\2 am", text)
    text = re.sub(r"(\b)([Ll]et)'s", r"\1\2 us", text)
    text = re.sub(r"(\b)([Ww])on't", r"\1\2ill not", text)
    text = re.sub(r"(\b)([Ss])han't", r"\1\2hall not", text)
    text = re.sub(r"(\b)([Yy])(?:'all|a'll)", r"\1\2ou all", text)
    return text

def remove_repeat_puncts(m):
    text = m.group()
    text = "".join(sorted(set(text), reverse=True))
    return text

def unpack_emphasis(m):
    return m.group().replace('*', '')

def unpack_quotes(m):
    return m.group().replace('"', ' ').replace('"', ' ').replace(u'“', ' ').replace(u'”', ' ')


def clean_sentence(s):
    """
    Perform initial normalization on sentence.
    """
    #s = unicodedata.normalize('NFD', s)
    #s = s.encode('utf-8', 'ignore')
    s = s.decode("utf-8")
    s = re.sub(r' +', ' ', s.strip())
    
    # Part1: remove invalid or duplicated chars/segmentations
    s = re.sub(regexes['REPEAT_PUNCTS'], lambda x: remove_repeat_puncts(x), s)
    s = re.sub(regexes['INVALID_HASHTAG'], ' ', s)
    s = re.sub('&amp;', ' ', s)
    
    # Part2: unpack wrapped contents
    s = re.sub(regexes['EMPHASIS'], lambda x: unpack_emphasis(x), s)
    s = re.sub(regexes['QUOTES'], lambda x: unpack_quotes(x), s)
    
    # Part3: replace some categorial words with categorial tag
    for t in to_tag:
        s = re.sub(regexes[t], '<'+t+'>', s)
    
    # Part4: deal with hashtags
    # For this moment, let's keep the hash tags as valid words.
    
    # tokenize
    s = ' '.join(tokenizer.tokenize(s))
    # remove repeating spaces and leading/tailing spaces
    s = re.sub(r' +', ' ', s.strip())
    return s

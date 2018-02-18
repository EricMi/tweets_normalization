# -*- coding: utf-8 -*-

import string
import re
from nltk.tokenize import TweetTokenizer
from time import time

regexes = {
    'QUOTES': r'(\"[^\"]{2,}\")|(“[^”]{2,}”)',
    'URL': r'(https|http):[\S^\"^\”^\']+',
    'HEAD': r'^(RT|HT|MT) @\w+: ',
    'UNAME': r'@[\w]+',
    'EMPHASIX': '(?:\*[^\*]+\*)',
    'NUMBER': r'\b\d+(?:[.,\']\d+)?\b',
    'EMAIL': r'(?:^|(?<=[^\w@.)]))(?:[\w+-](?:\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(?:\.(?:[a-z]{2,})){1,3}(?:$|(?=\b))',
    'INVALID_HASHTAG': r'#[^\w][\S]*',
    'REPEAT_PUNCTS' : '([!?.]){2,}'
}

tokenizer = TweetTokenizer()

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

def unpack_quotes(m):
    return m.group().replace('"', '').replace('“', '').replace('”', '')

def unpack_emphasis(m):
    return m.group().replace('*', '')

def remove_repeat_puncts(m):
    text = m.group()
    text = "".join(sorted(set(text), reverse=True))
    return text

def unpack_number(m):
    return 'NUMERIC_VALUE'

def unpack_email(m):
    return "EMAIL_ADDRESS"

def clean_sentence(s):
    """
    Perform initial normalization on sentence.
    """
    # unpack quotes
    s = re.sub(regexes['QUOTES'], lambda x: unpack_quotes(x), s)
    # remove url
    s = re.sub(regexes['URL'], ' ', s)
    # unpack contractions
    s = unpack_contractions(s)
    # remove tweets head (RT|MT|HT) and username
    s = re.sub(regexes['HEAD'], ' ', s)
    s = re.sub(regexes['UNAME'], ' ', s)
    # unpack emphasis
    s = re.sub(regexes['EMPHASIX'], lambda x: unpack_emphasis(x), s)
    # unpack numeric value
    s = re.sub(regexes['NUMBER'], lambda x: unpack_number(x), s)
    # unpack email address
    s = re.sub(regexes['EMPHASIX'], lambda x: unpack_email(x), s)
    # remove repeat punctuations
    s = re.sub(regexes['REPEAT_PUNCTS'], lambda x: remove_repeat_puncts(x), s)
    # remove invalid hashtag
    s = re.sub(regexes['INVALID_HASHTAG'], ' ', s)
    # tokenize
    s = ' '.join(tokenizer.tokenize(s))
    # remove repeating spaces and leading/tailing spaces
    s = re.sub(r' +', ' ', s).strip()
    return s
    

def clean_corpus(f_in, f_out, head=0):
    """
    Clean a whole corpus file and write cleaned sentences line by line into the output file.
    f_in: input (raw corpus) file path
    f_out: output (cleaned corpus) file path
    """
    start = time()
    print "Starting clean corpus..."
    with open(f_in, 'r') as raw_file:
        cleaned_file = open(f_out, 'w')
        for i, line in enumerate(raw_file):
            if i % 50000 == 0 and i > 0:
                print "%d lines done..." % i
            cleaned_l = clean_sentence(line)
            if len(cleaned_l) > 0:
                cleaned_file.write("%s\n" % cleaned_l.encode('utf-8'))
            if head > 0 and i > head:
                break
        raw_file.close()
        cleaned_file.close()
    print "Corpus clean done in %0.3fs." % (time() - start)

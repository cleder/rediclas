# -*- coding: utf-8 -*-
import sys, os
import re
import unicodedata
import redis


PAT_ALPHABETIC = re.compile('(((?![\d])\w)+)', re.UNICODE)
DEACCENT = True
redis_server = None

def redis_from_config(config):
    rh = config.registry.settings['redis.host']
    rp = int(config.registry.settings['redis.port'])
    rd = int(config.registry.settings['redis.db'])
    rs = redis.Redis(host=rh, port=rp, db=rd)
    return rs

def deaccent(text):
    """
    Remove accentuation from the given string. Input text is either a unicode string or utf8 encoded bytestring.

    Return input string with accents removed, as unicode.

    >>> deaccent("Šéf chomutovských komunistů dostal poštou bílý prášek")
    u'Sef chomutovskych komunistu dostal postou bily prasek'
    """
    if not isinstance(text, unicode):
        text = unicode(text, 'utf8') # assume utf8 for byte strings, use default (strict) error handling
    norm = unicodedata.normalize("NFD", text)
    result = u''.join(ch for ch in norm if unicodedata.category(ch) != 'Mn')
    return unicodedata.normalize("NFC", result)


def tokenize(text, lowercase=False, deacc=False, errors="strict"):
    """
    Iteratively yield tokens as unicode strings, optionally also lowercasing them
    and removing accent marks.

    Input text may be either unicode or utf8-encoded byte string.

    The tokens on output are maximal contiguous sequences of alphabetic
    characters (no digits!).

    >>> list(tokenize('Nic nemůže letět rychlostí vyšší, než 300 tisíc kilometrů za sekundu!', deacc = True))
    [u'Nic', u'nemuze', u'letet', u'rychlosti', u'vyssi', u'nez', u'tisic', u'kilometru', u'za', u'sekundu']
    """
    if not isinstance(text, unicode):
        text = unicode(text, encoding='utf8', errors=errors)
    if lowercase:
        text = text.lower()
    if deacc:
        text = deaccent(text)
    for match in PAT_ALPHABETIC.finditer(text):
        yield match.group()


def simple_preprocess(doc, deacc=True):
    """
    Convert a document into a list of tokens.

    This lowercases, tokenizes, stems, normalizes etc. -- the output are final,
    utf8 encoded strings that won't be processed any further.
    """
    tokens = [token.encode('utf8') for token in tokenize(doc, lowercase=True, deacc=deacc, errors='ignore')
            if 2 <= len(token) <= 15 and not token.startswith('_')]
    return tokens


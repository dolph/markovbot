import re

import db


_DICTIONARY = None
_IGNORED_WORDS = None
_ALL_WORDS = None

def load_words(filename):
    try:
        fp = open(filename, 'r')
        words = fp.readlines()
    finally:
        fp.close()

    return set(word.strip() for word in words)


def get_dictionary():
    global _DICTIONARY

    if _DICTIONARY is None:
        _DICTIONARY = load_words('popular.txt')

    return _DICTIONARY


def get_ignored_words():
    global _IGNORED_WORDS

    if _IGNORED_WORDS is None:
        _IGNORED_WORDS = load_words('ignore.txt')

    return _IGNORED_WORDS


def get_all_words():
    global _ALL_WORDS

    if _ALL_WORDS is None:
        _ALL_WORDS = get_dictionary().union(get_ignored_words())

    return _ALL_WORDS


def slugify(s):
    s = s.lower()
    s = s.replace(' ', '_')
    s = s.replace('-', '_')
    s = s.replace('/', '_')
    s = s.replace('.', '_')
    s = re.sub('\W', '', s)
    s = s.replace('_', ' ')
    s = re.sub('\s+', ' ', s)
    s = s.strip()
    s = s.replace(' ', '-')
    return s


def simplify(s):
    s = s.split(' ')

    for i, w in enumerate(s):
        slug = slugify(w)

        if slug in get_dictionary():
            s[i] = slug

    return ' '.join(s)


def topics(s):
    topics = set(slugify(s).split('-'))
    topics = topics.difference(get_ignored_words())
    return topics


def useful(s):
    s = set(slugify(s).split('-'))
    pronouns = s.difference(get_all_words())
    pronoun_ratio = 1.0 * len(pronouns) / len(s)
    return pronoun_ratio <= .15


def consume(s):
    s = simplify(s)

    if not s or not useful(s):
        print 'Ignoring', s
        return

    s = s.split(' ')

    for i, w in enumerate(s):
        w1 = s[i]
        w2 = s[i + 1] if i + 1 < len(s) else None
        w3 = s[i + 2] if i + 2 < len(s) else None

        if i == 0:
            db.add_link(None, w1, w2)

        if w2 is not None:
            db.add_link(w1, w2, w3)


def produce(w=None):
    s = []

    w1, w2 = db.get_first()
    s.append(w1)
    if w2:
        s.append(w2)

    w3 = True
    while w1 and w2 and w3:
        w3 = db.get_next(w1, w2)

        if w3 is not None:
            s.append(w3)

        w1 = w2
        w2 = w3

    return ' '.join(s)

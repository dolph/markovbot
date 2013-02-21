import random
import re


_DATA = {}


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


def consume(s):
    s = slugify(s)
    s = s.split('-')

    for i, w in enumerate(s):
        if i == 0:
            _DATA.setdefault(None, [])
            _DATA[None].append(w)

        if i + 1 == len(s):
            next_ = None
        else:
            next_ = s[i + 1]

        _DATA.setdefault(w, [])
        _DATA[w].append(next_)


def produce(w=None):
    s = []

    w = get_next_word()
    while w:
        s.append(w)
        w = get_next_word(w)

    return ' '.join(s)


def get_next_word(w=None):
    words = list(_DATA[w])
    random.shuffle(words)
    return words.pop()

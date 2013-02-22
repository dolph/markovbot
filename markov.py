import re

import db


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

import random
import re

import sqlalchemy as sql
from sqlalchemy import orm
from sqlalchemy.ext import declarative


engine = sql.create_engine('sqlite:///markov.db', echo=False)
Session = orm.sessionmaker(bind=engine)
Base = declarative.declarative_base()


class Link(Base):
    __tablename__ = 'links'

    id = sql.Column(sql.Integer, primary_key=True)
    word = sql.Column(sql.String, index=True)
    next_word = sql.Column(sql.String)


Base.metadata.create_all(engine)


def reset():
    session = Session()
    session.query(Link).delete()
    session.commit()


def add_link(w1, w2):
    session = Session()
    ref = Link(word=w1, next_word=w2)
    session.add(ref)
    session.commit()


def get_next(w=None):
    session = Session()
    words = [r.next_word for r in session.query(Link).filter_by(word=w).all()]
    random.shuffle(words)
    return words.pop()


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
            add_link(None, w)

        if i + 1 == len(s):
            w2 = None
        else:
            w2 = s[i + 1]

        add_link(w, w2)


def produce(w=None):
    s = []

    w = get_next()
    while w:
        s.append(w)
        w = get_next(w)

    return ' '.join(s)

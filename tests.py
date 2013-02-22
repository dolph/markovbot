import unittest

import db
import markov


class TestChains(unittest.TestCase):
    def tearDown(self):
        db.reset()

    def test_consume_one_word(self):
        markov.consume('Word.')

        self.assertEqual(db.list_next(None, 'word'), [None])

    def test_consume_str(self):
        markov.consume('This is a very simple test.')

        self.assertEqual(db.list_next(None, 'this'), ['is'])
        self.assertEqual(db.list_next('this', 'is'), ['a'])
        self.assertEqual(db.list_next('is', 'a'), ['very'])
        self.assertEqual(db.list_next('a', 'very'), ['simple'])
        self.assertEqual(db.list_next('very', 'simple'), ['test'])
        self.assertEqual(db.list_next('simple', 'test'), [None])

    def test_consume_str_with_multiple_paths(self):
        markov.consume('This is a test and is a loop.')

        self.assertEqual(db.list_next(None, 'this'), ['is'])
        self.assertEqual(db.list_next('this', 'is'), ['a'])
        self.assertEqual(db.list_next('is', 'a'), ['test', 'loop'])
        self.assertEqual(db.list_next('a', 'test'), ['and'])
        self.assertEqual(db.list_next('test', 'and'), ['is'])
        self.assertEqual(db.list_next('and', 'is'), ['a'])
        self.assertEqual(db.list_next('a', 'loop'), [None])

    def test_consume_multiple_strings(self):
        markov.consume('This is a test.')
        markov.consume('This is a statement.')
        markov.consume('This sentence is short.')

        self.assertIn(markov.produce(), [
            'this is a test',
            'this is a statement',
            'this sentence is short',
            'this sentence is a test',
            'this sentence is a statement',
        ])

    def test_produce_string(self):
        markov.consume('This is a very simple test.')
        self.assertEqual(markov.produce(), 'this is a very simple test')


class TestReduction(unittest.TestCase):
    def test_topics(self):
        s = markov.topics('Hello, my name is Dolph, how are you?')
        self.assertEqual(s, set(['hello', 'name', 'dolph']))

    def test_topics_archer(self):
        s = markov.topics(
            'Pam: So are all kinds of shit, but look at these odds. Half the '
            'people that work here are field agents...')
        self.assertEqual(
            s,
            set(['pam', 'shit', 'odds', 'people', 'field', 'work', 'agents']))

    def test_simplify(self):
        s = markov.simplify('Hello, my name is Dolph, how are you?')
        self.assertEqual(s, 'hello my name is Dolph, how are you')

    def test_useful(self):
        self.assertTrue(markov.useful('Hello, my name is Dolph, how are you?'))
        self.assertFalse(markov.useful('This is a link to Google http://google.com/'))


if __name__ == '__main__':
    unittest.main()

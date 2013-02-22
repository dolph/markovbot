import unittest

import db
import markov


class TestChains(unittest.TestCase):
    def tearDown(self):
        db.reset()

    def test_consume_one_word(self):
        markov.consume('Word.')

        self.assertEqual(db.list_next(None, 'Word.'), [None])

    def test_consume_str(self):
        markov.consume('This is a very simple test.')

        self.assertEqual(db.list_next(None, 'This'), ['is'])
        self.assertEqual(db.list_next('This', 'is'), ['a'])
        self.assertEqual(db.list_next('is', 'a'), ['very'])
        self.assertEqual(db.list_next('a', 'very'), ['simple'])
        self.assertEqual(db.list_next('very', 'simple'), ['test.'])
        self.assertEqual(db.list_next('simple', 'test.'), [None])

    def test_consume_str_with_multiple_paths(self):
        markov.consume('This is a test and is a loop.')

        self.assertEqual(db.list_next(None, 'This'), ['is'])
        self.assertEqual(db.list_next('This', 'is'), ['a'])
        self.assertEqual(db.list_next('is', 'a'), ['test', 'loop.'])
        self.assertEqual(db.list_next('a', 'test'), ['and'])
        self.assertEqual(db.list_next('test', 'and'), ['is'])
        self.assertEqual(db.list_next('and', 'is'), ['a'])
        self.assertEqual(db.list_next('a', 'loop.'), [None])

    def test_consume_multiple_strings(self):
        markov.consume('This is a test.')
        markov.consume('This is a statement.')
        markov.consume('This sentence is short.')

        self.assertIn(markov.produce(), [
            'This is a test.',
            'This is a statement.',
            'This sentence is short.',
            'This sentence is a test.',
            'This sentence is a statement.',
        ])

    def test_produce_string(self):
        markov.consume('This is a very simple test.')
        self.assertEqual(markov.produce(), 'This is a very simple test.')


if __name__ == '__main__':
    unittest.main()

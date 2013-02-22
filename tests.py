import unittest

import markov


class TestChains(unittest.TestCase):
    def tearDown(self):
        markov.reset()

    def test_consume_str(self):
        markov.consume('This is a very simple test.')

        self.assertEqual(markov.list_next(None, 'this'), ['is'])
        self.assertEqual(markov.list_next('this', 'is'), ['a'])
        self.assertEqual(markov.list_next('is', 'a'), ['very'])
        self.assertEqual(markov.list_next('a', 'very'), ['simple'])
        self.assertEqual(markov.list_next('very', 'simple'), ['test'])
        self.assertEqual(markov.list_next('simple', 'test'), [None])

    def test_consume_str_with_multiple_paths(self):
        markov.consume('This is a test and is a loop.')

        self.assertEqual(markov.list_next(None, 'this'), ['is'])
        self.assertEqual(markov.list_next('this', 'is'), ['a'])
        self.assertEqual(markov.list_next('is', 'a'), ['test', 'loop'])
        self.assertEqual(markov.list_next('a', 'test'), ['and'])
        self.assertEqual(markov.list_next('test', 'and'), ['is'])
        self.assertEqual(markov.list_next('and', 'is'), ['a'])
        self.assertEqual(markov.list_next('a', 'loop'), [None])

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


if __name__ == '__main__':
    unittest.main()

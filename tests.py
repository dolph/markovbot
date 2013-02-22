import unittest

import markov


class TestChains(unittest.TestCase):
    def tearDown(self):
        markov.reset()

    def test_consume_str(self):
        markov.consume('This is a very simple test.')
        """
        self.assertEqual(markov._DATA, {
            None: ['this'],
            'this': ['is'],
            'is': ['a'],
            'a': ['very'],
            'very': ['simple'],
            'simple': ['test'],
            'test': [None],
        })
        """

    def test_consume_str_with_multiple_paths(self):
        markov.consume('This is a test and is a loop.')
        """
        self.assertEqual(markov._DATA, {
            None: ['this'],
            'this': ['is'],
            'is': ['a', 'a'],
            'a': ['test', 'loop'],
            'test': ['and'],
            'and': ['is'],
            'loop': [None],
        })
        """

    def test_consume_multiple_strings(self):
        markov.consume('This is a test.')
        markov.consume('This is a statement.')
        markov.consume('This sentence is short.')
        """
        self.assertEqual(markov._DATA, {
            None: ['this', 'this', 'this'],
            'this': ['is', 'is', 'sentence'],
            'sentence': ['is'],
            'is': ['a', 'a', 'short'],
            'a': ['test', 'statement'],
            'statement': [None],
            'short': [None],
            'test': [None],
        })
        """

        self.assertIn(markov.produce(), [
            'this is a test',
            'this is a statement',
            'this sentence is short',
            'this is short',
            'this sentence is a test',
            'this sentence is a statement',
        ])

    def test_produce_string(self):
        markov.consume('This is a very simple test.')
        self.assertEqual(markov.produce(), 'this is a very simple test')


if __name__ == '__main__':
    unittest.main()

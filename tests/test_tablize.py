from wingcommander import tablize
import unittest


class TestTablize(unittest.TestCase):
    data_list = [
        ["python", "multiparadigm", "ducktyped", "python"],
        ["ruby", "object oriented", "ducktyped", "ruby"],
        ["c++", "object oriented", "static", "g++"],
        ["haskell", "functional", "static", "ghc"]
    ]

    def test_basic(self):
        ''' Checks the basic functionality of `tablize`
        Just provides a basic dataset and makes sure the expected layout is
        returned.
        '''
        self.assertEqual('''
 python |   multiparadigm | ducktyped | python
   ruby | object oriented | ducktyped |   ruby
    c++ | object oriented |    static |    g++
haskell |      functional |    static |    ghc''',
                         '\n'.join([''] + tablize(self.data_list)))

    def test_labels(self):
        ''' Tests that the top row is an aligned set of column labels
        If the keyword 'labels' is set, the top row is for labelling the
        columns.  The labels truncate against the columns.
        '''
        self.assertEqual(
            "languag |        paradigm |    typing | compil",
            tablize(self.data_list,
                    labels=["language", "paradigm", "typing", "compiler"])[0])

    def test_truncation(self):
        ''' Tests that columns can be truncated
        If the max_length keyword is set, columns get truncated to that size.
        '''

        self.assertEqual('''
py | mu | du | py
ru | ob | du | ru
c+ | ob | st | g+
ha | fu | st | gh''', '\n'.join([''] + tablize(self.data_list, max_length=2)))

    def test_alignment(self):
        ''' Tests custom alignment settings
        Provides custom alignment values and asserts that they are honored.
        '''
        self.assertEqual('''
python  |  multiparadigm  | ducktyped | python
ruby    | object oriented | ducktyped |   ruby
c++     | object oriented |    static |    g++
haskell |   functional    |    static |    ghc''',
                         '\n'.join([''] + tablize(
                             self.data_list, alignment=["l", "c", "r", "r"])))

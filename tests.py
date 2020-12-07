from logical_expressions import parse
from indexator import Indexator
from document import Document
import os
import pymorphy2
import unittest

morphy = pymorphy2.MorphAnalyzer()


class Tests(unittest.TestCase):

    def test_logical_expression(self):
        expression = "кот and not кошка or гном"
        result = parse(expression, morphy)
        expected_search_words_1 = ['кот']
        expected_ban_words_1 = ['кошку', 'кошкою', 'кошках', 'кошек', 'кошками', 'кошке', 'кошки', 'кошкам', 'кошка',
                                'кошкой']
        expected_search_words_2 = ['гном']
        expected_ban_words_2 = []
        self.assertEqual(result[0][0].search_words, set(expected_search_words_1))
        self.assertEqual(result[0][0].ban_words, set(expected_ban_words_1))
        self.assertEqual(result[1][0].search_words, set(expected_search_words_2))
        self.assertEqual(result[1][0].ban_words, set(expected_ban_words_2))

    def test_different_encoding(self):
        indexator = Indexator("dir_for_tests\\different_encoding")
        self.assertEqual(len(indexator.find("кот")), 3)

    def test_document_and_tf(self):
        path = "dir_for_tests\\docs\\file1.txt"
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().lower()
            document = Document(path=path, text=text, m_time=os.stat(path).st_mtime)
        self.assertEqual(document.word_to_tf["кот"], 0.25)


if __name__ == '__main__':
    unittest.main()

from chardet.universaldetector import UniversalDetector
from document import Document
from pathlib import Path
import math
import os

encoding = {
    'windows-1251': "cp1251",
    'IBM866': "cp866",
    'ascii': "ascii",
    'utf-8': 'utf-8'
}


class Indexator:
    def __init__(self, dir_name):
        result = list(Path(dir_name).rglob("*.[tT][xX][tT]"))
        self.dir_name = dir_name
        self.indexes = {}
        self.documents = {}
        for file in result:
            self.index_document(file)
        self.word_to_idf = {}
        for word in self.indexes:
            self.word_to_idf[word] = self.calc_idf(word)

    def calc_idf(self, word):
        if word not in self.indexes:
            return 0
        return math.log10(len(self.documents) / len(self.indexes[word]))

    def find(self, word):
        if word not in self.indexes:
            return set()
        return self.indexes[word]

    def re_index(self):
        result = list(Path(self.dir_name).rglob("*.[tT][xX][tT]"))
        self.indexes = {}
        for file in result:
            path = str(file.absolute())
            if self.is_file_need_reindex(path):
                self.index_document(file)
            else:
                self.index_created_document(self.documents[path])

    def is_file_need_reindex(self, path):
        return not (path in self.documents and self.documents[path].m_time == os.stat(path).st_mtime)

    def index_document(self, file):
        encod = self.get_encoding_of_file(str(file.absolute()))
        if encod not in encoding:
            with file.open() as f:
                text = f.read().lower()
                if len(text) != 0:
                    raise AttributeError(f"Unexpected encoding - {encod} in file {file.absolute()}")
        with file.open(encoding=encoding[encod]) as f:
            text = f.read().lower()
            path = str(file.absolute())
            document = Document(path=path, text=text, m_time=os.stat(path).st_mtime)
            self.documents[path] = document
            self.index_created_document(document)

    def index_created_document(self, document):
        for word in document.all_words:
            if word not in self.indexes:
                self.indexes[word] = set()
            self.indexes[word].add(document.path)

    def get_encoding_of_file(self, file_path):
        detector = UniversalDetector()
        with open(file_path, 'rb') as fh:
            for line in fh:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
        return detector.result['encoding']

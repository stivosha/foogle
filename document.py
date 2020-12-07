import re


class Document:
    def __init__(self, path, text, m_time):
        matches = re.finditer(r"\w+", text.lower())
        self.m_time = m_time
        self.words_count = 0
        self.all_words = set()
        self.path = path
        self.indexes = {}
        for match in matches:
            word = match.string[match.start():match.end()]
            self.all_words.add(word)
            self.words_count += 1
            if word not in self.indexes:
                self.indexes[word] = []
            self.indexes[word].append(match.start())
        self.word_to_tf = {}
        for word in self.all_words:
            self.word_to_tf[word] = self.calc_tf(word)

    def calc_tf(self, word):
        if word not in self.indexes:
            raise KeyError(f"There is no such word in this document: {self.path}")
        return len(self.indexes[word]) / self.words_count

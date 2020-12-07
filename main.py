from indexator import Indexator
from arg_parser import Args
from logical_expressions import parse
from result import Result
import pymorphy2
import store

separator_line = "*" * 64


class Foogle:
    def __init__(self):
        self.args = Args()
        self.morphy = None
        if self.args.morphy:
            self.morphy = pymorphy2.MorphAnalyzer()
        self.indexator = None

    def find(self, word):
        indexator = self.get_indexator()
        return indexator.find(word)

    def execute_expressions2(self, expression):
        results = parse(expression, self.morphy)
        for i in range(len(results)):
            paths_without_ban_words = None
            for word in results[i].search_words:
                doc_paths = self.find(word)
                temp_set = set()
                for path in doc_paths:
                    if self.indexator.documents[path].all_words.isdisjoint(results[i].ban_words):
                        temp_set.add(path)
                if paths_without_ban_words is None:
                    paths_without_ban_words = temp_set.copy()
                else:
                    paths_without_ban_words.intersection_update(temp_set)
                    if len(paths_without_ban_words) == 0:
                        break
            results[i].paths_without_ban_words = paths_without_ban_words
        return Result(self.indexator, results, index_enable=self.args.index_enable)

    def execute_expressions(self, expression):
        results = parse(expression, self.morphy)
        doc_to_found_words = {}
        for i in range(len(results)):
            request, morphy_words = results[i]
            all_result = None
            for main_word in morphy_words:
                paths_without_ban_words = set()
                for morphy_word in morphy_words[main_word]:
                    doc_paths = self.find(morphy_word)
                    for path in doc_paths:
                        if self.indexator.documents[path].all_words.isdisjoint(results[i][0].ban_words):
                            if path not in doc_to_found_words:
                                doc_to_found_words[path] = []
                            doc_to_found_words[path].append(morphy_word)
                            paths_without_ban_words.add(path)
                if all_result is None:
                    all_result = paths_without_ban_words.copy()
                all_result.intersection_update(paths_without_ban_words)
                if len(all_result) == 0:
                    break
            results[i][0].paths_without_ban_words = all_result
        return Result(self.indexator, [result[0] for result in results],
                      path_to_word=doc_to_found_words, index_enable=self.args.index_enable)

    def index_dir(self, dir_name):
        indexator = Indexator(dir_name)
        store.store_indexator(indexator)

    def re_index_dir(self):
        indexator = self.get_indexator()
        indexator.re_index()
        store.store_indexator(indexator)

    def get_indexator(self):
        if self.indexator is None:
            self.indexator = store.get_indexator()
        return self.indexator


foogle = Foogle()

if foogle.args.word is not None:
    word = foogle.args.word
    result = foogle.execute_expressions(word)
    print(result.to_str())
elif foogle.args.dir is not None:
    foogle.index_dir(foogle.args.dir)
elif foogle.args.reindex:
    foogle.re_index_dir()

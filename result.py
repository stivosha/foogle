separator_line = "*" * 64


class Result:
    def __init__(self, indexator, results, path_to_word, index_enable=False):
        self.indexator = indexator
        self.results = results
        self.index_enable = index_enable
        self.path_to_word = path_to_word

    def to_str(self):
        output = ''
        output += separator_line + '\n'
        for result in self.results:
            output += f"result for\nsearch words: {', '.join(result.search_words)}\n"
            output += f"ban words: {', '.join(result.ban_words)}\n"
            output += f"count: {len(result.paths_without_ban_words)}\n"
            for path in result.paths_without_ban_words:
                output += path + '\n'
                if not self.index_enable:
                    continue
                for word in self.path_to_word[path]:
                    indexes = self.indexator.documents[path].indexes[word]
                    idf = self.indexator.word_to_idf[word]
                    tf = self.indexator.documents[path].word_to_tf[word]
                    output += f"{word} with {idf * tf} at {', '.join(str(index) for index in indexes)}\n"
            output += separator_line + '\n'
        return output

from morfologia import get_similar_words


class Request:
    def __init__(self, search_words=None, ban_words=None):
        self.search_words = set()
        if search_words is not None:
            self.search_words = self.search_words.union(search_words)
        self.ban_words = set()
        if ban_words is not None:
            self.ban_words = self.ban_words.union(ban_words)
        self.main_words = {}
        self.paths_without_ban_words = []

    def add_search_word(self, word):
        self.main_words[word] = word
        self.search_words.add(word)

    def add_ban_word(self, word):
        self.main_words[word] = word
        self.ban_words.add(word)

    def get_copy2(self, morphy=None):
        if morphy is not None:
            new_words = set()
            for i in self.search_words:
                morphy_words = get_similar_words(i, morphy)
                for word in morphy_words:
                    self.main_words[i] = word
                new_words = new_words.union(morphy_words)
            self.search_words = self.search_words.union(new_words.copy())
            new_words.clear()
            for i in self.ban_words:
                morphy_words = get_similar_words(i, morphy)
                for word in morphy_words:
                    self.main_words[i] = word
                new_words = new_words.union(morphy_words)
            self.ban_words = self.ban_words.union(new_words.copy())
            self.search_words = self.search_words.difference(self.ban_words)
        if len(self.search_words) == 0:
            raise AttributeError("The expression can't contain only ban words")
        return Request(self.search_words.copy(), self.ban_words.copy())

    def get_copy(self, morphy=None):
        if morphy is not None:
            new_words = set()
            morphy_words = {}
            for i in self.search_words:
                morphy_words[i] = get_similar_words(i, morphy)
            for i in self.ban_words:
                new_words = new_words.union(get_similar_words(i, morphy))
            self.ban_words = self.ban_words.union(new_words.copy())
            keys_need_del = []
            for word_key in morphy_words:
                if word_key in self.ban_words:
                    keys_need_del.append(word_key)
            for key_need_del in keys_need_del:
                morphy_words.pop(keys_need_del, None)
                self.search_words.remove(key_need_del)
        else:
            morphy_words = {}
            for word in self.search_words:
                morphy_words[word] = [word]
        if len(self.search_words) == 0:
            raise AttributeError("The expression can't contain only ban words")
        return Request(self.search_words.copy(), self.ban_words.copy()), morphy_words


def parse(expression, morphy):
    parts = expression.split()
    requests = []
    temp = Request()
    i = 0
    while i < len(parts):
        if parts[i] == "or":
            requests.append(temp.get_copy(morphy))
            temp = Request()
        elif parts[i] == "not":
            temp.add_ban_word(parts[i + 1])
            i += 1
        elif parts[i] != "and":
            temp.add_search_word(parts[i])
        i += 1
    requests.append(temp.get_copy(morphy))
    return requests

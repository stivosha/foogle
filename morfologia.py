def get_similar_words(word, morph):
    return set(i.word for i in morph.parse(word)[0].lexeme)

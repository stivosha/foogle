import pickle


def store_indexator(indexator):
    with open("indexes.txt", "wb") as f:
        pickle.dump(indexator, f)


def get_indexator():
    with open("indexes.txt", "rb") as f:
        indexator = pickle.load(f)
    return indexator

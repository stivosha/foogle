import argparse


class Args:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Foogle, simple local file indexer')
        parser.add_argument('-w', '--word', type=str, dest='word', help='The word we are looking for')
        parser.add_argument('-d', '--dir', type=str, dest='dir', help='Directory where we are looking')
        parser.add_argument('-r', '--reindex', action="store_true",
                            help='A flag that indicates whether we need to index the directory')
        parser.add_argument('-m', '--morphy', action="store_true", help='Enable morphy analyzer')
        parser.add_argument('-i', '--index', action="store_true", help='Show index of occurring words')
        args = parser.parse_args()
        args_count = 0
        if args.word is not None:
            args_count += 1
        if args.dir is not None:
            args_count += 1
        if args.reindex:
            args_count += 1
        if args_count == 0:
            raise AttributeError("You can't run the program without arguments.")
        elif args_count != 1:
            raise AttributeError("The program can only work in one mode")
        self.word = args.word
        self.dir = args.dir
        self.reindex = args.reindex
        self.morphy = args.morphy
        self.index_enable = args.index

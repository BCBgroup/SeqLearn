import pandas as pd


class EmbeddingLoader:
    def __init__(self, sequences, word_length, file):
        self.sequences = sequences
        self.word_length = word_length
        self.sentences = []
        emb_df = pd.read_csv(file, index_col=0)
        self.vocab = emb_df.index
        self.embedding_layer = emb_df.values
        self.frequency = None

    def __seq_splitter(self, seq):
        words = list(map(lambda x: seq[x:(x + self.word_length)], range((len(seq) - self.word_length + 1))))
        self.sentences.append(words)

    def __freq_calc(self):
        def adder(idx):
            self.frequency[idx] += 1

        self.frequency = dict.fromkeys(range(len(self.vocab)), 0)
        list(map(lambda sent: list(map(lambda word: adder(word), sent)), self.sentences))
        self.frequency = {k: v / total for total in (sum(self.frequency.values()),) for k, v in self.frequency.items()}
        self.frequency = self.frequency.values()

    def __corpus_maker(self):
        list(map(lambda seq: self.__seq_splitter(seq), self.sequences))
        self.vocab = dict(list(enumerate(self.vocab)))
        self.vocab = dict((v, k) for k, v in self.vocab.items())
        self.sentences = list(map(lambda x: list(map(lambda y: self.vocab.get(y, 0), x)), self.sentences))
        self.__freq_calc()

    def embed(self):
        self.__corpus_maker()

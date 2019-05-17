from settings import PAD_token, SOS_token, EOS_token, NWL_token, SUBSTITUTES


class Voc:
    def __init__(self):
        self.trimmed = False
        self.word2index = {}
        self.countWords = {}
        self.index2word = {PAD_token: "PAD", SOS_token: "SOS",
                           EOS_token: "EOS", NWL_token: "NL"}
        self.num_words = 4  # Count SOS, EOS, PAD
        self.substitutes = SUBSTITUTES

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.countWords[word] = 1
            self.index2word[self.num_words] = word
            self.num_words += 1
        else:
            self.countWords[word] += 1

    def addSentence(self, sentence):
        for word in sentence:
            self.addWord(word)

    def createVocFromPairs(self, pairs):
        for question, answer in pairs:
            self.addSentence(question)
            self.addSentence(answer)

    def sentenceToIndex(self, sentence):
        return [self.word2index[word] for word in sentence]

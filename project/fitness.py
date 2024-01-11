import math

class TrigramFitness:
    epsilon = 1e-10

    def __init__(self):
        # Trigrams
        self.trigrams = [math.log10(self.epsilon) for _ in range(26426)]
        try:
            with open("data/trigrams", "r", encoding="utf-8") as file:
                for line in file:
                    key, value = line.strip().split(',')
                    i = self.tri_index(ord(key[0]) - 65, ord(key[1]) - 65, ord(key[2]) - 65)
                    self.trigrams[i] = float(value)
        except FileNotFoundError:
            self.trigrams = None

    @staticmethod
    def tri_index(a, b, c):
        return (a << 10) | (b << 5) | c

    def score(self, text):
        if (self.trigrams is None):
        # Handle the case when trigrams data is not available
            return 0  # Or any other appropriate value

        fitness = 0
        current = 0
        next1 = ord(text[0]) - 65
        next2 = ord(text[1]) - 65
        for i in range(2, len(text)):
            current = next1
            next1 = next2
            next2 = ord(text[i]) - 65
            fitness += self.trigrams[self.tri_index(current, next1, next2)]
        fitness /= len(text)    # Normalize fitness to per-character, to make it comparable with other fitness functions
        #fitness = 10 ** fitness
        return fitness

class BigramFitness:
    epsilon = 1e-10

    def __init__(self):
        # Bigrams
        self.bigrams = [math.log10(self.epsilon) for _ in range(826)]
        try:
            with open("data/bigrams.txt", "r", encoding="utf-8") as file:
                for line in file:
                    key, value = line.strip().split(',')
                    i = self.bi_index(ord(key[0]) - 65, ord(key[1]) - 65)
                    self.bigrams[i] = float(value)
        except FileNotFoundError:
            self.bigrams = None

    @staticmethod
    def bi_index(a, b):
        return (a << 5) | b

    def score(self, text):
        if (self.bigrams is None):
        # Handle the case when bigrams data is not available
            return 0  # Or any other appropriate value

        fitness = 0
        current = ord(text[0]) - 65
        for i in range(1, len(text)):
            next = ord(text[i]) - 65
            fitness += self.bigrams[self.bi_index(current, next)]
            current = next
        fitness /= len(text)    # Normalize fitness to per-character, to make it comparable with other fitness functions
        #fitness = 10 ** fitness
        return fitness

class UnigramFitness:
    epsilon = 1e-10

    def __init__(self):
        # Unigrams
        self.unigrams = [math.log10(self.epsilon) for _ in range(26)]
        try:
            with open("data/single.txt", "r", encoding="utf-8") as file:
                for line in file:
                    key, value = line.strip().split(',')
                    i = ord(key) - 65
                    self.unigrams[i] = float(value)
        except FileNotFoundError:
            self.unigrams = None

    def score(self, text):
        if (self.unigrams is None):
        # Handle the case when unigrams data is not available
            return 0  # Or any other appropriate value

        fitness = 0
        for c in text:
            fitness += self.unigrams[ord(c) - 65]
        fitness /= len(text)    # Normalize fitness to per-character, to make it comparable with other fitness functions
        #fitness = 10 ** fitness
        return fitness

class QuadrigramFitness:
    epsilon = 1e-10

    def __init__(self):
        # Quadrigrams
        self.quadrigrams = [math.log10(self.epsilon) for _ in range(42171)]
        try:
            with open("data/quadgrams.txt", "r", encoding="utf-8") as file:
                for line in file:
                    key, value = line.strip().split(',')
                    i = self.quad_index(ord(key[0]) - 65, ord(key[1]) - 65, ord(key[2]) - 65, ord(key[3]) - 65)
                    self.quadrigrams[i] = float(value)
        except FileNotFoundError:
            self.quadrigrams = None

    @staticmethod
    def quad_index(a, b, c, d):
        return (a << 9) | (b << 6) | (c << 3) | d

    def score(self, text):
        if (self.quadrigrams is None):
        # Handle the case when quadrigrams data is not available
            return 0  # Or any other appropriate value

        fitness = 0
        current = 0
        next1 = ord(text[0]) - 65
        next2 = ord(text[1]) - 65
        next3 = ord(text[2]) - 65
        for i in range(3, len(text)):
            current = next1
            next1 = next2
            next2 = next3
            next3 = ord(text[i]) - 65
            fitness += self.quadrigrams[self.quad_index(current, next1, next2, next3)]
        fitness /= len(text)    # Normalize fitness to per-character, to make it comparable with other fitness functions
        #fitness = 10 ** fitness
        return fitness
# Example usage:
# text_to_score = "IFWEAREGOINGTODEFEATTHEENEMYWEHAVEGOTTOSTARTGETTINGBUSY"
# text_to_score = "BHAYDGUFYGADVHABNAMLZKJSGEPQBHDFJNZMXBTUHDJAKDJBDNFJCKS"
# quadgram_fitness = QuadrigramFitness()
# score = quadgram_fitness.score(text_to_score)
# print("Fitness Score:", score)

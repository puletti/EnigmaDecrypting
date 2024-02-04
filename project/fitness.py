import math 
import numpy as np

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
        return fitness/len(text)

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
    
    #Index of coincidence. The probability of any random two letters being identical. 
    #Tends to be higher for proper sentences than for random encrypted text.
def ioc(text):
    histogram = [0] * 26
    for c in text:
        histogram[ord(c) - 65] += 1

    n = len(text)
    total = 0.0

    for v in histogram:
        total += v * (v - 1)

    ic = total / (n * (n - 1))
    #return the corresponding value in the normal distribution with mean 0.055 and variance 0.0006
    fitic =(np.exp(-(ic-0.055)**2/(2*0.000006))/(np.sqrt(2*np.pi*0.000006)))
    return fitic


# Example usage:
# text_to_score = ["IFIHADAHAMMER", "HELLOEVERYONE", "THEWEATHERISFINE", "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG", "THISISATEST", "LASTNIGHTSHESAIDBABYIFEELSODOWN", "NEVERMINDIMUSEFULL",
#                  "INMANYWAYSTHEYMISSTHEGOODOLDDAYS", "THEYWERESOBAD", "THEYDIDNTHAVEANYSNOW", "INFACTTHEYDIDNTHAVEANYTHINGYOUKNOW", "THEYDIDNTEVENHAVEAWAYTOGETOUTOFBED",
#                  "LUCASHADBEENPLANNINGTHEATTACKFORTWOWEEKS", "HEHADBEENWATCHINGTHEMILLFORTHEPASTMONTH", "HEKNEWTHATTHEGUARDSWEREFEWANDFARBETWEEN",
#                  "ITSRARE", "IDONTKNOWWHATITMEANS", "BUTITMEANSSOMETHING", "ITSNOTJUSTSOMETHINGTHATHAPPENED", "ITSNOTJUSTSOMETHINGTHATHAPPENEDTOME", "ITSNOTJUSTSOMETHINGTHATHAPPENEDTOMEANDMYFAMILY",
#                  "WHATEVERITIS", "THEARMYISCOMING", "HOUSTONWEHAVEAPROBLEM", "LEARNINGHOWTOCODE", "ITSCLEARTHATYOUARENOGOOD", "MAYBE", "IFIHADAHAMMER", "HELLOEVERYONE", "THEWEATHERISFINE", "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG", "THISISATEST", "LASTNIGHTSHESAIDBABYIFEELSODOWN", "NEVERMINDIMUSEFULL",
#                  "INMANYWAYSTHEYMISSTHEGOODOLDDAYS", "THEYWERESOBAD", "THEYDIDNTHAVEANYSNOW", "INFACTTHEYDIDNTHAVEANYTHINGYOUKNOW", "THEYDIDNTEVENHAVEAWAYTOGETOUTOFBED",
#                  "LUCASHADBEENPLANNINGTHEATTACKFORTWOWEEKS", "HEHADBEENWATCHINGTHEMILLFORTHEPASTMONTH", "HEKNEWTHATTHEGUARDSWEREFEWANDFARBETWEEN",
#                  "ITSRARE", "IDONTKNOWWHATITMEANS", "BUTITMEANSSOMETHING", "ITSNOTJUSTSOMETHINGTHATHAPPENED", "ITSNOTJUSTSOMETHINGTHATHAPPENEDTOME", "ITSNOTJUSTSOMETHINGTHATHAPPENEDTOMEANDMYFAMILY",
#                  "WHATEVERITIS", "THEARMYISCOMING", "HOUSTONWEHAVEAPROBLEM", "LEARNINGHOWTOCODE", "ITSCLEARTHATYOUARENOGOOD", "MAYBE"]
# randtext = ["NVHUQIMDBUVWQ", "NOAOUNRAOIUNEARCNVKVNJIZP", "JFOUT", "CCHVVVQAH", "XCGWJHRFJHGVDOERM", "CPTTPDQUXHUYNCVVUTQBPZUD", "KRJTVKEZMTRYCQEKFBZIFUAQOATQWE", "BSUQPTIEUHFBNDJVJVBAYGCAJDCNJAIGMKZOMVHBEWAQ",
#             "OWIWUEBNZMXJHBAH", "NDJ", "PQOAMCGDHZNCIWU", "PQOUEBZNCMHHDJABCGRTAICHBA", "PQOEUBCNZJSK", "GFTUUAZBNCMSDKWIIURGBD", "NMVXKKAH", "WRCHABDJJDJSKOA"]
# fit =[]
# fitrand = []
# for text in randtext:
#     import matplotlib.pyplot as plt
#     import numpy as np
#     #plot the distribution of the ioC for the given texts in a single histogram
#     fitrand.append(ioc(text))

# plt.hist(fitrand, bins=60)
# #PLOT A normal distribution with mean and variance of the ioc of the given texts
# plt.plot(np.linspace(0, 0.13, 100),np.exp(-(np.linspace(0, 0.13, 100)-np.mean(fitrand))**2/(2*np.var(fitrand)))/(np.sqrt(2*np.pi*np.var(fitrand))))
# plt.show()
# print("the mean of the ioc of the given texts is:", np.mean(fitrand), "and the variance is:", np.var(fitrand))
# for text in text_to_score:
#     import matplotlib.pyplot as plt
#     #plot the distribution of the ioC for the given texts in a single histogram
#     fit.append(ioc(text))

# plt.hist(fit, bins=60)
# #PLOT A normal distribution with mean and variance of the ioc of the given texts

# plt.plot(np.linspace(0, 0.13, 100),np.exp(-(np.linspace(0, 0.13, 100)-np.mean(fit))**2/(2*np.var(fit)))/(np.sqrt(2*np.pi*np.var(fit))))
# plt.show()
# print("the mean of the ioc of the given texts is:", np.mean(fit), "and the variance is:", np.var(fit))
# #text_to_score = "BSUQPTIEUHFBNDJVJVBAYGCAJDCNJAIGMKZOMVHBEWAQ"
# # quadgram_fitness = QuadrigramFitness()
# #score = ioc(text_to_score)
# #print("Fitness Score:", score)
# print(np.linspace(0, 0.13, 100),np.exp(-(np.linspace(0, 0.13, 100)-np.mean(fit))**2/(2*np.var(fit)))/(np.sqrt(2*np.pi*np.var(fit))))

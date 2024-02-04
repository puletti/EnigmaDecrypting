from inspyred import ec
from enigma.Enigma import Enigma
import fitness
import random
import numpy as np
import fitness
import copy

class EnigmaConfiguration:
    def __init__(self, rotors, reflector, rotor_positions, ring_settings, plugboard_connections, setting=None):
        self.rotors = rotors
        self.reflector = reflector
        self.rotor_positions = rotor_positions
        self.ring_settings = ring_settings
        self.plugboard_connections = plugboard_connections
        self.cipher_texts = ["SVHDKNGPIZAUOOZOEZGUAQHLTVREVUXLSQQRFPAHEKSAUOVKELJBVNWSPTLDBUWTOZ", "TRHOAKKOWZAZCPYYVWSAGWXUVURMEUP", "EYHPTNGRVVVJSTYUCLQIT", "SEMMRUEMZBFOVBORJHYLWAXPGUCFARNFQLQHWFPEJYTELA", "IZIILJBWXJZMDEOSKVXLJDUUUFOKCOAHLYWXLVHRVTUIPQQRRLMKQHQFQJRTWGNTOZTCGSEIIBR"]
        #self.cipher_texts = ["GTLYGLAPQMPNIUTF"]

        self.config = {
            "rotors": rotors or ["I", "V", "VI"],
            "reflector": reflector or "B",
            "rotor_positions": rotor_positions or [19, 2, 4],
            "ring_settings": ring_settings or [2, 7, 1],
            "plugboard_connections": plugboard_connections or "AP UD KI ZV TS"
        }
    
    def generator(self, random, args):
        alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
        plug = ""
        for i in range(random.randint(0, 13)):
            let1 = random.choice(alphabet)
            alphabet.remove(let1)
            let2 = random.choice(alphabet)
            alphabet.remove(let2)
            plug += let1 + let2 + " "

        #########
        if args["setting"] == "rotors":
            gener = EnigmaConfiguration(
                rotors=random.sample(["I", "II", "III", "IV", "V", "VI", "VII", "VIII"], 3),
                reflector=self.config["reflector"],
                rotor_positions=self.config["rotor_positions"],
                ring_settings=self.config["ring_settings"],
                plugboard_connections=self.config["plugboard_connections"]
            )
            return gener.config
        elif args["setting"] == "reflector":
            gener = EnigmaConfiguration(
                rotors=self.config["rotors"],
                reflector=random.choice(["B", "C"]),
                rotor_positions=self.config["rotor_positions"],
                ring_settings=self.config["ring_settings"],
                plugboard_connections=self.config["plugboard_connections"]
            )
            return gener.config
        elif args["setting"] == "rotor_positions":
            gener = EnigmaConfiguration(
                rotors=self.config["rotors"],
                reflector=self.config["reflector"],
                rotor_positions=random.sample(range(26), 3),
                ring_settings=self.config["ring_settings"],
                plugboard_connections=self.config["plugboard_connections"]
            )
            return gener.config
        elif args["setting"] == "ring_settings":
            gener = EnigmaConfiguration(
                rotors=self.config["rotors"],
                reflector=self.config["reflector"],
                rotor_positions=self.config["rotor_positions"],
                ring_settings=random.sample(range(26), 3),
                plugboard_connections=self.config["plugboard_connections"]
            )
            return gener.config
        elif args["setting"] == "plugboard_connections":
            gener = EnigmaConfiguration(
                rotors=self.config["rotors"],
                reflector=self.config["reflector"],
                rotor_positions=self.config["rotor_positions"],
                ring_settings=self.config["ring_settings"],
                plugboard_connections=plug
            )
            return gener.config
        #########
        else:
            gener = EnigmaConfiguration(
                rotors=random.sample(["I", "II", "III", "IV", "V", "VI", "VII", "VIII"], 3),
                reflector=random.choice(["B", "C"]),
                rotor_positions=random.sample(range(26), 3),
                ring_settings=random.sample(range(26), 3),
                #plugboard connections must be random couples of letters separated by a space with variable length (0-13)
                #the couples must be unique and the letters must be different
                plugboard_connections=plug            )
            return gener.config
    
    def evaluator(self, candidates, args):      #CHECK CAREFULLY!!!!
        fit = []
        score = []
        unigram = fitness.UnigramFitness()
        bigram = fitness.BigramFitness()
        trigram = fitness.TrigramFitness()
        quadgram = fitness.QuadrigramFitness()

        #########
        if args["setting"] == "rotors":
            for c in candidates:
                enigma = Enigma(c["rotors"], "C",[9, 22, 14], [12, 17, 11], "AH UD KE OV TR")
                #the fitness function is the sum of the scores of the 4 fitness functions and is evaluated on a set of encrypted texts given in input
                for cipher in self.cipher_texts:
                    score.append(1.5*quadgram.score(enigma.encrypt_string(cipher))+trigram.score(enigma.encrypt_string(cipher)) -fitness.ioc(enigma.encrypt_string(cipher)))
                fit.append(np.min(score))
                #fit.append(quadgram.score(enigma.encrypt_string)))
            return fit
        elif args["setting"] == "reflector":
            for c in candidates:
                enigma = Enigma(c["rotors"], c["reflector"], c["rotor_positions"], c["ring_settings"], c["plugboard_connections"])
                #the fitness function is the sum of the scores of the 4 fitness functions and is evaluated on a set of encrypted texts given in input
                for cipher in self.cipher_texts:
                    score.append(bigram.score(enigma.encrypt_string(cipher))-fitness.ioc(enigma.encrypt_string(cipher)))
                fit.append(np.mean(score))
                #fit.append(quadgram.score(enigma.encrypt_string)))
            return fit
        elif args["setting"] == "rotor_positions":
            for c in candidates:
                enigma = Enigma(c["rotors"], c["reflector"], c["rotor_positions"], c["ring_settings"], c["plugboard_connections"])
                #the fitness function is the sum of the scores of the 4 fitness functions and is evaluated on a set of encrypted texts given in input
                for cipher in self.cipher_texts:
                    score.append(trigram.score(enigma.encrypt_string(cipher))-fitness.ioc(enigma.encrypt_string(cipher)))
                fit.append(np.mean(score))
                #fit.append(quadgram.score(enigma.encrypt_string)))
            return fit
        elif args["setting"] == "ring_settings":
            for c in candidates:
                enigma = Enigma(c["rotors"], c["reflector"], c["rotor_positions"], c["ring_settings"], c["plugboard_connections"])
                #the fitness function is the sum of the scores of the 4 fitness functions and is evaluated on a set of encrypted texts given in input
                for cipher in self.cipher_texts:
                    score.append(quadgram.score(enigma.encrypt_string(cipher))-fitness.ioc(enigma.encrypt_string(cipher)))
                fit.append(np.mean(score))
                #fit.append(quadgram.score(enigma.encrypt_string)))
            return fit
        elif args["setting"] == "plugboard_connections":
            for c in candidates:
                enigma = Enigma(c["rotors"], c["reflector"], c["rotor_positions"], c["ring_settings"], c["plugboard_connections"])
                #the fitness function is the sum of the scores of the 4 fitness functions and is evaluated on a set of encrypted texts given in input
                for cipher in self.cipher_texts:
                    score.append(unigram.score(enigma.encrypt_string(cipher))+bigram.score(enigma.encrypt_string(cipher))+trigram.score(enigma.encrypt_string(cipher))+quadgram.score(enigma.encrypt_string(cipher)))
                fit.append(np.mean(score))
                #fit.append(quadgram.score(enigma.encrypt_string)))
            return fit
        #########

        else:
            for c in candidates:
                enigma = Enigma(c["rotors"], c["reflector"], c["rotor_positions"], c["ring_settings"], c["plugboard_connections"])
                #the fitness function is the sum of the scores of the 4 fitness functions and is evaluated on a set of encrypted texts given in input
                for cipher in self.cipher_texts:
                    score.append(1/fitness.ioc(enigma.encrypt_string(cipher))*(2.2*(unigram.score(enigma.encrypt_string(cipher))) + 1.4*(bigram.score(enigma.encrypt_string(cipher))) + 0.8*(trigram.score(enigma.encrypt_string(cipher))) + 0.3*quadgram.score(enigma.encrypt_string(cipher))))
                fit.append(np.mean(score))
                #fit.append(quadgram.score(enigma.encrypt_string)))
            return fit

    

#test
# test = EnigmaConfiguration(None, None, None, None, None)
# print(test.generator(random, None))
#print(test.config)

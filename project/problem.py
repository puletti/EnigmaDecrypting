from inspyred import ec
from enigma.Enigma import Enigma
import fitness
import random
import numpy as np
import fitness

class EnigmaConfiguration:
    def __init__(self, rotors, reflector, rotor_positions, ring_settings, plugboard_connections):
        self.rotors = rotors
        self.reflector = reflector
        self.rotor_positions = rotor_positions
        self.ring_settings = ring_settings
        self.plugboard_connections = plugboard_connections

        self.config = {
            "rotors": rotors or ["I", "II", "III"],
            "reflector": reflector or "B",
            "rotor_positions": rotor_positions or [0, 0, 0],
            "ring_settings": ring_settings or [0, 0, 0],
            "plugboard_connections": plugboard_connections or "AB CD EF GH IJ KL MN OP QR ST UV WX YZ" 
        }
    
    def generator(self, random, args):
        gener = EnigmaConfiguration(
            rotors=random.sample(["I", "II", "III", "IV", "V", "VI", "VII", "VIII"], 3),
            reflector=random.choice(["B", "C"]),
            rotor_positions=random.sample(range(26), 3),
            ring_settings=random.sample(range(26), 3),
            #plugboard connections must be random couples of letters separated by a space with variable length (0-13)
            plugboard_connections=" ".join(random.sample([chr(i) + chr(j) for i in range(65, 91) for j in range(65, 91)], random.randint(0, 13)))
        )
        return gener.config
    
    def evaluator(self, candidates, args):      #naive implementation usign the fitness function from fitness.py
        fit = []
        unigram = fitness.UnigramFitness()
        bigram = fitness.BigramFitness()
        trigram = fitness.TrigramFitness()
        quadgram = fitness.QuadrigramFitness()
        for c in candidates:
            enigma = Enigma.Enigma(c["rotors"], c["reflector"], c["rotor_positions"], c["ring_settings"], c["plugboard_connections"])
            fit.append(quadgram.score(enigma.encrypt_string("HELLOWORLD")))
        return fit

    def custom_crossover(parents, random, args):
        child = EnigmaConfiguration()
        for feature in child.config:
            # Perform crossover for each feature independently
            crossover_point = random.randint(0, min(len(parents[0].config[feature]), len(parents[1].config[feature])))
            child.config[feature] = parents[0].config[feature][:crossover_point] + parents[1].config[feature][crossover_point:]
        return child
    def custom_crossover_operator(random, candidates, args):
        parents = random.sample(candidates, 2)
        return custom_crossover(parents, random, args)

#test
# test = EnigmaConfiguration(None, None, None, None, None)
# print(test.generator(random, None))
#print(test.config)

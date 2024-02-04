import random
import numpy as np
from inspyred import ec
from enigma.Enigma import Enigma
import mutate
import crossover
import problem
import collections
import observer
import replacer
import distance
import archive
import inspyred.ec.analysis as analysis
collections.Iterable = collections.abc.Iterable
collections.Sequence= collections.abc.Sequence

def main(setting=None, best_rotor = None, best_reflector = None, best_rotor_positions = None, best_ring_settings = None, best_plugboard_connections = None):
    alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
    display = False
    args = {}
    args["mutation_rate"] = 1.5
    args["setting"] = setting

    ###############
    if setting == "rotors":
        args["problem"] = problem.EnigmaConfiguration(random.sample(["I", "II", "III", "IV", "V", "VI", "VII", "VIII"], 3),
                                                best_reflector,
                                                best_rotor_positions,
                                                best_ring_settings, best_plugboard_connections)
    elif setting == "reflector":
        args["problem"] = problem.EnigmaConfiguration(best_rotor,
                                                random.choice(["B", "C"]),
                                                best_rotor_positions,
                                                best_ring_settings, best_plugboard_connections)
    elif setting == "rotor_positions":
        args["problem"] = problem.EnigmaConfiguration(best_rotor,
                                                best_reflector,
                                                random.sample(range(26), 3),
                                                best_ring_settings, best_plugboard_connections)
    elif setting == "ring_settings":
        args["problem"] = problem.EnigmaConfiguration(best_rotor,
                                                best_reflector,
                                                best_rotor_positions,
                                                random.sample(range(26), 3), best_plugboard_connections)
    elif setting == "plugboard_connections":
        args["problem"] = problem.EnigmaConfiguration(best_rotor,
                                                best_reflector,
                                                best_rotor_positions,
                                                best_ring_settings,
                                                " ".join(random.sample([i + j for i in alphabet for j in alphabet if i != j],random.randint(0, 13))) )
    ###############
    else:
        args["problem"] = problem.EnigmaConfiguration(random.sample(["I", "II", "III", "IV", "V", "VI", "VII", "VIII"], 3),
                                                random.choice(["B", "C"]),
                                                random.sample(range(26), 3),
                                                random.sample(range(26), 3), " ".join(random.sample([i + j for i in alphabet for j in alphabet if i != j],random.randint(0, 13))) )
    
    args["max_generations"] = 700
    args["population_size"] = 30
    args["crossover_rate"] = 1.8
    args["mutation_rate"] = 3.5
    #args["num_offspring"] = 0.5
    args["num_elites"] = 2
    #args["tournament_size"] = 2
    args["selector"] = ec.selectors.rank_selection
    args["num_selected"] = 20

    args["distance_function"] = distance.distance_function
    args["crowding_distance"] = 5

    rand = random.Random()
    #rand.seed(123456789)

    EC = ec.EvolutionaryComputation(rand)

    EC.variator = [crossover.custom_crossover, mutate.mutate_setting]
    EC.observer = ec.observers.population_observer
    
    EC.replacer = ec.replacers.generational_replacement
    #EC.replacer = ec.replacers.crowding_replacement
    
    EC.terminator = ec.ec.terminators.generation_termination
    EC.archiver = archive.my_archiver


    final_pop = EC.evolve(
        generator=args["problem"].generator,
        evaluator=args["problem"].evaluator,
        pop_size=args["population_size"],
        maximize=False,
        **args
    )
    final_pop.sort(reverse=True)
    print(final_pop)
    #write the archive in a file
    with open("statistics.txt", "w") as file:
        file.write(str(EC.archive))

    #print the decoded texts
    for i in range(len(args["problem"].cipher_texts)):
        print("Decoded text: " + args["problem"].cipher_texts[i] + " -> " + Enigma(final_pop[0].candidate["rotors"], final_pop[0].candidate["reflector"], final_pop[0].candidate["rotor_positions"], final_pop[0].candidate["ring_settings"], final_pop[0].candidate["plugboard_connections"]).encrypt_string(args["problem"].cipher_texts[i]))

    #plot the fitness function at each generation
    if display:
        import matplotlib.pyplot as plt
        data = EC.archive
        med = []
        mean = []
        worst = []
        best = []
        for i in range(len(data)):
            worst.append(float(data[i][0]))
            best.append(float(data[i][1]))
            med.append(float(data[i][2]))
            mean.append(float(data[i][3]))
        # worst_norm = [float(i)/sum(worst) for i in worst]
        # best_norm = [float(i)/sum(best) for i in best]
        # med_norm = [float(i)/sum(med) for i in med]
        # mean_norm = [float(i)/sum(mean) for i in mean]
        plt.title('Fitness function')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.plot([-i for i in worst], label='worst')
        plt.plot([-i for i in best], label='best')
        plt.plot([-i for i in med], label='median')
        plt.plot([-i for i in mean], label='mean')
        #plt.boxplot([-i for i in best])
        plt.yscale('log')
        plt.legend()
        plt.savefig('EC_generic.pdf', format='pdf')
        plt.show()


    return final_pop[0].candidate   

def optimize_setting(settings = ["rotors", "rotor_positions", "ring_settings", "plugboard_connections", "reflector"]): 
                                #  "rotors", "rotor_positions", "ring_settings", "plugboard_connections", "reflector", 
                                # "rotors", "rotor_positions", "ring_settings", "plugboard_connections", "reflector", 
                                # "rotors", "rotor_positions", "ring_settings", "plugboard_connections", "reflector"
    #optimize one setting at a time
    #for each setting, the others are fixed
    sett = []
    best_rotor=None
    best_reflector=None
    best_rotor_positions=None
    best_ring_settings=None
    best_plugboard_connections=None
    for setting in settings:
        print("Optimizing setting: " + setting)
        candidate = main(setting, best_rotor, best_reflector, best_rotor_positions, best_ring_settings, best_plugboard_connections)
        if setting == "rotors":
            best_rotor = candidate[setting]
        elif setting == "reflector":
            best_reflector = candidate[setting]
        elif setting == "rotor_positions":
            best_rotor_positions = candidate[setting]
        elif setting == "ring_settings":
            best_ring_settings = candidate[setting]
        elif setting == "plugboard_connections":
            best_plugboard_connections = candidate[setting]
        best_setting = candidate[setting]
        sett.append(best_setting)
    print(sett)
    
    
if __name__ == '__main__':
    #main()     #optimize all settings at the same time
    optimize_setting()      #optimize one setting at a time

''' PROBLEMS:
- in the plugboard connections: the pair of letters to be swapped must be unique, but it is not. 
    possible solution: check if the pair of letters is already in the plugboard connections and if so, generate another pair
    act on the generator --> done
    
- the fitness function is not good enough: it is not able to distinguish between the correct and the wrong configurations.
    possible solution 1: change the fitness function.
    possible solution 2: change mutation and crossover operators to promote exploration of the search space. 
'''

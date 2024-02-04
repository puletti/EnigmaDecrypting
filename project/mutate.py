import random
import copy

def my_mutate(random, candidates, args):
    alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
    rate = args.setdefault('mutation_rate', 0.5)
    if random.random() < rate:
        rotors = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
        reflectors = ["B", "C"]
        c = copy.copy(candidates)
        mutants = []
        for i in range(len(candidates)):
            for feature in c[i]:
                if feature == "rotors":
                    #if random.random() < rate:
                    c[i][feature] = random.sample(rotors, 3)
                elif feature == "reflector":
                    #if random.random() < rate:
                    c[i][feature] = random.choice(reflectors)
                elif feature == "rotor_positions":
                    #if random.random() < rate:
                    c[i][feature] = random.sample(range(26), 3)
                elif feature == "ring_settings":
                    #if random.random() < rate:
                    c[i][feature] = random.sample(range(26), 3)
                elif feature == "plugboard_connections":
                    #if random.random() < rate:
                    alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
                    plug = ""
                    for j in range(random.randint(0, 13)):
                        let1 = random.choice(alphabet)
                        alphabet.remove(let1)
                        let2 = random.choice(alphabet)
                        alphabet.remove(let2)
                        plug += let1 + let2 + " "
                    c[i][feature] = plug
            mutants.append(c[i])
        return mutants
       
def mutate_setting(random, candidates, args):
    rate = args.setdefault('mutation_rate', 0.5)
    if random.random() < rate:
        c = copy.copy(candidates)
        mutants = []
        for i in range(len(candidates)):
            if args["setting"] == "rotors":
                c[i]["rotors"] = random.sample(["I", "II", "III", "IV", "V", "VI", "VII", "VIII"], 3)
            elif args["setting"] == "reflector":
                c[i]["reflector"] = random.choice(["B", "C"])
            elif args["setting"] == "rotor_positions":
                c[i]["rotor_positions"] = random.sample(range(26), 3)
            elif args["setting"] == "ring_settings":
                c[i]["ring_settings"] = random.sample(range(26), 3)
            elif args["setting"] == "plugboard_connections":
                alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split()
                plug = ""
                for j in range(random.randint(0, 13)):
                    let1 = random.choice(alphabet)
                    alphabet.remove(let1)
                    let2 = random.choice(alphabet)
                    alphabet.remove(let2)
                    plug += let1 + let2 + " "
                c[i]["plugboard_connections"] = plug
            #c[i][args["setting"]] = args["problem"].config[args["setting"]]
            mutants.append(c[i])
        return mutants
    

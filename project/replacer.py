def my_replacer(population, parents, offspring, args):
    psize = len(population)
    population.sort(reverse=True)
    offspring.sort(reverse=True)
    survivors = population[:psize // 4]
    num_remaining = psize - len(survivors)
    for i in range(num_remaining):
        survivors.append(offspring[i])
    return survivors

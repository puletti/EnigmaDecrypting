def my_observer(population, num_generations, num_evaluations, args):
    """
    Args:
        population (list): A list of `ec.Individual` objects.
        num_generations (int): The current generation number.
        num_evaluations (int): The current evaluation number.
        args (dict): A dictionary of keyword arguments.
    """
    best = max(population)
    print('Generation: {0}'.format(num_generations) + "\n")
    print('Population: {0}'.format(population) + "\n")
    print('Num Evaluations: {0}'.format(num_evaluations) + "\n")
    print('Best Solution: {0}'.format(str(best.candidate)) + "\n")
    

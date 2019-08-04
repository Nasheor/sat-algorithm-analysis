import localsearch
import functools
import random
import math
import time


def solve(chromosomes, num_genes, chromosome_fitness, generations=50):
    """
    :param chromosomes: Number of Clauses
    :param num_genes: Number of variables
    :param chromosome_fitness:  Weight of each clause
    :param generations: Number of steps
    :return: evolved weight values and time of execution

    Public method for solving Genetic algorithm  implementing the following
    1 - Initial population
    2 - Natural Selection
    3 - Crossover
    4 - Mutation
    5 - Fitness function
    """
    print("c Applying GA")
    # 1 - Initial Population
    current_configuration = localsearch.random_value_assignment(num_genes)

    # Number of pairs that should be picked to mate
    num_of_pairs = int(len(chromosomes)/2)

    # Mutation Probability
    mutation_rate = 1 / len(chromosomes)

    fitness_values = list()
    time_values = list()
    start = time.time()
    for generation in range(generations):
        # 2 - Generate a mating pool - Natural Selection
        parent_pairs, fitness_pair = generate_mating_pool(chromosomes, chromosome_fitness, num_of_pairs)
        index = 0
        for parent_pair in parent_pairs:

            # 3 - Generate Children from Parent pairs using either single point crossover or two point crossover
            children = generate_children(parent_pair)

            # 4 - Mutating the child chromosomes formed from crossover
            mutated_children = list()
            for child in children:
                if child is not None:
                    mutated_children.append(mutate(child, mutation_rate, current_configuration))
                else:
                    break

            # 5 - Calculating the fitness of the child chromosome
            for child in mutated_children:
                child_fitness = calculate_fitness(child, fitness_pair[index], current_configuration)
                worst_genome = chromosome_fitness.index(min(chromosome_fitness))
                # Create next generation by replacing the chromosome with the worst fitness
                if child_fitness > min(chromosome_fitness):
                    chromosomes[worst_genome] = child
                    chromosome_fitness[worst_genome] = child_fitness
            index += 1

        end = time.time()
        fitness_values.append(functools.reduce(lambda total, w: total + int(w), chromosome_fitness))
        time_values.append(end - start)
    return fitness_values, time_values


def generate_mating_pool(chromosomes, chromosome_fitness, num_of_pairs):

    """
    :param chromosomes: list of clauses
    :param chromosome_fitness: list of weights of each clause
    :param num_of_pairs: Number of parents pairs to be selected for crossover
    :return:

    Selects `num_of_pairs` from the list of chromosomes for crossover.
    It is defined as follows:
        1) Sum up the fitness values of all chromosomes in the population
        2) Generate a random number between 0 and the sum of the fitness values
        3) Select the first chromosome whose fitness value added to the sum of the fitness
           values of the previous chromosomes is greater than or equal to the random number
    """
    parents = []
    fitness = []

    # 1 - Stores the sum of all the fitness in the population
    total_fitness = functools.reduce(lambda total, w: total + int(w), chromosome_fitness)

    for pair in range(num_of_pairs):
        parent = []
        fit = []
        # 2 -Generating a random witness between 0 and sum of all fitness values
        random_fitness = random.randint(0, (total_fitness+1))
        iterations = 0
        while len(parent) < 2 and iterations < len(chromosomes):
            chromosome_index = 0
            cumulative_fitness = 0
            for fitness_value in chromosome_fitness:
                cumulative_fitness += fitness_value
                if cumulative_fitness >= random_fitness:
                    if chromosomes[chromosome_index] in parent:
                        chromosome_index += 1
                        continue
                    # 3 - Selecting the first chromosome that is not already a parent and the fitness when added
                    #     to the cumulative sum of previous chromosomes is greater than the random firness
                    else:
                        parent.append(chromosomes[chromosome_index])
                        fit.append(fitness_value)
                        chromosome_index += 1
                        break
                chromosome_index += 1
            iterations += 1
        parents.append(parent)
        fitness.append(fit)

    return parents, fitness


def generate_children(parent_pair):
    """
    :param parent_pair: [chromosome-1, chromosome-2] upon which the crossover will be done
    :return: list, list

    The child chromosomes are formed from either a single point crossover or two point crossover. The chance of
    a single point crossover or double point crossover is 50%

    """
    do_single_point_crossover = random.choice([True, False])
    first_child = None
    second_child = None
    if len(parent_pair) == 2:
        if do_single_point_crossover:
            cut_point = random.randint(0, int(len(parent_pair[0])/2))
            first_child = parent_pair[0][:cut_point] + parent_pair[1][cut_point:]
            second_child = parent_pair[1][:cut_point] + parent_pair[0][cut_point:]

        else:
            if len(parent_pair[1]) > len(parent_pair[0]):
                size = len(parent_pair[0])
                if size == 1:
                    first_point = 0
                else:
                    first_point = random.randint(0, int(len(parent_pair[0])/2))
                second_point = random.randint(first_point, len(parent_pair[0]))
            else:
                size = len(parent_pair[1])
                if size == 1:
                    first_point = 0
                else:
                    first_point = random.randint(0, int(len(parent_pair[1])/2))
                second_point = random.randint(first_point, len(parent_pair[1]))

            first_child = parent_pair[0][:first_point] + \
                parent_pair[1][first_point:second_point] + \
                parent_pair[0][second_point:]
            second_child = parent_pair[1][:first_point] + \
                parent_pair[0][first_point:second_point] + \
                parent_pair[1][second_point:]

    return first_child, second_child


def mutate(child, mutation_prob, current_configuration):
    """
    
    :param child: child chromosome to mutate
    :param mutation_prob: 
    :param current_configuration: 
    :return: the mutated child
    """
    current_rate = 1.0/random.randrange(1, len(child)+1)
    while current_rate == 0:
        current_rate = 1.0 / random.randrange(1, len(child)+1)

    # if the current _rate is grater than mutation prob, a gene from the child is fliped value
    if current_rate > mutation_prob:
        gene_to_mutate = random.randint(0, len(child)-1)
        var = abs(child[gene_to_mutate])-1
        current_configuration[var] = not current_configuration[var]
    return child


# Fitness is calculated based on the average of fitness of the two parents and the count of positive genes
def calculate_fitness(child, fitness_pair, current_configuration):
    """
    :param child: mutated child chromosome whose fitness is to be calculates
    :param fitness_pair: list of fitness values of the parent chromosomes
    :param current_configuration: current configuration of the variables
    :return: the fitness of the child chromosome

    The fitness of the child chromosome is calculated based on the number of positive values in the chromosome
    the value of the positive gene is added to the fitness of the parent chromosome and the value of negative gene
    is divided by 2 and subtracted from the fitness of the parent chromosome
    """
    average_fitness = int((fitness_pair[0] + fitness_pair[1])/2)
    fitness = 0
    for gene in child:
        value = current_configuration[abs(gene)-1]
        if (value and gene > 0) or (not value and gene < 0):
            fitness += abs(gene)
        else:
            fitness -= int(abs(gene)/2)

    if (fitness > 0) and fitness < math.pow(2, 63):
        return fitness
    return average_fitness

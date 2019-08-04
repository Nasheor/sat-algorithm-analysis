import gwsat
import ga
import sys
import matplotlib.pyplot as plt


def generate_plots_for_gwsat(filename):
    clauses, num_vars = parsed_cnf_file(filename)

    time_values, clauses_sat, random_walk_time, random_walk_result, choose_and_flip_time, choose_and_flip_result = \
        gwsat.solve(num_vars, clauses, len(clauses)//2, 0.4)

    steps = [step + 1 for step in range(len(clauses)//2)]

    print("c Generating graphs for GWSAT")

    # Plotting RTD graph for Time VS Steps
    plt.title("RTD graph for Time VS Restarts")
    plt.plot(time_values, steps)
    plt.ylabel("Steps")
    plt.xlabel("Time")
    plt.show()

    # Potting RTD graph for number of satisfied clauses over time
    plt.title("RTD graph for Time VS Number of satisfied clauses")
    plt.plot(time_values, clauses_sat)
    plt.xlabel("Time")
    plt.ylabel("Number of Satisfied Clauses")
    plt.show()

    # Plotting RTD graph for number of satisfied clauses using Random walk over time
    plt.title("RTD graph for Random Walk VS Number of satisfied clauses")
    plt.plot(random_walk_time, random_walk_result)
    plt.xlabel("Time")
    plt.ylabel("Number of Satisfied Clauses")
    plt.text(3, 8, "Total Number of Random Walks: "+str(len(random_walk_result)))
    plt.show()

    # Plotting RTD graph for number of satisfied clauses using Choose and Flip over time
    plt.title("RTD graph for Choose and Flip VS Number of satisfied clauses")
    plt.plot(choose_and_flip_time, choose_and_flip_result)
    plt.xlabel("Time")
    plt.ylabel("Number of Satisfied Clauses")
    plt.text(3, 8, "Total Number of Choose and Flips: "+str(len(choose_and_flip_result)))
    plt.show()

    # Plotting RTD graph for Random Walk vs Choose and Flip
    plt.title("RTD graph for Random Walk vs Choose and Flip")
    category = ["Max value Random Walk", " Max value Choose and Flip", "Min value Random Walk",
                "Min value Choose and Flip"]
    bars = plt.bar(category, [max(random_walk_result), max(choose_and_flip_result),
                              min(random_walk_result), min(choose_and_flip_result)])
    for bar in bars:
        val = bar.get_height()
        plt.text(bar.get_x(), val + .0055, val)
    plt.show()


def parsed_cnf_file(filename):
    """
    Parses the specified cnf file for gwsat

    Returns:

        - clauses: All the clauses into a set of frozensets
        - num_vars: Number of variables

    """
    clauses = []
    num_vars = 0
    with open(filename) as f:
        ok_to_read = False
        is_clause_done = False
        clause = []
        for line in f:
            if line[0] == "%":
                break
            if ok_to_read:
                values = list(map(int, line.strip().split()))
                if is_clause_done:
                    clause = []
                for value in values:
                    if value == 0:
                        is_clause_done = True
                        if clause not in clauses:
                            clauses.append(clause)
                    else:
                        clause.append(value)

                        if value < -num_vars or value > num_vars:
                            print('Error in variable value ', value, '. Its must be in range [1, ', num_vars, ']')
                            exit(0)
            if line[0] == "p":
                ok_to_read = True
                first_line = line.split()
                num_vars = int(first_line[2])

                if first_line[1] != "cnf":
                    print("Invalid File Type. File type has to be CNF")
                    exit(0)

    return clauses, num_vars


def generate_plots_for_ga(filename):
    chromosomes, num_genes, chromosome_fitness, top_fitness = parsed_wcnf_file(filename)

    generations = [generation+1 for generation in range(50)]
    fitness_values, time_values = ga.solve(chromosomes, num_genes, chromosome_fitness)

    print("c Generating graphs for GA")

    # Plotting RTD graph for time vs generations
    plt.title("RTD graph for Time VS Generations")
    plt.plot(time_values, generations)
    plt.ylabel("Generations")
    plt.xlabel("Time")
    plt.show()

    # Plotting RTD graph for Fitness stats over generations
    plt.title("RTD graph for Generations VS Fitness")
    plt.plot(generations, fitness_values)
    plt.ylabel("Fitness")
    plt.xlabel("Generation")
    plt.show()

    # Plotting RTD graph for Time vs Fitness values
    plt.title("RTD graph for Time VS Fitness")
    plt.plot(time_values, fitness_values)
    plt.ylabel("Fitness")
    plt.xlabel("Time")
    plt.show()


def parsed_wcnf_file(filename):
    """
    Parses the specified wcnf file for ga

    Returns:

        - chromosomes: All the clauses in the input file
        - num_genes: Number of variables
        - chromosome_fitness: Fitness of each clause in the  input file
        - top_fitness: Highest fitness in the input file

    """
    chromosomes = []
    num_genes = 0
    top_fitness = 0
    chromosome_fitness = []

    with open(filename) as f:
        ok_to_read = False
        is_clause_done = False
        chromosome = []
        for line in f:
            if line[0] == "%":
                break
            if ok_to_read:
                values = list(map(int, line.strip().split()))
                if is_clause_done:
                    chromosome = []
                for value in values:
                    if value == 0:
                        is_clause_done = True
                        if chromosome not in chromosomes:
                            chromosome_fitness.append(int(chromosome[0]))
                            del chromosome[0]
                            chromosomes.append(chromosome)
                    else:
                        chromosome.append(value)

                        if chromosome.index(value) != 0:
                            if value < -num_genes or value > num_genes:
                                print('Error in variable value ', value, '. Its must be in range [1, ', num_genes, ']')
            if line[0] == "p":
                ok_to_read = True
                first_line = line.split()
                num_genes = int(first_line[2])
                top_fitness = int(first_line[4])

                if first_line[1] != "wcnf":
                    print("Invalid File Type. File type has to be CNF")

    return chromosomes, num_genes, chromosome_fitness,  top_fitness


#######################
#                     #
# Program entry point #
#                     #
#######################
if __name__ == '__main__':
    """
    Execute the specified algorithm and prints the result
    """
    algorithm = sys.argv[1]
    file = sys.argv[2]
    if algorithm.upper() == "GWSAT":
        print("c Trying to read file ", file)
        generate_plots_for_gwsat(file)
    elif algorithm.upper() == "GA":
        print("c Trying to read file ", file)
        generate_plots_for_ga(file)
    else:
        print("Only GWSAT and GA available at the moment. Try Again")


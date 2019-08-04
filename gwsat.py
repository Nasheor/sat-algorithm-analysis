import localsearch
import random
import time


def join_clause(clause):
    """
    :param clause:
    :return: string

    Takes in array in the form of [25, 32, 44, 50]
    and returns "25 32 44 50"
    """
    return ' '.join(str(individual) for individual in clause)


def solve(num_vars, clauses, num_flips, wp, steps=50):
    """
    Solve(num_vars, clauses, num_flips, wp, steps) -> [bool,...]
    Try to find an interpretation that satisfies the given formula.
    The solution is composed by list of boolean values
    Note: there can't be repeated clauses or literals into a clause in the
    formula

    """
    max_sat_clauses = 0
    print("c Using GWSAT Algorithm")
    clauses_sat = list()
    time_values = list()
    random_walk_result = list()
    random_walk_time = list()
    choose_and_flip_result = list()
    choose_and_flip_time = list()
    solution_found = False

    start = time.time()
    for current_step in range(steps):
        current_configuration = localsearch.random_value_assignment(num_vars)
        list_sat_clauses = {join_clause(clause): 0 for clause in clauses}
        num_sat_clauses, list_sat_clauses = localsearch.initialize_clause_data(
            clauses,
            current_configuration,
            list_sat_clauses)
        for flip in range(num_flips):
            random_prob = random.random()
            # Execute Random walk or Choose and Flip
            # based on random probability generated
            if random_prob < wp:
                current_configuration, num_sat_clauses, list_sat_clauses = random_walk(
                    clauses,
                    current_configuration,
                    list_sat_clauses)
                operation = "random walk"
                if current_step == 0:
                    random_walk_result.append(num_sat_clauses)
                    random_walk_time.append((time.time()-start))
            else:
                current_configuration, num_sat_clauses, list_sat_clauses = localsearch.choose_and_flip(
                    clauses,
                    current_configuration,
                    list_sat_clauses
                )
                operation = "choose and flip"
                if current_step == 0:
                    choose_and_flip_time.append((time.time()-start))
                    choose_and_flip_result.append(num_sat_clauses)

            if num_sat_clauses > max_sat_clauses or num_sat_clauses == len(clauses):
                max_sat_clauses = num_sat_clauses
                solution_found = True
                # Solution found if the max number of satisfied clauses equals the number of satisfied
                # clauses in the input file
                if max_sat_clauses == len(clauses):
                    print("s Satifiable")
                    print("operation: ", operation)
                    print("solution found at flip number: ", flip)
                    print("solution config: ", current_configuration)

            if not solution_found:
                print("u Unsatisfiable configuration in ", num_flips)
            end = time.time()
            time_values.append(end-start)
            clauses_sat.append(num_sat_clauses)

        return time_values, clauses_sat, random_walk_time, random_walk_result, choose_and_flip_time, \
            choose_and_flip_result


def random_walk(clauses, current_configuration, list_sat_clauses):
    """
    :param clauses:
    :param current_configuration:
    :param list_sat_clauses:
    :return:

    Selects a variable using random walk approach, flips its value and returns the result of
    the variable switch to the calling function
    """

    random_gene = 0

    # Iterating over the list of clauses to find an unsatisfied clause
    # and selecting a random individual from the clause
    for clause in list_sat_clauses.keys():
        if list_sat_clauses[clause] == 0:
            random_gene = abs(int(random.sample(list(clause.split()), 1)[0]))
            break

    new_configuration = current_configuration.copy()

    # Reversing the value of the random gene that's selected
    new_configuration[random_gene-1] = not new_configuration[random_gene-1]

    return localsearch.get_result_of_input_change_in_clauses(
        clauses,
        new_configuration,
        list_sat_clauses
    )
from random import choice
import random


def random_value_assignment(num_vars):
    """
    random_value_assignment(num_vars:int): [boolean]

    Creates a random interpretation for this formula, starting with None to
    mach the range of values on the formula: [-num_vars, -1] U [1, num_vars]
    """
    values = []
    for i in range(num_vars):
        values.append(choice([True, False]))
    return values


def initialize_clause_data(clauses, current_config, list_sat_clauses):
    """
    initialize_clause_data(clauses, current_config, list_sat_clauses) -> num_sat_clauses, list_sat_clauses

    Initialize the number of sat literals per clause and counts the number of
    satisified clauses
    """
    num_sat_clauses = 0

    for clause in clauses:
        parsed_clause = ' '.join(str(individual) for individual in clause)
        for individual in clause:
            individual = abs(individual)
            if current_config[individual-1]:
                num_sat_clauses += 1
                list_sat_clauses[parsed_clause] += 1
                break

    return num_sat_clauses, list_sat_clauses


def choose_and_flip(clauses, current_configuration, list_sat_clauses=None):
    """
    Chooses and flips the variable that improves or worsens less possible the
    amount of satisfied clauses
    """
    chosen_var = random.randint(0, len(current_configuration))

    # Choosing a unsatisfied clause
    # for clause in list_sat_clauses.keys():
    #     if list_sat_clauses[clause]:
    #         tmp = clause.split()
    #         var = random.randint(0, len(tmp)-1)
    #         chosen_var = abs(int(tmp[var]))

    new_configuration = current_configuration.copy()
    new_configuration[chosen_var-1] = not new_configuration[chosen_var-1]

    return get_result_of_input_change_in_clauses(
        clauses,
        new_configuration,
        list_sat_clauses
    )


def get_result_of_input_change_in_clauses(clauses, new_configuration,
                                          list_sat_clauses=None):
    """
    Counts the number of satisfied clauses after flipping the value of 'var'
    """
    new_list_sat_clauses = list_sat_clauses
    new_num_sat_clauses = 0
    for clause in clauses:
        parsed_clause = ' '.join(str(individual) for individual in clause)
        for individual in clause:
            if (new_configuration[abs(individual)-1] and individual > 0) or \
                    not new_configuration[abs(individual)-1] and individual < 0:
                new_num_sat_clauses += 1
                if len(new_list_sat_clauses) > 1:
                    new_list_sat_clauses[parsed_clause] += 1
                break

    return new_configuration, new_num_sat_clauses, new_list_sat_clauses




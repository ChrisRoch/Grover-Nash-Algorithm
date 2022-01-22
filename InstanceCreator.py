import numpy as np

# Construct graphical game instances by defining the number of best response sets (BRS) and nash equilibria (NE)
number_sets = 9
number_ne = 1
set_list = [[['a1', 'b1', 'c0'], ['a0', 'b1', 'c0'], ['a0', 'b1', 'c1'], ['a1', 'b0', 'c0']],
            [['b1', 'a1', 'c0'], ['b0', 'a1', 'c0'], ['b1', 'a1', 'c1']],
            [['c1', 'b0', 'a0'], ['c0', 'b1', 'a1']]]

data = {'set_list': set_list, 'number_ne': number_ne, 'number_sets': number_sets}
np.save('./datasets/' + 'BRS_' + str(number_sets) + '_Number_NE_' + str(number_ne), data)
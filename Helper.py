from itertools import combinations
from qiskit.circuit.library import PhaseOracle
import numpy as np
import matplotlib.pyplot as plt


# Creates a list with all possible permutations of strategies of a given player.
def intra_function(x):
    return list(combinations(x, 2))


# The compatibility function iterates through the sets of best responses of two players and determines if two
# strategies are compatible, i.e, this function is checking the inter conditions.
def compatibility(x, y, strategies):
    union = []
    for K in x:
        m = strategies.get(str(K))
        for L in y:
            n = strategies.get(str(L))
            p = min(len(m), len(n))
            U = set(m) & set(n)
            if not len(U) == p:
                union.append([K, L])
                continue
    return union


def construct_dimacs_file(set_list, file_name):

    # A dictionary that labels the strategies of each player is created.
    # These labels will then be assigned to the variables when solving the SAT problem.
    # Furthermore an auxiliary list containing the indices of the players' strategies is created.
    strategies = {}
    index_list = []
    p = 0
    for i in range(len(set_list)):
        temp = []
        for j in range(len(set_list[i])):
            temp.append(p+1)
            p = p + 1
            strategies['%s' % (p)] = set_list[i][j]
        index_list.append(temp)

    # The CNF DIMACS file is created.
    # The number of variables in the SAT problem is determined by the total number of best strategies.
    f = open(file_name, "w+")
    f.write("c example DIMACS-CNF \r")
    f.write("p cnf %s a \r" % (len(strategies)))

    # Each player's intra conditions are written as CNF clauses to the DIMACS file.
    for k in index_list:
        h = intra_function(k)
        l = str(k).replace('[', '').replace(']', '').replace(",", "") + " 0"
        f.write("%s \r" % l)
        for i in range(len(h)):
            a = str(h[i]).replace('(', '-').replace(')', '').replace(',', '- ') + " 0"
            b = a.replace("-  ", " -")
            f.write("%s \r" % b)

    # A list of neighbouring players is created.
    # The list contains the indices of the strategies of neighbouring players.
    neigh = []
    for i in index_list:
        for j in index_list:
            u = []
            # The following if statements prevent double counting and redundant verification.
            if (i != j and len(i) < len(j)) or (i != j and len(i) == len(j)):
                if [j, i] in neigh:
                    continue
                else:
                    for l in strategies.get(str(i[0])):
                        # Checks if two strategies are compatible
                        u.append(any([str(l[0]) in p for p in strategies.get(str(j[0]))]))
                    if sum(u) >= len(strategies.get(str(i[0]))):
                        neigh.append([i, j])

    # The inter conditions are written in CNF clauses to the DIMACS file.
    # This iterates through all lists of best responses for neighbouring players and excludes them according to the
    # intra conditions for incompatible best responses and writes them as CNF clauses to the file.
    for b in neigh:
        if len(b[1]) <= len(b[0]):
            for x in compatibility(b[1], b[0], strategies):
                X = str(x).replace('[', '-').replace(']', '').replace(',', '-') + " 0"
                X = X.replace("- ", " -")
                f.write("%s \r" % X)
        if len(b[1]) > len(b[0]):
            for x in compatibility(b[0], b[1], strategies):
                X = str(x).replace('[', '-').replace(']', '').replace(',', '-') + " 0"
                X = X.replace("- ", " -")
                f.write("%s \r" % X)

    # Some final formatting of the file:
    with open(file_name, 'r') as f:
        get_all = f.readlines()

    # Writes the number of clauses on the beginning of the file, according to CNF DIMACS format.
    with open(file_name, 'w') as f:
        for i, line in enumerate(get_all, 1):
            if i == 2:
                f.writelines("p cnf %s %s \r" % (len(strategies), len(get_all) - 2))
            else:
                f.writelines(line)

    # This simply removes the last empty line on the file, as this empty line causes problems when using the SAT solver.
    with open(file_name, 'r') as f:
        data = f.read()
        with open(file_name, 'w') as w:
            w.write(data[:-1])

    with open(file_name, 'r') as f:
        dimacs = f.read()

    # print(dimacs)
    return strategies, dimacs


def decompose_oracle_circuit(level, circuit):
    for i in range(level):
        circuit = circuit.decompose()
    return circuit


def construct_phase_oracle_from_file(file_name):
    return PhaseOracle.from_dimacs_file(file_name)


def analyse_oracle_circuit(oracle, level_of_decomposition=2):
    decomposed_oracle_circuit = decompose_oracle_circuit(level_of_decomposition, oracle)

    print("Gate types on the decomposed circuit:", decomposed_oracle_circuit.count_ops())
    print("Circuit depth: ", decomposed_oracle_circuit.depth())
    print("Number of qubits and cbits in circuit:", decomposed_oracle_circuit.width())
    print("Total number of gate operations in circuit:", decomposed_oracle_circuit.size())
    print("Total number of ancillas:", decomposed_oracle_circuit.num_ancillas)


def plot_circuit_results(circuit_results, cutoff=6):
    # sorted by key, return a list of tuples
    lists = sorted(circuit_results.items(), reverse=True, key=lambda item: item[1])
    x, y = zip(*lists)  # unpack a list of pairs into two tuples
    n_measurements = sum(y)
    y_values = np.array(y) / n_measurements
    x_values = [j[::-1] for j in x]

    plt.bar(x_values[:cutoff], y_values[:cutoff])
    plt.xticks(rotation=45)
    plt.xlabel('Measured states (with defined cutoff)')
    plt.ylabel('Probability %')
    plt.tight_layout()
    plt.show()

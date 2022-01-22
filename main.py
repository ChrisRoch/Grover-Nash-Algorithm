from Helper import construct_dimacs_file, plot_circuit_results, analyse_oracle_circuit
from Helper import construct_phase_oracle_from_file
from Solver import apply_grover
from Verifier import verify_circuit_results
import numpy as np

if __name__ == '__main__':
    # Change to the name of the dataset
    dataset_name = 'BRS_9_Number_NE_1'

    data = np.load('./datasets/' + dataset_name + '.npy', allow_pickle=True)
    set_list = data.item().get('set_list')
    number_ne = data.item().get('number_ne')
    file_name = dataset_name + '.dimacs'

    # Constructs and saves the DIMAC file.
    strategies, dimacs_file = construct_dimacs_file(set_list, file_name)

    # The oracle circuit of the problem is created from the DIMACS file
    oracle = construct_phase_oracle_from_file(file_name)
    analyse_oracle_circuit(oracle, level_of_decomposition=2)

    # Grover's amplitude amplification is applied on the oracle
    circuit_results = apply_grover(oracle, len(strategies.items()), n_solutions=number_ne)
    plot_circuit_results(circuit_results, cutoff=6)

    # Result is decoded and printed
    nash_equilibria = verify_circuit_results(circuit_results, dimacs_file)
    nash_equilibria_decoded = []
    for q in nash_equilibria:
        nash_equilibria_decoded.append([pos + 1 for pos, char in enumerate(q) if char == "1"])

    for i in range(len(nash_equilibria)):
        print("%s is a NE" % (nash_equilibria[i]))
        print("With strategy profile:")
        for j in nash_equilibria_decoded[i]:
            print(strategies.get("%s" % (j)))


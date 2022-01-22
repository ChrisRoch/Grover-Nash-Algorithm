import math
from qiskit import Aer
from qiskit.utils import QuantumInstance
from qiskit.algorithms import Grover, AmplificationProblem


def apply_grover(oracle, n_qubits, n_solutions=1):
    backend = Aer.get_backend('qasm_simulator')
    quantum_instance = QuantumInstance(backend, shots=1024)

    problem = AmplificationProblem(oracle=oracle)

    # Use Grover's algorithm to solve the amplification problem
    # Number of iterations must be adjusted depending on the number of solutions
    number_iterations = math.ceil((math.pi / 4) * math.sqrt((2 ** n_qubits) / n_solutions))
    grover = Grover(iterations=number_iterations, quantum_instance=quantum_instance)
    result = grover.amplify(problem)

    circuit_results = result.circuit_results[-1]
    print("circuit results", circuit_results)
    return circuit_results

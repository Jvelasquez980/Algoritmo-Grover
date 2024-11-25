from qiskit import QuantumCircuit, transpile
from qiskit_aer.aerprovider import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np

def grover_algorithm(oracle_function, n_qubits):
    # Crear el circuito cuántico con espacio para mediciones
    qc = QuantumCircuit(n_qubits, n_qubits)

    # Inicialización en superposición uniforme
    qc.h(range(n_qubits))
    
    # Número de iteraciones recomendadas para maximizar la probabilidad
    n_iterations = int(np.floor(np.pi / 4 * np.sqrt(2**n_qubits)))
    
    for _ in range(n_iterations):
        # Aplicar el oráculo
        qc.compose(oracle_function, inplace=True)
        
        # Aplicar el operador de difusión
        qc.h(range(n_qubits))
        qc.x(range(n_qubits))
        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)
        qc.x(range(n_qubits))
        qc.h(range(n_qubits))

    # Medición
    qc.measure(range(n_qubits), range(n_qubits))
    
    # Simulación del circuito
    simulator = AerSimulator()
    transpiled_circuit = transpile(qc, simulator)
    result = simulator.run(transpiled_circuit, shots=1024).result()
    
    return result.get_counts()

# Ejemplo: Oráculo para buscar el estado |11>
def oracle_example():
    """Un oráculo que marca el estado |11> para n=2 qubits."""
    oracle = QuantumCircuit(2)
    oracle.cz(0, 1)  # Aplicar puerta CZ para marcar el estado |11>
    return oracle

# Probar el algoritmo con el oráculo ejemplo
oracle = oracle_example()
result = grover_algorithm(oracle, n_qubits=2)

# Mostrar resultados
print("Resultados:", result)
plot_histogram(result).show()

#No supe solucionar un error por lo que no puedo ver el histograma, una disculpa


"""
Ejemplo de código para ejecutar algoritmos cuánticos con Qiskit.
"""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, assemble, transpile
from qiskit_ibm_provider import IBMQ
from qiskit.providers.aer import Aer
from qiskit.providers.fake_provider import FakeAthens
from qiskit.visualization import plot_histogram, plot_gate_map
import qiskit.tools.jupyter
import numpy as np

# --- 1. Creación de un circuito con registros ---
print("--- Creando circuito con registros ---")
qr = QuantumRegister(2, 'a')
qc = QuantumCircuit(qr)
qc.h(qr[0])
qc.cx(qr[0], qr[1])
qc.draw()
print("Circuito con registros listo.")

# --- 2. Aer simulator y vector de estado ---
print("\n--- Simulando con Aer y obteniendo vector de estado ---")
sv_sim = Aer.get_backend('aer_simulator')
qc.save_statevector()
qobj = assemble(qc)
job = sv_sim.run(qobj)
ket = job.result().get_statevector()
print("Vector de estado (Bell State):")
for amplitude in ket:
    print(amplitude)

# --- 3. Registros clásicos y medición ---
print("\n--- Midiendo y obteniendo histograma ---")
cr = ClassicalRegister(2, 'creg')
qc.add_register(cr)
qc.measure(qr[0], cr[0])
qc.measure(qr[1], cr[1])

aer_sim = Aer.get_backend('aer_simulator')
qobj = assemble(qc, shots=8192)
job = aer_sim.run(qobj)

hist = job.result().get_counts()
print("Resultados de la medición (histograma):")
print(hist)

plot_histogram(hist)

# --- 4. Simplificación de la notación ---
print("\n--- Creando un circuito con notación simplificada ---")
qc = QuantumCircuit(2, 1)
qc.h(0)
qc.cx(0, 1)
qc.measure(1, 0)
qc.draw()
print("Circuito simplificado listo.")

# --- 5. Creando puertas personalizadas ---
print("\n--- Creando y usando una puerta personalizada ---")
sub_circuit = QuantumCircuit(3, name='toggle_cx')
sub_circuit.cx(0, 1)
sub_circuit.cx(1, 2)
sub_circuit.cx(0, 1)
sub_circuit.cx(1, 2)
toggle_cx = sub_circuit.to_instruction()

qr_new = QuantumRegister(4)
new_qc = QuantumCircuit(qr_new)
new_qc.append(toggle_cx, [qr_new[1], qr_new[2], qr_new[3]])
new_qc.draw()
print("Puerta personalizada agregada al nuevo circuito.")

# --- 6. Ejecución en hardware real o simulado con ruido ---
print("\n--- Transpilando y ejecutando en un simulador con ruido ---")
athens = FakeAthens()
qc_noise = QuantumCircuit(5, 5)
qc_noise.x(0)
for q in range(4):
    qc_noise.cx(0, q + 1)
qc_noise.measure_all()

t_qc = transpile(qc_noise, athens)
t_qc.draw()

qobj = assemble(t_qc)
counts = athens.run(qobj).result().get_counts()
print("Conteo de resultados con modelo de ruido:")
print(counts)
plot_histogram(counts)
import time
from datetime import datetime
import pdb

# Clase Paciente
class Paciente:
    def __init__(self, nombre, edad, sintomas):
        self.nombre = nombre
        self.edad = edad
        self.sintomas = sintomas
        self.hora_llegada = None
        self.duracion = None

# Clase ServicioUrgencias
class ServicioUrgencias:
    def __init__(self):
        self.pacientes_atendidos = []

    def atender(self, paciente):
        paciente.hora_llegada = datetime.now()
        print(f"Atendiendo a {paciente.nombre}, gravedad: {self.evaluar_gravedad(paciente)}")

        # Punto de depuración
        pdb.set_trace()

        inicio = time.time()
        self.tratar(paciente)
        fin = time.time()

        paciente.duracion = fin - inicio
        self.pacientes_atendidos.append(paciente)

    def evaluar_gravedad(self, paciente):
        if paciente.edad >= 70 or 'dolor' in paciente.sintomas.lower():
            return 'alta'
        elif paciente.edad >= 40:
            return 'media'
        else:
            return 'baja'

    def tratar(self, paciente):
        print(f"Tratando a {paciente.nombre}... (simulación)")
        time.sleep(2)

# Función principal
def main():
    urgencias = ServicioUrgencias()

    paciente1 = Paciente("Ana", 68, "dolor de pecho")
    paciente2 = Paciente("Luis", 25, "fiebre y tos")
    paciente3 = Paciente("Marta", 73, "dolor de cabeza")

    urgencias.atender(paciente1)
    urgencias.atender(paciente2)
    urgencias.atender(paciente3)

    print("\n--- Pacientes Atendidos ---")
    for p in urgencias.pacientes_atendidos:
        print(f"{p.nombre} | Edad: {p.edad} | Llegó: {p.hora_llegada.strftime('%H:%M:%S')} | Duración: {p.duracion:.2f}s")

if __name__ == "__main__":
    main()

from abc import ABC, abstractmethod

# --- Productos ---
class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

# --- Pedidos ---
class Pedido:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto: Producto):
        self.productos.append(producto)

    def calcular_total(self) :
        return sum(p.precio for p in self.productos)

# --- Interfaces específicas (ISP) ---
class PreparaCafe(ABC):
    @abstractmethod
    def preparar_cafe(self):
        pass

class PreparaTostadas(ABC):
    @abstractmethod
    def preparar_tostada(self):
        pass

# --- Máquinas de bebidas ---
class IBebida(ABC):
    @abstractmethod
    def preparar(self):
        pass

# Máquina de café
class Cafetera(PreparaCafe, IBebida):
    def preparar_cafe(self):
        print("☕ Cafetera: Café listo")
    def preparar(self):
        self.preparar_cafe()

# Máquina de tostadas
class Tostadora(PreparaTostadas):
    def preparar_tostada(self):
        print("🍞 Tostadora: Tostada lista")

# Máquina de jugo (no hereda de IBebida para respetar LSP)
class MaquinaDeJugo(IBebida):
    def preparar(self):
        print("🧃 Máquina de jugo preparando bebida fría...")

# Intenta heredar incorrectamente de máquina de bebidas calientes - ejemplo
class MalHerenciaJugo(IBebida):
    def __init__(self):
        raise TypeError("No se puede heredar de una máquina de bebidas calientes para jugo.")

# --- Bebidas específicas (OCP) ---
# Añadimos Té sin modificar clases existentes
class Te(IBebida):
    def preparar(self):
        print("🍵 Té preparado")

# --- Control en la cafetería ---
# Usamos abstractions para inyectar dependencias (DIP)
class ICaja(ABC):
    @abstractmethod
    def cobrar(self, monto):
        pass

class Caja(ICaja):
    def cobrar(self, monto):
        print(f"💰 Total a pagar: ${monto:.2f}")

# Clase para descuentos (Fidelidad)
class DescuentoFidelidad:
    def aplicar(self, total, tiene_tarjeta):
        if tiene_tarjeta:
            print("🎉 Descuento de fidelidad aplicado (10%)")
            return total * 0.9
        return total

# --- Clase principal de la cafetería ---
class Cafeteria:
    def __init__(
        self,
        maquina_bebida: IBebida,
        caja: ICaja,
        descuento: DescuentoFidelidad
    ):
        self.maquina_bebida = maquina_bebida
        self.pedido = Pedido()
        self.caja = caja
        self.descuento = descuento

    def agregar_producto(self, producto: Producto):
        self.pedido.agregar_producto(producto)

    def atender_cliente(self, tiene_tarjeta= False):
        # Preparar bebida
        self.maquina_bebida.preparar()

        # Calcular total
        total = self.pedido.calcular_total()

        # Aplicar descuento
        total_con_descuento = self.descuento.aplicar(total, tiene_tarjeta)

        # Cobrar
        self.caja.cobrar(total_con_descuento)

# --- Ejecución ---

if __name__ == "__main__":
    # Productos
    cafe = Producto("Café Americano", 35.0)
    te_verde = Producto("Té Verde", 28.0)

    # Componentes
    maquina_cafe = Cafetera()
    caja = Caja()
    descuento = DescuentoFidelidad()

    # Crear cafetería con máquina de café
    cafeteria = Cafeteria(maquina_bebida=maquina_cafe, caja=caja, descuento=descuento)

    # Agregar productos
    cafeteria.agregar_producto(cafe)
    cafeteria.agregar_producto(te_verde)

    # Atender cliente con tarjeta de fidelidad
    print("=== Atención con tarjeta de fidelidad ===")
    cafeteria.atender_cliente(tiene_tarjeta=True)

    # <Opcional: cambiar máquina por jugo o té, y volver a atender>
    print("\n=== Cambio a máquina de jugo ===")
    maquina_jugo = MaquinaDeJugo()
    cafeteria2 = Cafeteria(maquina_bebida=maquina_jugo, caja=caja, descuento=descuento)
    cafeteria2.agregar_producto(Producto("Jugo de naranja", 40))
    cafeteria2.atender_cliente(tiene_tarjeta=False)

    print("\n=== Cambio a máquina de té ===")
    maquina_te = Te()
    cafeteria3 = Cafeteria(maquina_bebida=maquina_te, caja=caja, descuento=descuento)
    cafeteria3.agregar_producto(Producto("Té negro", 25))
    cafeteria3.atender_cliente(tiene_tarjeta=True)



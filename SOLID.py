from abc import ABC, abstractmethod


class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio


class Pedido:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto: Producto):
        self.productos.append(producto)

    def calcular_total(self) :
        return sum(p.precio for p in self.productos)


class PreparaCafe(ABC):
    @abstractmethod
    def preparar_cafe(self):
        pass

class PreparaTostadas(ABC):
    @abstractmethod
    def preparar_tostada(self):
        pass


class IBebida(ABC):
    @abstractmethod
    def preparar(self):
        pass


class Cafetera(PreparaCafe, IBebida):
    def preparar_cafe(self):
        print("☕ Cafetera: Café listo")
    def preparar(self):
        self.preparar_cafe()


class Tostadora(PreparaTostadas):
    def preparar_tostada(self):
        print("🍞 Tostadora: Tostada lista")


class MaquinaDeJugo(IBebida):
    def preparar(self):
        print("🧃 Máquina de jugo preparando bebida fría...")


class MalHerenciaJugo(IBebida):
    def __init__(self):
        raise TypeError("No se puede heredar de una máquina de bebidas calientes para jugo.")


class Te(IBebida):
    def preparar(self):
        print("🍵 Té preparado")


class ICaja(ABC):
    @abstractmethod
    def cobrar(self, monto):
        pass

class Caja(ICaja):
    def cobrar(self, monto):
        print(f"💰 Total a pagar: ${monto:.2f}")


class DescuentoFidelidad:
    def aplicar(self, total, tiene_tarjeta):
        if tiene_tarjeta:
            print("🎉 Descuento de fidelidad aplicado (10%)")
            return total * 0.9
        return total


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
     
        self.maquina_bebida.preparar()

   
        total = self.pedido.calcular_total()


        total_con_descuento = self.descuento.aplicar(total, tiene_tarjeta)

        self.caja.cobrar(total_con_descuento)



if __name__ == "__main__":
   
    cafe = Producto("Café Americano", 35.0)
    te_verde = Producto("Té Verde", 28.0)

   
    maquina_cafe = Cafetera()
    caja = Caja()
    descuento = DescuentoFidelidad()

   
    cafeteria = Cafeteria(maquina_bebida=maquina_cafe, caja=caja, descuento=descuento)

   
    cafeteria.agregar_producto(cafe)
    cafeteria.agregar_producto(te_verde)

   
    print("=== Atención con tarjeta de fidelidad ===")
    cafeteria.atender_cliente(tiene_tarjeta=True)

   
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



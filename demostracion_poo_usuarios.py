# Clase base para ítems de biblioteca
class ItemBiblioteca:
    def __init__(self, titulo, autor):
        self._titulo = titulo
        self._autor = autor
        self._disponible = True
        self._prestado_a = None

    @abstractmethod
    def obtener_info(self):
        pass

    def prestar(self, usuario):
        if self._disponible:
            self._disponible = False
            self._prestado_a = usuario
            return True
        return False

    def devolver(self):
        if not self._disponible:
            self._disponible = True
            self._prestado_a = None
            return True
        return False

    @property
    def titulo(self):
        return self._titulo

    @property
    def disponible(self):
        return self._disponible

    @property
    def prestado_a(self):
        return self._prestado_a


class Libro(ItemBiblioteca):
    def __init__(self, titulo, autor, paginas):
        super().__init__(titulo, autor)
        self._paginas = paginas

    def obtener_info(self):
        estado = "Disponible" if self._disponible else f"Prestado a {self._prestado_a.nombre}"
        return f"Libro: {self._titulo}, Autor: {self._autor}, Páginas: {self._paginas}, Estado: {estado}"


class Revista(ItemBiblioteca):
    def __init__(self, titulo, autor, edicion):
        super().__init__(titulo, autor)
        self._edicion = edicion

    def obtener_info(self):
        estado = "Disponible" if self._disponible else f"Prestado a {self._prestado_a.nombre}"
        return f"Revista: {self._titulo}, Autor: {self._autor}, Edición: {self._edicion}, Estado: {estado}"


# Clase base Usuario
class Usuario:
    def __init__(self, nombre, id_usuario):
        self._nombre = nombre
        self._id_usuario = id_usuario
        self._items_prestados = []

    @abstractmethod
    def mostrar_info(self):
        pass

    @property
    def nombre(self):
        return self._nombre

    def prestar_item(self, item):
        if item.prestar(self):
            self._items_prestados.append(item)
            return f"{self._nombre} ha prestado '{item.titulo}'."
        return f"No se pudo prestar '{item.titulo}'."

    def devolver_item(self, item):
        if item in self._items_prestados and item.devolver():
            self._items_prestados.remove(item)
            return f"{self._nombre} ha devuelto '{item.titulo}'."
        return f"No se pudo devolver '{item.titulo}'."

    def listar_items(self):
        return [item.titulo for item in self._items_prestados]


class Estudiante(Usuario):
    def __init__(self, nombre, id_usuario, carrera):
        super().__init__(nombre, id_usuario)
        self._carrera = carrera

    def mostrar_info(self):
        return f"Estudiante: {self._nombre}, ID: {self._id_usuario}, Carrera: {self._carrera}"


class Profesor(Usuario):
    def __init__(self, nombre, id_usuario, departamento):
        super().__init__(nombre, id_usuario)
        self._departamento = departamento

    def mostrar_info(self):
        return f"Profesor: {self._nombre}, ID: {self._id_usuario}, Departamento: {self._departamento}"


class Biblioteca:
    def __init__(self, nombre):
        self._nombre = nombre
        self._items = []

    def agregar_item(self, item):
        self._items.append(item)
        return f"'{item.titulo}' agregado a la biblioteca."

    def mostrar_inventario(self):
        return "\n".join(item.obtener_info() for item in self._items)

    def mostrar_prestamos(self):
        prestamos = [f"{item.titulo} → {item.prestado_a.nombre}" for item in self._items if not item.disponible]
        return "\n".join(prestamos) if prestamos else "No hay préstamos."


# Programa principal
def main():
    biblioteca = Biblioteca("Biblioteca Central")

    # Crear ítems
    libro = Libro("El Quijote", "Cervantes", 863)
    revista = Revista("Science", "AAAS", 2024)

    print(biblioteca.agregar_item(libro))
    print(biblioteca.agregar_item(revista))

    # Crear usuarios
    estudiante = Estudiante("Lucía Pérez", "E102", "Medicina")
    profesor = Profesor("Carlos Ruiz", "P045", "Biología")

    print(estudiante.mostrar_info())
    print(profesor.mostrar_info())

    # Préstamos
    print(estudiante.prestar_item(libro))
    print(profesor.prestar_item(revista))

    # Mostrar inventario y préstamos
    print("\nInventario actual:")
    print(biblioteca.mostrar_inventario())

    print("\nPréstamos activos:")
    print(biblioteca.mostrar_prestamos())

    # Devoluciones
    print(estudiante.devolver_item(libro))
    print(profesor.devolver_item(revista))

    # Mostrar inventario final
    print("\nInventario después de devoluciones:")
    print(biblioteca.mostrar_inventario())


if __name__ == "__main__":
    main()

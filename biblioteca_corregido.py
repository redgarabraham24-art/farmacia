
class ItemBiblioteca:
    def __init__(self, titulo, autor):
        self._titulo = titulo  #Atributo protegido (Encapsulamiento)
        self._autor = autor
        self._disponible = True

#Metodo abstracto (Abstraccion)
    def obtener_info(self):
        pass

#Metodos para encapsulamiento
    def prestar(self):   #Encapsulamiento
        if self._disponible:
            self._disponible = False
            return f"{self._titulo} ha sido prestado."
        return f"{self._titulo} no está disponible."

    def devolver(self):
        if not self._disponible:
            self._disponible = True
            return f"{self._titulo} ha sido devuelto."
        return f"{self._titulo} ya está disponible."

#Clase que hereda de ItemBiblioteca (Herencia)
class Libro(ItemBiblioteca):
    def __init__(self, titulo, autor, paginas): #Constructor
        super().__init__(titulo, autor)  #Llamada al constructor de la clase base
        self._paginas = paginas

    #Polimorfismo: sobreescribe el metodo obtener_info
    def obtener_info(self):
        return f"Libro: {self._titulo}, Autor: {self._autor}, Páginas: {self._paginas}, Disponible: {self._disponible}"

#Clase que hereda de ItemBiblioteca (Herencia) 
class Revista(ItemBiblioteca):
    def __init__(self, titulo, autor,numero_edicion): #Constructor
        super().__init__(titulo, autor)
        self._numero_edicion = numero_edicion  

    #Polimorfismo: sobreescribe el metodo obtener_info
    def obtener_info(self):
        return f"Revista: {self._titulo}, Autor: {self._autor}, Edición: {self._numero_edicion}, Disponible: {self._disponible}"

#Clase para gestionar la biblioteca
class Biblioteca:
    def __init__(self, nombre):  #Constructor
        self._nombre = nombre
        self._items = []  #Lista para almacenar libros y revistas

    #Metodo para agregar items (Encapsulamiento)
    def agregar_item(self, item):
        self._items.append(item)
        return f"{item._titulo} agregado a la biblioteca."

    #Metodo para mostrar todos los items
    def mostrar_items(self):
        return "\n".join([item.obtener_info() for item in self._items])

#Ejemplo de uso
def main():
    #Instancia de la clase Biblioteca (Instancia)
    biblioteca = Biblioteca("Biblioteca Central")
    
    #Instancias de las clases Libro y Revista (Instancia)
    libro1 = Libro("Cien años de soledad", "Gabriel Garcia Marquez", 417)
    libro2 = Libro("1984", "George Orwell", 328)
    revista1 = Revista("National Geographic", "Varios", 202)

    #Agregar items de la biblioteca
    print(biblioteca.agregar_item(libro1))
    print(biblioteca.agregar_item(libro2))
    print(biblioteca.agregar_item(revista1))

    #Mostrar informacion de los items
    print("\nInventario de la biblioteca:")
    print(biblioteca.mostrar_items())

    #Demostracion de metodos de prestamo y devolucion
    print("\n" + libro1.prestar())
    print(libro1.obtener_info())
    print(libro1.devolver())
    print(libro1.obtener_info())

if __name__ == "__main__":
    main()

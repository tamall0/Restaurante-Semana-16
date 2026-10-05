import json
import os
from typing import List, TypeVar, Callable
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

T = TypeVar('T')

class ArchivoServicio:
    def __init__(self, 
                 ruta_productos: str = "datos/productos.json", 
                 ruta_usuarios: str = "datos/usuarios.json",
                 ruta_ventas: str = "datos/ventas.json"):
        self.ruta_productos = ruta_productos
        self.ruta_usuarios = ruta_usuarios
        self.ruta_ventas = ruta_ventas

    def _cargar_coleccion(self, ruta: str, transformador: Callable[[dict], T]) -> List[T]:
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                if not isinstance(datos, list):
                    return []
                return [transformador(item) for item in datos]
        except (FileNotFoundError, json.JSONDecodeError, PermissionError):
            return []

    def _guardar_coleccion(self, ruta: str, coleccion: List[T]) -> bool:
        try:
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump([item.a_diccionario() for item in coleccion], archivo, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def cargar_productos(self) -> List[Producto]:
        return self._cargar_coleccion(self.ruta_productos, Producto.desde_diccionario)

    def cargar_usuarios(self) -> List[Usuario]:
        return self._cargar_coleccion(self.ruta_usuarios, Usuario.desde_diccionario)

    def cargar_ventas(self) -> List[Venta]:
        return self._cargar_coleccion(self.ruta_ventas, Venta.desde_diccionario)

    def guardar_ventas(self, ventas: List[Venta]) -> bool:
        return self._guardar_coleccion(self.ruta_ventas, ventas)
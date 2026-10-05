import os
from typing import List, Tuple, Optional
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self, ruta_productos: str, ruta_usuarios: str, ruta_ventas: str):
        self.archivo_servicio = ArchivoServicio()
        self.ruta_productos = ruta_productos
        self.ruta_usuarios = ruta_usuarios
        self.ruta_ventas = ruta_ventas

        self.productos: List[Producto] = []
        self.usuarios: List[Usuario] = []
        self.ventas: List[Venta] = []
        self.usuario_actual: Optional[Usuario] = None

        self._cargar_datos()

    def _obtener_json(self, ruta: str) -> list:
        if not os.path.exists(ruta):
            return []
        for m in ["cargar_json", "leer_json", "cargar", "leer"]:
            if hasattr(self.archivo_servicio, m):
                res = getattr(self.archivo_servicio, m)(ruta)
                if res and isinstance(res, list):
                    return res
        return []

    def _guardar_json_archivo(self, ruta: str, datos: list) -> None:
        for m in ["guardar_json", "escribir_json", "guardar", "escribir"]:
            if hasattr(self.archivo_servicio, m):
                getattr(self.archivo_servicio, m)(ruta, datos)
                break

    def _cargar_datos(self) -> None:
        # Carga de usuarios con respaldo por defecto
        raw_usr = self._obtener_json(self.ruta_usuarios)
        self.usuarios = []
        if raw_usr:
            for u in raw_usr:
                if isinstance(u, dict):
                    self.usuarios.append(Usuario.from_dict(u))
                elif isinstance(u, Usuario):
                    self.usuarios.append(u)

        if not self.usuarios:
            self.usuarios = [
                Usuario("admin", "Administrador Principal", "1234", "Administrador"),
                Usuario("emp01", "Carlos Empleado", "1234", "Empleado"),
                Usuario("cli01", "Ana Cliente", "1234", "Cliente")
            ]
            self._guardar_usuarios()

        # Carga de productos incluyendo el parámetro de categoría
        raw_prod = self._obtener_json(self.ruta_productos)
        self.productos = []
        if raw_prod:
            for p in raw_prod:
                if isinstance(p, dict):
                    self.productos.append(Producto.from_dict(p))
                elif isinstance(p, Producto):
                    self.productos.append(p)

        if not self.productos:
            self.productos = [
                Producto(1, "Hamburguesa Especial", 8.50, "Comidas"),
                Producto(2, "Pizza Familiar", 15.00, "Comidas"),
                Producto(3, "Gaseosa 1.5L", 2.50, "Bebidas")
            ]

        # Carga de ventas
        raw_ventas = self._obtener_json(self.ruta_ventas)
        self.ventas = []
        if raw_ventas:
            for v in raw_ventas:
                if isinstance(v, dict):
                    self.ventas.append(Venta.from_dict(v))
                elif isinstance(v, Venta):
                    self.ventas.append(v)

    def _guardar_usuarios(self) -> None:
        data = [u.to_dict() if hasattr(u, "to_dict") else u for u in self.usuarios]
        self._guardar_json_archivo(self.ruta_usuarios, data)

    def _guardar_ventas(self) -> None:
        data = [v.to_dict() if hasattr(v, "to_dict") else v for v in self.ventas]
        self._guardar_json_archivo(self.ruta_ventas, data)

    def validar_acceso(self, id_usuario: str, clave: str) -> bool:
        id_ingresado = str(id_usuario).strip().lower()
        clave_ingresada = str(clave).strip()

        for u in self.usuarios:
            u_id = str(getattr(u, "id_usuario", "")).strip().lower()
            u_clave = str(getattr(u, "clave", "")).strip()

            if u_id == id_ingresado and u_clave == clave_ingresada:
                self.usuario_actual = u
                return True

        return False

    def obtener_usuario_actual(self) -> Optional[Usuario]:
        return self.usuario_actual

    def obtener_usuarios(self) -> List[Usuario]:
        return self.usuarios

    def obtener_productos(self) -> List[Producto]:
        return self.productos

    def obtener_ventas(self) -> List[Venta]:
        return self.ventas

    def obtener_usuario_por_id(self, id_usuario: str) -> Optional[Usuario]:
        for u in self.usuarios:
            if str(u.id_usuario).strip().lower() == str(id_usuario).strip().lower():
                return u
        return None

    def registrar_usuario(self, id_usuario: str, nombre: str, clave: str, rol: str) -> Tuple[bool, str]:
        if not id_usuario or not nombre or not clave:
            return False, "Todos los campos son obligatorios."
        if self.obtener_usuario_por_id(id_usuario):
            return False, f"El ID '{id_usuario}' ya existe."

        nuevo = Usuario(id_usuario=id_usuario, nombre=nombre, clave=clave, rol=rol)
        self.usuarios.append(nuevo)
        self._guardar_usuarios()
        return True, "Usuario registrado con éxito."

    def actualizar_usuario(self, id_usuario: str, nombre: str, clave: str, rol: str) -> Tuple[bool, str]:
        usr = self.obtener_usuario_por_id(id_usuario)
        if not usr:
            return False, "El usuario no existe."

        usr.nombre = nombre
        if clave:
            usr.clave = clave
        usr.rol = rol

        self._guardar_usuarios()
        return True, "Usuario actualizado con éxito."

    def eliminar_usuario(self, id_usuario: str) -> Tuple[bool, str]:
        usr = self.obtener_usuario_por_id(id_usuario)
        if not usr:
            return False, "El usuario no existe."

        if self.usuario_actual and str(self.usuario_actual.id_usuario).lower() == str(id_usuario).lower():
            return False, "No puede eliminar la cuenta activa."

        self.usuarios.remove(usr)
        self._guardar_usuarios()
        return True, "Usuario eliminado con éxito."

    def registrar_venta(self, id_usuario: str, id_producto: int) -> Tuple[bool, str]:
        from datetime import datetime

        usr = self.obtener_usuario_por_id(id_usuario)
        
        prod = None
        for p in self.productos:
            p_id = getattr(p, "id_producto", None)
            if str(p_id) == str(id_producto):
                prod = p
                break

        if not usr:
            return False, f"El usuario '{id_usuario}' no existe."
        if not prod:
            return False, f"El producto ID '{id_producto}' no existe."

        nuevo_id = max([getattr(v, "id_venta", 0) for v in self.ventas], default=0) + 1
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        nueva_venta = Venta(
            id_venta=nuevo_id,
            usuario_id=str(id_usuario),
            producto_id=int(id_producto),
            fecha=fecha_actual,
            total=float(prod.precio)
        )

        self.ventas.append(nueva_venta)
        self._guardar_ventas()
        return True, f"Venta #{nuevo_id} registrada por ${prod.precio:.2f}."
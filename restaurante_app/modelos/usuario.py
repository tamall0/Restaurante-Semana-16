from typing import Dict, Any

class Usuario:
    def __init__(self, id_usuario: str, nombre: str, clave: str, rol: str = "Cliente"):
        self.id_usuario = str(id_usuario)
        self.nombre = str(nombre)
        self.clave = str(clave)
        self.rol = str(rol)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "clave": self.clave,
            "rol": self.rol
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Usuario":
        return cls(
            id_usuario=data.get("id_usuario", ""),
            nombre=data.get("nombre", ""),
            clave=data.get("clave", ""),
            rol=data.get("rol", "Cliente")  # Si no existe el campo rol, asigna Cliente por defecto
        )

    def __str__(self) -> str:
        return f"[{self.rol}] {self.id_usuario} - {self.nombre}"
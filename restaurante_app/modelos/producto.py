from typing import Dict, Any

class Producto:
    def __init__(self, id_producto: int, nombre: str, precio: float, categoria: str = "General"):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": self.precio,
            "categoria": self.categoria
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Producto":
        return cls(
            id_producto=int(data.get("id_producto", 0)),
            nombre=str(data.get("nombre", "")),
            precio=float(data.get("precio", 0.0)),
            categoria=str(data.get("categoria", "General"))
        )

    def __str__(self) -> str:
        return f"[{self.categoria}] #{self.id_producto} - {self.nombre} (${self.precio:.2f})"
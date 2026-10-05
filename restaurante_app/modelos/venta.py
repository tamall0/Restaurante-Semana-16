from datetime import datetime
from typing import Dict, Any

class Venta:
    def __init__(self, id_venta: int, usuario_id: str, producto_id: int, fecha: str = None, total: float = 0.0):
        self.id_venta = id_venta
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.fecha = fecha if fecha else self.obtener_fecha_actual()
        self.total = total

    @staticmethod
    def obtener_fecha_actual() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_venta": self.id_venta,
            "usuario_id": self.usuario_id,
            "producto_id": self.producto_id,
            "fecha": self.fecha,
            "total": self.total
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Venta":
        return cls(
            id_venta=int(data.get("id_venta", 0)),
            usuario_id=str(data.get("usuario_id", "")),
            producto_id=int(data.get("producto_id", 0)),
            fecha=str(data.get("fecha", "")),
            total=float(data.get("total", 0.0))
        )

    def __str__(self) -> str:
        return f"Venta #{self.id_venta} - User: {self.usuario_id} - Prod: {self.producto_id} - ${self.total:.2f}"
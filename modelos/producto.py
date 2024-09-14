
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float

from config import Base
from modelos.pedidosproductos import PedidoProducto

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    cantidad_disponible = Column(Integer, nullable=False)
    pedidos = relationship('Pedido', secondary='pedido_producto', back_populates='productos')
    
    
    def actualizar_inventario(self, cantidad):
        if self.cantidad_disponible >= cantidad:
            self.cantidad_disponible -= cantidad
            return True
        return False
    

    def to_dict(self):
        return {"id": self.id, 
                "nombre": self.nombre, 
                "precio": self.precio,
                "cantidad_disponible": self.cantidad_disponible}

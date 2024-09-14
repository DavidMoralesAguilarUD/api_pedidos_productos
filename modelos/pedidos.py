from flask import session
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from config import Base, Session
from modelos.pedidosproductos import PedidoProducto
from modelos.producto import Producto

session = Session()
class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True)
    cliente = Column(String(100), nullable=False)
    total = Column(Float, nullable=False)
    productos = relationship('Producto', secondary='pedido_producto', back_populates='pedidos')
    impuesto = Column(Float, default=0.15)
    descuento = Column(Float, default=0)


    def calcular_total(self):
        productos_cantidades = (
          session.query(Producto, PedidoProducto.cantidad)
          .join(PedidoProducto, Producto.id == PedidoProducto.producto_id)
          .filter(PedidoProducto.pedido_id == self.id)
          ).all()
        session.rollback()  

        total_sin_impuesto = sum(p.precio * cantidad for p, cantidad in productos_cantidades)
        total_con_impuesto = total_sin_impuesto * (1 + self.impuesto)
        total_con_descuento = total_con_impuesto - (total_con_impuesto * self.descuento)
        
        
        return total_sin_impuesto, total_con_impuesto, total_con_descuento

    
    def procesar_pedido(self):
        productos_sin_stock = []
        todos_en_stock = True

        # Obtener productos y sus cantidades desde la tabla intermedia
        productos_cantidades = (
          session.query(Producto, PedidoProducto.cantidad)
          .join(PedidoProducto, Producto.id == PedidoProducto.producto_id)
          .filter(PedidoProducto.pedido_id == self.id)
          ).all()
        session.rollback()  

        # Verificar inventario y actualizar
        for producto, cantidad in productos_cantidades:
            if not producto.actualizar_inventario(cantidad):
                productos_sin_stock.append(producto.nombre)
                todos_en_stock = False
                
        # Calcular el total
        total_sin_impuesto, total_con_impuesto, total_con_descuento = self.calcular_total()

        resultado = {
            "cliente": self.cliente,
            "total_sin_impuesto": total_sin_impuesto,
            "total_con_impuesto": total_con_impuesto,
            "total_con_descuento": total_con_descuento,
            "productos_sin_stock": productos_sin_stock,
            "todos_en_stock": todos_en_stock,
            "productos": [
                {"nombre": p.nombre, "cantidad_disponible": p.cantidad_disponible}
                for p, _ in productos_cantidades
            ]
        }

        return resultado



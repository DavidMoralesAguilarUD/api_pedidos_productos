from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table, select

from config import Base


class PedidoProducto(Base):
    __tablename__ = 'pedido_producto'
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), primary_key=True)
    producto_id = Column(Integer, ForeignKey('productos.id'), primary_key=True)
    cantidad = Column('cantidad', Integer, nullable=False)

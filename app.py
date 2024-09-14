# app.py
from flask import Flask, jsonify, request
from config import  Base, Session, engine
from modelos.pedidos import Pedido, PedidoProducto
from modelos.producto import Producto

Base.metadata.create_all(engine)
session = Session()
app = Flask(__name__)

@app.route("/")
def index():

    return jsonify({"message": "Server up"}), 200



@app.route("/productos", methods=["GET"])
def obtener_productos():
   productos = session.query(Producto).all()
   productos_dict = [producto.to_dict() for producto in productos] 
   return jsonify(productos_dict)

@app.route("/productos", methods=["POST"])
def crear_produtos():
     productor1 = Producto(nombre="Laptop", precio=1.455, cantidad_disponible=10)
     session.add(productor1)
     session.commit()
     session.close()
     return jsonify({"success": "Productos Creados"}), 200


# Obtener un producto por ID
@app.route("/productos/<int:id>", methods=["GET"])
def obtener_producto(id):
    productos = session.query(Producto).all()
    producto = next((p for p in productos if p.id == id), None)
    if producto:
        return jsonify(producto.to_dict())
    else:
        return jsonify({"error": "Producto no encontrado"}), 404


# Ruta para procesar el pedido
@app.route("/pedidos/procesar", methods=["POST"])
def procesar_pedido():
    datos = request.json
    cliente = datos.get("cliente")
    productos_ids = datos.get("productos")
    cantidades = datos.get("cantidades")
    
    if not cliente or not productos_ids or not cantidades:
        return jsonify({"error": "Datos incompletos"}), 400
    
    # Crear el pedido
    nuevo_pedido = Pedido(cliente=cliente, total=0)
    session.add(nuevo_pedido)
    session.commit() 
    print(nuevo_pedido.cliente)
    # Asociar productos y cantidades al pedido
    for id, cantidad in zip(productos_ids, cantidades):
        producto = session.query(Producto).get(id)
        print(producto.id)
        if producto:
            if producto.actualizar_inventario(cantidad):
                pedido_producto = PedidoProducto(pedido_id=nuevo_pedido.id, producto_id=producto.id, cantidad=cantidad)
                session.add(pedido_producto)
                session.commit()

            else:
                return jsonify({"error": f"No hay suficiente stock para {producto.nombre}"}), 400
        else:
            return jsonify({"error": f"Producto con ID {id} no encontrado"}), 404

    session.commit()

    # Procesar el pedido y devolver el resultado
    resultado = nuevo_pedido.procesar_pedido()
    session.close()
    return resultado

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)

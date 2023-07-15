from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy  import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)  # Creamos una Instancia del Tipo Flask
CORS(app)              # Nos permite conectarnos desde el front y consumir todo 
                       # lo que creamos en app

# Conexión con la Base de Datos                  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/crud_23003'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #None
db = SQLAlchemy(app)   # Crea el Objeto db de la clase SQLAlchemy
ma = Marshmallow(app)  # Crea el Objeto ma de la clase Marshmallow

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Float())
    stock  = db.Column(db.Integer)
    imagen = db.Column(db.String(400))

    def __init__(self, nombre, precio, stock, imagen):
        self.nombre = nombre
        self.precio = precio
        self.stock  = stock
        self.imagen = imagen

# Resto de las Tablas

with app.app_context():
    db.create_all()  # Aquí Crea todas las tablas

    # *****************************************************

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'precio', 'stock', 'imagen')

producto_schema  = ProductoSchema()  # El Objeto producto_schema es p/traer 1 p
productos_schema = ProductoSchema(many=True)  # productos_schema es p/traer all

@app.route('/productos', methods = ['GET'])
def get_productos():
    all_productos = Producto.query.all()
    result = productos_schema.dump(all_productos)
    return jsonify(result)                    # Retorna el JSON de all productos

@app.route('/productos/<id>', methods = ['GET'])
def get_producto(id):
    producto = Producto.query.get(id)
    return producto_schema.jsonify(producto)  # Retorna el JSON de 1 prod recib

@app.route('/productos/<id>', methods = ['DELETE'])
def delete_producto(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)               # Elimina un Registro
    db.session.commit()
    return producto_schema.jsonify(producto)  # Muestra el Registro q Eliminamos

@app.route('/productos', methods = ['POST'])  # Crea un Registro
def create_producto():
    nombre = request.json['nombre']
    precio = request.json['precio']
    stock  = request.json['stock']
    imagen = request.json['imagen']
    nuevo_producto = Producto(nombre, precio, stock, imagen)
    db.session.add(nuevo_producto)
    db.session.commit()
    return producto_schema.jsonify(nuevo_producto)

@app.route('/productos/<id>', methods = ['PUT'])  # Modifica (Update)
def update_producto(id):
    producto = Producto.query.get(id)
    nombre = request.json['nombre']
    precio = request.json['precio']
    stock  = request.json['stock']
    imagen = request.json['imagen']

    producto.nombre = nombre
    producto.precio = precio
    producto.stock  = stock
    producto.imagen = imagen

    db.session.commit()
    return producto_schema.jsonify(producto)


if __name__ == '__main__':
    app.run(debug=True, port=5000)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Cuando se ejecute en el Terminal, si no tira ningún error...
# Chequear en el navegador este link: http://127.0.0.1:5000
#
# create database crud_23003;
# use crud_23003;
#
# create table productos (id int(11) auto_increment primary key, nombre varchar(100), precio float, stock int(11), imagen varchar(400));
#
#
# Datos Reales para probar la BBDD:
#
# insert into producto (nombre, precio, stock, imagen) values ('Mouse Inalam', 8221, 5, 'https://smarts.com.ar/media/catalog/product/cache/e12e3d3943d4efe8bfe0cb881ca8b49c/1/7/1756_1.jpg'), ('Mouse', 3500, 5, 'https://smarts.com.ar/media/catalog/product/cache/e12e3d3943d4efe8bfe0cb881ca8b49c/m/6/m601-rgb_ok.jpg'), ('Auricular Genius', 17056, 15, 'https://smarts.com.ar/media/catalog/product/cache/e12e3d3943d4efe8bfe0cb881ca8b49c/1/0/10731_1.jpg'), ('Auricular Redragon', 18830, 15, 'https://smarts.com.ar/media/catalog/product/cache/e12e3d3943d4efe8bfe0cb881ca8b49c/h/3/h350w-rgb-1_pandora2_ok.jpg'), ('Smartwatch Lenovo', 32137, 25, 'https://smarts.com.ar/media/catalog/product/cache/e12e3d3943d4efe8bfe0cb881ca8b49c/p/t/ptm7c02827---foto-1.jpg'), ('Smartwatch Ticwatch', 66037, 25, 'https://smarts.com.ar/media/catalog/product/cache/e12e3d3943d4efe8bfe0cb881ca8b49c/t/i/ticwatch-e3.gif'), ('Cámara IP Tapo', 31627, 20, 'https://smarts.com.ar/media/catalog/product/cache/e12e3d3943d4efe8bfe0cb881ca8b49c/c/a/camara-ip-c-movimiento-hd-1080p-tapoc200.jpg'), ('Disco Ext 2Tb WD', 52160, 10, 'https://smarts.com.ar/media/catalog/product/cache/e12e3d3943d4efe8bfe0cb881ca8b49c/w/d/wdbu6y0020bbk_01.jpg');
#
#
#
# Registro para añadir con la función create_producto
#
#     (id): (se carga solo xq es autoincremental)
# (nombre): Pendrive 128Gb 3.2 Kingston
# (precio): 7518
#  (stock): 30
# (imagen): https://smarts.com.ar/media/catalog/product/cache/e12e3d3943d4efe8bfe0cb881ca8b49c/1/4/14610_1.jpg
#
#
#
#
# Datos de Ejemplo (originales):
#
# insert into producto (nombre, precio, stock, imagen) values ('MouseXXL', 8000, 5, 'https://smarts.com.ar/media/catalog/product/cache/e12e3d3943d4efe8bfe0cb881ca8b49c/m/6/m601-rgb_ok.jpg1'), ('Mouse', 3500, 5, 'https://smarts.com.ar/media/catalog/product/cache/e12e3d3943d4efe8bfe0cb881ca8b49c/m/6/m601-rgb_ok.jpg');
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

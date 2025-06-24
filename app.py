import os
import mercadopago
from flask import Flask, render_template, request, session, url_for, flash, make_response
from forms import ContactForm
from flask_mail import Mail, Message
from flask_migrate import Migrate
from werkzeug.utils import redirect, secure_filename
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

from database import db
from models import Producto, ProductoForm, Servicio, ServicioForm, VisitasUnicas


app = Flask(__name__)
if os.environ.get("RENDER") != "true":
    load_dotenv() # Carga las variables desde .env al entorno

titulo = 'Py Data Storm'
app.secret_key= os.getenv('SECRET_KEY') # ****************** PASSWORD DE SESSIONES *************************

# Configuración MercadoPago
sdk = mercadopago.SDK(os.getenv('MP_ACCESS_TOKEN')) # ****************** PASSWORD MERCADO PAGO *************************


# CONFIGURACION DE LA BASE DE DATOS
# user_db = os.getenv('SQL_USER')
# pass_db = os.getenv('SQL_PASS') # ****************** PASSWORD BASE DE DATOS *************************
# url_db = os.getenv('SQL_HOST')
# name_db = os.getenv('SQL_DB')
# full_url_db = f'postgresql://{user_db}:{pass_db}@{url_db}/{name_db}'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INICIALIZACION - CONFIGURACION DE LA MIGRACION A LA BASE DE DATOS
db.init_app(app)
migrate = Migrate()
migrate.init_app(app,db)

# CREA LAS TABLAS PARA LA BASE DE DATOS ALCHEMY 
with app.app_context():
    try:
        print(f"DB URL: '{os.getenv('DATABASE_URL')}'")
        db.create_all()
        print("Tablas creadas o existentes.")
    except Exception as e:
        print(f"Error creando tablas: {e}")

# Configuración Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASS') # ****************** PASSWORD GMAIL *************************
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_SENDER')

mail = Mail(app)

# CONFIGURACION PARA PASAR EL CONTADOR DE LAS VISITAS A TODAS LAS RUTAS
@app.context_processor
def inject_visitas():
    visitas = VisitasUnicas.query.first()
    return dict(visitas=visitas.contador if visitas else 0)


# VARIABLE PARA FORMULARIOS
app.config['SECRET_KEY'] = os.getenv('PASS_FORM') # ****************** PASSWORD FORMULARIOS *************************

# *****************************************************************
# ******************** RUTAS ***********************************
# *****************************************************************

@app.errorhandler(404)
def pagina_No_Encontrada(error):
    return render_template('error.html', error=error, title=titulo), 404

@app.route('/')
def inicio():
    try:
        visitas = VisitasUnicas.query.first()
        if not visitas:
            visitas = VisitasUnicas(contador=0)
            db.session.add(visitas)
            db.session.commit()

        if not request.cookies.get('visitante'):
            visitas.contador += 1
            db.session.commit()
            nueva_respuesta = make_response(render_template('inicio.html', title=titulo, visitas=visitas.contador))
            nueva_respuesta.set_cookie('visitante', 'true', max_age=60*60*24*365)
            return nueva_respuesta
        else:
            return render_template('inicio.html', title=titulo)
        
    except OperationalError:
        # Si no existe la tabla, la creo
        db.create_all()
        return redirect(url_for('inicio'))

@app.route('/empresa')
def empresa():
    return render_template('empresa.html', title=titulo)

# *****************************************************************
# ****** RUTAS DE DETALLES SOBRE LOS PRODUCTOS Y SERVICIOS ********
# *****************************************************************

@app.route('/disenio')
def disenio():
    return render_template('PAGINAS-DETALLES/disenio.html', title=titulo)

@app.route('/bd')
def base_datos():
    return render_template('PAGINAS-DETALLES/baseDatos.html', title=titulo)

@app.route('/appweb')
def appweb():
    return render_template('PAGINAS-DETALLES/appWebs.html', title=titulo)

@app.route('/appesc')
def appescritorio():
    return render_template('PAGINAS-DETALLES/appEscrit.html', title=titulo)


# *****************************************************************
# *********************** DEMAS RUTAS *****************************
# *****************************************************************

@app.route('/mediosPago')
def mediosPago():
    return render_template('mediosPago.html', title=titulo)

@app.route('/contacto', methods=['GET','POST'])
def contacto():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message('Nuevo mensaje de contacto',
                      recipients=['pydatastorm@gmail.com'])  # a quién llega
        msg.body = f"""
            Nombre: {form.nombre.data}
            Apellido: {form.apellido.data}
            Email: {form.email.data}

            Comentario:
            {form.comentario.data}
            """
        mail.send(msg)
        flash('Mensaje enviado correctamente. A la brevedad te responderemos. ¡Gracias por contactarte!')
        return redirect(url_for('contacto'))
    return render_template('contacto.html', title=titulo, form=form)

# *****************************************************************
# ***************** Politica de Privacidad *************************
# *****************************************************************

@app.route('/politica')
def politica():
    return render_template('privacidad.html', title=titulo)

# *****************************************************************
# ***************** PRODUCTOS Y SERVICIOS *************************
# *****************************************************************

# RUTA PARA VER LOS PRODUCTOS Y SERVICIOS
# ***************************************
@app.route('/productos', methods=['GET', 'POST'])
def productos():
    form = ProductoForm()

    if form.validate_on_submit():
        # Si hay imagen, la guardamos
        if form.imagen.data:
            filename = secure_filename(form.imagen.data.filename)
            ruta_imagen = os.path.join(app.root_path, 'static/img/productos', filename)
            form.imagen.data.save(ruta_imagen)
        elif form.imagen.data and os.environ.get("RENDER") == "true":
    # En Render no guardamos la imagen porque no se puede
    # Solo usamos el nombre del archivo que ya subiste manualmente al repo
            filename = secure_filename(form.imagen.data.filename)
        else:
            filename = 'sinimagen.png'  # por si no cargan nada

        # Crear el producto
        nuevo_producto = Producto(
            nombre=form.nombre.data,
            detalle=form.detalle.data,
            precio=form.precio.data,
            imagen=filename
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto agregado correctamente.', 'success')
        return redirect(url_for('productos'))

    productos = Producto.query.all()
    for p in productos:
        print(f"{p.nombre}: {p.precio} ({type(p.precio)})")
    return render_template('/CRUD-PRODUCTOS/productos.html', title=titulo, prod=productos, prodForm=form)


@app.route('/servicios', methods=['GET', 'POST'])
def servicios():
    form = ServicioForm()

    if form.validate_on_submit():
        # Si hay imagen, la guardamos
        if form.imagen.data:
            filename = secure_filename(form.imagen.data.filename)
            ruta_imagen = os.path.join(app.root_path, 'static/img/servicios', filename)
            form.imagen.data.save(ruta_imagen)
        else:
            filename = 'sinimagen.png'  # si no sube imagen

        # Crear el servicio
        nuevo_servicio = Servicio(
            nombre=form.nombre.data,
            detalle=form.detalle.data,
            precio=form.precio.data,
            imagen=filename
        )
        db.session.add(nuevo_servicio)
        db.session.commit()
        flash('Servicio agregado correctamente.', 'success')
        return redirect(url_for('servicios'))  # ¡ojo! debe coincidir con el nombre de la función/ruta

    servicios = Servicio.query.all()
    return render_template('/CRUD-SERVICIOS/servicios.html', title=titulo, serv=servicios, form=form)


# RUTA PARA VER EL DETALLE DEL PRODUCTO Y SERVICIOS
# *************************************************
@app.route('/productos/detalle/<int:id>')
def detalleProd(id):
    producto = Producto.query.get_or_404(id)
    return render_template('/CRUD-PRODUCTOS/detalleProd.html', title=titulo, prod = producto)

@app.route('/servicios/detalle/<int:id>', methods=['GET','POST'])
def detalleServ(id):
    servicio = Servicio.query.get_or_404(id)
    return render_template('/CRUD-SERVICIOS/detalleServ.html', title=titulo, serv = servicio)

# RUTA PARA AGREGAR PRODUCTOS y SERVICIOS
# ***************************************
@app.route('/agregarProd', methods=['GET','POST'])
def agregarProd():
    producto = Producto()
    productoForm = ProductoForm(obj=producto)

    if request.method == 'POST':
        if productoForm.validate_on_submit():
            productoForm.populate_obj(producto)

            # Manejo de imagen según entorno
            if productoForm.imagen.data and productoForm.imagen.data.filename != '':
                filename = secure_filename(productoForm.imagen.data.filename)
                
                if app.config.get("RENDER"):
                    producto.imagen = filename
                else:
                    ruta_imagen = os.path.join(app.root_path, 'static/img/productos', filename)
                    productoForm.imagen.data.save(ruta_imagen)
                    producto.imagen = filename
            else:
                producto.imagen = 'sinimagen.png'

            db.session.add(producto)
            db.session.commit()
            flash('Producto agregado correctamente.', 'success')
            return redirect(url_for('productos'))

    return render_template('CRUD-PRODUCTOS/agregarProd.html', title=titulo, prodForm=productoForm)


@app.route('/agregarServ', methods=['GET','POST'])
def agregarServ():
    servicio = Servicio()
    servicioForm = ServicioForm(obj=servicio)

    if request.method == 'POST':
        if servicioForm.validate_on_submit():
            servicioForm.populate_obj(servicio)

            if servicioForm.imagen.data and servicioForm.imagen.data.filename != '':
                filename = secure_filename(servicioForm.imagen.data.filename)
                
                if app.config.get("RENDER"):
                    servicio.imagen = filename
                else:
                    ruta_imagen = os.path.join(app.root_path, 'static/img/servicios', filename)
                    servicioForm.imagen.data.save(ruta_imagen)
                    servicio.imagen = filename
            else:
                servicio.imagen = 'sinimagen.png'

            db.session.add(servicio)
            db.session.commit()
            flash('Servicio agregado correctamente.', 'success')
            return redirect(url_for('servicios'))

    return render_template('/CRUD-SERVICIOS/agregarServ.html', title=titulo, servForm=servicioForm)



# RUTA PARA EDITAR PRODUCTOS y SERVICIOS
# **************************************
@app.route('/editarProd/<int:id>', methods=['GET','POST'])
def editarProd(id):
    producto = Producto.query.get_or_404(id)
    productoForm = ProductoForm(obj=producto)
    if request.method == 'POST':
        if productoForm.validate_on_submit():
            productoForm.populate_obj(producto)
            if productoForm.imagen_nombre.data:
                producto.imagen = productoForm.imagen_nombre.data
            db.session.commit()
            flash('Producto agregado correctamente.', 'success')
            return redirect(url_for('editarProd', id=id)) # ACA REDIRIGIR A LA PAGINA DONDE SE VEAN TODOS
    return render_template('/CRUD-PRODUCTOS/editarProd.html', title=titulo, editarForm = productoForm, producto = producto)

@app.route('/editarServ/<int:id>', methods=['GET','POST'])
def editarServ(id):
    servicio = Servicio.query.get_or_404(id)
    servicioForm = ServicioForm(obj=servicio)
    if request.method == 'POST':
        if servicioForm.validate_on_submit():
            servicioForm.populate_obj(servicio)
            if servicioForm.imagen_nombre.data:
                servicio.imagen = servicioForm.imagen_nombre.data
            db.session.commit()
            flash('Servicio agregado correctamente.', 'success')
            return redirect(url_for('editarServ', id=id)) # ACA REDIRIGIR A LA PAGINA DONDE SE VEAN TODOS
    return render_template('/CRUD-SERVICIOS/editarServ.html', title=titulo, editarForm = servicioForm, servicio = servicio)

# RUTA PARA ELIMINAR PRODUCTOS y SERVICIOS
# ****************************************
@app.route('/eliminarProd/<int:id>', methods=['GET','POST'])
def eliminarProd(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('productos')) # ACA REDIRIGIR A LA PAGINA DONDE SE VEAN TODOS

@app.route('/eliminarServ/<int:id>', methods=['GET','POST'])
def eliminarServ(id):
    servicio = Servicio.query.get_or_404(id)
    db.session.delete(servicio)
    db.session.commit()
    flash('Servicio eliminado correctamente.', 'success')
    return redirect(url_for('servicios')) # ACA REDIRIGIR A LA PAGINA DONDE SE VEAN TODOS

# *****************************************************************
# ******************** CARRITO ***********************************
# *****************************************************************
# ------- AGREGAR PRODUCTOS AL CARRITO --------
@app.route('/agregar_carrito_producto/<int:producto_id>')
def agregar_carritoProd(producto_id):
    # Simulo traer producto de la base de datos
    producto = Producto.query.get_or_404(producto_id)

    if 'carrito' not in session:
        session['carrito'] = {}

    carrito = session['carrito']

    # Si ya está, sumo cantidad
    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1
    else:
        carrito[str(producto_id)] = {
            'nombre': producto.nombre,
            'precio': producto.precio,
            'cantidad': 1
        }

    session['carrito'] = carrito
    flash(f'Producto {producto.nombre} agregado al carrito.')
    return redirect(url_for('productos'))

# ------- AGREGAR SERVICIOS AL CARRITO --------
@app.route('/agregar_carrito_servicio/<int:servicio_id>')
def agregar_carritoServ(servicio_id):
    # Simulo traer producto de la base de datos
   servicio = Servicio.query.get_or_404(servicio_id)
   if 'carrito' not in session:
        session['carrito'] = {}

   carrito = session['carrito']

    # Si ya está, sumo cantidad
   if str(servicio_id) in carrito:
        carrito[str(servicio_id)]['cantidad'] += 1
   else:
        carrito[str(servicio_id)] = {
            'nombre': servicio.nombre,
            'precio': servicio.precio,
            'cantidad': 1
        }

   session['carrito'] = carrito
   flash(f'Servicio {servicio.nombre} agregado al carrito.')
   return redirect(url_for('servicios'))

# ------- VER EL CARRITO --------
@app.route('/ver_carrito')
def ver_carrito():
    carrito = session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    return render_template('carrito.html', carrito=carrito, total=total)

# ------- ELIMINAR PRODUCTOS DEL CARRITO --------
@app.route('/eliminar_carrito/<int:producto_id>')
def eliminar_del_carritoProd(producto_id):
    carrito = session.get('carrito', {})
    carrito.pop(str(producto_id), None)
    session['carrito'] = carrito
    flash('Producto eliminado del carrito.')
    return redirect(url_for('ver_carrito'))

# ------- ELIMINAR SERVICIOS DEL CARRITO --------
@app.route('/eliminar_carrito/<int:servicio_id>')
def eliminar_del_carritoServ(servicio_id):
    carrito = session.get('carrito', {})
    carrito.pop(str(servicio_id), None)
    session['carrito'] = carrito
    flash('Servicio eliminado del carrito.')
    return redirect(url_for('ver_carrito'))

# *****************************************************************
# ******************** PAGOS CON MERCADO PAGO *********************
# *****************************************************************

@app.route('/comprar_producto/<int:id_producto>')
def comprar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)

    preference_data = {
        "items": [
            {
                "title": producto.nombre,
                "quantity": 1,
                "currency_id": "ARS",  # O "USD"
                "unit_price": float(producto.precio)
            }
        ],
        "back_urls": {
            "success": url_for('pago_exitoso', _external=True),
            "failure": url_for('pago_fallido', _external=True),
        },
        "auto_return": "approved"
    }

    preference_response = sdk.preference().create(preference_data)
    if preference_response.get("status") == 201:
       preference = preference_response["response"]
       return redirect(preference["init_point"])
    else:
       flash("No se pudo generar el enlace de pago. Revisá los datos.")
       return redirect(url_for('ver_carrito'))

# Rutas de retorno
@app.route('/pago_exitoso')
def pago_exitoso():
    session.pop('carrito', None)
    return "Pago exitoso."

@app.route('/pago_fallido')
def pago_fallido():
    return "Pago rechazado."

@app.route('/comprar_carrito')
def comprar_carrito():
    carrito = session.get('carrito', {})
    if not carrito:
        flash("El carrito está vacío.")
        return redirect(url_for('ver_carrito'))

    items = []
    for id, item in carrito.items():
        items.append({
            "title": item['nombre'],
            "quantity": item['cantidad'],
            "currency_id": "ARS",
            "unit_price": float(item['precio'])
        })

    preference_data = {
        "items": items,
        "back_urls": {
            "success": url_for('pago_exitoso', _external=True),
            "failure": url_for('pago_fallido', _external=True),
        },
        
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    print("Success URL:", url_for('pago_exitoso', _external=True))
    print("Failure URL:", url_for('pago_fallido', _external=True))

    if "init_point" in preference:
        return redirect(preference["init_point"])
    else:
        flash("No se pudo generar el enlace de pago. Revisá la configuración.")
        return redirect(url_for('ver_carrito'))

# *****************************************************************
# *********** RUTA TEMPORAL PARA ACTUALIZAR BD DE RENDER  **********
# *****************************************************************
@app.route('/update_db')
def update_db():
    try:
        with app.app_context():
            with db.engine.connect() as connection:
                connection.execute(text("""
                    ALTER TABLE servicio
                    ALTER COLUMN precio TYPE integer USING round(precio)
                """))
                connection.execute(text("""
                    ALTER TABLE producto
                    ALTER COLUMN precio TYPE integer USING round(precio)
                """))
                connection.execute(text("""
                    ALTER TABLE producto ALTER COLUMN detalle TYPE TEXT;
                    ALTER TABLE servicio ALTER COLUMN detalle TYPE TEXT;
                """))
                
        return "Columnas actualizadas correctamente."
    except Exception as e:
        return f"Error al actualizar columnas: {e}"

@app.route('/ver_columnas')
def ver_columnas():
    columnas = []
    with app.app_context():
        result = db.session.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'producto';
        """))
        columnas = [f"{row.column_name} — {row.data_type}" for row in result]
    return '<br>'.join(columnas)

if __name__ == '__main__':
    # PRUEBA SI SE CONECTA A LA BASE DE DATOS
    with app.app_context():
        try:
            print(f"DB URL: '{os.getenv('DATABASE_URL')}'")
            db.create_all()
            print("Tablas creadas o existentes.")
        except Exception as e:
            print(f"Error creando tablas: {e}")

    # 🚀 Levanta la app en el puerto que Render espera
    port = int(os.environ.get('PORT', 5000))  # Render te da el puerto en PORT
    app.run(host='0.0.0.0', port=port)
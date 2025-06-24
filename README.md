## 📌 Descripción del proyecto

**Py Data Storm** es una aplicación web desarrollada en **Python + Flask** que permite:

✅ Gestionar productos y servicios desde una base de datos.  
✅ Visualizar productos y servicios en tarjetas (cards) con imagen, detalle y precio.  
✅ Agregar productos y servicios a un carrito de compras.  
✅ Realizar pagos en línea a través de **MercadoPago**.  
✅ Controlar la cantidad de visitas únicas mediante cookies.  
✅ Enviar mensajes de contacto a una casilla de email configurada.  
✅ Contar con panel de administración CRUD (Crear, Leer, Actualizar, Eliminar) para productos y servicios.  
✅ Gestionar datos sensibles mediante variables de entorno protegidas con **dotenv**.

---

## 🛠️ Tecnologías utilizadas

- **Python 3.12**
- **Flask**
- **Flask-SQLAlchemy**
- **Flask-Migrate**
- **Flask-Mail**
- **MercadoPago SDK**
- **dotenv**

---

## 📚 Funcionalidades

- 📦 **Gestión de productos y servicios**
  - Agregar, editar y eliminar productos y servicios con imágenes.
  - Visualización de cards dinámicas con información de cada item.

- 🛒 **Carrito de compras**
  - Agregar productos y servicios al carrito.
  - Visualizar y eliminar ítems del carrito.

- 💳 **Pasarela de pagos MercadoPago**
  - Pago directo de productos o carrito completo.
  - Redirecciones según resultado del pago (éxito o error).

- 📈 **Contador de visitas únicas**
  - Almacena en base de datos la cantidad de usuarios únicos mediante cookies.

- 📬 **Formulario de contacto**
  - Envía mensajes desde la web a un email corporativo mediante **Flask-Mail**.

- 🔐 **Seguridad**
  - Variables sensibles gestionadas mediante archivo `.env` y dotenv.
  - Protección de contraseñas de sesión, credenciales de base de datos y API keys.

---

## 📦 Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tuusuario/tu-repo.git
   cd tu-repo
Crear un entorno virtual:

bash
Copiar
Editar
python -m venv .venv
source .venv/Scripts/activate  # En Windows
Instalar dependencias:

bash
Copiar
Editar
pip install -r requirements.txt
Crear archivo .env con tus credenciales:

env
Copiar
Editar
SECRET_KEY=tu_clave_secreta
MP_ACCESS_TOKEN=tu_token_mercadopago
SQL_USER=usuario
SQL_PASS=contraseña
SQL_HOST=localhost
SQL_DB=nombre_base
SQL_FULL_URL=postgresql://usuario:contraseña@localhost/nombre_base
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USER=tu_email@gmail.com
MAIL_PASS=tu_password_email
MAIL_SENDER=tu_email@gmail.com
Crear y migrar base de datos:

bash
Copiar
Editar
flask db init
flask db migrate -m "Primera migración"
flask db upgrade
Ejecutar la aplicación:

bash
Copiar
Editar
python app.py
📸 Capturas

### 🏠 Página de inicio
![Inicio](static/img/capturas_readme/inicio.png)
![Inicio](static/img/capturas_readme/inicio2.png)

### 📦 Productos
![Productos](static/img/capturas_readme/productos.png)
![Productos](static/img/capturas_readme/productos2.png)

### 🛠️ Servicios
![Productos](static/img/capturas_readme/servicios.png)
![Productos](static/img/capturas_readme/servicios2.png)

### 📬 Formulario de Contacto
![Productos](static/img/capturas_readme/contacto.png)
![Productos](static/img/capturas_readme/contacto2.png)

### 🛒 Carrito
![Carrito](static/img/capturas_readme/carrito.png)
![Carrito](static/img/capturas_readme/carrito2.png)


📣 Autor
👨‍💻 Federico E. Santos
Programador Web Full Stack

📃 Licencia
Este proyecto está bajo la licencia MIT.
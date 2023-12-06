from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from config import config
from models.ModelUsers import ModelUsers, User
from models.ModelProduct import Product, ModelProducts

app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = '123456789'
app.config.from_object(config['development'])
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(id):
    return ModelUsers.get_by_id(mysql, id)

# Decorador para requerir autenticación de administrador
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # Verificar si el usuario está autenticado y es un administrador
        if not current_user.is_authenticated or current_user.usertype != 1:
            abort(403)  # Acceso prohibido
        return func(*args, **kwargs)
    return decorated_view

@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user = User(0, request.form['username'], request.form['password'], 0, 0)
            print("Intento de inicio de sesión para el usuario:", user.username)
            
            with app.app_context():
                logged_user = ModelUsers.login(mysql, user)
            
            print("Usuario autenticado:", logged_user)
            
            if logged_user is not None:
                login_user(logged_user)
                if logged_user.usertype == 1:
                    return redirect(url_for("admin"))  # Redirige a la página de administrador
                else:
                    return redirect(url_for("shop"))
            else:
                print("Acceso rechazado. Verifica tu nombre de usuario y contraseña.")
                flash("Acceso rechazado. Verifica tu nombre de usuario y contraseña.", 'error')  
                return render_template("auth/login.html")
        except ValueError as ve:
            print("Contraseña incorrecta:", ve)
            flash("Contraseña incorrecta. Verifica tu nombre de usuario y contraseña.", 'error')
            return render_template("auth/login.html")
        except Exception as e:
            print("Error al interactuar con la base de datos:", e)
            flash("Ocurrió un error durante el inicio de sesión. Por favor, inténtalo nuevamente.", 'error')
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")
    
@app.route("/add_product", methods=["POST"])
@admin_required
def add_product():
    if request.method == "POST":
        try:
            name = request.form['name']
            price = float(request.form['price'])
            image_url = request.form['image_url']

            new_product = Product(id=None, name=name, price=price, image_url=image_url)

            added_product = ModelProducts.add_product(mysql, new_product)

            flash(f"Producto '{added_product.name}' agregado exitosamente.", 'success')
            return redirect(url_for("admin"))
        except Exception as e:
            print("Error al agregar producto:", e)
            flash("Ocurrió un error al agregar el producto. Por favor, inténtalo nuevamente.", 'error')
            return redirect(url_for("admin"))
    else:
        return redirect(url_for("admin"))


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    if request.method == "GET":
        # Obtener el producto para mostrar en el formulario de edición
        product = ModelProducts.get_product_by_id(mysql, product_id)
        return render_template("edit_product.html", product=product)
    elif request.method == "POST":
        # Procesar el formulario de edición
        updated_name = request.form['editName']
        updated_price = float(request.form['editPrice'])
        updated_image_url = request.form['editImage']

        updated_product = Product(id=product_id, name=updated_name, price=updated_price, image_url=updated_image_url)

        ModelProducts.update_product(mysql, updated_product)

        flash(f"Producto '{updated_product.name}' actualizado exitosamente.", 'success')
        return redirect(url_for("admin"))

@app.route("/admin/delete/<int:product_id>")
@login_required
def delete_product(product_id):
    try:
        # Verifica si el product_id es 0, si es así, redirige a la página de administrador
        if product_id == 0:
            return redirect(url_for("admin"))

        ModelProducts.delete_product(mysql, product_id)
        flash(f"Producto eliminado exitosamente.", 'success')
    except Exception as e:
        print("Error al borrar producto:", e)
        flash("Ocurrió un error al borrar el producto. Por favor, inténtalo nuevamente.", 'error')

    return redirect(url_for("admin"))

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if request.method == "POST" and "editProduct" in request.form:
        # Procesar el formulario de edición
        product_id = int(request.form["editProduct"])
        updated_name = request.form['editName']
        updated_price = float(request.form['editPrice'])
        updated_image_url = request.form['editImage']

        updated_product = Product(id=product_id, name=updated_name, price=updated_price, image_url=updated_image_url)

        ModelProducts.update_product(mysql, updated_product)

        flash(f"Producto '{updated_product.name}' actualizado exitosamente.", 'success')
        return redirect(url_for("admin"))

    products = ModelProducts.get_all_products(mysql)
    users = ModelUsers.get_all_users(mysql)
  

    # Renderizar la plantilla y pasar los productos a la plantilla
    return render_template("adminT.html", products=products, users=users)

# ...

@app.route("/add_user", methods=["POST"])
@admin_required
def add_user():
    if request.method == "POST":
        try:
            username = request.form['username']
            password = request.form['password']
            full_name = request.form['full_name']
            user_type = int(request.form['user_type'])

            # Llamada al nuevo método para agregar usuario en tu modelo
            ModelUsers.add_user(mysql, username, password, full_name, user_type)

            flash(f"Usuario '{username}' agregado exitosamente.", 'success')
            return redirect(url_for("admin"))
        except Exception as e:
            print("Error al agregar usuario:", e)
            flash("Ocurrió un error al agregar el usuario. Por favor, inténtalo nuevamente.", 'error')
            return redirect(url_for("admin"))
    else:
        return redirect(url_for("admin"))

@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    if request.method == "GET":
        # Obtener el usuario para mostrar en el formulario de edición
        user = ModelUsers.get_by_id(mysql, user_id)
        return render_template("edit_user.html", user=user)
    elif request.method == "POST":
        try:
            # Procesar el formulario de edición
            updated_username = request.form['editUsername']
            updated_full_name = request.form['editFullName']
            updated_user_type = int(request.form['editUserType'])

            # Obtener la contraseña actual del usuario
            current_user_info = ModelUsers.get_by_id(mysql, user_id)
            current_password = current_user_info.password

            # Crear un nuevo objeto User con los datos actualizados
            updated_user = User(id=user_id, username=updated_username, password=current_password, fullname=updated_full_name, usertype=updated_user_type)

            # Llamar al método para actualizar el usuario en el modelo
            ModelUsers.update_user(mysql, updated_user)

            flash(f"Usuario '{updated_user.username}' actualizado exitosamente.", 'success')
            return redirect(url_for("admin"))
        except Exception as e:
            print("Error al actualizar usuario:", e)
            flash("Ocurrió un error al actualizar el usuario. Por favor, inténtalo nuevamente.", 'error')
            return redirect(url_for("admin"))
        
@app.route('/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    try:
        ModelUsers.delete_user(mysql, user_id)
        flash(f"Usuario eliminado exitosamente.", 'success')
    except Exception as e:
        print("Error al borrar usuario:", e)
        flash("Ocurrió un error al borrar el usuario. Por favor, inténtalo nuevamente.", 'error')

    return redirect(url_for("admin"))


@app.route("/shop")
@login_required
def shop():
    products = ModelProducts.get_all_products(mysql)
    
    return render_template('shop.html', products=products)

@app.route("/info")                                                            
@login_required
def info():
    return render_template("info.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
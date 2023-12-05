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


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    products = ModelProducts.get_all_products(mysql)
    return render_template("adminT.html", products=products)


@app.route("/shop")
@login_required
def shop():
    return render_template("shop.html")

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
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



class User(UserMixin):
    def __init__(self, id, username, password, fullname, usertype):
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.usertype = usertype
        
    def get_user_type(self):
        return self.usertype


class ModelUsers:
    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.connection.cursor()
            cursor.execute("call sp_verifyIdentity(%s, %s)", (user.username, user.password))
            row = cursor.fetchone()
            if row and len(row) >= 5:
                logged_user = User(row[0], row[1], row[2], row[3], row[4])
                return logged_user
            else:
                return None
        except Exception as ex:
            print("Error en el modelo de usuarios:", ex)
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def get_by_id(cls, mysql, id):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, username, usertype, fullname FROM users WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row:
                user = User(row[0], row[1], '', row[3], row[2])
                return user
            else:
                return None
        except Exception as ex:
            print("Error al obtener usuario por ID:", ex)
            raise Exception(ex)
        finally:
            cursor.close()
    @staticmethod
    def add_user(mysql, username, password, full_name, user_type):
        try:
            cursor =  mysql.connection.cursor()

            # Llamar al procedimiento almacenado
            cursor.callproc('sp_AddUser', (username, password, full_name, user_type))

            # Confirmar los cambios en la base de datos
            mysql.connection.commit()
        except Exception as e:
            # Manejar el error, si es necesario
            raise e
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()
            
    @staticmethod
    def get_all_users(mysql):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, username, usertype, fullname FROM users")
            rows = cursor.fetchall()

            users = []
            for row in rows:
                user = User(row[0], row[1], '', row[3], row[2])
                users.append(user)

            return users
        except Exception as ex:
            print("Error al obtener todos los usuarios:", ex)
            raise Exception(ex)
        finally:
            cursor.close()
import mysql.connector

class DevelopmentConfig:
    DEBUG = True
    MYSQL_HOST = "brzb0069vyov66ptxq0k-mysql.services.clever-cloud.com"
    MYSQL_USER = "uwu7l1vlgnzkywe5"
    MYSQL_PASSWORD = "u6FX0ndWZxqo73xlp8VI"
    MYSQL_DB = "brzb0069vyov66ptxq0k"

config = {
    "development": DevelopmentConfig
}

# Obtén la configuración específica para el entorno de desarrollo
config_dev = config["development"]

# Construye la cadena de conexión según la configuración
conn_str = {
    'host': config_dev.MYSQL_HOST,
    'user': config_dev.MYSQL_USER,
    'password': config_dev.MYSQL_PASSWORD,
    'database': config_dev.MYSQL_DB,
    'raise_on_warnings': True
}

# Intenta establecer la conexión
try:
    connection = mysql.connector.connect(**conn_str)
    print("Conexión exitosa.")
except mysql.connector.Error as err:
    print(f"Error al conectar a la base de datos: {err}")
finally:
    # Cierra la conexión al finalizar
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Conexión cerrada.")

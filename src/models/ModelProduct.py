class Product:
    def __init__(self, id, name, price, image_url):
        self.id = id
        self.name = name
        self.price = price
        self.image_url = image_url
        
class ModelProducts:
    @classmethod
    def add_product(cls, db, product):
        try:
            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO products (name, price, image_url) VALUES (%s, %s, %s)",
                           (product.name, product.price, product.image_url))
            db.connection.commit()

            # Obtén el ID del producto recién insertado
            cursor.execute("SELECT LAST_INSERT_ID()")
            product_id = cursor.fetchone()[0]

            # Crea un objeto Product con el ID asignado
            new_product = Product(id=product_id, name=product.name, price=product.price, image_url=product.image_url)
            return new_product
        except Exception as ex:
            print("Error al agregar producto:", ex)
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def get_all_products(cls, db):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id, name, price, image_url FROM products")
            rows = cursor.fetchall()

            products = []
            for row in rows:
                product = Product(id=row[0], name=row[1], price=row[2], image_url=row[3])
                products.append(product)

            return products
        except Exception as ex:
            print("Error al obtener todos los productos:", ex)
            raise Exception(ex)
        finally:
            cursor.close()
    @classmethod
    def delete_product(cls, db, product_id):
        try:
            cursor = db.connection.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            db.connection.commit()
        except Exception as ex:
            print("Error al borrar producto:", ex)
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def update_product(cls, db, product):
        try:
            cursor = db.connection.cursor()
            cursor.execute("UPDATE products SET name = %s, price = %s, image_url = %s WHERE id = %s",
                           (product.name, product.price, product.image_url, product.id))
            db.connection.commit()
        except Exception as ex:
            print("Error al actualizar producto:", ex)
            raise Exception(ex)
        finally:
            cursor.close()
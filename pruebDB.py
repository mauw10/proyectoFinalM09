import mysql.connector

# Configuración de la conexión a la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="moad",
    password="moad",
    database="login"
)

# Crear un cursor para ejecutar consultas SQL
cursor = mydb.cursor()

# Consulta para obtener el nombre de todas las tablas en la base de datos
cursor.execute("SHOW TABLES")

# Obtener los resultados de la consulta
tables = cursor.fetchall()

# Imprimir el nombre de cada tabla
for table in tables:
    print(table[0])

# Cerrar el cursor y la conexión
cursor.close()
mydb.close()

from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "contraseña"


mydb = mysql.connector.connect(
    host="localhost",
    user="moad",
    password="moad",
    database="login"
)

@app.route("/")
def index():
    login = True  # Variable para mostrar login por defecto
    return render_template('home.html', login=login)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']

        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE nombre = %s', (nombre,))
        user = cursor.fetchone()

        if user:
            if password == user[1]:  # Comparación directa de la contraseña
                session['nombre'] = nombre
                return redirect(url_for('home'))
            else:
                return render_template('login.html', login=True, error_login='Contraseña incorrecta')
        else:
            return render_template('login.html', login=True, error_login='Usuario no encontrado')

    return render_template('login.html', login=True)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']

        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE nombre = %s', (nombre,))
        user = cursor.fetchone()

        if user:
            return render_template('index.html', login=False, error_registro='El nombre de usuario ya está en uso')

        cursor.execute('INSERT INTO usuarios (nombre, contraseña) VALUES (%s, %s)', (nombre, password))
        mydb.commit()

        session['nombre'] = nombre
        return redirect(url_for('home'))

    return render_template('registro.html', login=False)


@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/addmail', methods=['GET', 'POST'])
def addmail():
    if 'nombre' in session:
        if request.method == 'POST':
            nombre = request.form['nom']
            correo = request.form['correu']
            modif = request.form.get('modif') == 'True'  # Ver si se quiere modificar

            cursor = mydb.cursor()

            cursor.execute('SELECT * FROM contactos WHERE nombre = %s', (nombre,))
            contacto = cursor.fetchone()

            if contacto:
                if modif:
                    cursor.execute('UPDATE contactos SET correo = %s WHERE nombre = %s', (correo, nombre))
                    mydb.commit()
                    result_msg = "MODIFICAT"
                else:
                    result_msg = "JAEXISTEIX"
            else:
                cursor.execute('INSERT INTO contactos (nombre, correo) VALUES (%s, %s)', (nombre, correo))
                mydb.commit()
                result_msg = "AGREGADO"

            return render_template('addmail.html', nom=nombre, correu=correo, result_msg=result_msg)

        return render_template('addmail.html')
    else:
        return redirect(url_for('login'))

@app.route('/getmail', methods=['GET', 'POST'])
def getmail():
    if 'nombre' in session:
        if request.method == 'POST':
            nombre = request.form['nom']

            cursor = mydb.cursor()
            cursor.execute('SELECT * FROM contactos WHERE nombre = %s', (nombre,))
            contacto = cursor.fetchone()

            if contacto:
                correo = contacto[1]
            else:
                correo = "NOTROBAT"

            return render_template('getmail.html', nom=nombre, correu=correo)

        return render_template('getmail.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('nombre', None)
    return redirect(url_for('home'))

@app.route('/calcular', methods=['POST'])
def calcular():
    nombre = request.form['nombre']
    edad = int(request.form['edad'])  # Convierte la edad a entero

    año_actual = 2024
    año_cumplira_100 = año_actual + (100 - edad)
    año_nacimiento =  año_actual - edad

    return render_template('nombre_edad.html', nombre=nombre, edad=edad, año_cumplira_100=año_cumplira_100, año_nacimiento=año_nacimiento)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/nombre_edad')
def nombre_edad():
    return render_template('nombre_edad.html')

if __name__ == '__main__':
    app.run(debug=True)
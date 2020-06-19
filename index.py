
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt

#inicio de la aplicacion
app = Flask(__name__)

#conexion a la base de datos
app.config['mysql_host'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prestamo'

mysql = MySQL(app)

#ruta para login
@app.route('/', methods=["GET","POST"])
def login():
	if request.method == "POST":
		nombre = request.form['nombre']
		password = request.form['password'].encode('utf-8')

		curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		curl.execute("SELECT * FROM admin WHERE nombre=%s",(nombre,))
		user = curl.fetchone()
		curl.close()

		if len(user) > 0:
			if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
				session['nombre'] = user['nombre']
				session['password'] = user['password']
				return render_template("inicio.html")
				#redirect(url_for("inicio"))
			else:
				return "Error password or name not match"
		else:
			return "Error name not found"
	else:
		return render_template("login.html")


#ruta para crear un administrador
@app.route('/admin', methods=["GET","POST"])
def admin():
	if request.method == 'GET':
		return render_template("admin.html")
	else:
		nombre = request.form['nombre']
		password = request.form['password'].encode('utf-8')
		hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO admin(nombre, password) VALUES (%s,%s)",(nombre, hash_password))
		mysql.connection.commit()
		session['nombre'] = nombre
		session['hash_password'] = hash_password
		return  redirect(url_for("inicio"))

#ruta para el inicio
@app.route('/inicio', methods=['GET','POST'])
def inicio():
	if request.method == "POST":
		cliente = request.form['nombre']
		curl = mysql.connection.cursor()
		curl.execute("SELECT * FROM cliente WHERE nombre=%s",(cliente,))
		#conn.commit()
		mysql.connection.commit()
		data = curl.fetchall()

		if len(data) == 0 and cliente == 'all':
			curl.execute("SELECT nombre FROM cliente")
			#connn.commit()
			mysql.connection.commit()
			data = curl.fetchall()
		return render_template("inicio.html", data = data)
	return render_template("inicio.html")

	


#ruta para logout
@app.route('/logout')
def logout():
	session.clear()
	return redirect("/")

#ruta para nuevo cliente
@app.route('/cliente', methods=["GET","POST"])
def cliente():
	if request.method == 'GET':
		return	render_template("cliente.html")
	else:
		nombre = request.form['nombre']
		email = request.form['email']
		telefono = request.form['telefono']
		cantidad = request.form['cantidad']
		fecha = request.form['fecha']
		semanas = request.form['semanas']
		semanaspagadas = request.form['semanaspagadas']
		semanasnopagadas = request.form['semanasnopagadas']
		pagoporsemanas = request.form['pagoporsemanas']
		cantidadpagada = request.form['cantidadpagada']
		cantidadnopagada = request.form['cantidadnopagada']
		totalpagar = request.form['totalpagar']

		curl = mysql.connection.cursor()
		curl.execute("INSERT INTO cliente(nombre, email, telefono, cantidad,fecha, semanas, semanaspagadas, semanasnopagadas, pagoporsemanas, cantidadpagada, cantidadnopagada, totalpagar) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(nombre, email, telefono, cantidad, fecha, semanas, semanaspagadas, semanasnopagadas, pagoporsemanas, cantidadpagada, cantidadnopagada, totalpagar))
		mysql.connection.commit()
		return redirect(url_for("inicio"))




#ruta para ver clientes
@app.route('/verclientes')
def verclientes():
	curl = mysql.connection.cursor()
	curl.execute("SELECT * FROM cliente")
	data = curl.fetchall()
	return render_template("verclientes.html", clientes = data)


#capital
@app.route('/capital')
def capital():
	curl = mysql.connection.cursor()
	curl.execute("SELECT SUM(cantidad), SUM(totalpagar), SUM(totalpagar) - SUM(cantidad), SUM(totalpagar) - SUM(cantidadpagada), SUM(cantidadpagada) FROM cliente")
	data = curl.fetchall()
	print(data)	
	return render_template("capital.html", capital = data)


#ruta para eliminar
@app.route('/delete/<string:id>', methods = ["POST","GET"])
def delete(id):
	curl = mysql.connection.cursor()
	curl.execute("DELETE FROM cliente WHERE id = {0}".format(id))
	mysql.connection.commit()
	return redirect(url_for("verclientes"))

#ruta para edicar 
@app.route('/edit/<id>')
def get_contact(id):
	curl = mysql.connection.cursor()
	curl.execute('SELECT * FROM cliente WHERE id = {0}'.format(id))
	data = curl.fetchall()
	print(data)
	return render_template("edit.html", cliente = data[0])

#ruta para actualizar
@app.route('/update/<id>', methods = ['POST'])
def update(id):
	if request.method == 'POST':
		nombre = request.form['nombre']
		email = request.form['email']
		telefono = request.form['telefono']
		cantidad = request.form['cantidad']
		fecha = request.form['fecha']
		semanas = request.form['semanas']
		semanaspagadas = request.form['semanaspagadas']
		semanasnopagadas = request.form['semanasnopagadas']
		pagoporsemanas = request.form['pagoporsemanas']
		cantidadpagada = request.form['cantidadpagada']
		cantidadnopagada = request.form['cantidadnopagada']
		totalpagar = request.form['totalpagar']

		curl = mysql.connection.cursor()
		curl.execute("""

			UPDATE cliente
			SET nombre = %s,
			    email = %s,
			    telefono = %s,
			    cantidad = %s,
			    fecha = %s,
			    semanas = %s,
			    semanaspagadas = %s,
			    semanasnopagadas = %s,
			    pagoporsemanas = %s,
			    cantidadpagada = %s,
			    cantidadnopagada = %s,
			    totalpagar = %s
			WHERE id = %s

			""",(nombre, email, telefono, cantidad, fecha, semanas, semanaspagadas, semanasnopagadas, pagoporsemanas, cantidadpagada, cantidadnopagada, totalpagar, id))
		mysql.connection.commit()
		return redirect(url_for("verclientes"))




#verificar el archivo principal
if __name__ == '__main__':
	app.secret_key = "012345678kndhe)(*"
	app.run(debug = True)
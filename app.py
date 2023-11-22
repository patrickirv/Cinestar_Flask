from flask import Flask, render_template
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cinestar'

mysql = MySQL(app)

@app.route("/")
def index():
	return render_template("index.html")


@app.route('/cines')
def cines():
	cur = mysql.connection.cursor()
	cur.execute ("call sp_getCines")
	result = cur.fetchall()
	cur.close()
	return render_template("cines.html",cines = result)


@app.route("/cine/<id>")
def cine(id):
	cur = mysql.connection.cursor()

	cur.execute('call sp_getCine(%s)', (id))
	resultCine = cur.fetchall()

	cur.execute('call sp_getCineTarifas(%s)', (id))
	resultTarifas = cur.fetchall()

	cur.execute('call sp_getCinePeliculas(%s)', (id))
	resultPeliculas = cur.fetchall()

	cur.close()
	
	return render_template('cine.html', cine = resultCine, tarifas = resultTarifas, peliculas = resultPeliculas)


@app.route("/peliculas/<id>")
def peliculas(id):
	if id == 'cartelera':
		parametro = 1
	else:
		parametro = 2
	cur = mysql.connection.cursor()
	cur.execute ('call sp_getPeliculas(%s)',(parametro,))
	result = cur.fetchall()
	cur.close()
	return render_template('peliculas.html', peliculas = result)


@app.route("/pelicula/<id>")
def pelicula(id):
	cur = mysql.connection.cursor()
	cur.execute ('call sp_getPelicula(%s)',(id,))
	result = cur.fetchall()
	cur.close()
	return render_template("pelicula.html", pelicula = result)

if __name__ == "__main__":
	app.run(debug=True)
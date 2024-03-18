from flask import Flask, request, jsonify
import requests
import pymysql
from datetime import datetime
from flask_cors import CORS
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
CORS(app)

# Función para conectarse a la base de datos
def connect_db():
	db_config = {
		'host': config['default']['host'],
		'user': config['default']['username'],
		'port': int(config.get('default', 'port', fallback=3306)),
		'password': config['default']['password'],
		'database': config['default']['db_name'],
		'cursorclass': pymysql.cursors.DictCursor
	}

	connection = pymysql.connect(**db_config)

	return connection


def insertar_clima_db(data):
	connection = connect_db()
	success = False

	try:
		temperatura = data['main']['temp']
		humedad = data['main']['humidity']
		viento = data['wind']['speed']
		descripcion = data['weather'][0]['description']
		fecha = data['fecha']
		url = data['url']
		lat = data['lat']
		lon = data['lon']

		with connection.cursor() as cursor:
			sql = "INSERT INTO clima (lat, lon, fecha, temperatura, humedad, viento, descripcion, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
			cursor.execute(sql, (lat, lon, fecha, temperatura, humedad, viento, descripcion, url))
		
		connection.commit()
		success = True
	finally:
		connection.close()

	return success
	

@app.route('/guardar-clima', methods=['POST'])
def guardar_clima():
	# Obtener lat y lon de los datos enviados en la petición
	lat = request.form.get('lat')
	lon = request.form.get('lon')
	fecha = datetime.now().strftime('%Y-%m-%d')  # Fecha actual para el ejemplo
	# Realizar la petición a la API de clima
	api_key = config['default']['api-key']
	url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"

	# Realizamos petición, guardamos datos, y devolvemos json
	request_response = requests.get(url)
	response_data = {
		"success": False,
		"message": "Error al obtener los datos del clima."
	}

	if request_response.status_code == 200:
		data = request_response.json()
		data['fecha'] = fecha
		data['url'] = url
		data['lat'] = lat
		data['lon'] = lon
		temperatura = data['main']['temp']
		humedad = data['main']['humidity']
		viento = data['wind']['speed']
		descripcion = data['weather'][0]['description']
		fecha = data['fecha']
		url = data['url']
		inserted = insertar_clima_db(data)

		if inserted:
			response_data = {
				"success": True,
				"message": "Datos del clima guardados correctamente.",
				"fecha": fecha,
				"temperatura": temperatura,
				"humedad": humedad,
				"viento": viento,
				"descripcion": descripcion,
				"url": url
			}
		else:
			response_data = {
				"success": False,
				"message": "Error al insertar datos en base de datos."
			}

	response = jsonify(response_data)

	return response


if __name__ == '__main__':
	app.run(debug=True)

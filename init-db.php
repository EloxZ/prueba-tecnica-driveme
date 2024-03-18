<?php

$config = parse_ini_file('config.ini');
$host = $config['host'];
$dbname = $config['db_name'];
$password = $config['password'];
$username = $config['username'];
// Crear conexión
$conn = new mysqli($host, $username, $password);

// Verificar conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Intentar seleccionar la base de datos
if (!$conn->select_db($dbname)) {
    // Si no se puede seleccionar, intentamos crearla
    $sql = "CREATE DATABASE IF NOT EXISTS $dbname";
    if ($conn->query($sql) === TRUE) {
        echo "Base de datos creada exitosamente\n";
        // Seleccionar la base de datos creada
        $conn->select_db($dbname);

        // Crear las tablas
        $crearTablas = [
            "CREATE TABLE IF NOT EXISTS clima (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE,
                lat VARCHAR(255),
                lon VARCHAR(255),
                temperatura VARCHAR(255),
                humedad VARCHAR(255),
                viento VARCHAR(255),
                descripcion VARCHAR(255),
				url VARCHAR(255)
            )"
        ];

        foreach ($crearTablas as $sql) {
            if ($conn->query($sql) === TRUE) {
                echo "Tabla creada exitosamente\n";
            } else {
                echo "Error al crear la tabla: " . $conn->error;
            }
        }

    } else {
        echo "Error al crear la base de datos: " . $conn->error;
    }
} else {
    echo "Conexión a la base de datos existente\n";
}


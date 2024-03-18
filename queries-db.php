<?php

function obtenerDatosClima($conn) {
    $datosClima = [];
    $sql = "SELECT fecha, lat, lon, temperatura, humedad, viento, descripcion, url FROM clima";

    $result = $conn->query($sql);
    if ($result && $result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $datoClima = [
                'fecha' => $row['fecha'],
                'temperatura' => $row['temperatura'],
                'humedad' => $row['humedad'],
                'viento' => $row['viento'],
                'descripcion' => $row['descripcion'],
                'url' => $row['url'],
                'lat' => $row['lat'],
                'lon' => $row['lon']
            ];

            $datosClima[] = $datoClima;
        }
    }

    return $datosClima;
}
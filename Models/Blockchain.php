<?php

class Blockchain
{
    private $PDO;

    public function __construct()
    {
        require_once __DIR__ . '/../config/conexion.php';
        $con = new Database();
        $this->PDO = $con->conexion();
    }

    //Función para mostrar el historial, con simulación blockchain, se modifico la el see pasado
    public function see()
    {
        $sql = "SELECT b.id, u.usuario, b.fecha, b.estado, b.anterior_hash, b.hash
                FROM blockchain b 
                JOIN usuarios u ON b.id_usuario = u.id
                ORDER BY b.id ASC";

        $stmt = $this->PDO->query($sql);
        $bloques = [];

        while ($fila = $stmt->fetch(PDO::FETCH_ASSOC)) {
            $fecha = new DateTime($fila['fecha']);
            $fila['fecha'] = $fecha->format('Y-m-d H:i:s');
            $bloques[] = $fila;
        }

        return $bloques;
    }

       //Función para mostrar los detalles del usuario creado
       public function show($id){  
        $stmt = $this->PDO->prepare("
            SELECT 
                *  
            FROM usuarios
            WHERE id = :id
            LIMIT 1
        ");
        $stmt->bindParam(":id", $id);
        return ($stmt->execute()) ? $stmt->fetch() : false;
    }
}

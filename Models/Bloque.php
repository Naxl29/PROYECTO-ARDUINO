<?php

class Bloque
{
    private $PDO;

    public function __construct()
    {
        require_once __DIR__ . '/../config/conexion.php';
        $con = new Database();
        $this->PDO = $con->conexion();
        date_default_timezone_set('America/Bogota');
    }
    

    public function obtenerUltimoHash()
    {
        $sql = "SELECT hash FROM blockchain ORDER BY id DESC LIMIT 1";
        $stmt = $this->PDO->query($sql);
        $fila = $stmt->fetch(PDO::FETCH_ASSOC);
        return $fila['hash'] ?? '0';
    }

    //Función para crear un nuevo usuario
    public function createUser($usuario, $contrasena)
    {
        $sql = "INSERT INTO usuarios (usuario, contrasena) VALUES (:nombre, :contrasena)";
        $stmt = $this->PDO->prepare($sql);
        $stmt->bindParam(':nombre', $usuario);
        $stmt->bindParam(':contrasena', $contrasena);
        if ($stmt->execute()) {
            return $this->PDO->lastInsertId(); // ID del nuevo usuario
        } else {
            return false;
        }
    }

    // Función para insertar crear un nuevo bloque utilizando el id de usuario
    public function createBlo($id_usuario, $estado)
    {
        $anteriorHash = $this->obtenerUltimoHash();
        $fecha = date("Y-m-d H:i:s");
        $datos = $fecha . $estado . $anteriorHash;
        $hash = hash('sha256', $datos);

        $sql = "INSERT INTO blockchain (id_usuario, fecha, estado, anterior_hash, hash)
                VALUES (:id_usuario, :fecha, :estado, :anterior_hash, :hash)";
        $stmt = $this->PDO->prepare($sql);
        $stmt->bindParam(':id_usuario', $id_usuario);
        $stmt->bindParam(':fecha', $fecha);
        $stmt->bindParam(':estado', $estado);
        $stmt->bindParam(':anterior_hash', $anteriorHash);
        $stmt->bindParam(':hash', $hash);

        return $stmt->execute();
    }

    // Función para iniciar sesión
    public function login($usuario, $contrasena)
    {
        $stmt = $this->PDO->prepare("SELECT * FROM usuarios WHERE usuario = :usuario AND contrasena = :contrasena");
        $stmt->bindParam(':usuario', $usuario);
        $stmt->bindParam(':contrasena', $contrasena);
        $stmt->execute();
        return ($stmt->rowCount() > 0) ? $stmt->fetch() : false;
  
    }
}

    
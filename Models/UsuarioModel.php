<?php

class UsuarioModel{
    private $PDO;

    //Función que conecta con la bd, esta será reemplazada por el blockchain
    public function __construct()
        {
            require_once("c://laragon/www/PROYECTO-ARDUINO/conexion.php");
            $con = new Database();
            $this->PDO = $con->conexion();
        }

    //Función para crear o agregar un usuario. Esta función está utilizando una conexión con base de datos, esto solo con la finalidad de probar si sí funciona.
    public function createUser($usuario, $contraseña){
        $stmt = $this->PDO->prepare("INSERT INTO usuarios VALUES(null, :usuario, :contraseña)");
        $stmt->bindParam(':usuario', $usuario); 
        $stmt->bindParam(':contraseña', $contraseña); 
        return ($stmt->execute()) ? $this->PDO->lastInsertId() : false; 
    }

    //Función para mostrar los usuarios
    public function index(){
        $stmt = $this->PDO->prepare("SELECT * FROM usuarios");
        return ($stmt->execute()) ? $stmt->fetchAll() : false;
    }

}
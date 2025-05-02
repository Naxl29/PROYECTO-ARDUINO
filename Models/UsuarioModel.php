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
    public function createUser($usuario, $contrasena){
        $stmt = $this->PDO->prepare("INSERT INTO usuarios VALUES(null, :usuario, :contrasena)");
        $stmt->bindParam(':usuario', $usuario); 
        $stmt->bindParam(':contrasena', $contrasena); 
        return ($stmt->execute()) ? $this->PDO->lastInsertId() : false; 
    }

    //Función para mostrar los usuarios
    public function see(){
        $stmt = $this->PDO->prepare("SELECT * FROM usuarios");
        return ($stmt->execute()) ? $stmt->fetchAll() : false;
    }

    // Función para iniciar sesión
    public function login($usuario, $contrasena){
        $stmt = $this->PDO->prepare("SELECT * FROM usuarios WHERE usuario = :usuario AND contrasena = :contrasena");
        $stmt->bindParam(':usuario', $usuario);
        $stmt->bindParam(':contrasena', $contrasena);
        $stmt->execute();
        return ($stmt->rowCount() > 0) ? $stmt->fetch() : false;
  
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

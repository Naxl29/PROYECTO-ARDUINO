<?php

class UsuarioController{
    private $model;

    //Función para conectar con el modelo que utiliza la bd
    public function __construct(){
        require_once("c://laragon/www/PROYECTO-ARDUINO/Models/UsuarioModel.php");
        $this->model = new UsuarioModel();
    }

    //Función para guardar cuando se crea un nuevo usuario
    public function save($usuario, $contrasena){
        $id = $this->model->createUser($usuario, $contrasena);
        return ($id!=false) ? header("Location:show.php?id=" .$id) : header("Location:create.php");
    }   

    //Esta función será para mostrar los detalles de cada usuario cuando se crea
    public function see(){
        return ($this->model->see()) ? $this->model->see() : false;
    }
    
    //Función para tomar el id del último usuario que se creó y mostrar los detalles de su creación
    public function show($id){
        return ($this->model->show($id) != false) ? $this->model->show($id) : header("Location:index.php");
    }

    //Función para iniciar sesión
    public function login($usuario, $contrasena){
        $user = $this->model->login($usuario, $contrasena);
        if ($user) {
            session_start();
            $_SESSION['usuario'] = $user['usuario'];
            $_SESSION['usuario'] = $user['id'];
            header("Location: button.php"); 
            exit;
        } else {
            header("Location: login.php");
            exit;
            header("Location: login.php?error=1"); // Redirigir a la página de inicio de sesión con un error
            session_start(); // Inicia la sesión si aún no está iniciada
            $_SESSION['login_error'] = "Usuario o contraseña incorrectos."; // Guarda el mensaje de error en la sesión
            header("Location: login.php"); // Redirige de vuelta a la página de inicio de sesión

        }
    }
    
}

    
?>
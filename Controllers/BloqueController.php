<?php
    //Controlador creado para manejar la inserción de datos
    class BloqueController{
        private $model;

        //Función para conectar con el modelo que utiliza la bd
        public function __construct(){
            require_once __DIR__ . '/../Models/Bloque.php';
            $this->model = new Bloque;
        }

        //Función para guardar cuando se crea un nuevo usuario
        public function save($usuario, $contrasena){
            $id = $this->model->createUser($usuario, $contrasena);
            return ($id!=false) ? header("Location:show.php?id=" .$id) : header("Location:create.php");
        } 

        // Esta función se agrego para obtener el estado del boton
        public function saveEstado($id_usuario, $estado) 
        {
                $id_usuario = (int)$id_usuario;
                $resultado = $this->model->createBlo($id_usuario, $estado);
                return $resultado === true;
        }
         
         //Función para iniciar sesión conectada a los modelo Bloque
        public function login($usuario, $contrasena) 
        {
            $user = $this->model->login($usuario, $contrasena);
            if ($user) {
                session_start();
                $_SESSION['usuario'] = $user['usuario'];
                header("Location: button.php"); // O a la página que quieras mostrar después de iniciar sesión
            } else {
                header("Location: login.php?error=1"); // Redirigir a la página de inicio de sesión con un error
                session_start(); // Inicia la sesión si aún no está iniciada
                $_SESSION['login_error'] = "Usuario o contraseña incorrectos."; // Guarda el mensaje de error en la sesión
                header("Location: login.php"); // Redirige de vuelta a la página de inicio de sesión

            }
        }
    }
?>

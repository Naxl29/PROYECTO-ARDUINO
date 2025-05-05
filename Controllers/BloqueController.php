<?php

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

        public function saveEstado($id_usuario, $estado) 
        {
                $id_usuario = (int)$id_usuario;
                $resultado = $this->model->createBlo($id_usuario, $estado);
                return $resultado === true;
        }
         
         //Función para iniciar sesión (en BloqueController.php)
        public function login($usuario, $contrasena)
        {
            $user = $this->model->login($usuario, $contrasena);
            if ($user) {
                session_start();

                $_SESSION['usuario'] = $user['usuario'];
                $_SESSION['id_usuario'] = $user['id']; 

                header("Location: button.php");

            } else {
                header("Location: login.php");
            }
        }
    }
?>

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
    public function index(){
        return ($this->model->index()) ? $this->model->index() : false;
    }
}
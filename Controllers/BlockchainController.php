<?php
    //Controlador creado para manejar la vista 
    class BlockchainController{
        private $model;

        //Función para conectar con el modelo que utiliza la bd
        public function __construct(){
            require_once __DIR__ . '/../Models/Blockchain.php';
            $this->model = new Blockchain;
        }

        // Función para mostrar el usuario recien creado
        public function show($id)
        {
            return ($this->model->show($id) != false) ? $this->model->show($id) : header("Location:index.php");
        }


        //Esta función será para mostrar los detalles de cada usuario cuando se crea
        public function see()
        {
            return ($this->model->see()) ? $this->model->see() : false;
        }
    }
?>
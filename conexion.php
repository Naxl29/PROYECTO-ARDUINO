<?php

//Conexión con la bd
class Database {
    private string $host = "localhost";
    private string $database = "dbprueba";
    private string $user = "root";
    private string $password = "";

    public function conexion(){
        try{
            $PDO = new PDO("mysql:host=".$this->host.";dbname=".$this->database,$this->user,$this->password);
            return $PDO;
        } catch(PDOException $e){
            return $e->getMessage();
        }

    }
}
from Models import Bloque
class BloqueController:
    def __init__(self):
        self.model= Bloque(self)  # Modelo de bloques
        
    def createBlock(self, id_usuario, estado): # Crear un nuevo bloque
        # Crear un nuevo bloque
        return self.model.createBloque(id_usuario, estado) 
    def see(self):
        # Mostrar todos los bloques
        return self.bloque_model.see()
  
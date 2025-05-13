from models.blockchain import Blockchain

class BlockchainController:
    def __init__(self):
        self.model = Blockchain()
    
    def show(self, id):
        return self.model.show(id)
    
    def see(self):
        return self.model.see()

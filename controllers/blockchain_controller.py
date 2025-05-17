from models.blockchain import Blockchain

class BlockchainController:
    def __init__(self):
        self.model = Blockchain()
    
    def show(self, id):
        return self.model.show(id)
    
    def see(self):
        return self.model.see()
    
    def get_block_by_hash(self, block_hash):
        conn = self.model.db.conexion() 
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM blockchain WHERE hash = %s LIMIT 1"
        cursor.execute(sql, (block_hash,))
        block = cursor.fetchone()

        cursor.close()
        conn.close()

        return block
import sqlite3
import finances

# Classe de banco de dados
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.profit_rate = 0
        
        # Sobre a tabela de produtos
        self.product_table = {
            "table": "products",
            "id": "id",
            "name": "prod_name",
            "base_price": "base_price",
            "profit": "profit",
            "price": "unit_price"
        }
    
    
    # Função que verifica se o produto existe
    def _prod_exists(self, prod_id):
        self.cursor.execute(f"SELECT * FROM {self.product_table['table']} WHERE id={prod_id}")
        res = self.cursor.fetchone()
        
        if res is None:
            return False
        else:
            return True
        
    
    # Função que gera a tabela caso não exista
    def initialize(self):
        # Pegar o script de criação
        self.cursor.execute(open("dbscript.sql", "r").read())
        self.conn.commit()
        
    
    # Adiciona produto
    def add_prod(self, name, base_price):
        row = (
            name,
            base_price,
            finances.get_profit(self.profit_rate, base_price),
            finances.add_profit(self.profit_rate, base_price)
            ) # A linha 
        
        self.cursor.execute(
            f"INSERT INTO {self.product_table['table']} ({self.product_table['name']}, {self.product_table['base_price']}, {self.product_table['profit']}, {self.product_table['price']}) VALUES (?, ?, ?, ?)  RETURNING {self.product_table['id']}",
            row
        )
        #self.cursor.execute(f"INSERT INTO {self.product_table['table']} ({self.product_table['name']}, {self.product_table['price']}) VALUES (?, ?) RETURNING {self.product_table['id']}", (name, price))
        
        prod_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return prod_id 
        
    
    # Remover produto
    def remove_prod(self, prod_id):
        if self._prod_exists(prod_id):
            self.cursor.execute(f"DELETE FROM {self.product_table['table']} WHERE id={prod_id}")
            self.conn.commit()
            return True
        else:
            return False
        
        
    def update_price(self, prod_id, price):
        if self._prod_exists(prod_id):
            row = (
                prod_id,
                price,
                finances.get_profit(self.profit_rate, price),
                finances.add_profit(self.profit_rate, price)
            )
            
            self.cursor.execute(
                f"UPDATE {self.product_table['table']} SET {self.product_table['base_price']}=?, {self.product_table['profit']}=?, {self.product_table['price']}=? WHERE {self.product_table['id']}=?",
                row
            )
            #self.cursor.execute(f"UPDATE {self.product_table['table']} SET {self.product_table['price']}={price} WHERE {self.product_table['id']}={prod_id}")
            self.conn.commit()
            return True
        else:
            return False
        
        
    def update_name(self, prod_id, name):
        if self._prod_exists(prod_id):
            self.cursor.execute(f'UPDATE {self.product_table['table']} SET {self.product_table['name']}="{name}" WHERE {self.product_table['id']}={prod_id}')
            self.conn.commit()
            return True
        else:
            return False
        
        
    def get_prod(self, prod_id):
        if self._prod_exists(prod_id):
            self.cursor.execute(f"SELECT * FROM {self.product_table['table']} WHERE id={prod_id}")
            return self.cursor.fetchone()
        else:
            return False
        
        
if __name__ == "__main__":
    db = Database("database.db")
    db.initialize()
    prod_id = db.add_prod("Teste", 100)
    db.update_price(prod_id, 200)
    db.update_name(prod_id, "Teste 2")
    print(db.get_prod(prod_id))
    db.remove_prod(prod_id)
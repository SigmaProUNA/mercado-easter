import sqlite3
import finances
import exceptions

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
            "price": "unit_price",
            "stock": "stock"
        }
    
    
    # Função que verifica se o produto existe
    def prod_exists(self, prod_id):
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
    def add_prod(self, name, base_price, stock):
        row = (
            name,
            base_price,
            finances.get_profit(self.profit_rate, base_price),
            finances.add_profit(self.profit_rate, base_price),
            stock
            ) # A linha 
        
        self.cursor.execute(
            f"INSERT INTO {self.product_table['table']} ({self.product_table['name']}, {self.product_table['base_price']}, {self.product_table['profit']}, {self.product_table['price']}, {self.product_table['stock']}) VALUES (?, ?, ?, ?, ?)  RETURNING {self.product_table['id']}",
            row
        )
        #self.cursor.execute(f"INSERT INTO {self.product_table['table']} ({self.product_table['name']}, {self.product_table['price']}) VALUES (?, ?) RETURNING {self.product_table['id']}", (name, price))
        
        prod_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return prod_id 
        
    
    # Remover produto
    def remove_prod(self, prod_id):
        if self.prod_exists(prod_id):
            self.cursor.execute(f"DELETE FROM {self.product_table['table']} WHERE id={prod_id}")
            self.conn.commit()
            return True
        else:
            raise exceptions.ProdNotFoundException(f"Produto {prod_id} não encontrado")
        
    def update_price(self, prod_id, price):
        if self.prod_exists(prod_id):
            row = (
                price,
                finances.get_profit(self.profit_rate, price),
                finances.add_profit(self.profit_rate, price),
                prod_id
            )
            
            self.cursor.execute(
                f"UPDATE {self.product_table['table']} SET {self.product_table['base_price']}=?, {self.product_table['profit']}=?, {self.product_table['price']}=? WHERE {self.product_table['id']}=?",
                row
            )
            #self.cursor.execute(f"UPDATE {self.product_table['table']} SET {self.product_table['price']}={price} WHERE {self.product_table['id']}={prod_id}")
            self.conn.commit()
            return True
        else:
            raise exceptions.ProdNotFoundException(f"Produto {prod_id} não encontrado")
        
        
    def update_name(self, prod_id, name):
        if self.prod_exists(prod_id):
            self.cursor.execute(f'UPDATE {self.product_table['table']} SET {self.product_table['name']}="{name}" WHERE {self.product_table['id']}={prod_id}')
            self.conn.commit()
            return True
        else:
            raise exceptions.ProdNotFoundException(f"Produto {prod_id} não encontrado")
        
        
    def get_prod(self, prod_id):
        if self.prod_exists(prod_id):
            self.cursor.execute(f"SELECT * FROM {self.product_table['table']} WHERE id={prod_id}")
            res =  self.cursor.fetchone()
            return {
                "id": res[0],
                "name": res[1],
                "base_price": res[2],
                "profit": res[3],
                "price": res[4],
                "stock": res[5]
            }
        else:
            raise exceptions.ProdNotFoundException(f"Produto {prod_id} não encontrado")
        

    def prod_stock_update(self, prod_id, stock):
        if self.prod_exists(prod_id):
            self.cursor.execute(f"UPDATE {self.product_table['table']} SET {self.product_table['stock']}={stock} WHERE {self.product_table['id']}={prod_id}")
            self.conn.commit()
        else:
            raise exceptions.ProdNotFoundException(f"Produto {prod_id} não encontrado")
            

    # Definir o rate de profit para calculo
    def set_profit(self, profit: float):
        self.profit_rate = profit / 100
        

    def search_by_name(self, name):
        self.cursor.execute(f"SELECT * FROM {self.product_table['table']} WHERE UPPER({self.product_table['name']}) LIKE UPPER('%{name}%')")
        res = self.cursor.fetchall()
        
        headers = ["id", "name", "base_price", "profit", "price", "stock"]
        rows = []
        
        # Resultados de pesquisa
        for row in res:
            rows.append([x for x in row])
        
        return {
            "headers": headers,
            "rows": rows
        }
    
        
if __name__ == "__main__":
    pass

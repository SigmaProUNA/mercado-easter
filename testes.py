import pytest
import os
import json
import tempfile
from unittest.mock import patch, MagicMock

# Imports dos módulos do projeto
import fastmath
import finances
import database
import exceptions
import market_backend


class TestFastMath:
    """Testes básicos para fastmath.py"""
    
    def test_is_integer(self):
        assert fastmath.is_integer("123") == True
        assert fastmath.is_integer("abc") == False
        assert fastmath.is_integer("") == False
    
    def test_is_number(self):
        assert fastmath.is_number("123") == True
        assert fastmath.is_number("3,14") == True
        assert fastmath.is_number("3/4") == True
        assert fastmath.is_number("abc") == False
    
    def test_is_money(self):
        assert fastmath.is_money("10,50") == True
        assert fastmath.is_money("10,5") == False
        assert fastmath.is_money("abc") == False


class TestFinances:
    """Testes básicos para finances.py"""
    
    def test_cents_to_money(self):
        result = finances.cents_to_money(1050)
        assert result == "R$ 10,50"
        
        result = finances.cents_to_money(100)
        assert result == "R$ 1,00"
    
    def test_money_to_cents(self):
        assert finances.money_to_cents("R$ 10,50") == 1050
        assert finances.money_to_cents("R$ 1,00") == 100
    
    def test_get_profit(self):
        assert finances.get_profit(0.2, 1000) == 200
        assert finances.get_profit(0.1, 500) == 50
    
    def test_add_profit(self):
        assert finances.add_profit(0.2, 1000) == 1200
        assert finances.add_profit(0.1, 500) == 550


class TestDatabase:
    """Testes para Database"""
    
    @pytest.fixture
    def temp_db(self):
        """Cria banco temporário para testes"""
        db_path = ":memory:"
        
        sql_script = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prod_name TEXT NOT NULL,
            base_price INTEGER NOT NULL,
            profit INTEGER NOT NULL,
            unit_price INTEGER NOT NULL,
            stock INTEGER NOT NULL
        );
        """
        
        with patch('builtins.open', MagicMock(return_value=MagicMock(read=MagicMock(return_value=sql_script)))):
            db = database.Database(db_path)
            db.initialize()
            db.set_profit(20.0)
        
        return db
    
    def test_add_prod(self, temp_db):
        prod_id = temp_db.add_prod("Produto Teste", 1000, 50)
        assert prod_id > 0
        
        product = temp_db.get_prod(prod_id)
        assert product['name'] == "Produto Teste"
        assert product['base_price'] == 1000
        assert product['stock'] == 50
    
    def test_prod_exists(self, temp_db):
        prod_id = temp_db.add_prod("Produto Teste", 1000, 50)
        assert temp_db.prod_exists(prod_id) == True
        assert temp_db.prod_exists(99999) == False
    
    def test_get_prod_not_found(self, temp_db):
        with pytest.raises(exceptions.ProdNotFoundException):
            temp_db.get_prod(99999)
    
    def test_update_price(self, temp_db):
        prod_id = temp_db.add_prod("Produto Teste", 1000, 50)
        temp_db.update_price(prod_id, 1500)
        
        product = temp_db.get_prod(prod_id)
        assert product['base_price'] == 1500
    
    def test_remove_prod(self, temp_db):
        prod_id = temp_db.add_prod("Produto Teste", 1000, 50)
        temp_db.remove_prod(prod_id)
        assert temp_db.prod_exists(prod_id) == False


class TestMarket:
    """Testes para Market"""
    
    @pytest.fixture
    def market_instance(self):
        config_data = {
            "db_path": ":memory:",
            "profit": 20.0,
            "sell_csv_path": "temp_sells.csv"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name
        
        with patch('report.SellReport') as mock_report:
            mock_report.return_value.initialize.return_value = None
            
            sql_script = """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prod_name TEXT NOT NULL,
                base_price INTEGER NOT NULL,
                profit INTEGER NOT NULL,
                unit_price INTEGER NOT NULL,
                stock INTEGER NOT NULL
            );
            """
            
            with patch('builtins.open', MagicMock(return_value=MagicMock(read=MagicMock(return_value=sql_script)))):
                market = market_backend.Market(config_path)
                market.add_prod("Produto A", 1000, 10)
                market.add_prod("Produto B", 1500, 5)
                
        os.unlink(config_path)
        return market
    
    def test_sell_success(self, market_instance):
        transaction = market_instance.sell(1, 2)
        
        assert transaction['prod_id'] == 1
        assert transaction['quantity'] == 2
        assert len(market_instance.current_transaction) == 1
    
    def test_sell_product_not_found(self, market_instance):
        with pytest.raises(exceptions.ProdNotFoundException):
            market_instance.sell(99999, 1)
    
    def test_sell_not_enough_stock(self, market_instance):
        with pytest.raises(exceptions.NotEnoughItemsException):
            market_instance.sell(1, 20)
    
    def test_finish_transaction(self, market_instance):
        market_instance.sell(1, 2)
        market_instance.csv.report = MagicMock()
        
        market_instance.finish_transaction()
        
        assert len(market_instance.current_transaction) == 0
        product = market_instance.db.get_prod(1)
        assert product['stock'] == 8  # 10 - 2
    
    def test_search(self, market_instance):
        result = market_instance.search("Produto")
        assert len(result['rows']) == 2
    
    def test_add_prod(self, market_instance):
        market_instance.add_prod("Produto C", 800, 15)
        result = market_instance.search("Produto C")
        assert len(result['rows']) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
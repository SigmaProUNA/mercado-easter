import pytest
import os
import json
from io import StringIO
from unittest.mock import patch, MagicMock

# importa os outros módulos do projeto, apenas os essenciais
# colocando isso aqui só pra garantir que tá rodando o teste quando vai pra main
import fastmath
import finances
import database
import exceptions
import market_backend


# verificação numérica e monetária
class TestFastMath:
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


# pra funções financeiras de conversão e lucro
class TestFinances:
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
        assert finances.add_profit(1.2, 1000) == 1200
        assert finances.add_profit(1.1, 500) == 550


# módulo de banco de dados
class TestDatabase:
    @pytest.fixture
    def temp_db(self):
        """Cria um banco em memória para testes"""
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


# backend do mercado (venda, busca, etc.)
class TestMarket:
    @pytest.fixture
    def market_instance(self):
        """Cria instância de mercado simulada"""
        config_data = {
            "db_path": ":memory:",
            "profit": 20.0,
            "sell_csv_path": "temp_sells.csv"
        }
        fake_config = json.dumps(config_data)

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

        open_orig = open

        def open_side_effect(path, *args, **kwargs):
            if "fake_path.json" in path:
                return StringIO(fake_config)
            elif path.endswith(".sql"):
                return StringIO(sql_script)
            return open_orig(path, *args, **kwargs)

        with patch("builtins.open", side_effect=open_side_effect):
            with patch('report.SellReport') as mock_report:
                mock_report.return_value.initialize.return_value = None
                market = market_backend.Market("fake_path.json")
                market.add_prod("Produto A", 1000, 10)
                market.add_prod("Produto B", 1500, 5)

        return market

    def test_sell_success(self, market_instance):
        transaction = market_instance.sell(1, 2)
        assert transaction['prod_id'] == 1
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
    
    def test_search(self, market_instance):
        result = market_instance.search("Produto")
        assert len(result['rows']) == 2
    
    def test_add_prod(self, market_instance):
        market_instance.add_prod("Produto C", 800, 15)
        result = market_instance.search("Produto C")
        assert len(result['rows']) == 1


# Executa os testes diretamente se o arquivo for rodado
if __name__ == "__main__":
    pytest.main([__file__, "-v"])

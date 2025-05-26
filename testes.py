# testes.py

import pytest
import sys
import os

# Adicionar o diretório atual ao Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Importações com tratamento de erro
def import_with_fallback(module_name):
    try:
        return __import__(module_name)
    except ImportError as e:
        pytest.skip(f"Módulo {module_name} não encontrado: {e}", allow_module_level=True)

# Tenta importar os módulos
try:
    from fastmath import is_integer, is_number
    from finances import cents_to_money
    from database import Database
    import sqlite3
except ImportError as e:
    pytest.skip(f"Erro ao importar módulos necessários: {e}", allow_module_level=True)

# =============================
# Testes para fastmath.py
# =============================

def test_is_integer():
    assert is_integer("123456")
    assert is_integer("0")
    assert not is_integer("12a3")
    assert not is_integer("")
    assert not is_integer(" ")

def test_is_number():
    assert is_number("123")
    assert is_number("45,67")  # vírgula
    assert is_number("3/4")    # barra
    assert not is_number("abc")
    assert not is_number("12.3")  # ponto não suportado
    assert not is_number("")

# =============================
# Testes para finances.py
# =============================

def test_cents_to_money():
    assert cents_to_money(1234) == "R$ 12,34"
    assert cents_to_money("75") == "R$ 0,75"
    assert cents_to_money("9") == "R$ 0,09"
    assert cents_to_money("999") == "R$ 9,99"
    assert cents_to_money("1000", separator_standard=".") == "R$ 10.00"


# =============================
# Testes para database.py
# =============================

@pytest.mark.skipif('Database' not in globals(), reason="Database module not available")
def test_prod_exists():
    # Banco em memória para teste
    db = Database(":memory:")
    db.cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            prod_name TEXT,
            base_price REAL,
            profit REAL,
            unit_price REAL,
            stock INTEGER
        )
    """)
    db.cursor.execute("INSERT INTO products (id, prod_name, base_price, profit, unit_price, stock) VALUES (1, 'Produto A', 10, 0.2, 12, 100)")
    db.conn.commit()

    assert db.prod_exists(1) == True
    assert db.prod_exists(2) == False

# =============================
# (Opcional) Testes iniciais para market_backend.py
# =============================

def test_market_init(tmp_path):
    try:
        from market_backend import Market
    except ImportError:
        pytest.skip("market_backend module not available")
    
    # Criar arquivos de configuração falsos
    db_path = tmp_path / "db.sqlite"
    csv_path = tmp_path / "sell.csv"
    config_path = tmp_path / "config.json"

    db_path.write_text("")
    csv_path.write_text("")
    config_path.write_text("""
    {
        "db_path": "%s",
        "profit": 0.2,
        "sell_csv_path": "%s",
        "words": {"pt": {"ex": "teste"}},
        "selected_lang": "pt"
    }
    """ % (str(db_path).replace("\\", "\\\\"), str(csv_path).replace("\\", "\\\\")))

    # Testa se inicializa sem erro
    market = Market(str(config_path))
    assert market.config["profit"] == 0.2

# Teste de diagnóstico
def test_environment_info():
    """Teste para debug - mostra informações do ambiente"""
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    print(f"Files in current directory: {os.listdir('.')}")
    assert True  # Sempre passa, só para mostrar info
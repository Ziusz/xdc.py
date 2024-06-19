import pytest
import time
from xdc.xrc20 import XRC20

@pytest.fixture
def xrc20_instance():
    rpc_url = "https://rpc.apothem.network"
    return XRC20(rpc_url)

@pytest.fixture
def token_address():
    return ""

@pytest.fixture
def test_account():
    return ""

@pytest.fixture
def test_account_private_key():
    return ""

@pytest.fixture
def another_account():
    return ""

@pytest.fixture
def another_account_private_key():
    return ""    

@pytest.fixture(autouse=True)
def slow_down_tests():
    yield
    time.sleep(3)

def is_transaction_hash(web3, tx_hash):
    try:
        transaction = web3.eth.get_transaction(tx_hash)
        return True
    except:
        return False 

def test_name(xrc20_instance, token_address):
    name = xrc20_instance.name(token_address)
    assert isinstance(name, str)

def test_total_supply(xrc20_instance, token_address):
    total_supply = xrc20_instance.total_supply(token_address)
    assert total_supply > 0

def test_decimals(xrc20_instance, token_address):
    decimals = xrc20_instance.decimals(token_address)
    assert isinstance(decimals, int)

def test_symbol(xrc20_instance, token_address):
    symbol = xrc20_instance.symbol(token_address)
    assert isinstance(symbol, str)

def test_balance_of(xrc20_instance, token_address, test_account):
    balance = xrc20_instance.balance_of(token_address, test_account)
    assert balance >= 0

def test_allowance(xrc20_instance, token_address, test_account, another_account):
    allowance = xrc20_instance.allowance(token_address, test_account, another_account)
    assert allowance >= 0    

def test_transfer_xdc(xrc20_instance, test_account, test_account_private_key, another_account):
    amount = 0.001
    tx_hash = xrc20_instance.transfer_xdc(test_account, test_account_private_key, another_account, amount)
    assert is_transaction_hash(xrc20_instance.w3, tx_hash)

def test_transfer_token(xrc20_instance, token_address, test_account, test_account_private_key, another_account):
    amount = 0.001
    tx_hash = xrc20_instance.transfer_token(token_address, test_account, test_account_private_key, another_account, amount)
    assert is_transaction_hash(xrc20_instance.w3, tx_hash)

def test_approve(xrc20_instance, token_address, test_account, test_account_private_key, another_account):
    amount = 0.001
    tx_hash = xrc20_instance.approve(token_address, test_account, test_account_private_key, another_account, amount)
    assert is_transaction_hash(xrc20_instance.w3, tx_hash)

def test_increase_allowance(xrc20_instance, token_address, test_account, test_account_private_key, another_account):
    amount = 0.001
    tx_hash = xrc20_instance.increase_allowance(token_address, test_account, test_account_private_key, another_account, amount)
    assert is_transaction_hash(xrc20_instance.w3, tx_hash)

def test_decrease_allowance(xrc20_instance, token_address, test_account, test_account_private_key, another_account):
    amount = 0.001
    tx_hash = xrc20_instance.decrease_allowance(token_address, test_account, test_account_private_key, another_account, amount)
    assert is_transaction_hash(xrc20_instance.w3, tx_hash)

def test_transfer_from(xrc20_instance, token_address, test_account, another_account, another_account_private_key):
    amount = 0.001
    tx_hash = xrc20_instance.transfer_from(token_address, test_account, another_account, another_account_private_key, token_address, amount)
    assert is_transaction_hash(xrc20_instance.w3, tx_hash)

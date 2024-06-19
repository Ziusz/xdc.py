# xdc.py

xdc.py is a Python library for interacting with XDC (XinFin Digital Contract) tokens (XRC20 for now) using web3.py.

## Installation

You can install xdc.py using pip:

```bash
pip install xdc
```

## Usage

### Initializing the XRC20 Object

```python
import xdc

# Initialize XRC20 object with RPC URL
rpc_url = 'https://rpc.xdcrpc.com'  # Replace with your RPC URL
xrc20 = xdc.XRC20(rpc_url)
```

### Getting Token Information

#### Get Token Name

```python
token_address = '0x...'  # Token's contract address
name = xrc20.name(token_address)
print(f"Token Name: {name}")
```

#### Get Total Supply

```python
token_address = '0x...'  # Token's contract address
total_supply = xrc20.total_supply(token_address)
print(f"Total Supply: {total_supply}")
```

#### Get Decimals

```python
token_address = '0x...'  # Token's contract address
decimals = xrc20.decimals(token_address)
print(f"Decimals: {decimals}")
```

#### Get Symbol

```python
token_address = '0x...'  # Token's contract address
symbol = xrc20.symbol(token_address)
print(f"Symbol: {symbol}")
```

#### Get Balance of an Address

```python
token_address = '0x...'  # Token's contract address
owner_address = '0x...'  # Address to which you want to check the balance
balance = xrc20.balance_of(token_address, owner_address)
print(f"Balance of {owner_address}: {balance}")
```

### Transferring XDC and Tokens

#### Transfer XDC

```python
owner_address = '0x...'  # Sender's address
owner_private_key = '0x...'  # Sender's private key
receiver_address = '0x...'  # Receiver's address
amount = 1  # Amount to transfer in XDC

tx_hash = xrc20.transfer_xdc(owner_address, owner_private_key, receiver_address, amount)
print(f"Transfer XDC Transaction Hash: {tx_hash}")
```

#### Transfer Tokens

```python
token_address = '0x...'  # Token's contract address
owner_address = '0x...'  # Sender's address
owner_private_key = '0x...'  # Sender's private key
receiver_address = '0x...'  # Receiver's address
amount = 1  # Amount of tokens to transfer

tx_hash = xrc20.transfer_token(token_address, owner_address, owner_private_key, receiver_address, amount)
print(f"Transfer Token Transaction Hash: {tx_hash}")
```

#### Approve Token Transfer

```python
token_address = '0x...'  # Token's contract address
owner_address = '0x...'  # Sender's address (address that allows to spend tokens)
owner_private_key = '0x...'  # Owner's private key
spender_address = '0x...'  # Spender's address (address allowed to spend tokens)
amount = 1  # Amount of tokens to approve

tx_hash = xrc20.approve(token_address, owner_address, owner_private_key, spender_address, amount)
print(f"Approve Token Transfer Transaction Hash: {tx_hash}")
```

#### Increase/Decrease Allowance

```python
token_address = '0x...'  # Token's contract address
owner_address = '0x...'  # Owner's address (address that allows to spend tokens)
owner_private_key = '0x...'  # Owner's private key
spender_address = '0x...'  # Spender's address (address allowed to spend tokens)
amount = 1  # Amount of tokens to adjust allowance

# Increase Allowance
tx_hash_increase = xrc20.increase_allowance(token_address, owner_address, owner_private_key, spender_address, amount)
print(f"Increase Allowance Transaction Hash: {tx_hash_increase}")

# Decrease Allowance
tx_hash_decrease = xrc20.decrease_allowance(token_address, owner_address, owner_private_key, spender_address, amount)
print(f"Decrease Allowance Transaction Hash: {tx_hash_decrease}")
```

#### Transfer Tokens From

```python
token_address = '0x...'  # Token's contract address
owner_address = '0x...'  # Owner's address (address that allows to spend tokens)
spender_address = '0x...'  # Spender's address (address allowed to spend tokens)
spender_private_key = '0x...'  # Spender's private key
receiver_address = '0x...'  # Receiver's address
amount = 1  # Amount of tokens to transfer

tx_hash = xrc20.transfer_from(token_address, owner_address, spender_address, spender_private_key, receiver_address, amount)
print(f"Transfer From Transaction Hash: {tx_hash}")
```

## License

This library is licensed under the MIT License.

## Acknowledgments

- Built with [web3.py](https://web3py.readthedocs.io/en/stable/)
- Tested with [pytest](https://docs.pytest.org/en/stable/)

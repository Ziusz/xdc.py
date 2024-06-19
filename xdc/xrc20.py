from web3 import Web3
from web3.middleware import geth_poa_middleware
from decimal import *

xrc20abi = "[{\"constant\":true,\"inputs\":[],\"name\":\"name\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_spender\",\"type\":\"address\"},{\"name\":\"_value\",\"type\":\"uint256\"}],\"name\":\"approve\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"totalSupply\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_from\",\"type\":\"address\"},{\"name\":\"_to\",\"type\":\"address\"},{\"name\":\"_value\",\"type\":\"uint256\"}],\"name\":\"transferFrom\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"decimals\",\"outputs\":[{\"name\":\"\",\"type\":\"uint8\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"_owner\",\"type\":\"address\"}],\"name\":\"balanceOf\",\"outputs\":[{\"name\":\"balance\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[],\"name\":\"symbol\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"_to\",\"type\":\"address\"},{\"name\":\"_value\",\"type\":\"uint256\"}],\"name\":\"transfer\",\"outputs\":[{\"name\":\"\",\"type\":\"bool\"}],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"_owner\",\"type\":\"address\"},{\"name\":\"_spender\",\"type\":\"address\"}],\"name\":\"allowance\",\"outputs\":[{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"},{\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"fallback\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"name\":\"owner\",\"type\":\"address\"},{\"indexed\":true,\"name\":\"spender\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"value\",\"type\":\"uint256\"}],\"name\":\"Approval\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"name\":\"from\",\"type\":\"address\"},{\"indexed\":true,\"name\":\"to\",\"type\":\"address\"},{\"indexed\":false,\"name\":\"value\",\"type\":\"uint256\"}],\"name\":\"Transfer\",\"type\":\"event\"}]"

class XRC20:
    def __init__(self, rpc_url):
        self.rpc_url = rpc_url
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def get_contract_instance(self, token_address):
        return self.w3.eth.contract(address=token_address, abi=xrc20abi)

    def name(self, token_address):
        return self.get_contract_instance(token_address).functions.name().call()

    def total_supply(self, token_address):
        total_supply = self.get_contract_instance(token_address).functions.totalSupply().call()
        return self.w3.from_wei(total_supply, 'ether')

    def decimals(self, token_address):
        return self.get_contract_instance(token_address).functions.decimals().call()

    def symbol(self, token_address):
        return self.get_contract_instance(token_address).functions.symbol().call()

    def balance_of(self, token_address, owner_address):
        owner = self.w3.to_checksum_address(owner_address)
        balance = self.get_contract_instance(token_address).functions.balanceOf(owner).call()
        return self.w3.from_wei(balance, 'ether')

    def allowance(self, token_address, owner_address, spender_address):
        owner = self.w3.to_checksum_address(owner_address)
        spender = self.w3.to_checksum_address(spender_address)
        allowance = self.get_contract_instance(token_address).functions.allowance(owner, spender).call()
        return self.w3.from_wei(allowance, 'ether')

    def transfer_xdc(self, owner_address, owner_private_key, receiver_address, amount):
        owner = self.w3.to_checksum_address(owner_address)
        receiver = self.w3.to_checksum_address(receiver_address)
        amount = self.w3.to_wei(amount, 'ether')

        nonce = self.w3.eth.get_transaction_count(owner)
        gas_price = self.w3.eth.gas_price
        estimate_gas = self.w3.eth.estimate_gas({'to': receiver, 'from': owner, 'value': amount})

        tx = {
            'nonce': nonce,
            'to': receiver,
            'value': amount,
            'gas': estimate_gas,
            'gasPrice': gas_price,
        }

        signed_tx = self.w3.eth.account.sign_transaction(tx, owner_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.to_hex(tx_hash)

    def transfer_token(self, token_address, owner_address, owner_private_key, receiver_address, amount):
        owner = self.w3.to_checksum_address(owner_address)
        receiver = self.w3.to_checksum_address(receiver_address)

        balance = self.balance_of(token_address, owner)
        if amount > balance:
            return "Amount exceeds balance"

        amount = self.w3.to_wei(amount, 'ether')

        transfer = self.get_contract_instance(token_address).functions.transfer(receiver, amount)
        estimate_gas = transfer.estimate_gas({'from': owner})
        nonce = self.w3.eth.get_transaction_count(owner)
        gas_price = self.w3.eth.gas_price

        tx = {
            'nonce': nonce,
            'to': token_address,
            'data': transfer.build_transaction({'gas': estimate_gas, 'gasPrice': gas_price, 'nonce': nonce})['data'],
            'gas': estimate_gas,
            'gasPrice': gas_price,
        }

        signed_tx = self.w3.eth.account.sign_transaction(tx, owner_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.to_hex(tx_hash)

    def approve(self, token_address, owner_address, owner_private_key, spender_address, amount):
        owner = self.w3.to_checksum_address(owner_address)
        spender = self.w3.to_checksum_address(spender_address)
        amount = self.w3.to_wei(amount, 'ether')

        approve = self.get_contract_instance(token_address).functions.approve(spender, amount)
        estimate_gas = approve.estimate_gas({'from': owner})
        nonce = self.w3.eth.get_transaction_count(owner)
        gas_price = self.w3.eth.gas_price

        tx = {
            'nonce': nonce,
            'to': token_address,
            'data': approve.build_transaction({'gas': estimate_gas, 'gasPrice': gas_price, 'nonce': nonce})['data'],
            'gas': estimate_gas,
            'gasPrice': gas_price,
        }

        signed_tx = self.w3.eth.account.sign_transaction(tx, owner_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.to_hex(tx_hash)

    def increase_allowance(self, token_address, owner_address, owner_private_key, spender_address, amount):
        owner = self.w3.to_checksum_address(owner_address)
        spender = self.w3.to_checksum_address(spender_address)
        amount = self.w3.to_wei(amount, 'ether')

        current_allowance = self.allowance(token_address, owner, spender)
        new_allowance = amount + self.w3.to_wei(current_allowance, 'ether')

        approve = self.get_contract_instance(token_address).functions.approve(spender, new_allowance)
        estimate_gas = approve.estimate_gas({'from': owner})
        nonce = self.w3.eth.get_transaction_count(owner)
        gas_price = self.w3.eth.gas_price

        tx = {
            'nonce': nonce,
            'to': token_address,
            'data': approve.build_transaction({'gas': estimate_gas, 'gasPrice': gas_price, 'nonce': nonce})['data'],
            'gas': estimate_gas,
            'gasPrice': gas_price,
        }

        signed_tx = self.w3.eth.account.sign_transaction(tx, owner_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.to_hex(tx_hash)

    def decrease_allowance(self, token_address, owner_address, owner_private_key, spender_address, amount):
        owner = self.w3.to_checksum_address(owner_address)
        spender = self.w3.to_checksum_address(spender_address)
        amount = self.w3.to_wei(amount, 'ether')

        current_allowance = self.allowance(token_address, owner, spender)
        new_allowance = max(0, self.w3.to_wei(current_allowance, 'ether') - amount)

        approve = self.get_contract_instance(token_address).functions.approve(spender, new_allowance)
        estimate_gas = approve.estimate_gas({'from': owner})
        nonce = self.w3.eth.get_transaction_count(owner)
        gas_price = self.w3.eth.gas_price

        tx = {
            'nonce': nonce,
            'to': token_address,
            'data': approve.build_transaction({'gas': estimate_gas, 'gasPrice': gas_price, 'nonce': nonce})['data'],
            'gas': estimate_gas,
            'gasPrice': gas_price,
        }

        signed_tx = self.w3.eth.account.sign_transaction(tx, owner_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.to_hex(tx_hash)

    def transfer_from(self, token_address, owner_address, spender_address, spender_private_key, receiver_address, amount):
        owner = self.w3.to_checksum_address(owner_address)
        receiver = self.w3.to_checksum_address(receiver_address)
        spender = self.w3.to_checksum_address(spender_address)
        amount = self.w3.to_wei(amount, 'ether')

        transfer_from = self.get_contract_instance(token_address).functions.transferFrom(owner, receiver, amount)
        estimate_gas = transfer_from.estimate_gas({'from': spender})
        nonce = self.w3.eth.get_transaction_count(spender)
        gas_price = self.w3.eth.gas_price

        tx = {
            'nonce': nonce,
            'to': token_address,
            'data': transfer_from.build_transaction({'gas': estimate_gas, 'gasPrice': gas_price, 'nonce': nonce})['data'],
            'gas': estimate_gas,
            'gasPrice': gas_price,
        }

        signed_tx = self.w3.eth.account.sign_transaction(tx, spender_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return self.w3.to_hex(tx_hash)

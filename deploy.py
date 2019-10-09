import json
import web3
import sys

from web3.contract import ConciseContract
from solc import compile_files
from web3 import Web3
from binascii import hexlify


def error():
    print("args must need: 'contract name', must need args=[]")
    print("-----------------------------------------")
    print('Example: standard "Test Contract" TF 6')
    print("-----------------------------------------")
    exit(1)


if len(sys.argv) != 5:
    error()


file_name = "Experiment.sol"

if not file_name:
    error()

token_name = sys.argv[2]
token_symbol = sys.argv[3]
token_decimal = int(sys.argv[4])


file_path = "./src/" + file_name
# infura_provider = web3.HTTPProvider('https://kovan.infura.io')
infura_provider = web3.HTTPProvider('https://mainnet.infura.io')
web3_provider = web3.Web3(infura_provider)
print("provider is ok...")

PSK = "***"
GAS_PRICE = web3.Web3.toWei(20, 'gwei')

compiled_sol = compile_files([file_path])
contract_interface = compiled_sol["{}:Token".format(file_path)]

# Instantiate and deploy contract
stable_coin = web3_provider.eth.contract(
    abi=contract_interface['abi'],
    bytecode=contract_interface['bin'])

print("{} contract is ok...".format(file_name))


def main(init: int, name: str, symbol: str, decimal: int):
    from_address = web3.eth.Account.privateKeyToAccount(PSK)
    gas_limit = 3500000
    nonce = web3_provider.eth.getTransactionCount(
        web3.Web3.toChecksumAddress(from_address.address))

    unicorn_tx = stable_coin.constructor(
        init, name, symbol, decimal
    ).buildTransaction({
        'gasPrice': GAS_PRICE,
        'gas': gas_limit,
        'nonce': nonce,
    })

    signed_tx = web3_provider.eth.account.signTransaction(
        unicorn_tx, private_key=PSK)

    print("start send to provider...")

    tx_bytes = web3_provider.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_hash = hexlify(tx_bytes).decode()
    print('Transfer: send transaction ok: {}'.format(tx_hash))


if __name__ == "__main__":
    main(10000000 * 10 ** token_decimal, token_name, token_symbol, token_decimal)

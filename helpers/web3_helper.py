from web3 import Web3
from helpers.abi_helper import ERC20_ABI

# create a Binance web3 object
def create_web3() -> Web3:
	# create w3 object for Binance Smart Chain
	BSC = 'https://bsc-dataseed.binance.org/'
	w3 = Web3(Web3.HTTPProvider(BSC))
	
	return w3



# grab latest block number from Binance chain
def get_latest(w3: Web3) -> int:
	return w3.eth.get_block_number()



# return bnb balance of given addr
def get_bnb_balance(addr: str, w3: Web3) -> int:
	return Web3.fromWei(w3.eth.get_balance(addr), 'ether')



# return balance of given token @ given addr
def get_token_balance(wallet_addr: str, token_addr: str, w3: Web3) -> int:
	# create contract obj that can interact w/ token's smart contract
	token_contract = w3.eth.contract(address=token_addr, abi=ERC20_ABI)

	# get token balance
	balance = token_contract.functions.balanceOf(wallet_addr).call()

	return balance
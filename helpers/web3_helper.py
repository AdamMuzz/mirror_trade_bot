from web3 import Web3

# wrapper to create a Binance web3 object
def create_web3() -> Web3:

	BSC = 'https://bsc-dataseed.binance.org/'
	w3 = Web3(Web3.HTTPProvider(BSC))
	
	return w3



# simple wrapper to grab latest block number from Binance chain
def get_latest(w3: Web3) -> int:

	return w3.eth.get_block_number()
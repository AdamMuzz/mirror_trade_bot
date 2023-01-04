from web3 import Web3

#simple wrapper to grab latest block number from Binance chain
def get_latest(w3: Web3) -> int:
	return w3.eth.get_block_number()
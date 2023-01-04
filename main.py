from web3 import Web3
from web3.middleware import geth_poa_middleware

from helpers.web3_helper import get_latest



if __name__ == '__main__':
	#create w3 obj for Binance chain
	w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org:443'))
	w3.middleware_onion.inject(geth_poa_middleware, layer=0)

	print(get_latest(w3))


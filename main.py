from helpers.web3_helper import create_web3, get_latest
from helpers.pancake_helper import create_pancake


if __name__ == '__main__':

	# create w3 obj for Binance chain
	try:
		w3 = create_web3()
		print(f'connected to binance chain: {w3.isConnected()}')
	except:
		print('unable to connect to binance chain')

	# create pancake router contract obj
	try:
		pan_contract = create_pancake(w3)
	except:
		print('unable to create pancake router contract')

	# grab current positions from self's wallet


	print(get_latest(w3))


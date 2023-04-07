from web3 import Web3
from requests import get
import time

from config import TARGET_ADDR

# processes new pending txn events emitted to grab txn details
#	returns 2, token_addr, [path] 	if target addr buying
#	returns 1, token_addr, [path] 	if selling
#	returns 0, None, None			if not target addr
def fetch_event_details(event, w3: Web3, router):
	try:
		hash = w3.toHex(event)					# get txn hash
		details = w3.eth.get_transaction(hash) 	# get txn via its hash
	except:
		return (0, None, None)

	# if txn from target addr
	if details['from'] == TARGET_ADDR:
		# decode function data
		print("target")
		try:
			input = router.decode_function_input(details['input'])
			func = str(input[0])
			path = input[1]['path']

			# if buying
			if "swapExactETH" in func:
				return (2, path[-1], path)
			# if selling
			elif "swapExactTokens" in func:
				return (1, path[0], path)
		except:
			pass # was not a pancake router function

	return (0, None, None)
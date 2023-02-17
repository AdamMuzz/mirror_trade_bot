from web3 import Web3
from requests import get
from helpers.web3_helper import get_latest
from config import BSCSCAN_API_KEY, TARGET_ADDR

# scans current block for trade activity from target address
def scan_for_trades(w3: Web3) -> list[dict]:
	response = []

	# get latest block num
	start = get_latest(w3) - 5

	# check for any trades on current block
	url = 'https://api.bscscan.com/api'\
	'?module=account'\
	'&action=tokentx'\
	f'&address={TARGET_ADDR}'\
	'&page=1'\
	'&offset=5'\
	f'&startblock={start}'\
	'&endblock=999999999'\
	'&sort=asc'\
	f'&apikey={BSCSCAN_API_KEY}'\

	# parse json response
	try:
		response = get(url).json()['result']
	except:
		print("failed to fetch trades")

	return response
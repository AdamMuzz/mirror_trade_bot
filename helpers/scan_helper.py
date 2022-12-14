from web3 import Web3
from requests import get
from web3_helper import get_latest
from config import BscScan_api_key, target_addr

def scan_for_trades(w3: Web3) -> list(int):
	#get latest block num
	start = get_latest(w3)

	#check for any trades on current block
	url = 'https://api.bscscan.com/api'\
   '?module=account'\
   '&action=tokentx'\
   f'&address={target_addr}'\
   '&page=1'\
   '&offset=5'\
   f'&startblock={start}'\
   '&endblock=999999999'\
   '&sort=asc'\
   f'&apikey={BscScan_api_key}'\

	response = get(url).json()

	return True
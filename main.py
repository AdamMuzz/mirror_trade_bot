import time
from datetime import datetime as dt

from helpers.web3_helper import create_web3, get_bnb_balance, get_token_balance
from helpers.scan_helper import fetch_event_details
from helpers.pancake_helper import create_pancake, buy_token, confirm_token, sell_token
from config import USER_ADDR, AMOUNTS

def get_time():
	return dt.now().strftime("%m/%d %H:%M:%S")



# handles txn events
def handle_event(event):
	res, token_addr, path = fetch_event_details(event, w3, pan_router)		# grab details

	# if txn not from target wallet do nothing
	if res == 0:
		return

	balance = get_token_balance(USER_ADDR, token_addr, w3)				# get current token balance

	# if buying
	if res == 2:
		if get_bnb_balance(USER_ADDR, w3) < 0.2:							# maintain some BNB reserves
			return
	
		# if target is buying and self has not bought
		if balance == 0:
			print(f"{get_time()}  BUY: {token_addr}")
			# try and buy HIGH --> MID --> LOW beans of token
			for i in range(3):
				amount = AMOUNTS[i]
					
				buy_hash = buy_token(amount, path, w3, pan_router)
				status = w3.eth.wait_for_transaction_receipt(buy_hash)['status']	# wait for txn to get processed, 1 is success, 0 is failure
				if status:
					print(f"    buy confirmation: {buy_hash}")
					confirm_hash = confirm_token(path[-1], w3)						# if successful, confirm token then break out
					print(f"    confirm confirmation: {confirm_hash}")
					break
				else:
					print(f"    failed to buy @ {amount}")							# else, lower buy amount & try again
		# if target is buying and self alr owns
		elif balance > 0:
			print(f"{get_time()}  DOUBLE DOWN: {token_addr}")

			# try and buy LOW beans
			amount = AMOUNTS[-1]
					
			buy_hash = buy_token(amount, path, w3, pan_router)
			status = w3.eth.wait_for_transaction_receipt(buy_hash)['status']
			if status:
				print(f"    buy confirmation: {buy_hash}")							# no need to confirm b/c alr done via initial buy
			else:
				print(f"    failed to double down")
	# if selling
	elif res == 1 and balance > 0:
		print(f"{get_time()}  SELL: {token_addr}")
		sell_hash = sell_token(balance, path, w3, pan_router)

		status = w3.eth.wait_for_transaction_receipt(sell_hash)['status']
		if status:
			print(f"    sell confirmation: {sell_hash}")
		else:
			print(f"    failed to sell")



# repeatedly poll for new txns
#	for each new event, call handle_event() on it
def event_loop(event_filter, poll_interval):
	while True:
		for event in event_filter.get_new_entries():
			handle_event(event)
		time.sleep(poll_interval)



# set poll filter to be pending txns
# set poll interval to be 0.4s
def main():
	block_filter = w3.eth.filter('pending')
	event_loop(block_filter, 1)



if __name__ == '__main__':
	# create w3 obj for Binance chain, PancakeSwap router, PancakeSwap factory
	try:
		w3 = create_web3()
		pan_router, pan_factory = create_pancake(w3)
		print(f'connected to binance chain: {w3.isConnected()}')
	except:
		print('unable to connect to setup chain and pancakeswap')
		exit()

	# run main logic for bot
	main()
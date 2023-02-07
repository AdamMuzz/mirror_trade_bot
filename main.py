from helpers.web3_helper import create_web3, get_token_balance
from helpers.pancake_helper import create_pancake, buy_token, sell_token, confirm_token
from helpers.scan_helper import scan_for_trades
from config import USER_ADDR, TARGET_ADDR, AMOUNTS
from time import sleep
from datetime import datetime as dt

# helper function to format date info for logging trade activity
def get_time():
	return dt.now().strftime("%m/%d %H:%M:%S")



if __name__ == '__main__':
	#########
	# setup #
	#########

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



	################
	# driver logic #
	################

	prev_hash = None
	cur_hash = None

	# bot runs 24/7
	while True:
		# update prev to be current from last run
		prev_hash = cur_hash
	
		# grab most recent trade from trades from most recent block
		trades = scan_for_trades(w3)
		trade = trades[0] if trades else False

		# if a new trade is present
		if trade and trade['hash'] != prev_hash:
			# update current hash to this trade
			cur_hash = trade['hash']

			token_addr = w3.toChecksumAddress(trade['contractAddress'])		# grab token addr
			balance = get_token_balance(w3, token_addr, USER_ADDR)			# grab cur balance
			destination = w3.toChecksumAddress(trade['to'])					# grab destination (if to == target --> they are receiving tokens --> buy)

			# if TARGET is buying & self has not bought
			if destination == TARGET_ADDR and balance == 0:
				print(f"{get_time()} buying {trade['tokenSymbol']}")

				# try and buy 0.15 --> 0.10 --> 0.05 beans of token
				for i in range(3):
					amount = AMOUNTS[i]
					
					buy_hash = buy_token(token_addr, amount, w3, pan_contract)
					# wait for txn to get processed, 1 is success, 0 is failure
					status = w3.eth.wait_for_transaction_receipt(buy_hash)['status']
					if status:
						print(f"{get_time()} buy confirmation: {buy_hash}")				# if successful, confirm token then break out
						confirm_hash = confirm_token(token_addr, w3)
						print(f"{get_time()} confirm confirmation: {confirm_hash}")
						break
					else:
						print(f"{get_time()} failed to buy @ {amount}")					# else, lower buy amount & try again
			# if TARGET is buying and self has bought
				#########
				# TO DO #
				#########
			# if TARGET is selling & self owns
			elif destination != TARGET_ADDR and balance > 0:
				print(f"{get_time()} selling {trade['tokenSymbol']}")
				sell_hash = sell_token(token_addr, w3, pan_contract)
				print(f"{get_time()} sell confirmation: {sell_hash}")
	
		# wait 1.25s so dont hit API limit
		sleep(1.25)

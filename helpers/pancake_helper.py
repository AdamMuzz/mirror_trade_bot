from config import PAN_ADDR, WBNB_ADDR, USER_ADDR, PRIV_KEY, MAX_NUMBER, GAS_BUFFER, GAS_PRICE
from helpers.abi_helper import PAN_ROUTER_ABI, ERC20_ABI
from web3 import Web3
import time

# simple method to create a pancake router v2 contract obj
def create_pancake(w3: Web3):
	# create contract w/ pancake router v2 methods
	return w3.eth.contract(address=PAN_ADDR, abi=PAN_ROUTER_ABI)



# buys AMOUNT of specified token TKN_ADDR
def buy_token(tkn_addr: str, amount: float, w3: Web3, pan_contract) -> str:
	# define transaction
	buy_txn = pan_contract.functions.swapExactETHForTokens(
		0,													# slippage (0 == inf)
		[WBNB_ADDR,tkn_addr],								# trade from BNB --> token
		USER_ADDR,											# wallet to send tokens to
		(int(time.time()) + 1000)							# deadline
	).buildTransaction({
		'from': USER_ADDR,									# wallet to fund trade
		'value': w3.toWei(amount, 'ether'),					# amount to buy
		'gas': 0,											# gas limit
		'gasPrice': w3.toWei(GAS_PRICE,'gwei'),				# gas price
		'nonce': w3.eth.get_transaction_count(USER_ADDR)	# metamask nonce
	})

	# get estimated gas cost
	EST_GAS = w3.eth.estimate_gas(buy_txn) + GAS_BUFFER
	buy_txn.update({'gas': EST_GAS})

	# sign and send transaction
	signed_txn = w3.eth.account.sign_transaction(buy_txn, private_key=PRIV_KEY)
	txn_hash = w3.toHex(w3.eth.send_raw_transaction(signed_txn.rawTransaction))

	return txn_hash



# confirms the token @ TKN_ADDR s.t. pancake swap may sell it
def confirm_token(tkn_addr: str, w3: Web3) -> str:
	# if token alr confirmed --> return true
	txn_hash = True

	# define token contract
	token_contract = w3.eth.contract(address=tkn_addr, abi=ERC20_ABI)

	# check if needs approval
	if token_contract.functions.allowance(USER_ADDR, PAN_ADDR).call() == 0:

		# build approve transaction
		approve_txn = token_contract.functions.approve(PAN_ADDR, MAX_NUMBER).buildTransaction({
			'from': USER_ADDR,
			'gasPrice': w3.toWei(GAS_PRICE, 'gwei'),
			'nonce': w3.eth.get_transaction_count(USER_ADDR)
		})

		# sign and send
		signed_txn = w3.eth.account.sign_transaction(approve_txn, private_key=PRIV_KEY)
		txn_hash = w3.toHex(w3.eth.send_raw_transaction(signed_txn.rawTransaction))

	return txn_hash



# sells all tokens @ TKN_ADDR
def sell_token(tkn_addr, w3: Web3, pan_contract) -> str:
	# get amount owned
	tkn_contract = w3.eth.contract(address=tkn_addr, abi=ERC20_ABI)
	amount = tkn_contract.functions.balanceOf(USER_ADDR).call()

	# define transaction
	sell_txn = pan_contract.functions.swapExactTokensForETH(
		amount,												# amount of token to sell
		0,													# slippage (0 == inf)
		[tkn_addr, WBNB_ADDR],								# trade from token --> BNB
		USER_ADDR,											# wallet to send BNB to
		(int(time.time()) + 1000)							# deadline
	).buildTransaction({
		'from': USER_ADDR,									# contract sending addr
		'gas': 0,											# gas limit
		'gasPrice': w3.toWei(GAS_PRICE, 'gwei'),			# gas price
		'nonce': w3.eth.get_transaction_count(USER_ADDR)	# MetaMask nonce
	})

	# get estimated gas cost
	EST_GAS = w3.eth.estimate_gas(sell_txn) + GAS_BUFFER
	sell_txn.update({'gas': EST_GAS})

	# sign and send
	signed_txn = w3.eth.account.sign_transaction(sell_txn, private_key=PRIV_KEY)
	txn_hash = w3.toHex(w3.eth.send_raw_transaction(signed_txn.rawTransaction))

	return txn_hash
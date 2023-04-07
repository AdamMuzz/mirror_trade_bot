USER_ADDR = 'INSERT'						# addr of wallet to use for executing trades
TARGET_ADDR = 'INSERT'						# addr of wallet to track

PRIV_KEY = 'INSERT'	# private metamask wallet key

PAN_ROUTER_ADDR = '0x10ED43C718714eb63d5aA57B78B54704E256024E'					# pancakeswap V2 router contract addr
PAN_FACTORY_ADDR = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'					# pancakeswap V2 factory contract addr

WBNB_ADDR = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'						# wrapped BNB contract addr

AMOUNTS = (0.15, 0.10, 0.05)													# custom set of amounts to attempt to purchase at

GAS_BUFFER = 100000
GAS_PRICE = '6'
GAS_LIMIT = 500000

MAX_NUMBER = (2**64 - 1) * 10**18												# 2^64 eth	...not gonna ever buy this much of something
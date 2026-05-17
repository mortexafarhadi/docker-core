# from typing import Optional, Tuple
#
# from _0_utils.base_variables import (
#     DOGE_WALLET_PK,
#     BITCOIN_WALLET_PK,
#     LITECOIN_WALLET_PK,
#     SOLANA_WALLET_PK,
#     BITCOIN_WALLET_ADDRESS,
#     DOGE_WALLET_ADDRESS,
#     LITECOIN_WALLET_ADDRESS,
# )
# from .utils.BLOCK_CYPHER_SERVICE import (
#     send_doge_block_cypher_coin,
#     get_btc_balance_by_address,
#     get_doge_balance_by_address,
#     get_ltc_balance_by_address,
#     send_utxo_via_blockcypher,
# )
# from .utils.CHECK_ADDRESS import check_address_validation
# from .utils.SMART_CONTRACT import get_contract_balance, send_payment
# from .utils.SOL import SolanaWalletManager
# from .utils.TRX import TronWalletManager
# from .utils.USDT_TO_CRYPTO import usdt_to_crypto, crypto_to_usdt
#
#
# def send_btc(to_address: str, amount_usdt) -> Tuple[bool, Optional[str]]:
#     """
#     ارسال BTC از آدرسی که با BIP84 (bc1...) یا هر نوع دیگری موجودی دارد.
#     نیازمند:
#     - BITCOIN_WALLET_PK (WIF)
#     - BITCOIN_WALLET_ADDRESS (آدرسی که واقعاً UTXO دارد)
#     - usdt_to_crypto(amount_usdt, 'btc') در پروژه شما
#     - check_address_validation(to_address, 'btc') در پروژه شما
#     """
#     if not BITCOIN_WALLET_PK:
#         print("BITCOIN_WALLET_PK not set in .env")
#         return False, None
#     if not BITCOIN_WALLET_ADDRESS:
#         print("BITCOIN_WALLET_ADDRESS not set in .env")
#         return False, None
#
#     _network = "btc"  # اگر تست‌نت: 'btc-testnet'
#     _amount_btc = usdt_to_crypto(amount_usdt, _network)
#     print(f"{_network} amount is {_amount_btc}")
#
#     if not check_address_validation(to_address, _network):
#         print("Address Non Valid")
#         return False, None
#
#     ok, tx_hash, detail = send_utxo_via_blockcypher(
#         from_wif=BITCOIN_WALLET_PK,
#         from_address=BITCOIN_WALLET_ADDRESS,
#         to_address=to_address,
#         amount_str=_amount_btc,
#         coin_symbol=_network,
#     )
#     if not ok:
#         print(f"[BTC] Error: {detail}")
#         return False, None
#     return True, tx_hash
#
#
# def send_ltc(to_address: str, amount_usdt) -> Tuple[bool, Optional[str]]:
#     """
#     ارسال LTC از آدرس BIP84 (ltc1...) یا سایر انواع.
#     نیازمند:
#     - LITECOIN_WALLET_PK (WIF)
#     - LITECOIN_WALLET_ADDRESS (آدرسی که واقعاً UTXO دارد)
#     - usdt_to_crypto(amount_usdt, 'ltc') در پروژه شما
#     - check_address_validation(to_address, 'ltc') در پروژه شما
#     """
#     if not LITECOIN_WALLET_PK:
#         print("LITECOIN_WALLET_PK not set in .env")
#         return False, None
#     if not LITECOIN_WALLET_ADDRESS:
#         print("LITECOIN_WALLET_ADDRESS not set in .env")
#         return False, None
#
#     _network = "ltc"  # if user testnet: 'ltc-testnet'
#     _amount = usdt_to_crypto(amount_usdt, _network)
#     print(f"{_network} amount is {_amount}")
#
#     if not check_address_validation(to_address, _network):
#         print("Address Non Valid")
#         return False, None
#
#     ok, tx_hash, detail = send_utxo_via_blockcypher(
#         from_wif=LITECOIN_WALLET_PK,
#         from_address=LITECOIN_WALLET_ADDRESS,
#         to_address=to_address,
#         amount_str=_amount,
#         coin_symbol=_network,
#     )
#     if not ok:
#         print(f"[LTC] Error: {detail}")
#         return False, None
#     return True, tx_hash
#
#
# def send_doge(to_address, amount_usdt):
#     _DOGE_WALLET_PK = DOGE_WALLET_PK
#     if _DOGE_WALLET_PK is None:
#         print("DOGE_WALLET_PK dont set in .env")
#         return False, None
#
#     _network = "doge"
#     _amount = usdt_to_crypto(amount_usdt, _network)
#     print(f"{_network} amount is {_amount}")
#     _address_status = check_address_validation(to_address, _network)
#     if not _address_status:
#         print("Address Non Valid")
#         return False, None
#     try:
#         tx_hash = send_doge_block_cypher_coin(
#             _DOGE_WALLET_PK, to_address, _amount, _network
#         )
#         if tx_hash is None:
#             print("Dogecoin Payment Service Error")
#             return False, None
#         return True, tx_hash
#     except Exception as e:
#         print(f"[DOGE] Error: {e}")
#         return False, None
#
#
# def send_trx(
#     to_address: str,
#     amount_usdt: float,
#     memo: Optional[str] = None,
#     wait: bool = True,
# ):
#     manager = TronWalletManager(network="mainnet")
#
#     _network = "trx"
#     _amount = usdt_to_crypto(amount_usdt, _network)
#     print(f"{_network} amount is {_amount}")
#     _address_status = check_address_validation(to_address, _network)
#     if not _address_status:
#         print("Address Non Valid")
#         return False, None
#     result = manager.send_trx(to_address, _amount, memo, wait)
#     if result is None:
#         print("Tron Payment Service Error")
#         return False, None
#     if not result.get("confirmed"):
#         print("Tron Payment Service Wrong")
#         return False, result.get("txid")
#     return True, result.get("txid")
#
#
# def send_sol(to_address, amount_usdt, memo=None):
#     sol = SolanaWalletManager(SOLANA_WALLET_PK)
#
#     _network = "sol"
#     _amount = usdt_to_crypto(amount_usdt, _network)
#     print(f"{_network} amount is {_amount}")
#     _address_status = check_address_validation(to_address, _network)
#     if not _address_status:
#         print("Address Non Valid")
#         return False, None
#     result = sol.send_sol(to_address, _amount, memo=memo)
#     if result is None:
#         print("Solana Payment Service Error")
#         return False, None
#     if not result.get("confirmed"):
#         print("Solana Payment Service Wrong")
#         return False, result.get("signature")
#     return True, result.get("signature")
#
#
# def send_eth(to_address, amount_usdt):
#     try:
#         _network = "eth"
#         _amount = usdt_to_crypto(amount_usdt, _network)
#         print(f"{_network} amount is {_amount}")
#         _address_status = check_address_validation(to_address, _network)
#         if not _address_status:
#             print("Address Non Valid")
#             return False, None
#         return send_payment(chain=_network, to=to_address, amount=_amount)
#     except Exception as e:
#         print(f"Ethereum Payment Service Error :{e}")
#         return False, None
#
#
# def send_avax(to_address, amount_usdt):
#     try:
#         _network = "avax"
#         _amount = usdt_to_crypto(amount_usdt, _network)
#         print(f"{_network} amount is {_amount}")
#         _address_status = check_address_validation(to_address, _network)
#         if not _address_status:
#             print("Address Non Valid")
#             return False, None
#         return send_payment(chain=_network, to=to_address, amount=_amount)
#     except Exception as e:
#         print(f"Avalanche Payment Service Error :{e}")
#         return False, None
#
#
# def send_pol(to_address, amount_usdt):
#     try:
#         _network = "pol"
#         _amount = usdt_to_crypto(amount_usdt, _network)
#         print(f"{_network} amount is {_amount}")
#         _address_status = check_address_validation(to_address, _network)
#         if not _address_status:
#             print("Address Non Valid")
#             return False, None
#         return send_payment(chain=_network, to=to_address, amount=_amount)
#     except Exception as e:
#         print(f"Polygon Payment Service Error :{e}")
#         return False, None
#
#
# def get_doge_balance():
#     if not DOGE_WALLET_ADDRESS:
#         print("DOGE_WALLET_ADDRESS not set in .env")
#         return False, None
#     balance_coin = get_doge_balance_by_address(DOGE_WALLET_ADDRESS).get("final")
#     balance_usdt = crypto_to_usdt(balance_coin, "doge")
#     return balance_coin, balance_usdt
#
#
# def get_ltc_balance():
#     if not LITECOIN_WALLET_ADDRESS:
#         print("LITECOIN_WALLET_ADDRESS not set in .env")
#         return False, None
#     balance_coin = get_ltc_balance_by_address(LITECOIN_WALLET_ADDRESS).get("final")
#     balance_usdt = crypto_to_usdt(balance_coin, "ltc")
#     return balance_coin, balance_usdt
#
#
# def get_sol_balance():
#     sol = SolanaWalletManager(SOLANA_WALLET_PK)
#     balance_coin = sol.get_balance().get("balance_sol")
#     balance_usdt = crypto_to_usdt(balance_coin, "sol")
#     return balance_coin, balance_usdt
#
#
# def get_trx_balance():
#     manager = TronWalletManager(network="mainnet")
#     balance_coin = manager.get_balance()
#     balance_usdt = crypto_to_usdt(balance_coin, "trx")
#     return balance_coin, balance_usdt
#
#
# def get_btc_balance():
#     if not BITCOIN_WALLET_ADDRESS:
#         print("BITCOIN_WALLET_ADDRESS not set in .env")
#         return False, None
#     balance_coin = get_btc_balance_by_address(BITCOIN_WALLET_ADDRESS).get("final")
#     balance_usdt = crypto_to_usdt(balance_coin, "btc")
#     return balance_coin, balance_usdt
#
#
# def get_eth_balance():
#     balance_coin = get_contract_balance("eth")
#     print(balance_coin)
#     balance_usdt = crypto_to_usdt(balance_coin, "eth")
#     print(balance_usdt)
#     return balance_coin, balance_usdt
#
#
# def get_pol_balance():
#     balance_coin = get_contract_balance("pol")
#     balance_usdt = crypto_to_usdt(balance_coin, "pol")
#     return balance_coin, balance_usdt
#
#
# def get_avax_balance():
#     balance_coin = get_contract_balance("avax")
#     balance_usdt = crypto_to_usdt(balance_coin, "avax")
#     return balance_coin, balance_usdt
#
#
# # def send_dash(to_address, amount_usdt):
# #     _DASH_WALLET_PK = DASH_WALLET_PK
# #     if _DASH_WALLET_PK is None:
# #         print(f'DASH_WALLET_PK dont set in .env')
# #         return False, None
# #
# #     _network = 'dash'
# #     _amount = usdt_to_crypto(amount_usdt, _network)
# #     print(f"{_network} amount is {_amount}")
# #     _address_status = check_address_validation(to_address, _network)
# #     if not _address_status:
# #         print('Address Non Valid')
# #         return False, None
# #     tx_hash = send_block_cypher_coin(_DASH_WALLET_PK, to_address, _amount, _network)
# #     if tx_hash is None:
# #         print(f'Dash Payment Service Error')
# #         return False, None
# #     return True, tx_hash
#
# # def send_bnb(to_address, amount_usdt):
# #     try:
# #         _network = 'bnb'
# #         _amount = usdt_to_crypto(amount_usdt, _network)
# #         print(f"{_network} amount is {_amount}")
# #         _address_status = check_address_validation(to_address, _network)
# #         if not _address_status:
# #             print('Address Non Valid')
# #             return False, None
# #         return send_payment(chain=_network, to=to_address, amount=_amount)
# #         return True, tx_hash
# #     except Exception as e:
# #         print(f'Binance Smart Chain Payment Service Error :{e}')
# #         return False, None
#
# # def send_arb(to_address, amount_usdt):
# #     try:
# #         _network = 'arb'
# #         _amount = usdt_to_crypto(amount_usdt, _network)
# #         print(f"{_network} amount is {_amount}")
# #         _address_status = check_address_validation(to_address, _network)
# #         if not _address_status:
# #             print('Address Non Valid')
# #             return False, None
# #         return send_payment(chain=_network, to=to_address, amount=_amount)
# #         return True, tx_hash
# #     except Exception as e:
# #         print(f'Arbitrum Payment Service Error :{e}')
# #         return False, None
#
# # def get_dash_balance():
# #     if not DASH_WALLET_ADDRESS:
# #         print('DASH_WALLET_ADDRESS not set in .env')
# #         return False, None
# #     balance_coin = get_dash_balance_by_address(DASH_WALLET_ADDRESS).get('final')
# #     balance_usdt = crypto_to_usdt(balance_coin, 'dash')
# #     return balance_coin, balance_usdt
#
# # def get_bnb_balance():
# #     balance_coin = get_contract_balance('bnb')
# #     balance_usdt = crypto_to_usdt(balance_coin, 'bnb')
# #     return balance_coin, balance_usdt
#
# # def get_arb_balance():
# #     balance_coin = get_contract_balance('arb')
# #     balance_usdt = crypto_to_usdt(balance_coin, 'arb')
# #     return balance_coin, balance_usdt

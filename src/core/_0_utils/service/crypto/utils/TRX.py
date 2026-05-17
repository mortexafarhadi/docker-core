# from typing import Optional, Dict, Any
#
# from tronpy import Tron
# from tronpy.keys import PrivateKey
# from tronpy.providers import HTTPProvider
#
# from _0_utils.base_variables import TRON_API_TRONGRID, TRX_WALLET_PK
#
# # TRX -> SUN (1 TRX = 1_000_000 sun)
# SUN = 1_000_000
#
#
# class TronWalletManager:
#     """Manage Tron Wallet for Transfers and Balance Checking"""
#
#     def __init__(self, network: str = "mainnet"):
#         """
#         Args:
#         network: 'mainnet' or 'nile' (testnet)
#         """
#         self.network = network
#         provider = HTTPProvider(api_key=TRON_API_TRONGRID)
#         self.client = Tron(network=network, provider=provider)
#
#         # Set private key
#         pk_hex = TRX_WALLET_PK[2:] if TRX_WALLET_PK.startswith("0x") else TRX_WALLET_PK
#         self.private_key = PrivateKey(bytes.fromhex(pk_hex))
#         self.address = self.private_key.public_key.to_base58check_address()
#
#     def get_balance(self, address: Optional[str] = None, in_trx: bool = True) -> float:
#         """
#         Get wallet balance
#
#         Args:
#         address: Wallet address (if None, the wallet's own address is used)
#         in_trx: If True, returns balance in TRX, otherwise in SUN
#
#         Returns:
#         Balance as float
#         """
#         try:
#             target_address = address or self.address
#             account = self.client.get_account(target_address)
#             balance_sun = account.get("balance", 0)
#
#             if in_trx:
#                 return balance_sun / SUN
#             return float(balance_sun)
#
#         except Exception as e:
#             print(f"Error in receiving balance: {e}")
#             raise
#
#     def get_account_info(self, address: Optional[str] = None) -> Dict[str, Any]:
#         """
#         Get full account information
#
#         Args:
#         address: Wallet address
#
#         Returns:
#         Dictionary containing account information
#         """
#         try:
#             target_address = address or self.address
#             account = self.client.get_account(target_address)
#
#             return {
#                 "address": target_address,
#                 "balance_trx": account.get("balance", 0) / SUN,
#                 "balance_sun": account.get("balance", 0),
#                 "bandwidth": account.get("free_net_usage", 0),
#                 "energy": account.get("account_resource", {}).get("energy_usage", 0),
#                 "create_time": account.get("create_time", None),
#             }
#
#         except Exception as e:
#             print(f"Error retrieving account information: {e}")
#             raise
#
#     def check_sufficient_balance(
#         self, amount_trx: float, fee_margin: float = 0.1
#     ) -> bool:
#         """
#         Check if there is enough balance for transfer
#
#         Args:
#         amount_trx: Amount of TRX to transfer
#         fee_margin: Margin for fee (default 0.1 TRX)
#
#         Returns:
#         True if there is enough balance
#         """
#         try:
#             current_balance = self.get_balance()
#             required_amount = amount_trx + fee_margin
#             return current_balance >= required_amount
#
#         except Exception as e:
#             print(f"Error in check Balance: {e}")
#             return False
#
#     def send_trx(
#         self,
#         to_address: str,
#         amount_trx: float,
#         memo: Optional[str] = None,
#         wait: bool = True,
#         check_balance: bool = True,
#     ) -> Dict[str, Any]:
#         """
#         Send TRX to destination address
#
#         Args:
#         to_address: Destination address (e.g. 'T...')
#         amount_trx: Amount of TRX (e.g. 1.5)
#         memo: Optional transaction text
#         wait: If True, waits for confirmation in the block
#         check_balance: If True, checks the balance first
#
#         Returns:
#         Result dictionary or Exception on error
#         """
#         # Check Balance
#         if check_balance:
#             if not self.check_sufficient_balance(amount_trx):
#                 current_balance = self.get_balance()
#                 raise ValueError(
#                     f"Insufficient inventory! Current inventory: {current_balance:.6f} TRX، "
#                     f"Required quantity:{amount_trx:.6f} TRX"
#                 )
#
#         # Convert to SUN
#         amount_sun = int(amount_trx * SUN)
#
#         try:
#             # Create transaction
#             builder = self.client.trx.transfer(self.address, to_address, amount_sun)
#
#             if memo:
#                 builder = builder.memo(memo)
#
#             # Sign and Send
#             txn = builder.build().sign(self.private_key)
#             txid = txn.txid
#             ret = txn.broadcast()
#
#             result = {
#                 "success": True,
#                 "txid": txid,
#                 "from_address": self.address,
#                 "to_address": to_address,
#                 "amount_trx": amount_trx,
#                 "amount_sun": amount_sun,
#                 "broadcast_result": ret,
#             }
#
#             if wait:
#                 receipt = ret.wait(timeout=60)
#                 result["receipt"] = receipt
#                 result["confirmed"] = True
#
#             return result
#
#         except Exception as e:
#             print(f"Error sending TRX:{e}")
#             raise
#
#     def get_transaction_info(self, txid: str) -> Dict[str, Any]:
#         try:
#             tx_info = self.client.get_transaction_info(txid)
#             return tx_info
#         except Exception as e:
#             print(f"Error receiving transaction information:{e}")
#             raise

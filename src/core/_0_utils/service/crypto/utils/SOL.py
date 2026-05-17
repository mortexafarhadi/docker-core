# from solana.rpc.api import Client
# from solders.keypair import Keypair
# from solders.pubkey import Pubkey
# from solders.system_program import TransferParams, transfer
# from solders.message import Message
# from solders.transaction import VersionedTransaction
# from solders.instruction import Instruction
# from solders.signature import Signature
# import base58
# from decimal import Decimal
# from typing import Dict, Optional
# import logging
# import time
#
# logger = logging.getLogger(__name__)
#
#
# class SolanaWalletManager:
#     MAINNET = "https://api.mainnet-beta.solana.com"
#     DEVNET = "https://api.devnet.solana.com"
#     TESTNET = "https://api.testnet.solana.com"
#
#     LAMPORTS_PER_SOL = 1_000_000_000
#     MEMO_PROGRAM_ID = "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"
#
#     def __init__(self, private_key: str, network: str = MAINNET):
#         """
#         Args:
#             private_key: format base58 or Number list
#             network: Address Solana Network RPC
#         """
#         self.client = Client(network)
#         self.keypair = self._load_keypair(private_key)
#         self.network = network
#
#     def _load_keypair(self, private_key: str) -> Keypair:
#         try:
#             if isinstance(private_key, str) and len(private_key) > 50:
#                 decoded = base58.b58decode(private_key)
#                 return Keypair.from_bytes(decoded)
#             elif isinstance(private_key, (list, bytes)):
#                 return Keypair.from_bytes(bytes(private_key))
#             else:
#                 raise ValueError("Private key Format not valid")
#         except Exception as e:
#             logger.error(f"Error loading private key: {e}")
#             raise
#
#     def get_balance(self, address: Optional[str] = None) -> Dict:
#         """
#         Args:
#             address: Wallet address (if None, the current wallet is checked)
#
#         Returns:
#             Dict includes inventory to SOL and lamports
#         """
#         try:
#             if address:
#                 pubkey = Pubkey.from_string(address)
#             else:
#                 pubkey = self.keypair.pubkey()
#
#             response = self.client.get_balance(pubkey)
#             lamports = response.value
#             sol = lamports / self.LAMPORTS_PER_SOL
#
#             return {
#                 "success": True,
#                 "address": str(pubkey),
#                 "balance_sol": sol,
#                 "balance_lamports": lamports,
#             }
#         except Exception as e:
#             logger.error(f"Error in receiving inventory: {e}")
#             return {"success": False, "error": str(e)}
#
#     def send_sol(
#         self, to_address: str, amount_sol: float, memo: Optional[str] = None
#     ) -> Dict:
#         """
#         Send SOL to the destination address with optional memo
#
#         Args:
#             to_address: Destination address (Public Key)
#             amount_sol: SOL amount to send (as a decimal number)
#             memo: Optional memo tag (required for exchange deposits)
#
#         Returns:
#             Dict contains transaction information
#         """
#         try:
#             to_pubkey = Pubkey.from_string(to_address)
#             lamports = int(amount_sol * self.LAMPORTS_PER_SOL)
#
#             balance = self.get_balance()
#             if not balance["success"]:
#                 return balance
#
#             estimated_fee = 5000
#             if balance["balance_lamports"] < (lamports + estimated_fee):
#                 return {
#                     "success": False,
#                     "error": f'Insufficient balance. Balance: {balance["balance_sol"]} SOL, Required: {(lamports + estimated_fee) / self.LAMPORTS_PER_SOL} SOL',
#                 }
#
#             recent_blockhash_resp = self.client.get_latest_blockhash()
#             recent_blockhash = recent_blockhash_resp.value.blockhash
#
#             instructions = []
#
#             # Add memo instruction if provided
#             if memo:
#                 memo_instruction = self._create_memo_instruction(memo)
#                 instructions.append(memo_instruction)
#
#             # Add transfer instruction
#             transfer_instruction = transfer(
#                 TransferParams(
#                     from_pubkey=self.keypair.pubkey(),
#                     to_pubkey=to_pubkey,
#                     lamports=lamports,
#                 )
#             )
#             instructions.append(transfer_instruction)
#
#             message = Message.new_with_blockhash(
#                 instructions, self.keypair.pubkey(), recent_blockhash
#             )
#
#             transaction = VersionedTransaction(message, [self.keypair])
#
#             response = self.client.send_transaction(transaction)
#             signature = response.value
#
#             # Wait for confirmation (reduced timeout since transaction is actually succeeding)
#             confirmed = self._wait_for_confirmation(signature, timeout=30)
#
#             # Even if confirmation times out, transaction might be successful
#             # Return success with warning
#             result = {
#                 "success": True,
#                 "signature": str(signature),
#                 "from_address": str(self.keypair.pubkey()),
#                 "to_address": to_address,
#                 "amount_sol": amount_sol,
#                 "amount_lamports": lamports,
#                 "memo": memo if memo else None,
#                 "explorer_url": self._get_explorer_url(str(signature)),
#             }
#
#             if confirmed:
#                 result["message"] = "Transaction confirmed successfully"
#                 result["confirmed"] = True
#             else:
#                 result["message"] = (
#                     "Transaction sent successfully (confirmation pending - check explorer)"
#                 )
#                 result["confirmed"] = False
#
#             return result
#
#         except Exception as e:
#             logger.error(f"Error in Submit SOL: {e}")
#             return {"success": False, "error": str(e)}
#
#     def _create_memo_instruction(self, memo: str) -> Instruction:
#         """
#         Create memo instruction for transaction
#
#         Args:
#             memo: Memo text (exchange tag or note)
#
#         Returns:
#             Instruction object
#         """
#         memo_program_id = Pubkey.from_string(self.MEMO_PROGRAM_ID)
#         memo_bytes = memo.encode("utf-8")
#
#         memo_instruction = Instruction(
#             program_id=memo_program_id, data=memo_bytes, accounts=[]
#         )
#
#         return memo_instruction
#
#     def _wait_for_confirmation(
#         self, signature, timeout: int = 30, check_interval: float = 1.0
#     ) -> bool:
#         """
#         Wait for transaction confirmation with timeout
#
#         Args:
#             signature: Transaction signature (Signature object)
#             timeout: Maximum wait time (seconds)
#             check_interval: Check interval (seconds)
#
#         Returns:
#             True if confirmed, False if timeout
#         """
#         start_time = time.time()
#
#         # Convert to Signature object if string
#         if isinstance(signature, str):
#             sig_obj = Signature.from_string(signature)
#         else:
#             sig_obj = signature
#
#         while time.time() - start_time < timeout:
#             try:
#                 response = self.client.get_signature_statuses([sig_obj])
#
#                 # Check if response has valid data
#                 if response and hasattr(response, "value") and response.value:
#                     status = response.value[0]
#
#                     if status is not None:
#                         # Check for errors
#                         if hasattr(status, "err") and status.err:
#                             logger.error(f"Transaction error: {status.err}")
#                             return False
#
#                         # Check confirmation status
#                         if (
#                             hasattr(status, "confirmation_status")
#                             and status.confirmation_status
#                         ):
#                             confirmation_level = str(status.confirmation_status).lower()
#
#                             if (
#                                 "confirmed" in confirmation_level
#                                 or "finalized" in confirmation_level
#                             ):
#                                 logger.info(
#                                     f"Transaction confirmed: {confirmation_level}"
#                                 )
#                                 return True
#
#                         # If no confirmation_status but status exists, might be confirmed
#                         elif hasattr(status, "confirmations") and status.confirmations:
#                             if status.confirmations > 0:
#                                 logger.info(
#                                     f"Transaction confirmed with {status.confirmations} confirmations"
#                                 )
#                                 return True
#
#                 time.sleep(check_interval)
#
#             except Exception as e:
#                 logger.debug(f"Check attempt error: {e}")
#                 time.sleep(check_interval)
#
#         logger.warning(
#             f"Timeout after {timeout}s - transaction may still be processing"
#         )
#         return False
#
#     def estimate_fee(self) -> Dict:
#         """
#         Transaction fee estimate
#
#         Returns:
#             Dict includes fees to SOL and lamports
#         """
#         try:
#             fee_lamports = 5000
#             fee_sol = fee_lamports / self.LAMPORTS_PER_SOL
#
#             return {
#                 "success": True,
#                 "fee_sol": fee_sol,
#                 "fee_lamports": fee_lamports,
#             }
#         except Exception as e:
#             return {"success": False, "error": str(e)}
#
#     def _get_explorer_url(self, signature: str) -> str:
#         """Create explorer link for transaction"""
#         if self.network == self.MAINNET:
#             return f"https://solscan.io/tx/{signature}"
#         elif self.network == self.DEVNET:
#             return f"https://solscan.io/tx/{signature}?cluster=devnet"
#         else:
#             return f"https://solscan.io/tx/{signature}?cluster=testnet"

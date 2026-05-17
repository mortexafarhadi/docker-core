# # services/payout_treasury.py
# from decimal import Decimal
#
# from eth_account import Account
# from eth_account.signers.local import LocalAccount
# from web3 import Web3
# from web3.exceptions import ContractLogicError
# from web3.logs import DISCARD
#
# from _0_utils.functions.json import read_json
#
# NETWORKS_FILE = "_0_utils/service/crypto/utils/metadata/networks.json"
# ABI_FILE = "___utils/service/crypto/utils/metadata/abi.json"
#
# NETWORK_CONFIGS = read_json(NETWORKS_FILE, {})
# CONTRACT_ABI = read_json(ABI_FILE, [])
#
# from _0_utils.base_variables import SMART_CONTRACT_OWNER_PK
#
#
# def _get_w3(chain: str) -> Web3:
#     cfg = NETWORK_CONFIGS.get(chain)
#     if not cfg or not cfg["rpc_url"]:
#         raise ValueError(f"Invalid network or undefined RPC: {chain}")
#     w3 = Web3(Web3.HTTPProvider(cfg["rpc_url"], request_kwargs={"timeout": 60}))
#     if not w3.is_connected():
#         raise RuntimeError(f"Unable to connect to RPC {chain}")
#     return w3
#
#
# def _get_contract(w3: Web3, chain: str):
#     cfg = NETWORK_CONFIGS[chain]
#     address = cfg["contract"]
#     if not address:
#         raise ValueError(f"Contract address not set for network {chain}")
#     return w3.eth.contract(address=Web3.to_checksum_address(address), abi=CONTRACT_ABI)
#
#
# def _get_account() -> LocalAccount:
#     pk = SMART_CONTRACT_OWNER_PK
#     if not pk:
#         raise ValueError("PRIVATE_KEY not set")
#     return Account.from_key(pk)
#
#
# def _suggest_fees(w3: Web3) -> dict:
#     # Attempt for EIP-1559, otherwise legacy
#     try:
#         priority = w3.eth.max_priority_fee  # May error on some RPCs
#     except Exception:
#         priority = w3.to_wei(2, "gwei")
#     try:
#         latest = w3.eth.get_block("latest")
#         base = latest.get("baseFeePerGas")
#         if base is not None:
#             max_fee = int(base + priority * 2)
#             return {
#                 "maxFeePerGas": max_fee,
#                 "maxPriorityFeePerGas": int(priority),
#             }
#     except Exception as e:
#         print(e)
#     # fallback legacy
#     gas_price = w3.eth.gas_price
#     return {"gasPrice": int(gas_price)}
#
#
# def _preflight(contract, from_addr: str, to_addr: str, amount_wei: int, w3):
#     try:
#         if contract.functions.paused().call():
#             raise RuntimeError("Contract is in Pause state")
#     except Exception as e:
#         print(e)
#
#     on_chain_balance = w3.eth.get_balance(contract.address)
#     if on_chain_balance < amount_wei:
#         raise RuntimeError("Not enough contract inventory")
#
#     try:
#         contract.functions.sendPayment(to_addr, amount_wei).call({"from": from_addr})
#     except ContractLogicError as e:
#         raise RuntimeError(f"Preflight failed: {e}") from e
#
#
# def _raw_tx(signed):
#     return getattr(signed, "raw_transaction", None) or getattr(
#         signed, "rawTransaction", None
#     )
#
#
# def _required_for_fees(gas_limit: int, fees: dict) -> int:
#     # In EIP-1559 you must be able to cover gas_limit * maxFeePerGas
#     if "gasPrice" in fees:
#         return gas_limit * int(fees["gasPrice"])
#     return gas_limit * int(fees["maxFeePerGas"])
#
#
# def wei_to_ether(w3, wei_amount: int) -> Decimal:
#     """Convert Wei to Ether"""
#     return Decimal(str(w3.from_wei(wei_amount, "ether")))
#
#
# def _ensure_gas_funds(w3, account_addr: str, gas_limit: int, fees: dict):
#     bal = w3.eth.get_balance(account_addr)
#     required = _required_for_fees(gas_limit, fees)
#     if bal < required:
#         raise RuntimeError(
#             f"Lack of balance for gas fee: balance={w3.from_wei(bal, 'ether')} "
#             f"Amount needed = {w3.from_wei(required, 'ether')} (MATIC)"
#         )
#
#
# def get_contract_balance(chain: str):
#     w3 = _get_w3(chain)
#     contract = _get_contract(w3, chain)
#     on_chain_balance = w3.eth.get_balance(contract.address)
#     return wei_to_ether(w3, on_chain_balance)
#
#
# def send_payment(chain: str, to: str, amount):
#     try:
#         w3 = _get_w3(chain)
#         contract = _get_contract(w3, chain)
#         account = _get_account()
#
#         to_checksum = Web3.to_checksum_address(to)
#         amount_wei = w3.to_wei(str(amount), "ether")
#
#         _preflight(contract, account.address, to_checksum, amount_wei, w3)
#
#         gas_estimate = contract.functions.sendPayment(
#             to_checksum, amount_wei
#         ).estimate_gas({"from": account.address})
#         gas_limit = int(gas_estimate * 1.2)
#
#         fees = _suggest_fees(w3)
#         _ensure_gas_funds(w3, account.address, gas_limit, fees)  # Gas balance check
#
#         tx = contract.functions.sendPayment(to_checksum, amount_wei).build_transaction(
#             {
#                 "from": account.address,
#                 "nonce": w3.eth.get_transaction_count(account.address),
#                 "chainId": NETWORK_CONFIGS[chain]["chain_id"],
#                 "gas": gas_limit,
#                 **fees,
#             }
#         )
#
#         signed = account.sign_transaction(tx)
#         raw = _raw_tx(signed)
#         if raw is None:
#             raise TypeError(
#                 "Unsupported SignedTransaction object (no raw_transaction/rawTransaction)"
#             )
#         tx_hash = w3.eth.send_raw_transaction(raw)
#         receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
#
#         try:
#             events = contract.events.PaymentSent().process_receipt(
#                 receipt, errors=DISCARD
#             )
#             evt = events[0]["args"] if events else None
#         except Exception:
#             evt = None
#
#         # data = {
#         #     "tx_hash": tx_hash.hex(),
#         #     "status": receipt.status,
#         #     "gas_used": receipt.gasUsed,
#         #     "event": {
#         #         "executor": evt.get("executor") if evt else None,
#         #         "to": evt.get("to") if evt else None,
#         #         "amount_wei": int(evt.get("amount")) if evt else None,
#         #     } if evt else None,
#         # }
#         return True, tx_hash.hex()
#     except Exception as e:
#         print(f"Send Contract Payment Error : {e}")
#         return False, None

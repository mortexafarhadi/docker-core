# from decimal import Decimal, ROUND_DOWN
# from typing import Optional, Dict, Any, Tuple, List
#
# import base58
# import requests
# from blockcypher import get_address_overview
# from blockcypher import simple_spend
# from ecdsa import SigningKey, SECP256k1
# from ecdsa.util import sigencode_der_canonize
#
# from ___utils.base_variables import BLOCK_CYPHER_API_TOKEN
#
# # from __future__ import annotations
#
#
# # -----------------------------
# # Utils
# # -----------------------------
# def to_satoshi(amount: str | Decimal | float | int) -> int:
#     d = Decimal(str(amount))
#     return int((d * Decimal("1e8")).to_integral_value(rounding=ROUND_DOWN))
#
#
# def from_satoshi(sats: int) -> Decimal:
#     return (Decimal(sats) / Decimal("1e8")).quantize(
#         Decimal("0.00000001"), rounding=ROUND_DOWN
#     )
#
#
# def get_bc_base_url(coin_symbol: str) -> str:
#     """
#     coin_symbol مجاز: 'btc', 'btc-testnet', 'ltc', 'ltc-testnet'
#     """
#     mapping = {
#         "btc": "https://api.blockcypher.com/v1/btc/main",
#         "btc-testnet": "https://api.blockcypher.com/v1/btc/test3",
#         "ltc": "https://api.blockcypher.com/v1/ltc/main",
#         "ltc-testnet": "https://api.blockcypher.com/v1/ltc/test3",
#     }
#     if coin_symbol not in mapping:
#         raise ValueError(f"Unsupported coin_symbol: {coin_symbol}")
#     return mapping[coin_symbol]
#
#
# def wif_to_privhex_and_compressed(wif: str) -> Tuple[str, bool]:
#     """
#     WIF را به کلید خصوصی hex و فلگ فشرده بودن تبدیل می‌کند.
#     برای BTC/LTC عمومی است (پیشوند شبکه را حذف می‌کند).
#     """
#     raw = base58.b58decode_check(wif)
#     # raw: [prefix (1)] + [priv (32)] + [optional 0x01 if compressed]
#     if len(raw) == 33:
#         return raw[1:].hex(), False
#     if len(raw) == 34 and raw[-1] == 0x01:
#         return raw[1:-1].hex(), True
#     # حالت‌های خاص: باز هم priv همان 32 بایت بعد از prefix است
#     return raw[1:33].hex(), (len(raw) == 34 and raw[-1] == 0x01)
#
#
# def privhex_to_compressed_pubkey_hex(priv_hex: str) -> str:
#     """
#     از کلید خصوصی، pubkey فشرده را تولید می‌کند (02/03 + 32بایت X).
#     برای P2WPKH (BIP84) لازم است.
#     """
#     sk = SigningKey.from_string(bytes.fromhex(priv_hex), curve=SECP256k1)
#     vk = sk.get_verifying_key()
#     x = vk.pubkey.point.x()
#     y = vk.pubkey.point.y()
#     prefix = 0x02 if (y % 2 == 0) else 0x03
#     return (bytes([prefix]) + x.to_bytes(32, "big")).hex()
#
#
# # -----------------------------
# # Balance helpers
# # -----------------------------
# def get_blockcypher_balance(address: str, coin_symbol: str) -> Optional[Dict[str, Any]]:
#     try:
#         ov = get_address_overview(
#             address, coin_symbol=coin_symbol, api_key=BLOCK_CYPHER_API_TOKEN
#         )
#     except Exception as e:
#         print(f"[{coin_symbol}] get_address_overview error: {e}")
#         return None
#
#     confirmed_sats = int(ov.get("balance", 0))
#     unconfirmed_sats = int(ov.get("unconfirmed_balance", 0))
#     final_sats = int(ov.get("final_balance", 0))
#     return {
#         "confirmed_sats": confirmed_sats,
#         "unconfirmed_sats": unconfirmed_sats,
#         "final_sats": final_sats,
#         "confirmed": from_satoshi(confirmed_sats),
#         "unconfirmed": from_satoshi(unconfirmed_sats),
#         "final": from_satoshi(final_sats),
#         "n_tx": ov.get("n_tx", 0),
#         "unconfirmed_n_tx": ov.get("unconfirmed_n_tx", 0),
#         "final_n_tx": ov.get("final_n_tx", 0),
#     }
#
#
# # def get_blockcypher_balance(address: str, coin: str) -> Optional[Dict[str, Any]]:
# #     """
# #     coin: 'btc', 'ltc', 'doge', 'dash', ...
# #     for test : 'btc-testnet'
# #     """
# #     if not address:
# #         print("Address is empty.")
# #         return None
# #
# #     try:
# #         overview = get_address_overview(
# #             address=address,
# #             coin_symbol=coin,
# #             api_key=BLOCK_CYPHER_API_TOKEN
# #         )
# #     except Exception as e:
# #         print(f"Error fetching balance for {coin} address {address}: {e}")
# #         return None
# #
# #     confirmed_sats = int(overview.get('balance', 0))
# #     unconfirmed_sats = int(overview.get('unconfirmed_balance', 0))
# #     final_sats = int(overview.get('final_balance', 0))
# #
# #     return {
# #         # In Satoshi terms
# #         'confirmed_sats': confirmed_sats,
# #         'unconfirmed_sats': unconfirmed_sats,
# #         'final_sats': final_sats,
# #
# #         # In terms of coins (Decimal)
# #         'confirmed': from_satoshi(confirmed_sats),
# #         'unconfirmed': from_satoshi(unconfirmed_sats),
# #         'final': from_satoshi(final_sats),
# #
# #         # Additional information
# #         'n_tx': overview.get('n_tx', 0),
# #         'unconfirmed_n_tx': overview.get('unconfirmed_n_tx', 0),
# #         'final_n_tx': overview.get('final_n_tx', 0),
# #     }
#
#
# def get_btc_balance_by_address(address: str):
#     return get_blockcypher_balance(address, "btc")
#
#
# def get_doge_balance_by_address(address: str):
#     return get_blockcypher_balance(address, "doge")
#
#
# def get_ltc_balance_by_address(address: str):
#     return get_blockcypher_balance(address, "ltc")
#
#
# def get_dash_balance_by_address(address: str):
#     return get_blockcypher_balance(address, "dash")
#
#
# # -----------------------------
# # Core sender (works for bech32/P2WPKH - BIP84)
# # -----------------------------
# def send_utxo_via_blockcypher(
#     from_wif: str,
#     from_address: str,
#     to_address: str,
#     amount_str: str | Decimal | float | int,
#     coin_symbol: str,  # 'btc' | 'ltc' | 'btc-testnet' | 'ltc-testnet'
#     api_token: str = BLOCK_CYPHER_API_TOKEN,
#     fee_preference: str = "medium",  # 'low' | 'medium' | 'high'
# ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
#     """
#     تراکنش UTXO را با BlockCypher (txs/new -> امضا -> txs/send) ارسال می‌کند.
#     برای BIP84 (bech32) و سایر انواع (P2PKH/P2SH-P2WPKH) کار می‌کند.
#     """
#     base_url = get_bc_base_url(coin_symbol)
#     value_sats = to_satoshi(amount_str)
#
#     # 0) بررسی اولیه موجودی (اختیاری ولی مفید)
#     bal = get_blockcypher_balance(from_address, coin_symbol)
#     if not bal:
#         print(f"[{coin_symbol}] Cannot fetch balance for {from_address}")
#     else:
#         if bal["final_sats"] < value_sats:
#             print(
#                 f"[{coin_symbol}] Not enough final balance. Have {bal['final_sats']} sats, need >= {value_sats} sats (fee not included)."
#             )
#
#     # 1) اسکلت تراکنش
#     new_tx_payload = {
#         "inputs": [{"addresses": [from_address]}],
#         "outputs": [{"addresses": [to_address], "value": value_sats}],
#         "preference": fee_preference,
#         "change_address": from_address,  # تغییر به آدرس فرستنده برگردد
#     }
#     r = requests.post(
#         f"{base_url}/txs/new",
#         json=new_tx_payload,
#         params={"token": api_token},
#         timeout=30,
#     )
#     tx_skel = r.json()
#     if r.status_code >= 400 or "errors" in tx_skel:
#         return False, None, {"stage": "new", "response": tx_skel}
#
#     # 2) امضای tosign ها
#     priv_hex, _compressed = wif_to_privhex_and_compressed(from_wif)
#     sk = SigningKey.from_string(bytes.fromhex(priv_hex), curve=SECP256k1)
#     pubkey_hex = privhex_to_compressed_pubkey_hex(priv_hex)
#
#     signatures: List[str] = []
#     for t in tx_skel.get("tosign", []):
#         sig_der = sk.sign_digest(bytes.fromhex(t), sigencode=sigencode_der_canonize)
#         signatures.append(sig_der.hex() + "01")  # SIGHASH_ALL
#
#     tx_skel["signatures"] = signatures
#     tx_skel["pubkeys"] = [pubkey_hex for _ in signatures]
#
#     # 3) ارسال تراکنش امضا‌شده
#     r2 = requests.post(
#         f"{base_url}/txs/send",
#         json=tx_skel,
#         params={"token": api_token},
#         timeout=30,
#     )
#     res = r2.json()
#     if r2.status_code >= 400 or "errors" in res:
#         return False, None, {"stage": "send", "response": res}
#
#     # 4) استخراج tx hash
#     tx = res.get("tx") or {}
#     tx_hash = tx.get("hash") or res.get("tx", {}).get("hash")
#     return True, tx_hash, res
#
#
# def send_doge_block_cypher_coin(pk_wallet, to, amount, coin="doge"):
#     """
#     Dogecoin : 'doge', Dash : 'dash',
#     """
#     _amount = to_satoshi(amount)
#     print(f"satoshi: {_amount}")
#     tx_hash = simple_spend(
#         from_privkey=pk_wallet,
#         to_address=to,
#         to_satoshis=_amount,
#         coin_symbol=coin,
#         api_key=BLOCK_CYPHER_API_TOKEN,
#     )
#     return tx_hash

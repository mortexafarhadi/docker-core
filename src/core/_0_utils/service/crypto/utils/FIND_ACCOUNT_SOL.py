# import hashlib
# import hmac
# import struct
# from typing import Dict, List, Optional
#
# import base58
# from mnemonic import Mnemonic
# from solana.rpc.api import Client
# from solders.keypair import Keypair
# from solders.pubkey import Pubkey
#
#
# class SolanaHDWallet:
#     DERIVATION_PATTERNS = [
#         "m/44'/501'/{}'/0'",
#         "m/44'/501'/{}'",
#         "m/44'/501'/0'/{}",
#         "m/44'/501'/0'/0/{}",
#     ]
#
#     def __init__(self, network: str = "https://api.mainnet-beta.solana.com"):
#         self.client = Client(network)
#         self.network = network
#
#     def _derive_key_from_path(self, seed: bytes, path: str) -> bytes:
#         parts = path.replace("m/", "").split("/")
#
#         master_key = self._get_master_key_from_seed(seed)
#
#         current_key = master_key
#         for part in parts:
#             if part.endswith("'"):
#                 index = int(part[:-1]) + 0x80000000
#             else:
#                 index = int(part)
#
#             current_key = self._derive_child_key(current_key, index)
#
#         return current_key[:32]
#
#     def _get_master_key_from_seed(self, seed: bytes) -> bytes:
#         return hmac.new(b"ed25519 seed", seed, hashlib.sha512).digest()
#
#     def _derive_child_key(self, parent_key: bytes, index: int) -> bytes:
#         if index >= 0x80000000:
#             data = b"\x00" + parent_key[:32] + struct.pack(">I", index)
#         else:
#             data = parent_key[:32] + struct.pack(">I", index)
#
#         return hmac.new(parent_key[32:], data, hashlib.sha512).digest()
#
#     def derive_keypair(self, seed_phrase: str, derivation_path: str) -> Keypair:
#         mnemo = Mnemonic("english")
#         if not mnemo.check(seed_phrase):
#             raise ValueError("❌ Seed phrase invalid")
#
#         seed = mnemo.to_seed(seed_phrase, passphrase="")
#
#         derived_seed = self._derive_key_from_path(seed, derivation_path)
#
#         return Keypair.from_seed(derived_seed)
#
#     def find_account_by_address(
#         self, seed_phrase: str, target_address: str, max_accounts: int = 100
#     ) -> Optional[Dict]:
#         print(f"🔍 Search Address: {target_address}")
#         print(
#             f"📊 Check {max_accounts} Account in {len(self.DERIVATION_PATTERNS)} Different Pattern"
#         )
#         print(
#             f"⏳ Total Check: {max_accounts * len(self.DERIVATION_PATTERNS)}  Derivation\n"
#         )
#         print("=" * 100)
#
#         checked_count = 0
#
#         for pattern_idx, pattern in enumerate(self.DERIVATION_PATTERNS):
#             print(
#                 f"\n🔸 Pattern {pattern_idx + 1}/{len(self.DERIVATION_PATTERNS)}: {pattern}"
#             )
#             print("-" * 100)
#
#             for account_idx in range(max_accounts):
#                 try:
#                     path = pattern.format(account_idx)
#
#                     keypair = self.derive_keypair(seed_phrase, path)
#                     address = str(keypair.pubkey())
#
#                     checked_count += 1
#
#                     if checked_count % 50 == 0:
#                         print(f"   ✓ Checked: {checked_count} Account...")
#
#                     if address.lower() == target_address.lower():
#                         print(f"\n{'🎉' * 50}")
#                         print("✅ Account Found")
#                         print(f"{'🎉' * 50}\n")
#
#                         balance = self._get_balance(address)
#
#                         return {
#                             "found": True,
#                             "derivation_path": path,
#                             "derivation_pattern": pattern,
#                             "account_index": account_idx,
#                             "address": address,
#                             "private_key_base58": base58.b58encode(
#                                 bytes(keypair)
#                             ).decode("utf-8"),
#                             "private_key_bytes": list(keypair.secret()),
#                             "public_key": str(keypair.pubkey()),
#                             "balance_sol": balance["balance_sol"],
#                             "balance_lamports": balance["balance_lamports"],
#                         }
#
#                 except Exception as e:
#                     if checked_count % 100 == 0:
#                         print(f"   ⚠️ Error in Number {checked_count}: {str(e)[:50]}")
#                     continue
#
#         print(f"\n{'=' * 100}")
#         print(f"❌ Account Not Found. Total Check: {checked_count} Derivation")
#         print(f"{'=' * 100}")
#         return None
#
#     def get_all_accounts(
#         self, seed_phrase: str, count: int = 10, pattern: Optional[str] = None
#     ) -> List[Dict]:
#         accounts = []
#
#         patterns = [pattern] if pattern else self.DERIVATION_PATTERNS
#
#         print(f"📋 Extract {count} First Account...\n")
#         print("=" * 100)
#
#         for pattern in patterns:
#             print(f"\n🔸 Pattern: {pattern}")
#             print("-" * 100)
#
#             for i in range(count):
#                 try:
#                     path = pattern.format(i)
#                     keypair = self.derive_keypair(seed_phrase, path)
#                     address = str(keypair.pubkey())
#                     balance = self._get_balance(address)
#
#                     account_info = {
#                         "account_index": i,
#                         "derivation_path": path,
#                         "derivation_pattern": pattern,
#                         "address": address,
#                         "private_key_base58": base58.b58encode(bytes(keypair)).decode(
#                             "utf-8"
#                         ),
#                         "private_key_bytes": list(keypair.secret()),
#                         "public_key": str(keypair.pubkey()),
#                         "balance_sol": balance["balance_sol"],
#                         "balance_lamports": balance["balance_lamports"],
#                     }
#
#                     accounts.append(account_info)
#
#                     print(f"\n   Account #{i}:")
#                     print(f"   Path: {path}")
#                     print(f"   Address: {address}")
#                     print(f"   Balance: {balance['balance_sol']:.6f} SOL")
#
#                     if balance["balance_sol"] > 0:
#                         print("   💰 This Account Have Balance!")
#
#                 except Exception as e:
#                     print(f"\n   ⚠️ Error in Account #{i}: {e}")
#                     continue
#
#             if not pattern:
#                 break
#
#         print("\n" + "=" * 100)
#         print(f"✅  {len(accounts)} Accounts were extracted.")
#
#         return accounts
#
#     def _get_balance(self, address: str) -> Dict:
#         try:
#             pubkey = Pubkey.from_string(address)
#             response = self.client.get_balance(pubkey)
#             lamports = response.value
#             sol = lamports / 1_000_000_000
#
#             return {"balance_sol": sol, "balance_lamports": lamports}
#         except Exception:
#             return {"balance_sol": 0.0, "balance_lamports": 0}
#
#
# def find_my_solana_account(seed_phrase: str, my_address: str, max_search: int = 100):
#     """
#     Args:
#         seed_phrase: 12 or 24 Word seed phrase
#         my_address: YOur SOL Address From Trust Wallet
#         max_search: Maximum Check Account
#     """
#     print("🚀 Start Search...\n")
#
#     wallet = SolanaHDWallet()
#     result = wallet.find_account_by_address(
#         seed_phrase=seed_phrase,
#         target_address=my_address,
#         max_accounts=max_search,
#     )
#
#     if result and result["found"]:
#         print("\n" + "📝" * 50)
#         print("Total Information Your Account:")
#         print("📝" * 50)
#         print(f"\n✅ Derivation Path: {result['derivation_path']}")
#         print(f"✅ Account Index: {result['account_index']}")
#         print(f"💼 Address: {result['address']}")
#         print(f"💰 Balance: {result['balance_sol']} SOL")
#         print("\n🔑 Private Key (Base58):")
#         print(f"   {result['private_key_base58']}")
#         print("\n🔢 Private Key (Bytes - For Use in Code):")
#         print(f"   {result['private_key_bytes']}")
#         print("\n⚠️  Store this information in a safe place.!")
#
#         return result
#     else:
#         print("\n❌ Account not found. Please check the following:")
#         print("   1. Seed phrase Check again.")
#         print("   2. Copy Address From Trust Wallet (Button Receive > Copy)")
#         print("   3. Increase max_search (for example 200 or 500)")
#         return None
#
#
# def show_all_my_accounts(seed_phrase: str, count: int = 10):
#     wallet = SolanaHDWallet()
#     accounts = wallet.get_all_accounts(seed_phrase=seed_phrase, count=count)
#
#     print("\n" + "📊" * 50)
#     print("Summary of your accounts:")
#     print("📊" * 50)
#
#     accounts_with_balance = [a for a in accounts if a["balance_sol"] > 0]
#
#     if accounts_with_balance:
#         print("\n💰 Accounts with balances:")
#         for acc in accounts_with_balance:
#             print(f"\n   Account #{acc['account_index']}:")
#             print(f"   Address: {acc['address']}")
#             print(f"   Balance: {acc['balance_sol']} SOL")
#             print(f"   Path: {acc['derivation_path']}")
#     else:
#         print("\n⚠️  No active accounts with balances found.")
#         print("    (The number of accounts reviewed may need to be increased.)")
#
#     return accounts

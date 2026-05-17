# import coinaddrvalidator
# from web3 import Web3
#
#
# # Core Logic
# def check_address_structural_validity(address: str, network: str) -> bool:
#     """Checking address structure validity with coinaddrvalidator and web3 (for EVM)."""
#
#     # Map of user input network symbols to coinaddrvalidator/Web3 standards (lowercase)
#     network_map = {
#         "ETH": "eth",
#         "BNB": "bnb",
#         "POL": "matic",
#         "MATIC": "matic",
#         "ARB": "eth",
#         "AVAX": "avax",
#         "BTC": "btc",
#         "DOGE": "doge",
#         "SOL": "sol",
#         "TRX": "trx",
#         "LTC": "ltc",
#         "DASH": "dash",
#     }
#
#     try:
#         validator_name = network_map.get(network.upper())
#         if not validator_name:
#             return False
#
#         # --- Structural Validation with coinaddrvalidator ---
#         result = coinaddrvalidator.validate(validator_name, address)
#
#         # --- Specific Validation for EVM (ETH, BNB, MATIC, ARB, AVAX) ---
#         # All EVM addresses share the same structure ('eth')
#         if validator_name in ["eth", "bnb", "matic"]:
#             # Checksummed address (mixed case) is preferred
#             if Web3.is_checksum_address(address):
#                 return True
#             # Non-checksummed address (e.g., all lowercase) is also structurally valid
#             return Web3.is_address(address)
#
#         # --- Validation for other coins (BTC, SOL, LTC, etc.) ---
#         return result.valid
#
#     except Exception:
#         return False
#
#
# def check_address_validation(address: str, network: str) -> bool:
#     supported_networks = [
#         "eth",
#         "bnb",
#         "pol",
#         "matic",
#         "arb",
#         "avax",
#         "btc",
#         "doge",
#         "sol",
#         "trx",
#         "ltc",
#         "dash",
#     ]
#
#     # Convert network input to lowercase for consistency
#     network = network.lower()
#     if network not in supported_networks:
#         print(f"❌ Network '{network}' is not supported.")
#         return False
#
#     is_valid_to_send = check_address_structural_validity(address, network)
#
#     return is_valid_to_send

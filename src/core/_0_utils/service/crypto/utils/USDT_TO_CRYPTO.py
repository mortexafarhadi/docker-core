# from decimal import Decimal, ROUND_DOWN
# from typing import Dict, Optional, List
#
# import requests
#
#
# class CryptoPriceConverter:
#     """Convert USDT amounts to any cryptocurrency using live prices"""
#
#     # API endpoints (multiple options for reliability)
#     COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"
#     BINANCE_API = "https://api.binance.com/api/v3/ticker/price"
#     COINBASE_API = "https://api.coinbase.com/v2/exchange-rates"
#
#     # Common CoinGecko IDs mapping (can be extended)
#     COINGECKO_IDS = {
#         "btc": "bitcoin",
#         "eth": "ethereum",
#         "bnb": "binancecoin",
#         "sol": "solana",
#         "xrp": "ripple",
#         "ada": "cardano",
#         "doge": "dogecoin",
#         "trx": "tron",
#         "ltc": "litecoin",
#         "pol": "polygon-ecosystem-token",
#         "matic": "matic-network",
#         "dot": "polkadot",
#         "dai": "dai",
#         "avax": "avalanche-2",
#         "shib": "shiba-inu",
#         "link": "chainlink",
#         "atom": "cosmos",
#         "uni": "uniswap",
#         "etc": "ethereum-classic",
#         "xlm": "stellar",
#         "bch": "bitcoin-cash",
#         "near": "near",
#         "apt": "aptos",
#         "algo": "algorand",
#         "vet": "vechain",
#         "icp": "internet-computer",
#         "fil": "filecoin",
#         "hbar": "hedera-hashgraph",
#         "arb": "arbitrum",
#         "op": "optimism",
#         "inj": "injective-protocol",
#         "imx": "immutable-x",
#         "mkr": "maker",
#         "render": "render-token",
#         "grt": "the-graph",
#         "ftm": "fantom",
#         "rune": "thorchain",
#         "aave": "aave",
#         "stx": "blockstack",
#         "theta": "theta-token",
#         "tia": "celestia",
#         "sei": "sei-network",
#         "kas": "kaspa",
#         "wbt": "whitebit",
#         "ton": "the-open-network",
#         "sui": "sui",
#         "pepe": "pepe",
#         "floki": "floki",
#         "bonk": "bonk",
#         "wif": "dogwifcoin",
#     }
#
#     def __init__(self, api_source: str = "binance"):
#         """
#         Initialize converter
#
#         Args:
#             api_source: 'coingecko', 'binance', or 'coinbase'
#         """
#         self.api_source = api_source
#         self._price_cache = {}
#         self._symbol_cache = {}
#
#     def normalize_symbol(self, symbol: str) -> str:
#         """Normalize coin symbol to lowercase"""
#         return symbol.lower().strip()
#
#     def get_coingecko_id(self, symbol: str) -> str:
#         """
#         Get CoinGecko ID for a symbol
#         First checks the mapping, if not found uses the symbol as-is
#         """
#         symbol_lower = self.normalize_symbol(symbol)
#         return self.COINGECKO_IDS.get(symbol_lower, symbol_lower)
#
#     def get_binance_pair(self, symbol: str) -> str:
#         """Get Binance trading pair (e.g., BTCUSDT)"""
#         symbol_upper = symbol.upper().strip()
#         return f"{symbol_upper}USDT"
#
#     def get_price_coingecko(self, coin: str) -> Optional[float]:
#         """Get price from CoinGecko API (supports 10,000+ coins)"""
#         try:
#             coin_id = self.get_coingecko_id(coin)
#
#             params = {"ids": coin_id, "vs_currencies": "usd"}
#
#             response = requests.get(self.COINGECKO_API, params=params, timeout=10)
#             response.raise_for_status()
#             data = response.json()
#
#             price = data.get(coin_id, {}).get("usd")
#             return float(price) if price else None
#
#         except Exception as e:
#             print(f"Error fetching {coin} price from CoinGecko: {e}")
#             return None
#
#     def get_price_binance(self, coin: str) -> Optional[float]:
#         """Get price from Binance API (supports major coins)"""
#         try:
#             symbol = self.get_binance_pair(coin)
#
#             params = {"symbol": symbol}
#             response = requests.get(self.BINANCE_API, params=params, timeout=10)
#             response.raise_for_status()
#             data = response.json()
#
#             price = data.get("price")
#             return float(price) if price else None
#
#         except Exception as e:
#             # Binance returns 400 if pair doesn't exist - not an error
#             print(e)
#             return None
#
#     def get_price_coinbase(self, coin: str) -> Optional[float]:
#         """Get price from Coinbase API"""
#         try:
#             response = requests.get(
#                 self.COINBASE_API, params={"currency": "USD"}, timeout=10
#             )
#             response.raise_for_status()
#             data = response.json()
#
#             rates = data.get("data", {}).get("rates", {})
#             coin_upper = coin.upper().strip()
#
#             if coin_upper in rates:
#                 rate = float(rates[coin_upper])
#                 return 1.0 / rate if rate > 0 else None
#
#             return None
#
#         except Exception as e:
#             print(f"Error fetching {coin} price from Coinbase: {e}")
#             return None
#
#     def search_coingecko_coin(self, query: str) -> Optional[Dict]:
#         """
#         Search CoinGecko for coin by symbol or name
#         Useful for finding the correct coin ID
#         """
#         try:
#             url = "https://api.coingecko.com/api/v3/search"
#             params = {"query": query}
#
#             response = requests.get(url, params=params, timeout=10)
#             response.raise_for_status()
#             data = response.json()
#
#             coins = data.get("coins", [])
#             if coins:
#                 # Return first match
#                 return {
#                     "id": coins[0].get("id"),
#                     "symbol": coins[0].get("symbol"),
#                     "name": coins[0].get("name"),
#                 }
#
#             return None
#
#         except Exception as e:
#             print(f"Error searching for {query}: {e}")
#             return None
#
#     def get_current_price(self, coin: str, use_cache: bool = True) -> Optional[float]:
#         """
#         Get current price of coin in USDT
#         Tries multiple sources for maximum compatibility
#
#         Args:
#             coin: Coin symbol (btc, eth, bnb, etc.)
#             use_cache: Use cached price if available
#
#         Returns:
#             Price in USDT or None if failed
#         """
#         coin = self.normalize_symbol(coin)
#
#         # Check cache
#         if use_cache and coin in self._price_cache:
#             return self._price_cache[coin]
#
#         # Try primary API source
#         price = None
#         if self.api_source == "coingecko":
#             price = self.get_price_coingecko(coin)
#         elif self.api_source == "binance":
#             price = self.get_price_binance(coin)
#         elif self.api_source == "coinbase":
#             price = self.get_price_coinbase(coin)
#
#         # Fallback strategy: try all sources
#         if price is None:
#             # Try Binance first (fastest)
#             if self.api_source != "binance":
#                 price = self.get_price_binance(coin)
#
#             # Try CoinGecko (most comprehensive)
#             if price is None and self.api_source != "coingecko":
#                 price = self.get_price_coingecko(coin)
#
#             # Try Coinbase as last resort
#             if price is None and self.api_source != "coinbase":
#                 price = self.get_price_coinbase(coin)
#
#         # Cache the price if found
#         if price is not None:
#             self._price_cache[coin] = price
#
#         return price
#
#     def usdt_to_coin(
#         self, amount_usdt: float, coin: str, precision: Optional[int] = 8
#     ) -> Optional[float]:
#         """
#         Convert USDT amount to cryptocurrency amount (USDT / Price)
#
#         Args:
#             amount_usdt: Amount in USDT/Tether
#             coin: Target coin symbol (any crypto)
#             precision: Decimal precision (default 8)
#
#         Returns:
#             Amount in target cryptocurrency
#         """
#         price = self.get_current_price(coin)
#
#         if price is None:
#             raise ValueError(f"Could not fetch price for {coin.upper()}")
#
#         if price <= 0:
#             raise ValueError(f"Invalid price for {coin.upper()}: {price}")
#
#         # Calculate amount: USDT / price = coin amount
#         coin_amount = Decimal(str(amount_usdt)) / Decimal(str(price))
#
#         if precision is not None:
#             coin_amount = coin_amount.quantize(
#                 Decimal(10) ** -precision, rounding=ROUND_DOWN
#             )
#
#         return float(coin_amount)
#
#     def coin_to_usdt(
#         self, amount_coin: float, coin: str, precision: Optional[int] = 2
#     ) -> Optional[float]:
#         """
#         Convert cryptocurrency amount to USDT amount (Coin Amount * Price)
#
#         Args:
#             amount_coin: Amount in the target cryptocurrency
#             coin: Source coin symbol (any crypto)
#             precision: Decimal precision (default 2 for fiat/usdt)
#
#         Returns:
#             Amount in USDT/Tether
#         """
#         price = self.get_current_price(coin)
#
#         if price is None:
#             raise ValueError(f"Could not fetch price for {coin.upper()}")
#
#         if price <= 0:
#             raise ValueError(f"Invalid price for {coin.upper()}: {price}")
#
#         # Calculate amount: coin_amount * price = USDT amount
#         usdt_amount = Decimal(str(amount_coin)) * Decimal(str(price))
#
#         if precision is not None:
#             usdt_amount = usdt_amount.quantize(
#                 Decimal(10) ** -precision, rounding=ROUND_DOWN
#             )
#
#         return float(usdt_amount)
#
#     def convert_usdt_to_multiple(
#         self, amount_usdt: float, coins: List[str]
#     ) -> Dict[str, Optional[float]]:
#         """
#         Convert USDT to multiple cryptocurrencies at once
#
#         Args:
#             amount_usdt: Amount in USDT
#             coins: List of coin symbols
#
#         Returns:
#             Dictionary with coin amounts
#         """
#         results = {}
#         for coin in coins:
#             try:
#                 amount = self.usdt_to_coin(amount_usdt, coin)
#                 results[coin.lower()] = amount
#             except Exception as e:
#                 print(f"Error converting to {coin.upper()}: {e}")
#                 results[coin.lower()] = None
#
#         return results
#
#     def convert_coins_to_usdt(
#         self, amounts: Dict[str, float]
#     ) -> Dict[str, Optional[float]]:
#         """
#         Convert multiple cryptocurrency amounts to their total USDT value
#
#         Args:
#             amounts: Dictionary of coin symbols and their amounts (e.g., {'btc': 0.01, 'eth': 0.5})
#
#         Returns:
#             Dictionary with coin symbols and their USDT value
#         """
#         results = {}
#         for coin, amount_coin in amounts.items():
#             try:
#                 usdt_value = self.coin_to_usdt(amount_coin, coin)
#                 results[coin.lower()] = usdt_value
#             except Exception as e:
#                 print(f"Error converting {coin.upper()} to USDT: {e}")
#                 results[coin.lower()] = None
#
#         return results
#
#     def get_conversion_info(self, amount_usdt: float, coin: str) -> Dict[str, any]:
#         """
#         Get detailed conversion information (USDT to Coin)
#
#         Args:
#             amount_usdt: Amount in USDT
#             coin: Target coin
#
#         Returns:
#             Dictionary with price and amount info
#         """
#         price = self.get_current_price(coin)
#
#         if price is None:
#             raise ValueError(f"Could not fetch price for {coin.upper()}")
#
#         amount = self.usdt_to_coin(amount_usdt, coin)
#
#         return {
#             "source_amount": amount_usdt,
#             "source_currency": "USDT",
#             "target_amount": amount,
#             "target_currency": coin.upper(),
#             "exchange_rate": price,
#             "calculation": f"{amount_usdt} USDT / ${price:.8f} per {coin.upper()} = {amount:.8f} {coin.upper()}",
#         }
#
#     def get_multiple_prices(self, coins: List[str]) -> Dict[str, Optional[float]]:
#         """
#         Get prices for multiple coins at once
#
#         Args:
#             coins: List of coin symbols
#
#         Returns:
#             Dictionary of coin prices in USDT
#         """
#         prices = {}
#         for coin in coins:
#             try:
#                 price = self.get_current_price(coin)
#                 prices[coin.lower()] = price
#             except Exception as e:
#                 print(f"Error fetching {coin} price: {e}")
#                 prices[coin.lower()] = None
#
#         return prices
#
#     def clear_cache(self):
#         """Clear price cache"""
#         self._price_cache = {}
#         self._symbol_cache = {}
#
#
# # ========== Simple Helper Functions ==========
#
#
# def usdt_to_crypto(amount_usdt: float, coin: str, api_source: str = "binance") -> float:
#     """
#     Simple function to convert USDT to ANY cryptocurrency (USDT -> Coin)
#
#     Args:
#         amount_usdt: Amount in USDT/Tether (e.g., 3.5)
#         coin: Target coin symbol (e.g., 'btc', 'eth', 'bnb', 'doge', etc.)
#         api_source: API source ('binance', 'coingecko', 'coinbase')
#
#     Returns:
#         Amount in target cryptocurrency
#     """
#     converter = CryptoPriceConverter(api_source=api_source)
#     return converter.usdt_to_coin(amount_usdt, coin)
#
#
# def crypto_to_usdt(amount_coin: float, coin: str, api_source: str = "binance") -> float:
#     """
#     Simple function to convert ANY cryptocurrency amount to USDT (Coin -> USDT)
#
#     Args:
#         amount_coin: Amount in the cryptocurrency (e.g., 0.001 for BTC)
#         coin: Source coin symbol (e.g., 'btc', 'eth', 'bnb', 'doge', etc.)
#         api_source: API source ('binance', 'coingecko', 'coinbase')
#
#     Returns:
#         Amount in USDT/Tether
#
#     Example:
#         >>> usdt_value = crypto_to_usdt(0.001, 'btc')
#     """
#     converter = CryptoPriceConverter(api_source=api_source)
#     return converter.coin_to_usdt(amount_coin, coin)
#
#
# def convert_usdt_to_coins(
#     amount_usdt: float, coins: List[str], api_source: str = "binance"
# ) -> Dict[str, float]:
#     """
#     Convert USDT to multiple cryptocurrencies
#
#     Args:
#         amount_usdt: Amount in USDT
#         coins: List of coin symbols
#         api_source: API source
#
#     Returns:
#         Dictionary with all converted amounts
#     """
#     converter = CryptoPriceConverter(api_source=api_source)
#     return converter.convert_usdt_to_multiple(amount_usdt, coins)
#
#
# def convert_coins_to_usdt_multiple(
#     amounts: Dict[str, float], api_source: str = "binance"
# ) -> Dict[str, float]:
#     """
#     Convert multiple cryptocurrency amounts to their USDT value
#
#     Args:
#         amounts: Dictionary of coin symbols and their amounts (e.g., {'btc': 0.01, 'eth': 0.5})
#         api_source: API source
#
#     Returns:
#         Dictionary with all converted USDT values
#     """
#     converter = CryptoPriceConverter(api_source=api_source)
#     return converter.convert_coins_to_usdt(amounts)
#
#
# def get_crypto_price(coin: str, api_source: str = "binance") -> float:
#     """
#     Get current price of ANY cryptocurrency in USDT
#
#     Args:
#         coin: Coin symbol (e.g., 'btc', 'eth', 'bnb', 'doge', etc.)
#         api_source: API source
#
#     Returns:
#         Price in USDT
#     """
#     converter = CryptoPriceConverter(api_source=api_source)
#     price = converter.get_current_price(coin)
#     if price is None:
#         raise ValueError(f"Could not fetch price for {coin.upper()}")
#     return price
#
#
# def get_multiple_crypto_prices(
#     coins: List[str], api_source: str = "binance"
# ) -> Dict[str, float]:
#     """
#     Get prices for multiple cryptocurrencies
#
#     Args:
#         coins: List of coin symbols
#         api_source: API source
#
#     Returns:
#         Dictionary of prices
#     """
#     converter = CryptoPriceConverter(api_source=api_source)
#     return converter.get_multiple_prices(coins)
#
#
# def search_coin(query: str) -> Optional[Dict]:
#     """
#     Search for coin information on CoinGecko
#     Useful when you're not sure of the exact symbol
#
#     Args:
#         query: Coin name or symbol
#
#     Returns:
#         Coin info (id, symbol, name)
#     """
#     converter = CryptoPriceConverter()
#     return converter.search_coingecko_coin(query)

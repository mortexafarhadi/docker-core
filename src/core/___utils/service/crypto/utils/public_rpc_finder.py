# # utils/public_rpc_finder.py
# import random
# import time
# from typing import List, Dict, Any, Optional
#
# import requests
#
# ALIASES = {
#     "ethereum": "eth",
#     "mainnet": "eth",
#     "eth": "eth",
#     "polygon": "polygon",
#     "matic": "polygon",
#     "poly": "polygon",
#     "avax": "avax",
#     "avalanche": "avax",
#     "avax-c": "avax",
#     "bsc": "bsc",
#     "bnb": "bsc",
#     "binance": "bsc",
# }
#
# EXPECTED_CHAIN_ID = {
#     "eth": 1,
#     "polygon": 137,
#     "avax": 43114,
#     "bsc": 56,
# }
#
# # کاندیدهای استاتیک (قابل به‌روزرسانی)
# STATIC_CANDIDATES: Dict[str, List[str]] = {
#     "eth": [
#         "https://ethereum.publicnode.com",
#         "https://1rpc.io/eth",
#         "https://eth-mainnet.public.blastapi.io",
#         "https://rpc.ankr.com/eth",
#         "https://cloudflare-eth.com",
#         "https://eth.rpc.blxrbdn.com",  # ممکن است نرخ‌محدود باشد
#     ],
#     "polygon": [
#         "https://polygon-rpc.com",
#         "https://polygon-bor.publicnode.com",
#         "https://polygon-mainnet.public.blastapi.io",
#         "https://rpc.ankr.com/polygon",
#         "https://1rpc.io/matic",
#         "https://endpoints.omniatech.io/v1/matic/mainnet/public",
#         "https://polygon.llamarpc.com",
#         "https://polygon.drpc.org",
#         "https://polygon.blockpi.network/v1/rpc/public",
#         "https://polygon.meowrpc.com",
#     ],
#     "avax": [
#         "https://api.avax.network/ext/bc/C/rpc",
#         "https://avalanche-c-chain-rpc.publicnode.com",
#         "https://rpc.ankr.com/avalanche",
#         "https://1rpc.io/avax/c",
#         "https://avax.meowrpc.com",
#     ],
#     "bsc": [
#         "https://bsc-dataseed.binance.org",
#         "https://bsc-dataseed1.binance.org",
#         "https://bsc-dataseed2.binance.org",
#         "https://bsc.publicnode.com",
#         "https://rpc.ankr.com/bsc",
#         "https://1rpc.io/bnb",
#         "https://bscrpc.com",
#         "https://bsc-mev.blockpi.network/v1/rpc/public",
#     ],
# }
#
# UA = {"User-Agent": "rpc-prober/1.0 (+https://example.com)"}
#
#
# def _normalize_chain(chain: str) -> str:
#     key = chain.strip().lower()
#     return ALIASES.get(key, key)
#
#
# def _hex_to_int(x: str) -> int:
#     return int(x, 16) if isinstance(x, str) and x.startswith("0x") else int(x)
#
#
# def _jsonrpc(url: str, method: str, params: list, timeout: float) -> dict:
#     payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
#     r = requests.post(url, json=payload, headers=UA, timeout=(3, timeout))
#     r.raise_for_status()
#     j = r.json()
#     if "error" in j:
#         raise RuntimeError(f"rpc-error {j['error']}")
#     return j["result"]
#
#
# def _probe(
#         url: str, expected_chain_id: int, timeout: float, attempts: int = 1
# ) -> Dict[str, Any]:
#     last_err: Optional[str] = None
#     for _ in range(max(1, attempts)):
#         t0 = time.perf_counter()
#         try:
#             cid_hex = _jsonrpc(url, "eth_chainId", [], timeout)
#             cid = _hex_to_int(cid_hex)
#             if expected_chain_id and cid != expected_chain_id:
#                 raise RuntimeError(
#                     f"wrong-chainid: got {cid}, expected {expected_chain_id}"
#                 )
#             t1 = time.perf_counter()
#             block = _jsonrpc(url, "eth_getBlockByNumber", ["latest", False], timeout)
#             t2 = time.perf_counter()
#
#             ts_hex = block.get("timestamp")
#             base_fee = block.get("baseFeePerGas")
#             ts_int = _hex_to_int(ts_hex) if ts_hex else None
#
#             latency_ms = (t1 - t0 + t2 - t1) * 1000.0
#             staleness_s = max(0.0, time.time() - ts_int) if ts_int else None
#             eip1559 = base_fee is not None
#
#             return {
#                 "url": url,
#                 "chain_id": cid,
#                 "latency_ms": round(latency_ms, 2),
#                 "staleness_s": (
#                     round(staleness_s, 2) if staleness_s is not None else None
#                 ),
#                 "eip1559": eip1559,
#                 "client": "jsonrpc",
#             }
#         except Exception as e:
#             last_err = str(e)
#             time.sleep(0.15)  # مکث کوتاه و تلاش مجدد
#             continue
#     raise RuntimeError(last_err or "probe-failed")
#
#
# def _from_chainlist(
#         expected_chain_id: int, timeout: float = 6.0, max_urls: int = 20
# ) -> List[str]:
#     """
#     دریافت کاندیدها از Chainlist و فیلتر URL های HTTPS بدون نیاز به API key.
#     """
#     try:
#         r = requests.get(
#             "https://chainid.network/chains.json",
#             headers=UA,
#             timeout=(3, timeout),
#         )
#         r.raise_for_status()
#         chains = r.json()
#         urls: List[str] = []
#         for c in chains:
#             if c.get("chainId") != expected_chain_id:
#                 continue
#             for u in c.get("rpc", []):
#                 if not isinstance(u, str):
#                     continue
#                 if u.startswith("wss://"):
#                     continue
#                 if not u.startswith("https://"):
#                     continue
#                 if "${" in u:  # نیازمند کلید
#                     continue
#                 urls.append(u)
#         # حذف تکراری و محدودسازی
#         uniq = list(dict.fromkeys(urls))
#         random.shuffle(uniq)
#         return uniq[:max_urls]
#     except Exception:
#         return []
#
#
# def find_best_public_rpc(
#         chain: str,
#         *,
#         timeout: float = 6.0,
#         attempts: int = 2,
#         max_staleness_s: float = 90.0,
#         use_chainlist: bool = True,
#         return_all: bool = False,
#         top_k: int = 1,
#         debug: bool = False,
# ) -> Any:
#     """
#     بهترین RPC عمومی برای شبکه: eth | polygon | avax | bsc
#     """
#     net = _normalize_chain(chain)
#     if net not in EXPECTED_CHAIN_ID:
#         raise ValueError(f"شبکه پشتیبانی نمی‌شود: {chain}")
#     expected_cid = EXPECTED_CHAIN_ID[net]
#
#     # آماده‌سازی کاندیدها
#     candidates: List[str] = []
#     candidates.extend(STATIC_CANDIDATES.get(net, []))
#     if use_chainlist:
#         candidates.extend(_from_chainlist(expected_cid, timeout=timeout))
#     # حذف تکراری‌ها و ترتیب تصادفی
#     seen = set()
#     de_duped = []
#     for u in candidates:
#         if u not in seen:
#             seen.add(u)
#             de_duped.append(u)
#     random.shuffle(de_duped)
#
#     results = []
#     errors: Dict[str, str] = {}
#     for url in de_duped:
#         try:
#             m = _probe(url, expected_cid, timeout=timeout, attempts=attempts)
#             # امتیازدهی: latency کمتر و staleness کمتر بهتر است
#             st = m["staleness_s"] if m["staleness_s"] is not None else 0.0
#             penalty = 0.0
#             if m["staleness_s"] is not None and m["staleness_s"] > max_staleness_s:
#                 penalty = 10_000.0
#             score = (
#                     (10000.0 / (1.0 + m["latency_ms"])) + (5000.0 / (1.0 + st)) - penalty
#             )
#             m["score"] = round(score, 2)
#             results.append(m)
#         except Exception as e:
#             if debug:
#                 errors[url] = str(e)
#             continue
#
#     if not results:
#         if debug and errors:
#             # برای عیب‌یابی
#             raise RuntimeError(
#                 "هیچ RPC عمومی سالمی پیدا نشد. دلایل:\n"
#                 + "\n".join([f"- {u}: {err}" for u, err in errors.items()])
#             )
#         raise RuntimeError(f"هیچ RPC عمومی سالمی برای شبکه {chain} پیدا نشد")
#
#     results.sort(key=lambda x: (-x["score"], x["staleness_s"] or 0.0, x["latency_ms"]))
#
#     if return_all:
#         return results[: max(1, top_k)]
#     return results[0]["url"]

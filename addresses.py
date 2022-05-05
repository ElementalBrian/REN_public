
class mainnetTokens:
    eth_address = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    zeros_address = "0x0000000000000000000000000000000000000000"

    WETH = {"address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "decimals": 18, "symbol": "WETH"}
    DAI = {"address": "0x6B175474E89094C44Da98b954EedeAC495271d0F", "decimals": 18, "symbol": "DAI"}
    USDC = {"address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "decimals": 6, "symbol": "USDC"}
    USDT = {"address": "0xdAC17F958D2ee523a2206206994597C13D831ec7", "decimals": 6, "symbol": "USDT"}
    REN = {"address": "0x408e41876cCCDC0F92210600ef50372656052a38", "decimals": 18, "symbol": "REN"}
    WBTC = {"address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599", "decimals": 8, "symbol": "WBTC"}

    coin_to_decimal = {}
    address_to_coin = {}
    for token in [WETH, DAI, USDC, USDT, REN, WBTC]:
        coin_to_decimal[token["symbol"]] = token["decimals"]
        address_to_coin[token["address"]] = token["symbol"]


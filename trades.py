import json, time, datetime
from web3 import Web3

class IAmButASimpleFarmer():

    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8547'))
        self.uniswapabi = json.load(open('abi/uniswapV2abi.json', 'r'))
        self.uniswaprouterabi = json.load(open('abi/uniswaprouterabi.json', 'r'))
        self.erc20abi = json.load(open('abi/erc20abi.json', 'r'))
        self.wethabi = json.load(open('abi/wethabi.json', 'r'))

        self.imbalancer_wallet = self.web3.eth.account.privateKeyToAccount("0xe0a8f44bae8acd33ed45cc686b25c32fd7b2df98546128aa31e35d57dcadea79")
        self.trading_wallet = self.web3.eth.account.privateKeyToAccount("0x7dc6d289dc1b7b62afb34622be427c2d727e2baf1635b151929059310d4a8140")

        self.deadline = int(time.mktime(datetime.datetime.now().timetuple()) + 300000000)

        self.exchange_address_dict = {
            "Uniswap": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "Sushiswap": "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F",
            "Shebaswap": "0x03f7724180AA6b939894B5Ca4314783B0b36b329",
            "Sakeswap": "0x9C578b573EdE001b95d51a55A3FAfb45f5608b1f"}

        self.token_address_dict = {
            "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F"}

        self.exchange_contract_dict = {
            "Uniswap": self.web3.eth.contract(abi=self.uniswaprouterabi, address=self.exchange_address_dict["Uniswap"]),
            "Sushiswap": self.web3.eth.contract(abi=self.uniswaprouterabi, address=self.exchange_address_dict["Sushiswap"]),
            "Shebaswap": self.web3.eth.contract(abi=self.uniswaprouterabi, address=self.exchange_address_dict["Shebaswap"]),
            "Sakeswap": self.web3.eth.contract(abi=self.uniswaprouterabi, address=self.exchange_address_dict["Sakeswap"])}

        self.token_contract_dict = {
            "WETH": self.web3.eth.contract(abi=self.wethabi, address=self.token_address_dict["WETH"]),
            "DAI": self.web3.eth.contract(abi=self.erc20abi, address=self.token_address_dict["DAI"])}

        self.chainId = 1


    def approvals(self, contract, token, wallet):
        transaction = self.token_contract_dict[token].functions.approve(self.exchange_address_dict[contract], 10000000000000000000000000000).buildTransaction({'chainId': self.chainId, 'gas': self.web3.toHex(50000),'gasPrice': self.web3.toHex(self.web3.eth.gasPrice*100),'nonce': self.web3.toHex(self.web3.eth.getTransactionCount(wallet.address)), 'from': wallet.address})
        signedTx = self.web3.eth.account.signTransaction(transaction, wallet.privateKey)
        txhash = self.web3.eth.sendRawTransaction(signedTx.rawTransaction)
        print(f"approval for {contract} to spend {token} for {wallet.address}")

    def wrap_weth(self, amount, wallet):
        transaction = self.token_contract_dict["WETH"].functions.deposit().buildTransaction({'value': amount,'chainId': self.chainId, 'gas': self.web3.toHex(50000),'gasPrice': self.web3.toHex(self.web3.eth.gasPrice*100),'nonce': self.web3.toHex(self.web3.eth.getTransactionCount(wallet.address)), 'from': wallet.address})
        signedTx = self.web3.eth.account.signTransaction(transaction, wallet.privateKey)
        txhash = self.web3.eth.sendRawTransaction(signedTx.rawTransaction)
        print(f"wrapped {amount/10**18} WETH: {txhash.hex()}")

    def get_dai(self, amount, wallet):
        transaction = self.exchange_contract_dict["Uniswap"].functions.swapExactETHForTokens(1, [self.token_address_dict["WETH"], self.token_address_dict["DAI"]], wallet.address, 1666666666).buildTransaction({'value': amount, 'chainId': self.chainId, 'gas': self.web3.toHex(250000), 'gasPrice': self.web3.toHex(self.web3.eth.gasPrice*100),'nonce': self.web3.toHex(self.web3.eth.getTransactionCount(wallet.address)), 'from': wallet.address})
        signedTx = self.web3.eth.account.signTransaction(transaction, wallet.privateKey)
        txhash = self.web3.eth.sendRawTransaction(signedTx.rawTransaction)
        print(f"swapped {amount/10**18} ETH for DAI: {txhash.hex()}")

    def swap(self, exchange, amountIn, amountOutMin, inToken, outToken, wallet):
        transaction = self.exchange_contract_dict[exchange].functions.swapExactTokensForTokens(amountIn, amountOutMin, [inToken, outToken], wallet.address, self.deadline).buildTransaction({'chainId': self.chainId, 'gas': self.web3.toHex(250000), 'gasPrice': self.web3.toHex(self.web3.eth.gasPrice*100), 'nonce': self.web3.toHex(self.web3.eth.getTransactionCount(wallet.address)), 'from': wallet.address})
        signedTx = self.web3.eth.account.signTransaction(transaction, wallet.privateKey)
        txhash = self.web3.eth.sendRawTransaction(signedTx.rawTransaction)
        print(f"{wallet.address} swapped {amountIn/10**18} {inToken} for {outToken}: {txhash.hex()}")


    def prices(self, exchange, amount, inToken, outToken):
        prices = {
            "Uniswap":  (self.exchange_contract_dict["Uniswap"].functions.getAmountsOut(amount, [inToken, outToken]).call()[1]),
            "Shebaswap":  (self.exchange_contract_dict["Shebaswap"].functions.getAmountsOut(amount, [inToken, outToken]).call()[1]),
            "Sakeswap":  (self.exchange_contract_dict["Sakeswap"].functions.getAmountsOut(amount, [inToken, outToken]).call()[1]),
            "Sushiswap":  (self.exchange_contract_dict["Sushiswap"].functions.getAmountsOut(amount, [inToken, outToken]).call()[1])
        }
        return float(prices[exchange])


    def create_imbalances(self, wallet):
        print("making trades to create imbalances")
        self.wrap_weth(250*10**18, wallet)
        self.swap("Sushiswap", self.token_contract_dict["WETH"].functions.balanceOf(wallet.address).call(), 1000, self.token_address_dict["WETH"], self.token_address_dict["DAI"], wallet)
        self.swap("Uniswap", self.token_contract_dict["DAI"].functions.balanceOf(wallet.address).call(), 1000, self.token_address_dict["DAI"], self.token_address_dict["WETH"], wallet)


    def execute_setup(self, wallet):
        for exchange in self.exchange_address_dict:
            for token in self.token_contract_dict:
                self.approvals(exchange, token, wallet)

        # check prices at current levels
        eth_amount = 10*10**18
        dai_amount = 10000*10**18
        uni_weth_to_dai = self.prices("Uniswap", eth_amount, self.token_address_dict["WETH"], self.token_address_dict["DAI"])/10**18
        uni_dai_to_weth = self.prices("Sushiswap", dai_amount, self.token_address_dict["DAI"], self.token_address_dict["WETH"])/10**18
        print("uniswap weth to dai price for", str(eth_amount/10**18), str(uni_weth_to_dai))
        print("sushiswap dai to weth price for", str(dai_amount/10**18), str(uni_dai_to_weth))

        # use alternate account to create a large imbalance between uniswap and sushiswap
        self.create_imbalances(wallet)
        self.create_imbalances(wallet)

        # check prices after the imbalance
        eth_amount = 10*10**18
        dai_amount = 10000*10**18
        uni_weth_to_dai = self.prices("Uniswap", eth_amount, self.token_address_dict["WETH"], self.token_address_dict["DAI"])/10**18
        uni_dai_to_weth = self.prices("Sushiswap", dai_amount, self.token_address_dict["DAI"], self.token_address_dict["WETH"])/10**18
        print("uniswap weth to dai price for", str(eth_amount/10**18), str(uni_weth_to_dai))
        print("sushiswap dai to weth price for", str(dai_amount/10**18), str(uni_dai_to_weth))


    def print_balances(self, wallet):
        print("printing balances for", wallet.address)
        eth_balance = self.web3.eth.getBalance(wallet.address) / (10 ** 18)
        weth_balance = self.token_contract_dict["WETH"].functions.balanceOf(wallet.address).call() / (10 ** 18)
        dai_balance = self.token_contract_dict["DAI"].functions.balanceOf(wallet.address).call() / (10 ** 18)
        print(eth_balance, "ETH in wallet")
        print(weth_balance, "WETH in wallet")
        print(dai_balance, "DAI in wallet")
        print("total ETH balance:", eth_balance + weth_balance)
        return eth_balance + weth_balance


    def execute_trades(self, wallet):
        starting_eth_balance = self.web3.eth.getBalance(wallet.address) / (10 ** 18)
        print(starting_eth_balance, "ETH in wallet")
        print(self.token_contract_dict["WETH"].functions.balanceOf(wallet.address).call() / (10 ** 18), "WETH in wallet")
        print(self.token_contract_dict["DAI"].functions.balanceOf(wallet.address).call() / (10 ** 18), "DAI in wallet")

        self.wrap_weth(10*10**18, self.trading_wallet)

        for exchange in self.exchange_address_dict:
            for token in self.token_contract_dict:
                self.approvals(exchange, token, self.trading_wallet)

        self.print_balances(self.trading_wallet)

        print('making trades for fun and profit..')
        self.swap("Uniswap", self.token_contract_dict["WETH"].functions.balanceOf(self.trading_wallet.address).call(), 1000, self.token_address_dict["WETH"], self.token_address_dict["DAI"], self.trading_wallet)

        self.swap("Sushiswap", self.token_contract_dict["DAI"].functions.balanceOf(self.trading_wallet.address).call(), 1000, self.token_address_dict["DAI"], self.token_address_dict["WETH"], self.trading_wallet)

        print("total profit:", self.print_balances(self.trading_wallet) - starting_eth_balance, "ETH")

    def run(self):
        self.execute_setup(self.imbalancer_wallet)
        self.execute_trades(self.trading_wallet)

if __name__ == "__main__":
    start = IAmButASimpleFarmer()
    start.run()

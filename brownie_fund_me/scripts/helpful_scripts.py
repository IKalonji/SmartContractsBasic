from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
INITIAL_ANSWER = 200000000000
LOCAL_ENVIRONMENT_BLOCKCHAIN = ['development', 'ganache-home']
FORKED_LOCAL_ENV = ['mainnet-fork', 'mainnet-fork-dev']

def get_account():
    if (network.show_active() in LOCAL_ENVIRONMENT_BLOCKCHAIN or network.show_active() in FORKED_LOCAL_ENV):
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])

def deploy_mocks():
    print("Active network is ", network.show_active())
    print("Deploying mocks")
    if len(MockV3Aggregator)<=0:
        MockV3Aggregator.deploy(DECIMALS, INITIAL_ANSWER, {"from": get_account()})
    return MockV3Aggregator[-1].address
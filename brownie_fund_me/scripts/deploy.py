from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_ENVIRONMENT_BLOCKCHAIN, FORKED_LOCAL_ENV

def deploy_fund_me():
    account = get_account()

    if (network.show_active() not in LOCAL_ENVIRONMENT_BLOCKCHAIN):
        price_feed_address = config['networks'][network.show_active()]['usd_eth_pricefeed']
    else:
        price_feed_address = deploy_mocks()
    fund_me = FundMe.deploy(price_feed_address, {"from":account}, publish_source=config["networks"][network.show_active()].get("verify"))
    print("Fund Me contrract deployed")

def main():
    deploy_fund_me()
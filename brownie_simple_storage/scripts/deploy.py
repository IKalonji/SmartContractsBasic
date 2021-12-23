from brownie import accounts, config, SimpleStorage, network

def deploy_simple_storage():
    account = get_account()
    # account = accounts.load("freecodecamp")
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)

    simple_storage = SimpleStorage.deploy({"from": account})
    print(simple_storage)
    stored_value = simple_storage.retrieve()
    print("stored value ", stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    stored_value2 = simple_storage.retrieve()
    print(stored_value2)

def get_account():
    if (network.show_active == 'development'):
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])

def main():
    deploy_simple_storage()
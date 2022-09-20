from algosdk import account, mnemonic

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print(private_key)
    print("My address: {}".format(address))
    print("My passphrase:\n{}".format(mnemonic.from_private_key(private_key)))


generate_algorand_keypair()
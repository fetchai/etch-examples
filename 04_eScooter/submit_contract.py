from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address
import sys
import time

def main(source, name):
    # Create keypair for the contract owner
    provider1 = Entity()
    address1 = Address(provider1)
    provider2 = Entity()
    address2 = Address(provider2)

    scooter1 = Entity()
    scooter_address1 = Address(scooter1)


    
    # Setting API up
    api = LedgerApi('127.0.0.1', 8100)

    # Need funds to deploy contract
    api.sync(api.tokens.wealth(provider1, 59000000))

    # Create contract
    contract = SmartContract(source)

    # Deploy contract
    api.sync(api.contracts.create(provider1, contract, 2456766))

    if name.endswith("contract.etch"):
        contract.action(api, 'addProvider', 2456766, [provider2, provider1], address2, address1 )
        contract.action(api, 'addScooter', 2456766, [provider2, provider1], address2, address1, 22, 1 )        

        print("Wait for txs to be mined ...")
        time.sleep(5)
        
        # Printing balance of the creating address1
        print(contract.query(api, 'getFleetSize'), " scooter in fleet")

if __name__ == '__main__': 
    # Loading contract
    if len(sys.argv) != 2:
      print("Usage: ", sys.argv[0], "[filename]")
      exit(-1)

    with open(sys.argv[1], "r") as fb:
      source = fb.read()

    main(source, sys.argv[1])
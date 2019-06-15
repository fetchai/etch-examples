from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address
import sys
import time

def main(source):
    # Create keypair for the contract owner
    entity = Entity()
    address = Address(entity)
    
    # Setting API up
    api = LedgerApi('127.0.0.1', 8100)

    # Need funds to deploy contract
    api.sync(api.tokens.wealth(entity, 5000000))

    # Create contract
    contract = SmartContract(source)

    # Deploy contract
    api.sync(api.contracts.create(entity, contract, 2456766))

    # Printing message
    print(contract.query(api, 'balanceOf', owner = address)) 

if __name__ == '__main__': 
    # Loading contract
    if len(sys.argv) != 2:
      print("Usage: ", sys.argv[0], "[filename]")
      exit(-1)

    with open(sys.argv[1], "r") as fb:
      source = fb.read()

    main(source)
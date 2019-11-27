from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import Contract
from fetchai.ledger.crypto import Entity, Address
import sys
import time

def main(source, train_data, train_labels, test_data, test_labels):

    # Create keypair for the contract owner
    entity = Entity()
    address = Address(entity)

    # Setting API up
    api = LedgerApi('127.0.0.1', 8000)

    # Need funds to deploy contract
    api.sync(api.tokens.wealth(entity, 10000000000000))

    # Create contract
    contract = Contract(source, entity)

    # Deploy contract
    api.sync(api.contracts.create(entity, contract, 1000000000))

    # # evaluate loss after training
    # print(contract.query(api, 'evaluate'))
    #
    # # evaluate loss after training
    # print(contract.query(api, 'evaluate'))
    #
    # # evaluate loss after training
    # print(contract.query(api, 'evaluate'))

if __name__ == '__main__':

    # Loading contract
    if len(sys.argv) != 6:
      print("Usage: ", sys.argv[0], "[filename] train_data.csv train_labels.csv test_data.csv test_labels.csv")
      exit(-1)

    with open(sys.argv[1], "r") as fb:
      source = fb.read()

    main(source, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
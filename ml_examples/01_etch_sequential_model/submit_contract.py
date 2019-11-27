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
    api.sync(api.tokens.wealth(entity, 100000))

    # Create contract
    contract = Contract(source, entity)

    # Deploy contract
    api.sync(api.contracts.create(entity, contract, 10000))

    # Printing message
    print(contract.action(api, 'main'))


def read_csv():


    return data

if __name__ == '__main__':

    # Loading contract
    if len(sys.argv) != 6:
      print("Usage: ", sys.argv[0], "[filename] train_data.csv train_labels.csv test_data.csv test_labels.csv")
      exit(-1)

    with open(sys.argv[1], "r") as fb:
      source = fb.read()

    read_csv

    main(source, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
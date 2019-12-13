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
    api.sync(contract.create(api, entity, 1000000000))

    # Run the synergetic contract

    # combine the data and label into one string for passing into the createProblem function
    data_string = contract.query(api, 'getData')
    label_string = contract.query(api, 'getLabel')
    print("initial data: " + data_string)
    print("initial label: " + label_string)

    # TODO : combine data and label

    # pass the combined input data
    api.sync(api.contracts.submit_data(entity, contract.digest, contract.address, value = (data_string + label_string)))
    api.wait_for_blocks(10)
    result = contract.query(api, 'query_result')



    # evaluate the initial loss
    initial_loss = contract.query(api, 'evaluate')
    print("initial loss: " + initial_loss)

    # grab the data and label tensor
    data_string = contract.query(api, 'getData')
    label_string = contract.query(api, 'getLabel')
    print("initial data: " + data_string)
    print("initial label: " + label_string)

    # train on some input data
    fet_tx_fee = 16000000
    api.sync(contract.action(api, 'train', fet_tx_fee, [entity], data_string, label_string))

    # predict loss after training
    prediction = contract.query(api, 'predict', data_string=data_string)
    print("model prediction: " + prediction)

if __name__ == '__main__':

    # Loading contract
    if len(sys.argv) != 6:
      print("Usage: ", sys.argv[0], "[filename] train_data.csv train_labels.csv test_data.csv test_labels.csv")
      exit(-1)

    with open(sys.argv[1], "r") as fb:
      source = fb.read()

    main(source, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
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
    # api.sync(api.contracts.create(entity, contract, 1000000000))
    api.sync(contract.create(api, entity, 1000000000))

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
    contract.action(api, 'train', fet_tx_fee, [entity], data_string, label_string)

    # # evaluate loss after training
    # print(contract.query(api, 'evaluate'))

# def setData(self):
#     """Function to set the historic data to the contract."""
#
#     new_data = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]]
#
#     seperator = ","
#     for items in self.data[len(self.data) - (256 + 32): len(self.data) - 32]:
#         mData.append(items["close"])
#
#     allData = seperator.join(map(str, mData))
#     fet_tx_fee = 100000000
#     self.api.sync(self.contract.action(
#         self.api, 'setHistorics', fet_tx_fee, [self.entity], allData))
#     print("Finished the setHistorics on the Contract")

if __name__ == '__main__':

    # Loading contract
    if len(sys.argv) != 6:
      print("Usage: ", sys.argv[0], "[filename] train_data.csv train_labels.csv test_data.csv test_labels.csv")
      exit(-1)

    with open(sys.argv[1], "r") as fb:
      source = fb.read()

    main(source, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
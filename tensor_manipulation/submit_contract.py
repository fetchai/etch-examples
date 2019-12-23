import os

from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import Contract
from fetchai.ledger.crypto import Entity, Address

HERE = os.path.dirname(__file__)


# generic contract setup
def contract_setup(source, benefactor, options):
    # Create keypair for the contract owner
    entity1 = Entity()
    Address(entity1)

    host = options['host']
    port = options['port']
    # create the APIs
    api = LedgerApi(host, port)

    # Transfer tokens from benefactor
    api.sync(api.tokens.transfer(benefactor, entity1, int(1e8), 1000))

    # Create contract
    contract = Contract(source, entity1)

    # Deploy contract
    api.sync(contract.create(api, entity1, api.tokens.balance(entity1)))

    return api, contract, entity1


# run function for running on end to end tests
def run(options, benefactor):
    source_file = os.path.join(HERE, "tensor_manipulation_contract.etch")

    with open(source_file, "r") as fp:
        source = fp.read()

    print(options)

    if benefactor is None or options is None:
        raise Exception("Must give options and benefactor")

    api, contract, entity = contract_setup(source, benefactor, options)

    # add two tensors and get result
    data_string = "2,3,4,5"
    label_string = "1,2,3,4"
    api.sync(contract.action(api, 'add', api.tokens.balance(entity),
                             [entity], data_string, label_string))
    prediction = contract.query(api, 'getOutput')
    print("Ouput is: " + prediction)

    # subtract two tensors and get result
    api.sync(contract.action(api, 'subtract', api.tokens.balance(entity),
                             [entity], data_string, label_string))
    prediction = contract.query(api, 'getOutput')
    print("Ouput is: " + prediction)

    api.sync(contract.action(api, 'multiply', api.tokens.balance(entity),
                             [entity], data_string, label_string))
    prediction = contract.query(api, 'getOutput')
    print("Ouput is: " + prediction)

    api.sync(contract.action(api, 'divide', api.tokens.balance(entity),
                             [entity], data_string, label_string))
    prediction = contract.query(api, 'getOutput')
    print("Ouput is: " + prediction)

    api.sync(contract.action(api, 'copy', api.tokens.balance(entity),
                             [entity], data_string))
    prediction = contract.query(api, 'getOutput')
    print("Ouput is: " + prediction)

    api.sync(contract.action(api, 'at', api.tokens.balance(entity),
                             [entity], data_string, 3))
    prediction = contract.query(api, 'getOutput')
    print("Ouput is: " + prediction)

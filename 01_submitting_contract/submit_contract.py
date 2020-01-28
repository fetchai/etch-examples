import os
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import Contract
from fetchai.ledger.crypto import Entity, Address

HERE = os.path.dirname(__file__)


def run(options, benefactor):
    # Create keypair for the contract owner
    entity = Entity()
    Address(entity)

    host = options['host']
    port = options['port']

    # create the APIs
    api = LedgerApi(host, port)

    # Transfer tokens from benefactor
    api.sync(api.tokens.transfer(benefactor, entity, int(1e7), 1000))

    # Load contract source
    source_file = os.path.join(HERE, "hello_world.etch")
    with open(source_file, "r") as fb:
        source = fb.read()

    # Create contract
    contract = Contract(source, entity)

    # Deploy contract
    api.sync(api.contracts.create(entity, contract, 10000))

    # Printing message
    print(contract.query(api, 'persistentGreeting'))

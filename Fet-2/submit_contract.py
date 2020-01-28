import os

from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import Contract
from fetchai.ledger.crypto import Entity, Address

HERE = os.path.dirname(__file__)


def run(options, benefactor):
    # Create keypair for the contract owner
    entity = Entity()
    address = Address(entity)

    # build the ledger API
    api = LedgerApi(options['host'], options['port'])

    # Need funds to deploy contract
    api.sync(api.tokens.transfer(benefactor, entity, int(1e7), 1000))

    # Load contract source
    source_file = os.path.join(HERE, "contract.etch")
    with open(source_file, "r") as fb:
        source = fb.read()

    # Create contract
    contract = Contract(source, entity)

    # Deploy contract
    fet_tx_fee = api.tokens.balance(entity)
    api.sync(api.contracts.create(entity, contract, fet_tx_fee))

    # Printing balance of the creating address
    print(contract.query(api, 'balanceOf', owner=address))

    # Getting the 9'th token id.
    token_id = contract.query(api, 'getTokenId', number=9)

    # Testing
    contract.query(api, 'isEqual', number=9, expected=token_id)

    # Locating the owner of a token
    print("Finding the owner of ", token_id)
    print(contract.query(api, 'ownerOf', token_id=token_id))

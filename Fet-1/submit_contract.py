from contextlib import contextmanager
from typing import List

from fetchai.ledger.api import LedgerApi, TokenApi
from fetchai.ledger.contract import Contract
from fetchai.ledger.crypto import Entity, Address


def print_address_balances(api: LedgerApi, contract: Contract, addresses: List[Address]):
    for idx, address in enumerate(addresses):
        print('Address{}: {:<6d} bFET {:<10d} TOK'.format(idx, api.tokens.balance(address),
                                                          contract.query(api, 'balanceOf', address=address)))
    print()


@contextmanager
def track_cost(api: TokenApi, entity: Entity, message: str):
    """
    Context manager for recording the change in balance over a set of actions
    Will be inaccurate if other factors change an account balance
    """
    if isinstance(entity, Entity):
        entity = Address(entity)
    elif not isinstance(entity, Address):
        raise TypeError("Expecting Entity or Address")

    balance_before = api.balance(entity)
    yield

    if not message:
        message = "Actions cost: "

    print(message + "{} TOK".format(api.balance(entity) - balance_before))


def main():
    # create our first private key pair
    entity1 = Entity()
    address1 = Address(entity1)

    # create a second private key pair
    entity2 = Entity()
    address2 = Address(entity2)

    # build the ledger API
    api = LedgerApi('127.0.0.1', 8000)

    # create wealth so that we have the funds to be able to create contracts on the network
    api.sync(api.tokens.wealth(entity1, 10000))

    # create the smart contract
    contract = Contract(CONTRACT_TEXT, entity1)

    with track_cost(api.tokens, entity1, "Cost of creation: "):
        api.sync(contract.create(api, entity1, 4000))

    # print the current status of all the tokens
    print('-- BEFORE --')
    print_address_balances(api, contract, [address1, address2])

    # transfer from one to the other using our newly deployed contract
    tok_transfer_amount = 200
    fet_tx_fee = 160
    with track_cost(api.tokens, entity1, "Cost of transfer: "):
        api.sync(contract.action(api, 'transfer', fet_tx_fee, [entity1], address1, address2, tok_transfer_amount))

    print('-- AFTER --')
    print_address_balances(api, contract, [address1, address2])


if __name__ == '__main__': 
    # Loading contract
    if len(sys.argv) != 2:
      print("Usage: ", sys.argv[0], "[filename]")
      exit(-1)

    with open(sys.argv[1], "r") as fb:
      source = fb.read()

    main(source)
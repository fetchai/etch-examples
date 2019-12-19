import os

from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import Contract
from fetchai.ledger.crypto import Entity, Address

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, "..", "data")

REGRESSION_DATA_TRAIN_FILE = os.path.join(DATA_DIR, "boston_train_data.csv")  # 5 training examples
REGRESSION_LABEL_TRAIN_FILE = os.path.join(DATA_DIR, "boston_train_label.csv")  # 5 training labels
REGRESSION_DATA_TEST_FILE = os.path.join(DATA_DIR, "boston_test_data.csv")  # 4 test examples
REGRESSION_LABEL_TEST_FILE = os.path.join(DATA_DIR, "boston_test_label.csv")  # 4 test labels

CLASSIFICATION_DATA_TRAIN_FILE = os.path.join(DATA_DIR, "mnist_train_data.csv")  # 1 training example
CLASSIFICATION_LABEL_TRAIN_FILE = os.path.join(DATA_DIR, "mnist_train_label.csv")  # 1 training label
CLASSIFICATION_DATA_TEST_FILE = os.path.join(DATA_DIR, "mnist_test_data.csv")  # 1 test example
CLASSIFICATION_LABEL_TEST_FILE = os.path.join(DATA_DIR, "mnist_test_label.csv")  # 1 test label


# generic contract setup
def contract_setup(source, benefactor, options):
    # Create keypair for the contract owner
    entity1 = Entity()
    Address(entity1)
    entity2 = Entity()
    Address(entity2)

    host = options['host']
    port = options['port']
    # create the APIs
    api = LedgerApi(host, port)

    # Transfer tokens from benefactor
    api.sync(api.tokens.transfer(benefactor, entity1, int(1e7), 1000))
    api.sync(api.tokens.transfer(benefactor, entity2, int(1e7), 1000))

    # Create contract
    contract = Contract(source, entity1)

    # Deploy contract
    api.sync(contract.create(api, entity1, int(1e7)))

    return api, contract, entity1, entity2


# helper function for reading in training data
def read_csv_as_string(fname):
    f = open(fname, 'r')
    return f.read()


def load_data(mode, training=True):
    if mode == "boston":

        if training:
            data_file = REGRESSION_DATA_TRAIN_FILE
            label_file = REGRESSION_LABEL_TRAIN_FILE
        else:
            data_file = REGRESSION_DATA_TEST_FILE
            label_file = REGRESSION_LABEL_TEST_FILE

    elif mode == "mnist":

        if training:
            data_file = CLASSIFICATION_DATA_TRAIN_FILE
            label_file = CLASSIFICATION_LABEL_TRAIN_FILE
        else:
            data_file = CLASSIFICATION_DATA_TEST_FILE
            label_file = CLASSIFICATION_LABEL_TEST_FILE
    else:
        raise Exception("Unknown mode")

    data_string = read_csv_as_string(data_file)
    label_string = read_csv_as_string(label_file)

    return data_string, label_string


def train_and_evaluate(api, contract, entity, data_string, label_string):
    # train on the input data
    fet_tx_fee = api.tokens.balance(entity)
    api.sync(contract.action(api, 'train', fet_tx_fee, [entity], data_string, label_string))

    # evaluate the initial loss
    initial_loss = contract.query(api, 'evaluate')
    print("initial_loss: " + initial_loss)


def main(source, mode, benefactor, options):
    api, contract, entity1, entity2 = contract_setup(source, benefactor, options)

    # load training data
    train_data_string, train_label_string = load_data(mode)
    print("initial data: " + train_data_string)
    print("initial label: " + train_label_string)

    # train and evaluate
    train_and_evaluate(api, contract, entity1, train_data_string, train_label_string)

    # make a prediction on the training data
    prediction = contract.query(api, 'predict', data_string=train_data_string)
    print("model training prediction: " + prediction)

    # load different set of data
    test_data_string, test_label_string = load_data(mode, False)
    print("test data: " + test_data_string)
    print("test label: " + test_label_string)

    # entity2 decides to set some new data and label
    fet_tx_fee = 160000
    api.sync(contract.action(api, 'setDataAndLabel', fet_tx_fee, [entity2], test_data_string, test_label_string))

    # entity 1 grabs the latest data for inspection
    # we don't need to do this - but we just demonstrate how here
    retrieved_test_data_string = contract.query(api, 'getData')
    retrieved_test_label_string = contract.query(api, 'getLabel')
    print("some new data: " + retrieved_test_data_string)
    print("some new label: " + retrieved_test_label_string)

    # entity 1 makes a prediction on the new (test) data
    prediction = contract.query(api, 'predict', data_string=retrieved_test_data_string)
    print("model test prediction: " + prediction)


# run function for running on end to end tests
def run(options, benefactor):
    mode = options.get("mode", "boston")
    if mode == "mnist":
        source_file = os.path.join(HERE, "model_classifier.etch")
    elif mode == "boston":
        source_file = os.path.join(HERE, "model_regressor.etch")
    else:
        raise Exception("Unknown mode: " + mode)

    with open(source_file, "r") as fp:
        source = fp.read()

    print(options)

    if benefactor is None or options is None:
        raise Exception("Must give options and benefactor")
    main(source, mode, benefactor, options)

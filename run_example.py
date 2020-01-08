import fnmatch
import os
import sys
from os.path import dirname, exists, join

# script to run etch-example using run_end_to_end_test.py

# NB: The script for running the smart contract needs to have a run function

HERE = dirname(__file__)
LEDGER_DIR = join(HERE, '..', 'ledger')
BUILD_DIR = join(LEDGER_DIR, 'build-debug')


def clean_files(build_root):
    """Clean files that are likely to interfere with testing"""
    for root, _, files in os.walk(build_root):
        for path in fnmatch.filter(files, '*.db'):
            data_path = join(root, path)
            print('Removing file:', data_path)
            os.remove(data_path)


def test_end_to_end(build_root, name_filter=None, ledger_dir=LEDGER_DIR):
    sys.path.append(ledger_dir)
    sys.path.append(os.path.join(ledger_dir, 'scripts', 'fetchai_netutils'))
    from scripts.end_to_end_test import run_end_to_end_test

    yaml_file = join(HERE, 'examples.yaml')

    # Check that the YAML file does exist
    if not exists(yaml_file):
        print('Failed to find yaml file for end_to_end testing:', yaml_file)
        sys.exit(1)

    # should be the location of constellation exe - if not the test will catch
    constellation_exe = join(build_root, 'apps/constellation/constellation')

    clean_files(build_root)

    run_end_to_end_test.run_test(
        build_root, yaml_file, constellation_exe, name_filter)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Run smart contracts using end_to_end_tests.')
    parser.add_argument('--ledger_dir', help='directory root for ledger, e.g. ./ledger',
                        default=LEDGER_DIR)
    parser.add_argument('--build_dir', help='directory root for constellation build, e.g. ./ledger/build-debug',
                        default=BUILD_DIR)
    parser.add_argument('--test_name', help="Name of test to run in examples.yaml file. Leave blank to run all tests.",
                        default=None)

    args = parser.parse_args()
    print(args)
    test_end_to_end(args.build_dir, args.test_name, args.ledger_dir)

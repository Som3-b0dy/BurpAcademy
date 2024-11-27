import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=True,
                        help='Add a target URL to exploit SQLi')
    parser.add_argument('-x', '--proxy', help='Add address to proxy traffic')
    return parser.parse_args()

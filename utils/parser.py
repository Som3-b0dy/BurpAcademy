import argparse

class Namespace:
    pass

def parse_args():
    n = Namespace()
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=True, help='Add a target URL to exploit SQLi')
    parser.add_argument('-x', '--proxy', default=False, help='Add address to proxy traffic', action='store_true')
    parser.parse_args(namespace=n)
    return n
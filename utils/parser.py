import argparse


def strip_url(args):
    if args.url.endswith('/'):
        args.url = args.url[:-1]
    return args


def parse_args():  # Initialising our parser for command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=True,
                        help='Add a target URL to exploit SQLi')
    parser.add_argument('-x', '--proxy', help='Add address to proxy traffic')
    args = parser.parse_args()
    args = strip_url(args)
    return args

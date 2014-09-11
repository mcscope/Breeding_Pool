import argparse


parser = argparse.ArgumentParser(description='A genetic simulation')
parser.add_argument('--mutation_rate', type=float, default = 0.1,
                   help='the chance a gene will mutate during a single breeding. 0-1')
parser.add_argument('--constant_mutation_depth', type=float, default = 1.0,
                   help='the chance a gene will mutate during a single breeding. 0-1')

parser.add_argument('--multi_mutation_depth', type=float, default = 0.1,
                   help='the chance a gene will mutate during a single breeding. 0-1')


options = parser.parse_args()




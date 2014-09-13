import argparse


parser = argparse.ArgumentParser(description='A genetic simulation')
parser.add_argument('--mutation_rate', type=float, default = 0.1,
                   help='the chance a gene will mutate during a single breeding. 0-1')
parser.add_argument('--constant_mutation_depth', type=float, default = 1.0,
                   help='how much a constant can mutate in one breeding')

parser.add_argument('--multi_mutation_depth', type=float, default = 0.1,
                   help='how much a multi can mutate in one breeding')


parser.add_argument('--constant_max_init', type=float, default = 255.0,
                   help='inital max value for constants')

parser.add_argument('--multi_max_init', type=float, default = 3.0,
                   help='inital max value for multis')

parser.add_argument('--new_gene_chance', type=float, default = 0.01,
                   help='chance of spontaneously making a new gene while making a gamete')



parser.add_argument('--multi_chance', type=float, default = 0.05,
                   help='chance of a random gene being a multi')


parser.add_argument('--xcells', type=int, default = 60,
                   help='width in cells')


parser.add_argument('--ycells', type=int, default = 60,
                   help='height in cells')

parser.add_argument('--cellsize', type=int, default = 10,
                   help='height in cells')



parser.add_argument('--show_genes', type=bool, default = False,
                   help='inital max value for multis')

options = parser.parse_args()




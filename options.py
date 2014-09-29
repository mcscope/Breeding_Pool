import argparse


parser = argparse.ArgumentParser(description='A genetic simulation')

parser.add_argument('--constant_mutation_depth', type=float, default = 4.0,
                   help='how much a constant can mutate in one breeding')

parser.add_argument('--multi_mutation_depth', type=float, default = 0.2,
                   help='how much a multi can mutate in one breeding')


parser.add_argument('--constant_max_init', type=float, default = 100.0,
                   help='inital max value for constants')

parser.add_argument('--multi_max_init', type=float, default = 2.0,
                   help='inital max value for multis')


parser.add_argument('--xcells', type=int, default = 80,
                   help='width in cells')


parser.add_argument('--ycells', type=int, default = 60,
                   help='height in cells')

parser.add_argument('--cellsize', type=int, default = 14,
                   help='width and height of the cells in pixels')

parser.add_argument('--width', type=float, default = 500.0,
                   help='width (swarmsim)')

parser.add_argument('--height', type=float, default = 500.0,
                   help='height (swarmsim)')

parser.add_argument('--fullscreen', type=bool, default = False,
                   help='display fullscreen')

parser.add_argument('--crosses', type=bool, default = False,
                   help='plants display as crosses')



parser.add_argument('--show_genes', type=bool, default = False,
                   help='str of a creature shows geneome, not ph')

options = parser.parse_args()




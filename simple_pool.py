from life import Creature, breed
import random

def cull_and_refill(gene_pool):
    size = len(gene_pool)
    cull_size = size//10
    sorted_pool = sorted(gene_pool, key=lambda x: x.penis_length, reverse=True)
    print sorted_pool[0]
    culled = sorted_pool[0:cull_size]
    return [breed(random.choice(culled), random.choice(culled)) for x in xrange(0,size)]

gene_pool = [Creature() for x in xrange(0,100000)]
for x in range(0,100):
    gene_pool = cull_and_refill(gene_pool)

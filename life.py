from genome import Genome, MutationRate
from options import options

class Creature(object):
    mutation_rate = MutationRate(mutation_rate=0.0, new_gene_chance=0.0, multi_chance=0.0)
    trait_ranges={"example_trait":(-1,1)}
    def __init__(self, genome=None,  ploida=None, ploidb=None, **kw):
        if genome:
            self.genome = genome
        elif ploida and ploidb:
            self.genome = Genome(ploida, ploidb)
        else:
            self.genome = Genome.random(self.traits, self.mutation_rate)
        self.phenotype = self.genome.make_phenotype(self.trait_ranges)
        self.__dict__.update(self.phenotype)

        self.subclass_init( **kw)

    def subclass_init(self, **kw):
        pass
    @property
    def traits(self):
        if not getattr(self, '_traits', None):
            self._traits = self.trait_ranges.keys()

        return self._traits

    def __str__(self):
        if options.show_genes:
            return str(self.genome)
        else:
            return str(self.phenotype)


def breed(creaturea, creatureb, **kw):
    if creaturea.__class__ != creatureb.__class__:
        raise Exception("Impossible to breed - mismatching classes")
    return creaturea.__class__(ploida=creaturea.genome.make_gamete(creaturea.mutation_rate), ploidb=creatureb.genome.make_gamete(creaturea.mutation_rate), **kw)

def bud(creature, **kw):
    return creature.__class__(genome=creature.genome.mutate(mutation_rate= creature.mutation_rate), **kw)

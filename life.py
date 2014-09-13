from genome import Genome
from options import options

class Creature(object):
    traits = ['strength', 'size', 'ferocity', 'anger', 'health', 'penis_length']

    def __init__(self, genome=None,  ploida=None, ploidb=None, **kw):
        if genome:
            self.genome = genome
        elif ploida and ploidb:
            self.genome = Genome(ploida, ploidb)
        else:
            self.genome = Genome.random(self.traits)
        self.phenotype = self.genome.make_phenotype()
        self.__dict__.update(self.phenotype)

        self.subclass_init( **kw)

    def subclass_init(self, **kw):
        pass

    def __str__(self):
        if options.show_genes:
            return str(self.genome)
        else:
            return str(self.phenotype)


def breed(creaturea, creatureb, **kw):
    if creaturea.__class__ != creatureb.__class__:
        raise Exception("Impossible to breed - mismatching classes")
    return creaturea.__class__(ploida=creaturea.genome.make_gamete(), ploidb=creatureb.genome.make_gamete(), **kw)

def bud(creature, **kw):
    return creature.__class__(genome=creature.genome.mutate(), **kw)

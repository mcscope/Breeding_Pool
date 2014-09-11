import random
from options import options
from utils import dictobj


class Phenotype(dictobj):
    pass


class Genome(object):

    """
    A genome is a group of genes - two of each type.
    It is all the genetic information that a creature would have"""

    def __init__(self, ploid_a, ploid_b):
        if ploid_a.keys() != ploid_b.keys():
            raise Exception("chromosome mismatch. You'd have a mule")

        self.chromosome = {trait: (ploid_a[trait], ploid_b[trait])
                            for trait in ploid_a.keys()}

    def make_phenotype(self):
        phenotype_values = {trait: self.combine(*genes)
                            for trait, genes in self.chromosome.iteritems()}
        return Phenotype(**phenotype_values)

    def make_gamete(self):
        return {trait: random.choice(genes).reproduce()
                for trait, genes in self.chromosome.iteritems()}

    @staticmethod
    def combine(genea, geneb):
        """
        Use Randall Monroe's gene mutlplier/constant system.
        He inspired this program
        """
        if type(genea) == Constant and type(geneb) == Constant:
            return max(genea.value, geneb.value)

        elif type(genea) == Multiplier and type(geneb) == Multiplier:
            return 1

        elif type(genea) == Constant and type(geneb) == Multiplier or \
            type(genea) == Multiplier and type(geneb) == Constant:
            return genea.value * geneb.value

        raise Exception("Should never reach this point - unknown gene type")


class Gene(object):

    """
    A gene represents a single allele.
    Once created, it's value never changes
    """

    def __init__(self, value=None):
        if value:
            self.value = value
        else:
            self.value = self.random_value()
    def reproduce(self):
        if random.random() < options.mutation_rate:

            return self.__class__(self._mutate())
        return self


class Constant(Gene):
    def random_value():
        return random.random * 20

    def _mutate(self):
        return self.value + options.constant_mutation_depth * (2 * random.random() - 1)


class Multiplier(Gene):

    def random_value():
        return random.random * 3

    def _mutate(self):
        return self.value + options.multi_mutation_depth * (2 * random.random() - 1)

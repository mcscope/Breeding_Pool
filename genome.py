import random
from options import options
from utils import dictobj
from collections import namedtuple
import math

# do not edit! added by PythonBreakpoints
from pudb import set_trace as _breakpoint


MutationRate = namedtuple("MutationRate", ['mutation_rate', "new_gene_chance", 'multi_chance'])


class Gene(object):

    """
    A gene represents a single allele.
    Once created, it's value never changes
    """

    def __init__(self, mutation_rate, value=None):
        if self.__class__ == Gene:
            if random.random() < mutation_rate.multi_chance:
                self.__class__ = Multiplier
            else:
                self.__class__ = Constant
        if value:
            self.value = value
        else:
            self.value = self.random_value()

        self.mutation_rate = mutation_rate

    def reproduce(self, mutation_rate = None):
        if random.random() < mutation_rate.mutation_rate:
            return self.__class__(mutation_rate, value=self._mutate())
        return self

    def random_value(self):
        raise NotImplementedError

    def _mutate(self):
        raise NotImplementedError

    def __str__(self):
        return "%s(%1.1f)" % (self.str_symb, self.value)

    def __repr__(self):
        return "%s(%f)" % (self.str_symb, self.value)

class Constant(Gene):
    str_symb = "C"
    def random_value(self):
        return random.random() * options.constant_max_init

    def _mutate(self):
        mutate_val = self.value + options.constant_mutation_depth * (random.random() + random.random() - 1)
        return max(0, mutate_val)

class Multiplier(Gene):
    str_symb = "M"

    def random_value(self):
        return random.random() * options.multi_max_init

    def _mutate(self):
        mutate_val = self.value + options.multi_mutation_depth * (random.random() + random.random() - 1)
        return max(0, mutate_val)

gene_types = [Constant, Multiplier]

class Genome(object):

    """
    A genome is a group of genes - two of each type.
    It is all the genetic information that a creature would have
    """


    def __init__(self, ploid_a, ploid_b):
        if ploid_a.keys() != ploid_b.keys():
            raise Exception("chromosome mismatch. You'd have a mule")

        self.chromosome = {trait: (ploid_a[trait], ploid_b[trait])
                            for trait in ploid_a.keys()}

    @classmethod
    def random(cls, traits, mutation_rate):
        ploid_a = {trait:Gene(mutation_rate) for trait in traits}
        ploid_b = {trait:Gene(mutation_rate) for trait in traits}
        return cls(ploid_a, ploid_b)

    def map_genome_codings_to_phenotype(self, genome_codings, trait_ranges):
        # formula is (min-max)sin(x ** 1/2) + (1 + min)
        # forces a smooth transition between values in the range (so no mod cliff)
        # it gets smoother as the numbers gets higher. evolutionary advantage?

        phenotype_values = {}
        for trait in genome_codings.keys():
            min_val, max_val =  trait_ranges[trait]
            x =  genome_codings[trait]
            range_from_min_to_max = (max_val - min_val )
            # normalized_value = ((math.sin(x ** 1/2.0) + 1.0) * 1/2)
            normalized_value = (x % 100.0) / 100.0
            mapped_value = range_from_min_to_max * normalized_value + min_val

            phenotype_values[trait] = mapped_value


        return phenotype_values

    def make_phenotype(self, trait_ranges):
        genome_codings = {trait: self.combine(*genes)
                            for trait, genes in self.chromosome.iteritems()}
        phenotype_values = self.map_genome_codings_to_phenotype(genome_codings, trait_ranges)
        return Phenotype(**phenotype_values)


    def make_gamete(self, mutation_rate=None):

        my_gamete = {trait: random.choice(genes).reproduce(mutation_rate)
                for trait, genes in self.chromosome.iteritems()}
        if random.random() < mutation_rate.new_gene_chance:
            my_gamete[random.choice(my_gamete.keys())] = Gene(mutation_rate)

        return my_gamete
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

    def mutate(self, mutation_rate=None):
        ploid_a = {}
        ploid_b = {}
        for trait, genes in self.chromosome.iteritems():
            ploid_a[trait] = genes[0].reproduce(mutation_rate)
            ploid_b[trait] = genes[1].reproduce(mutation_rate)
        return Genome(ploid_a, ploid_b)


    def __str__(self):
        chromosome_str =  ", ".join(["%s : %s/%s" % (trait, genes[0], genes[1])
                                for trait, genes in self.chromosome.iteritems()])

        return  "Genome: {%s}" % chromosome_str


class Phenotype(dictobj):
    pass



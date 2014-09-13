#!/usr/bin/env python2.7
import unittest
from mock import patch, Mock
from options import options
from genome import Multiplier, Constant, Genome, Phenotype, gene_types, Gene


class GenomeTester(unittest.TestCase):

    def test_genome_excepts_on_mule(self):
        self.assertRaises(Exception, Genome.__init__, ({"a": 1}, {"b": 1}))

    def test_make_gamete_calls_reproduce(self):
        flagger = Mock(**{'reproduce.return_value': "FLAG"})
        test_genome = Genome({"a": flagger}, {"a": flagger})
        test_gamete = test_genome.make_gamete()
        self.assertEqual(test_gamete.values()[0], "FLAG")

    def test_genome_mutate(self):
        test_genome = make_genome()
        mutated_genome = test_genome.mutate()
        self.assertEqual(test_genome.chromosome.keys(),
                         mutated_genome.chromosome.keys())
        for trait in test_genome.chromosome.keys():
            self.assert_in_mutant_range(test_genome.chromosome[trait][0],
                                        mutated_genome.chromosome[trait][0])
            self.assert_in_mutant_range(test_genome.chromosome[trait][1],
                                        mutated_genome.chromosome[trait][1])


    @patch('genome.random')
    def test_make_gamete(self, fake_random):
        # unfortuantely the order of choices is based on hash ordering.
        # I do my own recombination in this test to use the same hash ordering
        choices = [0, 1, 1, 0]
        fake_random.choice.side_effect = lambda x: x[choices.pop()]
        fake_random.random.return_value = options.new_gene_chance * 1.1 # don't get new_gene

        test_genome = make_genome()
        expected_gamete = {trait: fake_random.choice(genes)
                           for trait, genes in test_genome.chromosome.iteritems()}
        choices = [0, 1, 1, 0]
        test_gamete = test_genome.make_gamete()

        for trait, gene in test_gamete.iteritems():
            self.assert_in_mutant_range(gene, expected_gamete[trait])

    @patch('genome.random.random')
    def test_make_gamete_new_gene(self, fake_random):
        fake_random.random.return_value = options.new_gene_chance * 0.9 # get new_gene

        test_genome = make_genome()
        ##TODO: How to test that one of the genes is new?
        #currently this is just a smoke test
        # the new gene could be within mutation distance of the old gene

    def test_make_phenotype(self):
        test_genome = make_genome()
        test_phenotype = test_genome.make_phenotype()
        expected_attrs = {
            "size": 16.61,
            "speed": 1,
            "strength": 7.5,
            "health": 21
        }
        expected_phenotype = Phenotype(**expected_attrs)
        self.assertEqual(test_phenotype, expected_phenotype)

    def test_combine_two_constant(self):
        g1 = Constant(15.1)
        g2 = Constant(20.2)
        self.assertEqual(20.2, Genome.combine(g1, g2))

    def test_combine_half_and_half(self):
        g1 = Multiplier(0.333)
        g2 = Constant(20.2)
        self.assertEqual(6.7266, Genome.combine(g1, g2))
        # order shouldn't matter
        self.assertEqual(6.7266, Genome.combine(g2, g1))

    def test_combine_two_multiply(self):
        g1 = Multiplier(0.23)
        g2 = Multiplier(4.2)
        self.assertEqual(1, Genome.combine(g1, g2))

    def assert_in_mutant_range(self, genea, geneb):
        self.assertEqual(genea.__class__, geneb.__class__)
        difference = abs(genea.value - geneb.value)
        if type(geneb == Constant):
            self.assertLessEqual(difference, options.constant_mutation_depth)

        elif type(geneb == Multiplier):
            self.assertLessEqual(difference, options.multi_mutation_depth)
        else:
            self.assertTrue(False, "Unexpected gene type! %s" % geneb.__class__)


def make_genome():
    ploid_a = {
        "size": Constant(15.1),
        "speed": Multiplier(1.1),
        "strength": Multiplier(0.5),
        "health":  Constant(4)
    }
    ploid_b = {
        "size": Multiplier(1.1),
        "speed": Multiplier(4.1),
        "strength": Constant(15),
        "health":  Constant(21)
    }
    return Genome(ploid_a, ploid_b)



class GeneTester(unittest.TestCase):

    @patch('genome.random')
    def test_mutation_rate_notrigger(self, fake_random):
        fake_random.random.return_value = options.mutation_rate * 1.1
        g1 = Constant(10)
        g2 = g1.reproduce()
        self.assertEqual(g1.value, g2.value)

    @patch('genome.random')
    def test_mutation_rate_trigger(self, fake_random):
        fake_random.random.return_value = options.mutation_rate * 0.9
        g1 = Constant(10)
        g2 = g1.reproduce()
        self.assertNotEqual(g1.value, g2.value)

    @patch('genome.random')
    def test_mutation_rate_constant_in_range(self, fake_random):
        fake_random.random.return_value = options.mutation_rate * 0.9
        g1 = Constant(10)
        g2 = g1.reproduce()
        self.assertNotEqual(g1, g2)
        self.assertGreaterEqual(10 + options.constant_mutation_depth, g2.value)
        self.assertLessEqual(10 - options.constant_mutation_depth, g2.value)

    @patch('genome.random')
    def test_mutation_rate_multi_in_range(self, fake_random):
        fake_random.random.return_value = options.mutation_rate * 0.9
        g1 = Multiplier(2)
        g2 = g1.reproduce()
        self.assertNotEqual(g1, g2)
        self.assertGreaterEqual(2 + options.multi_mutation_depth, g2.value)
        self.assertLessEqual(2 - options.multi_mutation_depth, g2.value)

    def test_mutation_range_multi(self):
        value = Multiplier(2)._mutate()
        self.assertGreaterEqual(2 + options.multi_mutation_depth, value)
        self.assertLessEqual(2 - options.multi_mutation_depth, value)

    def test_mutation_range_constant(self):
        value = Constant(10)._mutate()
        self.assertGreaterEqual(10 + options.constant_mutation_depth, value)
        self.assertLessEqual(10 - options.constant_mutation_depth, value)

    def test_gene_random(self):
        g1 = Gene()
        self.assertIn(g1.__class__, gene_types)
        if g1.__class__ == Multiplier:
            self.assertLess(g1.value, options.multi_max_init)
        if g1.__class__ == Constant:
            self.assertLess(g1.value, options.constant_max_init)


if __name__ == '__main__':
    unittest.main()

from pid import pid_loop
import numpy as np
from time import sleep


class Breeder(object):

    def __init__(self, profile=None):
        # hyperparameters
        self.T_0 = 10.
        self.pop_size = 10
        self.num_to_breed = 4
        self.scheduling_char_time = 0.2
        self.num_generations = 20
        # used when initializing population
        self.param_upper_bound = 10
        self.param_lower_bound = -10

        # class variables
        self.curr_gen = 0
        self.population = self.init_pop()
        self.profile = profile

        # record for each time step
        self.max_fitness = []
        self.avg_fitness = []

    def curr_T(self):
        return self.T_0 * np.exp(- self.curr_gen * self.scheduling_char_time)

    def init_pop(self):
        pop = [list(np.random.uniform(low=self.param_upper_bound,
                                      high=self.param_upper_bound,
                                      size=3)) for _ in xrange(self.pop_size)]
        return np.array(pop)

    def eval_fitness(self):
        self.fitness = np.zeros(self.pop_size)
        for idx in xrange(self.pop_size):
            x_prof, x_hist = pid_loop(*list(self.population[idx]),
                                      profile=self.profile)
            self.fitness[idx] = self.objective(x_prof, x_hist)
            sleep(.5)

    def objective(self, x_prof, x_hist):
        return np.sqrt(np.mean((x_prof - x_hist) ** 2))

    def breed(self):
        next_gen = []
        most_fit = np.argsort(self.fitness)[:self.num_to_breed]
        breeding_pop = self.population[most_fit]
        breeding_fitness = self.fitness[most_fit]
        # keep most fit gene
        next_gen.append(breeding_pop[0])
        # boltzmann breeding
        for _ in xrange(self.pop_size - 1):
            new_gene = []
            for param_idx in xrange(3):
                new_param = self.boltzmann_breed(
                    breeding_pop[:, param_idx],
                    breeding_fitness[:, param_idx])
                new_gene.append(new_param)
            new_gene += np.random.randn(3) * self.curr_T()
            next_gen.append(new_gene)

        self.curr_gen += 1
        self.population = np.array(next_gen)

    def boltzmann_breed(self, params, fitness):
        """
        params: array of a particular characteristic
        """
        unweighted_probs = np.exp(-(fitness / self.curr_T()))
        Z = np.sum(unweighted_probs)
        probs = unweighted_probs / Z
        arr_select = np.where(np.cumsum(probs) < np.random.random())[0]
        return params[len(arr_select)]

    def optimize(self):
        """
        runs the breed loop
        """
        for gen in xrange(self.num_generations):
            print "Now evaluating for generation {}".format(self.curr_gen)
            self.eval_fitness()
            print "Evaluation finished. Average fitness: {}".format(np.mean(self.fitness))
            self.avg_fitness.append(np.mean(self.fitness))
            self.max_fitness.append(np.max(self.fitness))
            print "Now breeding next generation"
            self.breed()

        print "Evaluating fitness for final generation"
        self.eval_fitness()
        print "Evaluation finished. Average fitness: {}".format(np.mean(self.fitness))
        self.avg_fitness.append(np.mean(self.fitness))
        self.max_fitness.append(np.max(self.fitness))
        most_fit = np.argmax(self.fitness)
        print "all done!! Best parameteters: {}".format(self.population[most_fit])



    # method to evaluate fitness functions
    # method to breed

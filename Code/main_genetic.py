import genetic
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import Maze
import Player


class Main_genetic:
    def __init__(self, numparams, nbits, popsize, numGenerations, mutationProb, crossoverProb, a, b, maze):
        self.numparams = numparams
        self.nbits = nbits
        self.popsize = popsize
        self.numGenerations = numGenerations
        self.mutationProb = mutationProb
        self.crossoverProb = crossoverProb
        self.a = a
        self.b = b
        self.monster = None
        self.maze = maze
        self.flag = 0
        

    def fitness_function(self, x):
        joueur = Player.Player()
        fitness = []
        for chromosome in x:
            attribue_joueur = []
            for gene in chromosome:
                attribue_joueur.append(gene)
            joueur.set_attributes(attribue_joueur)
            
            result, score = self.monster.mock_fight(joueur)
            if result == 4:
                self.flag = 1
            if result == 0:
                penalite = -16
            elif result == 1:
                penalite = -8
            elif result == 2:
                penalite = -4
            elif result == 3:
                penalite = -2
            else:
                penalite = 0
            fitness.append(self.a*score + self.b*result + penalite)
        print(f'{result}')
        return fitness
    
    def display_generations(self, ga_sim):
        """
        Displays the progress of the fitness over all the generations
        """
        fig = plt.figure()
        n = np.arange(self.numGenerations)
        ax = fig.add_subplot(111)
        ax.plot(n, ga_sim.maxFitnessRecord, '-r', label='Generation Max')
        ax.plot(n, ga_sim.overallMaxFitnessRecord, '-b', label='Overall Max')
        ax.plot(n, ga_sim.avgMaxFitnessRecord, '--k', label='Generation Average')
        ax.set_title('Fitness value over generations')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Fitness value')
        ax.legend()
        fig.tight_layout()

        plt.show()

    def get_genetic(self):
        # Fix random number generator seed for reproducible results
        np.random.seed(0)

        ga_sim = genetic.Genetic(self.numparams, self.popsize, self.nbits)
        ga_sim.init_pop()
        ga_sim.set_fit_fun(self.fitness_function)
        ga_sim.encode_individuals()

        ga_sim.set_sim_parameters(self.numGenerations, self.mutationProb, self.crossoverProb)

        for _ in range(ga_sim.num_generations):

            ga_sim.decode_individuals()
            ga_sim.eval_fit()
            ga_sim.print_progress()
            if self.flag:
                return ga_sim.get_best_individual()
            ga_sim.new_gen()

        # Display best individual
        print('#########################')
        print('Best individual (encoded values):')
        print(ga_sim.get_best_individual())
        print('#########################')

        #self.display_generations(ga_sim)
        return ga_sim.get_best_individual()

    
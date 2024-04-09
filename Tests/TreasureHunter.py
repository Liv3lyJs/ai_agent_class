from PathFinder import *
import heapq
import numpy as np
import random 

class Treasures:
    population = []
    maze = []
    treasure_coords = []
    
    

    def __init__(self, mazefile):
        self.mazefile = mazefile
        self.valeur_min_pop = 0
        self.nbits = 8
        self.pop_size = 100
        self.precision = 2

    def readMaze(self):
        with open(self.mazefile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.maze.append(row)
        self.treasure_coords = [(i, j) for i, row in enumerate(self.maze) for j, value in enumerate(row) if value == 'T']
        nbTreasures = 0
        nbTreasures = len(self.treasure_coords)
        self.num_params = nbTreasures
        self.valeur_max_pop = nbTreasures

    def init_pop(self):
        # Initialize the population as a matrix, where each individual is a binary string.
        # Output:
        # - POPULATION, a binary matrix whose rows correspond to encoded individuals.
        for _ in range(self.pop_size):
            self.population.append(random.sample(range(self.valeur_min_pop, self.valeur_max_pop), self.num_params))

    def encode_individuals(self):
        # Encode the population from a vector of continuous values to a binary string.
        # Input:
        # - CVALUES, a vector of continuous values representing the parameters.
        # - NBITS, the number of bits per indivual used for encoding.
        # Output:
        # - POPULATION, a binary matrix with each row encoding an individual.
        """
        Encoder les valeurs en une matrice binaire representant les genes d'un individu pour chaque lignes.
        Il faut prealablement normaliser les donnees entre 0 et 1 et appeler la fonction ufloat2bin avec seulement
        un individu a la fois. Une fois la convertion faite, il faut combiner les np array resultants ensembles pour
        avoir une seule matrice par individus de la population. Ex: array([0., 1., 1., 0., 0., 1., 0., 0., 1., 0., 0., 1., 0., 1., 0., 0.]) 
        """
        encoded_population = []
        
        #Calcul de la valeur normalisee
        normalized_population = [[round((variable - self.valeur_min_pop) / (self.valeur_max_pop - self.valeur_min_pop), self.precision) for variable in individu] for individu in self.population]
        for element in normalized_population:
            self.cvalues = np.array(element)
            b_value = self.ufloat2bin(self.cvalues, self.nbits)
            b_value_combined = np.concatenate(b_value)
            encoded_population.append(b_value_combined)

        self.population = np.array(encoded_population)

    def decode_individuals(self):
        # Decode an individual from a binary string to a vector of continuous values.
        # Input:
        # - POPULATION, a binary matrix with each row encoding an individual.
        # - NUMPARAMS, the number of parameters for an individual.
        # Output:
        # - CVALUES, a vector of continuous values representing the parameters.
        """
        Faire les etapes inverse de l'encodage. Prendre un individus a la fois avec ses parametres
        representant son chromosome binaire et separer le chromosome entre les deux variables de la fitness
        function. Une fois que c'est fait, appel de la fonction bin2ufloat qui converti les valeurs en 
        nombres et il faut finir avec la denormalisation des donnees afin de pouvoir obtenir les donnees initiales. 
        """
        decoded_population = []

        for chromosomes in self.population:
            b_value = [chromosomes[i:i+self.nbits] for i in range(0, len(chromosomes), self.nbits)]
            c_value = self.bin2ufloat(b_value, self.nbits)
            decoded_population.append(c_value)

        denormalized_population = [[(variable * (self.valeur_max_pop - self.valeur_min_pop)) + self.valeur_min_pop for variable in individu] for individu in decoded_population]
        self.cvalues = np.array(denormalized_population)

    def eval_fit(self):
        # Evaluate the fitness function
        # Record the best individual and average of the current generation
        # WARNING, number of arguments need to be adjusted if fitness function changes
        self.fitness = self.fit_fun(self.cvalues[:, 0], self.cvalues[:, 1])
        if np.max(self.fitness) > self.bestIndividualFitness:
            self.bestIndividualFitness = np.max(self.fitness)
            self.bestIndividual = self.population[self.fitness == np.max(self.fitness)][0]
        self.maxFitnessRecord[self.current_gen] = np.max(self.fitness)
        self.overallMaxFitnessRecord[self.current_gen] = self.bestIndividualFitness
        self.avgMaxFitnessRecord[self.current_gen] = np.mean(self.fitness)

    def fitness_calc(self):
        MyAstar = PathFinder(self.mazefile, 0, 1)
        MyAstar.A_Star()
        return 0
    # Binary-Float conversion functions
    # usage: [BVALUE] = ufloat2bin(CVALUE, NBITS)
    #
    # Convert floating point values into a binary vector
    #
    # Input:
    # - CVALUE, a scalar or vector of continuous values representing the parameters.
    #   The values must be a real non-negative float in the interval [0,1]!
    # - NBITS, the number of bits used for encoding.
    #
    # Output:
    # - BVALUE, the binary representation of the continuous value. If CVALUES was a vector,
    #   the output is a matrix whose rows correspond to the elements of CVALUES.
    def ufloat2bin(cvalue, nbits):
        if nbits > 64:
            raise Exception('Maximum number of bits limited to 64')
        ivalue = np.round(cvalue * (2**nbits - 1)).astype(np.uint64)
        bvalue = np.zeros((len(cvalue), nbits))

        print(ivalue)

        # Overflow
        bvalue[ivalue > 2**nbits - 1] = np.ones((nbits,))

        # Underflow
        bvalue[ivalue < 0] = np.zeros((nbits,))

        bitmask = (2**np.arange(nbits)).astype(np.uint64)
        bvalue[np.logical_and(ivalue >= 0, ivalue <= 2**nbits - 1)] = (np.bitwise_and(np.tile(ivalue[:, np.newaxis], (1, nbits)), np.tile(bitmask[np.newaxis, :], (len(cvalue), 1))) != 0)
        return bvalue
    # usage: [CVALUE] = bin2ufloat(BVALUE, NBITS)
    #
    # Convert a binary vector into floating point values
    #
    # Input:
    # - BVALUE, the binary representation of the continuous values. Can be a single vector or a matrix whose
    #   rows represent independent encoded values.
    #   The values must be a real non-negative float in the interval [0,1]!
    # - NBITS, the number of bits used for encoding.
    #
    # Output:
    # - CVALUE, a scalar or vector of continuous values representing the parameters.
    #   the output is a matrix whose rows correspond to the elements of CVALUES.
    #
    def bin2ufloat(bvalue, nbits):
        if nbits > 64:
            raise Exception('Maximum number of bits limited to 64')
        ivalue = np.sum(bvalue * (2**np.arange(nbits)[np.newaxis, :]), axis=-1)
        cvalue = ivalue / (2**nbits - 1)
        return cvalue

if __name__ == '__main__':
    myTreasure = Treasures('assets/Mazes/obstacles')
    myTreasure.readMaze()
    print(myTreasure.treasure_coords)
    #myTreasure.init_pop()
    #myTreasure.encode_individuals()


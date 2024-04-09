import heapq
import numpy as np
import random 


class Genetic:
    num_params = 0
    pop_size = 0
    nbits = 0
    population = []
    selected_indices = []
    indice_delete = []

    def __init__(self, num_params, pop_size, nbits):
        self.num_params = num_params
        self.pop_size = pop_size
        self.nbits = nbits
        self.fitness = np.zeros((self.pop_size, 1))
        self.fit_fun = np.zeros
        self.cvalues = np.zeros((self.pop_size, num_params))
        self.num_generations = 1
        self.mutation_prob = 0
        self.crossover_prob = 0
        self.bestIndividual = []
        self.bestIndividualFitness = -1e10
        self.maxFitnessRecord = np.zeros((self.num_generations,))
        self.overallMaxFitnessRecord = np.zeros((self.num_generations,))
        self.avgMaxFitnessRecord = np.zeros((self.num_generations,))
        self.current_gen = 0
        self.crossover_modulo = 0

        self.valeur_min_pop = -1000
        self.valeur_max_pop = 1000
        self.precision = 2
        self.Fitness_record_stagnation = []
        self.stagnation_threshold  = 20
        self.fitness_gap_threshold = 0.03
        self.cpt_stagnation = 0
        self.cpt_threshold = 20

        #Selection parameters
        self.cross_over_parent = 370
        self.stagnation_param = 60

    def init_pop(self):
        """
        Initialiser la population de depart dans son espace de donnee originale. 
        Creer une valeur aleatoire entre min et max pour chaque variable du systeme.
        """
        self.population = []
        for _ in range(self.pop_size):
            self.population.append([round(random.uniform(self.valeur_min_pop, self.valeur_max_pop), self.precision) for _ in range(self.num_params)])
        print(len(self.population))

    def set_fit_fun(self, fun):
        self.fit_fun = fun

    def set_crossover_modulo(self, modulo):
        self.crossover_modulo = modulo

    def set_sim_parameters(self, num_generations, mutation_prob, crossover_prob):
        self.num_generations = num_generations
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.bestIndividual = []
        self.bestIndividualFitness = -1e10
        self.maxFitnessRecord = np.zeros((num_generations,))
        self.overallMaxFitnessRecord = np.zeros((num_generations,))
        self.avgMaxFitnessRecord = np.zeros((num_generations,))
        self.current_gen = 0

    def eval_fit(self):
        self.fitness = self.fit_fun(self.cvalues)
        if np.max(self.fitness) > self.bestIndividualFitness:
            self.bestIndividualFitness = np.max(self.fitness)
            self.bestIndividual = self.population[self.fitness == np.max(self.fitness)][0]
        self.maxFitnessRecord[self.current_gen] = np.max(self.fitness)
        self.overallMaxFitnessRecord[self.current_gen] = self.bestIndividualFitness
        self.Fitness_record_stagnation.append(self.bestIndividualFitness)
        self.avgMaxFitnessRecord[self.current_gen] = np.mean(self.fitness)

    def check_for_stagnation(self):
        if len(self.Fitness_record_stagnation) > self.stagnation_threshold:
            past_fitness = self.Fitness_record_stagnation[-self.stagnation_threshold - 1]
            improvement = self.bestIndividualFitness - past_fitness
            self.cpt_stagnation += 1

            if improvement <= self.fitness_gap_threshold and self.cpt_stagnation > self.cpt_threshold:
                self.cpt_stagnation = 0
                return True
        return False


    def print_progress(self):
        print('Generation no.%d: best fitness is %f, average is %f' %
              (self.current_gen, self.maxFitnessRecord[self.current_gen],
               self.avgMaxFitnessRecord[self.current_gen]))
        print('Overall best fitness is %f' % self.bestIndividualFitness)


    def get_best_individual(self):
        b_value = [self.bestIndividual[i:i+self.nbits] for i in range(0, len(self.bestIndividual), self.nbits)]
        c_value = bin2ufloat(b_value, self.nbits)
        denormalized_population = [[(variable * (self.valeur_max_pop - self.valeur_min_pop)) + self.valeur_min_pop for variable in c_value]]

        print(f'The best individial of the population is: {denormalized_population[0][0]} {denormalized_population[0][1]} {denormalized_population[0][2]} {denormalized_population[0][3]} {denormalized_population[0][4]}, {denormalized_population[0][5]}, {denormalized_population[0][6]} {denormalized_population[0][7]} {denormalized_population[0][8]} {denormalized_population[0][9]} {denormalized_population[0][10]} {denormalized_population[0][11]}')
        best = []
        for individu in denormalized_population:
            for value in individu:
                best.append(value)
        
        return best

    def encode_individuals(self):
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
            b_value = ufloat2bin(self.cvalues, self.nbits)
            b_value_combined = np.concatenate(b_value)
            encoded_population.append(b_value_combined)

        self.population = np.array(encoded_population)

    def decode_individuals(self):
        """
        Faire les etapes inverse de l'encodage. Prendre un individus a la fois avec ses parametres
        representant son chromosome binaire et separer le chromosome entre les deux variables de la fitness
        function. Une fois que c'est fait, appel de la fonction bin2ufloat qui converti les valeurs en 
        nombres et il faut finir avec la denormalisation des donnees afin de pouvoir obtenir les donnees initiales. 
        """
        decoded_population = []

        for chromosomes in self.population:
            b_value = [chromosomes[i:i+self.nbits] for i in range(0, len(chromosomes), self.nbits)]
            c_value = bin2ufloat(b_value, self.nbits)
            decoded_population.append(c_value)

        denormalized_population = [[(variable * (self.valeur_max_pop - self.valeur_min_pop)) + self.valeur_min_pop for variable in individu] for individu in decoded_population]
        self.cvalues = np.array(denormalized_population)

    def doSelection(self):
        """
        Selectionner les deux individus a partir de la roulette aleatoire en se basant sur les proportions
        de chaque indivius obtenu avec la fitness function. 
        """
        # #Normaliser les valeurs de la fitness function 
        min_fitness = np.min(self.fitness)
        max_fitness = np.max(self.fitness)
        normalized_fitness = (self.fitness - min_fitness) / (max_fitness - min_fitness)
        # #Calculer le ration de la fitness function pour tous les chromosomes
        total = sum(normalized_fitness)
        fit_fraction = [(individu * 100) / total for individu in normalized_fitness]
        #Calculer la somme totale du fit_franction 
        cumulative_sum = np.cumsum(fit_fraction)

        self.selected_indices = []

        while len(self.selected_indices) < self.cross_over_parent:
            #Generer un nombre aleatoire entre 0 et 100
            spin = np.random.rand() * 100
            #Find index of first individual that exceed random number
            selected_index = np.searchsorted(cumulative_sum, spin)
            #Get the selected individual
            if selected_index not in self.selected_indices:
                self.selected_indices.append(selected_index)

        self.indice_delete = []
        #Trouver les individus de la population les moins aptes afin de les remplaces
        individu_moins_performants = heapq.nsmallest(self.cross_over_parent, normalized_fitness)
        self.indice_delete = [np.where(normalized_fitness == metric)[0][0] for metric in individu_moins_performants]

        #Creation du tableau de retour
        tableau_retourn = []
        for i in range(0, self.cross_over_parent, 2):
            pair = (self.population[self.selected_indices[i]], self.population[self.selected_indices[i+1]])
            tableau_retourn.append(pair)

        return tableau_retourn

    def doCrossover(self, pairs):
        """
        Itterer sur les pairs de chromosomes, si un nombre aleatoire est plus grand que la probabilite de crossover, alors on peut la realiser,
        sinon on clone les parents. Pour ceux qui vont subir un crossover, ils faut definir l'indice ou le cross-over va se faire realiser et 
        cet indice est choisi de facon aleatoire par rapport a certaines contraintes. Par la suite le cross over est realise avec l'indice obtenu
        entre les deux chromosomes de la paire. 
        """
        self.set_crossover_modulo(self.nbits)
        new_population = []
        for (ind1, ind2) in pairs:
            if np.random.rand() < self.crossover_prob:
                #Calculer les points de coupure possibles
                possible_cut_points = list(range(self.crossover_modulo, (self.nbits*self.num_params), self.crossover_modulo))
                cut_point = np.random.choice(possible_cut_points)
                #Creer les enfants de la population 
                new_population.append(np.concatenate((ind1[:cut_point], ind2[cut_point:])))
                new_population.append(np.concatenate((ind2[:cut_point], ind1[cut_point:])))
            else:
                #Cloner les parents
                new_population.append(ind1)
                new_population.append(ind2)

        #Assigner les nouveaux individus a la population initiale
        for individu, index in zip(new_population, self.indice_delete):
            self.population[index] = individu

        return self.population 

    def doMutation(self):
        for i, chromosome in enumerate(self.population):
            if np.random.rand() < self.mutation_prob:
                #Definir quel gene sera inverse
                index = random.randint(0, ((self.nbits*self.num_params)-1))
                chromosome[index] = 1 - chromosome[index]
                self.population[i] = chromosome

    def stagnation_callback(self):
        if self.check_for_stagnation():
            #Normaliser les valeurs de la fitness function 
            min_fitness = np.min(self.fitness)
            max_fitness = np.max(self.fitness)
            normalized_fitness = (self.fitness - min_fitness) / (max_fitness - min_fitness)

            # #Trouver les individus de la population les moins aptes afin de les remplaces
            # self.indice_delete = []
            # individu_moins_performants = heapq.nsmallest(self.stagnation_param, normalized_fitness)
            # self.indice_delete = [np.where(normalized_fitness == metric)[0][0] for metric in individu_moins_performants]

            self.indice_delete = []
            #Choisir au hasard des individus a remplacer dans la population
            for _ in range(self.stagnation_param):
                self.indice_delete.append(random.randint(0, self.pop_size-1))

            #Replacer les individus les moins performants par des valeurs aleatoires
            new_population = [round(random.uniform(self.valeur_min_pop, self.valeur_max_pop), self.precision) for _ in range(self.stagnation_param)]
            for individu, index in zip(new_population, self.indice_delete):
                self.population[index] = individu

        return self.population 


    def new_gen(self):
        pairs = self.doSelection()
        self.population = self.doCrossover(pairs)
        self.doMutation()
        self.population = self.stagnation_callback()
        self.current_gen += 1


def ufloat2bin(cvalue, nbits):
    if nbits > 64:
        raise Exception('Maximum number of bits limited to 64')
    ivalue = np.round(cvalue * (2**nbits - 1)).astype(np.uint64)
    bvalue = np.zeros((len(cvalue), nbits))

    # Overflow
    bvalue[ivalue > 2**nbits - 1] = np.ones((nbits,))

    # Underflow
    bvalue[ivalue < 0] = np.zeros((nbits,))

    bitmask = (2**np.arange(nbits)).astype(np.uint64)
    bvalue[np.logical_and(ivalue >= 0, ivalue <= 2**nbits - 1)] = (np.bitwise_and(np.tile(ivalue[:, np.newaxis], (1, nbits)), np.tile(bitmask[np.newaxis, :], (len(cvalue), 1))) != 0)
    return bvalue

def bin2ufloat(bvalue, nbits):
    if nbits > 64:
        raise Exception('Maximum number of bits limited to 64')
    ivalue = np.sum(bvalue * (2**np.arange(nbits)[np.newaxis, :]), axis=-1)
    cvalue = ivalue / (2**nbits - 1)
    return cvalue

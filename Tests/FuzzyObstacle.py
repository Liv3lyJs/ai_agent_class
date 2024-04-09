import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import numpy as np
import math
from Constants import *

class ObstacleHandler():

    def __init__(self, obstacle_rect, player_rect, playerdirection, tile_size_x, tile_size_y, indice_row, indice_col):
        self.tile_size_x = tile_size_x
        self.tile_size_y = tile_size_y
        self.obstacle_rect = obstacle_rect
        self.player_rect = player_rect
        self.playerdirection = playerdirection
        self.indice_row = indice_row
        self.indice_col = indice_col



    def passable_down_left(self, playerdirection):
        if playerdirection == "LEFT" or playerdirection == "RIGHT":
            downwallcoords = self.down_wall_coords(self.indice_row)
            return abs(self.obstacle_rect.bottom - self.down_wall_coords(self.indice_row)) >= self.player_rect.height
        else : 
            leftwallcoords = self.left_wall_coords(self.indice_col)
            return abs(self.obstacle_rect.left - self.left_wall_coords(self.indice_col)) >= self.player_rect.width
        
    def passable_down_leftV3(self, playerdirection):
        if playerdirection == "LEFT" or playerdirection == "RIGHT":
            downwallcoords = self.down_wall_coords(self.indice_row)
            return abs(self.obstacle_rect.bottom - self.down_wall_coords(self.indice_row)) 
        else : 
            leftwallcoords = self.left_wall_coords(self.indice_col)
            return abs(self.obstacle_rect.left - self.left_wall_coords(self.indice_col)) 
    def angle_to_obstacle(self, player_x, player_y):
        dx = self.obstacle_center_x - player_x
        dy = -(self.obstacle_center_y - player_y)
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        return angle_deg
    
    def distance_to_obstacle(self, player_x, player_y):
        dx = self.obstacle_center_x - player_x
        dy = self.obstacle_center_y - player_y
        return math.hypot(dx, dy)
    
    def left_wall_coords(self,col):
        x = (self.tile_size_x*(col))
        return x
    def down_wall_coords(self,row):
        y = (self.tile_size_y*(row+1))
        return y
    def distance_to_wall(self):

        return 0
    def createFuzzyControllerV3(self):

        distmax = self.tile_size_x
        dist = ctrl.Antecedent(np.linspace(-distmax, distmax+1, 1000), 'dist')
        distwall = ctrl.Antecedent(np.linspace(0, self.tile_size_x+1, 1000), 'distwall')
        direction = ctrl.Consequent(np.linspace(0, 3, 1000), 'direction', defuzzify_method='centroid')

        # Accumulation (accumulation_method) methods for fuzzy variables:
        #    np.fmax
        #    np.multiply
        direction.accumulation_method = np.fmax
        distminobstacle = round((self.player_rect.width/2)+(self.obstacle_rect.width/2))

        dist['closerightorup'] = fuzz.trimf(dist.universe, [-1, distminobstacle/2, distminobstacle])
        dist['farrightup'] = fuzz.trapmf(dist.universe, [distminobstacle-2, distminobstacle+2, self.tile_size_x, self.tile_size_x])
        dist['closeleftordown'] = fuzz.trimf(dist.universe, [-distminobstacle, -distminobstacle/2, 1])
        dist['farleftdown'] = fuzz.trapmf(dist.universe, [-self.tile_size_x, -self.tile_size_x, -distminobstacle-2, -distminobstacle+2])
        distwall['far'] = fuzz.trapmf(distwall.universe, [self.player_rect.height-2, self.player_rect.height+2, self.tile_size_x, self.tile_size_x])
        distwall['near'] = fuzz.trapmf(distwall.universe, [0, 0, self.player_rect.height-2, self.player_rect.height-1])

        direction['rightup'] = fuzz.trimf(direction.universe, [0, 0, 0.8])
        direction['straight'] = fuzz.trimf(direction.universe, [0.6, 1, 1.4])
        direction['leftdown'] = fuzz.trimf(direction.universe, [1.2, 2, 2])
        

        rules = []
        rules.append(ctrl.Rule(antecedent=(distwall['far']) | dist['farleftdown'], consequent= direction['leftdown']))
        rules.append(ctrl.Rule(antecedent=(distwall['near']) | dist['farleftdown'], consequent= direction['rightup']))
        #rules.append(ctrl.Rule(antecedent=(dist['closeleftordown']), consequent= direction['rightup']))
        for rule in rules:
            rule.and_func = np.fmin
            rule.or_func = np.fmax

        system = ctrl.ControlSystem(rules)
        sim = ctrl.ControlSystemSimulation(system)
        return sim
    def createFuzzyControllerV2(self):

        distmax = 72
        dist = ctrl.Antecedent(np.linspace(-distmax, distmax+1, 1000), 'dist')
        direction = ctrl.Consequent(np.linspace(0, 5, 1000), 'direction', defuzzify_method='centroid')

        # Accumulation (accumulation_method) methods for fuzzy variables:
        #    np.fmax
        #    np.multiply
        direction.accumulation_method = np.fmax

        dist['closerightorup'] = fuzz.trapmf(dist.universe, [0, 0, (2*self.player_rect.height/3)-5, (2*self.player_rect.height/3)+5])
        dist['farrightup'] = fuzz.trapmf(dist.universe, [(2*self.player_rect.height/3)-5, (2*self.player_rect.height/3)+5, distmax, distmax])
        dist['closeleftordown'] = fuzz.trapmf(dist.universe, [-(2*self.player_rect.height/3)-5, -(2*self.player_rect.height/3)+5, 0, 0])
        dist['farleftdown'] = fuzz.trapmf(dist.universe, [-distmax, -distmax, -(2*self.player_rect.height/3)-5, -(2*self.player_rect.height/3)+5])

        direction['leftdown'] = fuzz.trapmf(direction.universe, [0, 0, 0.7, 0.9])
        direction['straight'] = fuzz.trapmf(direction.universe, [0.8, 0.9, 1.1, 1.2])
        direction['rightup'] = fuzz.trapmf(direction.universe, [1.1, 1.3, 2, 2])
        

        rules = []
        rules.append(ctrl.Rule(antecedent=(dist['farleftdown'])|dist['farrightup'], consequent= direction['straight']))
        rules.append(ctrl.Rule(antecedent=(dist['closerightorup']), consequent= direction['leftdown']))
        rules.append(ctrl.Rule(antecedent=(dist['closeleftordown']), consequent= direction['rightup']))
        for rule in rules:
            rule.and_func = np.fmin
            rule.or_func = np.fmax

        system = ctrl.ControlSystem(rules)
        sim = ctrl.ControlSystemSimulation(system)
        return sim
    def createFuzzyController(self):
        # TODO: Create the fuzzy variables for inputs and outputs.
        # Defuzzification (defuzzify_method) methods for fuzzy variables:
        #    'centroid': Centroid of area
        #    'bisector': bisector of area
        #    'mom'     : mean of maximum
        #    'som'     : min of maximum
        #    'lom'     : max of maximum/
        #distmaxx = tile_size_x * PERCEPTION_RADIUS
        #distmaxy = tile_size_y * PERCEPTION_RADIUS
        distmax = np.hypot(72,72)

        dist = ctrl.Antecedent(np.linspace(0, distmax+1, 1000), 'dist')
        angle = ctrl.Antecedent(np.linspace(-180, 181, 1000), 'angle')
        distwall = ctrl.Antecedent(np.linspace(0, 80, 1000), 'distwall')
        direction = ctrl.Consequent(np.linspace(0, 5, 1000), 'direction', defuzzify_method='centroid')


        # Accumulation (accumulation_method) methods for fuzzy variables:
        #    np.fmax
        #    np.multiply
        direction.accumulation_method = np.fmax
        #distx = xobs - xplayer
        # TODO: Create membership functions
        dist['near'] = fuzz.trapmf(dist.universe, [0, 0, distmax/4, 2*distmax/5]) 
        dist['far'] = fuzz.trapmf(dist.universe, [1*distmax/4, 3*distmax/5, distmax, distmax])
        angle['topright'] = fuzz.trimf(angle.universe, [-10, 55, 100])#0 a 90
        angle['downright'] = fuzz.trimf(angle.universe, [-100, -55, 20])#-90 a 0
        angle['topleft'] = fuzz.trimf(angle.universe, [80, 180, 180])#90 a 180
        angle['downleft'] = fuzz.trimf(angle.universe, [-180, -180, -80])#-180 a -90
        distwall['pass'] = fuzz.trapmf(distwall.universe, [27, 29, 80, 80])
        distwall['nopass'] = fuzz.trapmf(distwall.universe, [0, 0, 25, 28])
        
        # direction['center'] = fuzz.trimf(direction.universe, [0, 0, 1.2])
        # direction['up'] = fuzz.trimf(direction.universe, [0.8, 1.2, 2.2])
        # direction['down'] = fuzz.trimf(direction.universe, [1.8, 2.2, 3.2])
        # direction['left'] = fuzz.trimf(direction.universe, [2.8, 3.2, 4.2])
        # direction['right'] = fuzz.trimf(direction.universe, [3.8, 5, 5])


        direction['left'] = fuzz.trimf(direction.universe, [0, 0, 1.2])
        direction['right'] = fuzz.trimf(direction.universe, [0.8, 1.2, 2.2])
        direction['center'] = fuzz.trimf(direction.universe, [1.8, 2.2, 3.2])
        direction['up'] = fuzz.trimf(direction.universe, [2.8, 3.2, 4.2])
        direction['down'] = fuzz.trimf(direction.universe, [3.8, 5, 5])
        
        
        

        vertical = self.playerdirection == 'DOWN' or self.playerdirection =='UP'
        horizontal = self.playerdirection == 'LEFT' or self.playerdirection =='RIGHT'
        # TODO: Define the rules.
        rules = []
        if vertical: #obstacle to down wall
            rules.append(ctrl.Rule(antecedent=(angle['topright']|angle['downright']|(dist['far'])), consequent= direction['center']))
            rules.append(ctrl.Rule(antecedent=(((angle['topright']|angle['downright'])|(dist['near']))&distwall['pass'] ), consequent= direction['left']))
            rules.append(ctrl.Rule(antecedent=(((angle['topleft']|angle['downleft'])|(dist['near']))&distwall['nopass'] ), consequent= direction['right']))
        else:
            rules.append(ctrl.Rule(antecedent=(angle['topright']|angle['downright']|(dist['far']) ), consequent= direction['center']))
            rules.append(ctrl.Rule(antecedent=(angle['topright']|angle['topleft']|(dist['near'])|distwall['pass'] ), consequent= direction['down']))
            rules.append(ctrl.Rule(antecedent=(angle['downleft']|angle['downright']|(dist['near'])|distwall['nopass'] ), consequent= direction['up']))
            
        #else: #obstacle to left wall
            
        # Conjunction (and_func) and disjunction (or_func) methods for rules:
        #     np.fmin
        #     np.fmax
        for rule in rules:
            rule.and_func = np.fmin
            rule.or_func = np.fmax

        system = ctrl.ControlSystem(rules)
        sim = ctrl.ControlSystemSimulation(system)
        return sim

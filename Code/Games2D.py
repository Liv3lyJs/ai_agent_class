from pygame.locals import *
import pygame
from PathFinder import *
from Player import *
from Maze import *
from Constants import *
from DoorOpener import *
from FuzzyObstacle import *
import TreasureHunter
import main_genetic
from Monster import *

class App:
    windowWidth = WIDTH
    windowHeight = HEIGHT
    player = 0
    doorkey = None
    handleDoor = 'HANDLE DOOR'

    def __init__(self, mazefile):
        self._running = True
        self._win = False
        self._dead = False
        self._display_surf = None
        self._clock = None
        self._image_surf = None
        self.level = 0
        self.score = 0
        self.timer = 0.0
        self.player = Player()
        self.maze = Maze(mazefile)
        self.file = mazefile
        

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self._clock = pygame.time.Clock()
        pygame.display.set_caption("Dungeon Crawler")
        pygame.time.set_timer(pygame.USEREVENT, 10)
        self._running = True
        self.maze.make_maze_wall_list()
        self.maze.make_maze_item_lists()
        self._image_surf = pygame.image.load("assets/Images/knight.png")
        self.player.set_position(self.maze.start[0], self.maze.start[1])
        self.player.set_size(PLAYER_SIZE*self.maze.tile_size_x, PLAYER_SIZE*self.maze.tile_size_x)
        self._image_surf = pygame.transform.scale(self._image_surf, self.player.get_size())
        self.call_genetic = main_genetic.Main_genetic(numparams=12, nbits=16, popsize=500, numGenerations=450, mutationProb=0.15, 
                                                      crossoverProb=0.8, a=0.2, b=0.8, maze=self.maze)
        self.monster_interact = True
        self.Monster_row = 100
        self.Monster_col = 100
        self.do_treasures = False
        

    def on_keyboard_input(self, keys):
        if keys[K_RIGHT] or keys[K_d]:
            self.move_player_right()

        if keys[K_LEFT] or keys[K_a]:
            self.move_player_left()

        if keys[K_UP] or keys[K_w]:
            self.move_player_up()

        if keys[K_DOWN] or keys[K_s]:
            self.move_player_down()

        # Utility functions for AI
        if keys[K_p]:
            self.maze.make_perception_list(self.player, self._display_surf)
            # returns a list of 5 lists of pygame.rect inside the perception radius
            # the 4 lists are [wall_list, obstacle_list, item_list, monster_list, door_list]
            # item_list includes coins and treasure

        if keys[K_m]:
            for monster in self.maze.monsterList:
                print(monster.mock_fight(self.player))
            # returns the number of rounds you win against the monster
            # you need to win all four rounds to beat it

        if keys[K_SPACE]:
            questionList = self.maze.look_at_door(self.player, self._display_surf)
            # returns the state of the doors you can currently see
            # you need to unlock it by providing the correct key
            questionListString = f"{questionList[0]}"
            keyFinder = DoorOpener()
            self.doorkey = keyFinder.KeyFinder(questionListString)

        if keys[K_u]:
            self.maze.unlock_door(self.doorkey)
            # returns true if the door is unlocked, false if the answer is incorrect and the door remains locked
            # if the door is unlocked you can pass through it (no visible change... yet)

        if (keys[K_ESCAPE]):
            self._running = False

    # FONCTION À Ajuster selon votre format d'instruction
    def on_AI_input(self, instruction):
        if instruction == 'RIGHT':
            #for i in range(round(self.maze.tile_size_x/self.player.speed)):
            self.move_player_right()

        if instruction == 'LEFT':
            #for i in range(round(self.maze.tile_size_x/self.player.speed)):
            self.move_player_left()

        if instruction == 'UP':
            #for i in range(round(self.maze.tile_size_y/self.player.speed)):
            self.move_player_up()

        if instruction == 'DOWN':
            #for i in range(round(self.maze.tile_size_y/self.player.speed)):
            self.move_player_down()
        if instruction == 'STRAIGHT':
            #for i in range(round(self.maze.tile_size_y/self.player.speed)):
            pass
        if instruction == 'HANDLE DOOR':
            questionList = self.maze.look_at_door(self.player, self._display_surf)
            keyFinder = DoorOpener()
            self.doorkey = keyFinder.KeyFinder(f"{questionList[0]}")
            self.maze.unlock_door(self.doorkey)



    def on_collision(self):
        return self.on_wall_collision() or self.on_obstacle_collision() or self.on_door_collision()

    def move_player_right(self):
        self.player.moveRight()
        if self.on_collision():
            self.player.moveLeft()

    def move_player_left(self):
        self.player.moveLeft()
        if self.on_collision():
            self.player.moveRight()

    def move_player_up(self):
        self.player.moveUp()
        if self.on_collision():
            self.player.moveDown()

    def move_player_down(self):
        self.player.moveDown()
        if self.on_collision():
            self.player.moveUp()

    def on_wall_collision(self):
        collide_index = self.player.get_rect().collidelist(self.maze.wallList)
        if not collide_index == -1:
            # print("Collision Detected!")
            return True
        return False

    def on_obstacle_collision(self):
        collide_index = self.player.get_rect().collidelist(self.maze.obstacleList)
        if not collide_index == -1:
            # print("Collision Detected!")
            return True
        return False

    def on_coin_collision(self):
        collide_index = self.player.get_rect().collidelist(self.maze.coinList)
        if not collide_index == -1:
            self.maze.coinList.pop(collide_index)
            return True
        else:
            return False

    def on_treasure_collision(self):
        collide_index = self.player.get_rect().collidelist(self.maze.treasureList)
        if not collide_index == -1:
            self.maze.treasureList.pop(collide_index)
            return True
        else:
            return False

    def on_monster_collision(self):
        for monster in self.maze.monsterList:
            if self.player.get_rect().colliderect(monster.rect):
                return monster
        return False

    def on_door_collision(self):
        for door in self.maze.doorList:
            if self.player.get_rect().colliderect(door.rect):
                return True
        return False

    def on_exit(self):
        return self.player.get_rect().colliderect(self.maze.exit)

    def maze_render(self):
        self._display_surf.fill((0, 0, 0))
        self.maze.draw(self._display_surf)
        font = pygame.font.SysFont(None, 32)
        text = font.render("Coins: " + str(self.score), True, WHITE)
        self._display_surf.blit(text, (WIDTH - 120, 10))
        text = font.render("Time: " + format(self.timer, ".2f"), True, WHITE)
        self._display_surf.blit(text, (WIDTH - 300, 10))

    def on_render(self):
        self.maze_render()
        self._display_surf.blit(self._image_surf, (self.player.x, self.player.y))
        pygame.display.flip()

    def on_win_render(self):
        self.maze_render()
        font = pygame.font.SysFont(None, 120)
        text = font.render("YOU WIN!", True, GREEN)
        self._display_surf.blit(text, (0.1 * self.windowWidth, 0.4 * self.windowHeight))
        pygame.display.flip()

    def on_death_render(self):
        self.maze_render()
        font = pygame.font.SysFont(None, 120)
        text = font.render("YOU DIED!", True, RED)
        self._display_surf.blit(text, (0.1 * self.windowWidth, 0.4 * self.windowHeight))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
    def find_direction(self, currentRow, currentCol, nextRow, nextCol):
        if nextRow>currentRow:
            playerdirection = "DOWN"
        elif nextRow<currentRow:
            playerdirection = "UP"
        elif nextCol>currentCol:
            playerdirection = "RIGHT"
        elif nextCol<currentCol:
            playerdirection = "LEFT"
        return playerdirection
    def obstacle(self, perceptionList, currentRow, currentCol, nextRow, nextCol):
        if bool(perceptionList[1]):
            instruction = None
            playerdirection = self.find_direction(currentRow, currentCol, nextRow, nextCol)
            player_rect = self.player.get_rect()
            for obstacle in perceptionList[1]:
                tempcurrentCellrow, tempcurrentCellcol = self.maze.indices_from_coordinates(obstacle.centerx, obstacle.centery)
                #verify if the obstacle is in current cell or in the next cell
                if (tempcurrentCellrow, tempcurrentCellcol) == (currentRow,currentCol) or (tempcurrentCellrow, tempcurrentCellcol) == (nextRow, nextCol):
                    obstacle_rect = obstacle
                    #verify if we passed the obstacle
                    if not((playerdirection == "DOWN" and player_rect.bottom>obstacle_rect.top ) or (playerdirection == "UP" and player_rect.top<obstacle_rect.bottom) or (playerdirection == "LEFT" and player_rect.left<obstacle_rect.right) or (playerdirection == "RIGHT" and player_rect.right>obstacle_rect.left)):
                        MyObstacleHandler = ObstacleHandler(obstacle_rect, player_rect, playerdirection, self.maze.tile_size_x, self.maze.tile_size_y, currentRow, currentCol)
                        if playerdirection == "LEFT" or playerdirection == "RIGHT":
                            fuzz_ctrl = MyObstacleHandler.createFuzzyControllerV3()
                            dist = self.player.get_rect().centery - obstacle_rect.centery
                        else : 
                            fuzz_ctrl = MyObstacleHandler.createFuzzyControllerV3()
                            dist = obstacle_rect.centerx - self.player.get_rect().centerx
                        fuzz_ctrl.input['dist'] = dist
                        test = MyObstacleHandler.passable_down_leftV3(playerdirection)
                        fuzz_ctrl.input['distwall'] = MyObstacleHandler.passable_down_leftV3(playerdirection)
                        # for var in fuzz_ctrl.ctrl.fuzzy_variables:
                        #     var.view()
                        #     plt.show()
                        fuzz_ctrl.compute()

                        direction = fuzz_ctrl.output['direction']
                        # for rule in fuzz_ctrl.ctrl.rules:
                        #     print(rule)
                        passable = MyObstacleHandler.passable_down_left(playerdirection)
                        if playerdirection == "LEFT" or playerdirection == "RIGHT":
                            match direction:
                                case x if x > 1.1: instruction = "DOWN"
                                case x if x >= 0.9 and x <=1.1: "STRAIGHT"
                                case x if x < 0.9: instruction = "UP"
                            # if not(passable) and instruction == "DOWN": instruction= "UP"
                            # elif passable and instruction =="UP": instruction = "DOWN"

                        else :
                            match direction:
                                case x if x < 0.9: instruction = "RIGHT"
                                case x if x >=0.9 and x <=1.1: "STRAIGHT"
                                case x if x >1.1: instruction = "LEFT"
                            # if passable and instruction == "RIGHT": instruction= "LEFT"
                            # elif not(passable) and instruction =="LEFT": instruction = "RIGHT"
                        if dist == 0 and (playerdirection == "LEFT" or playerdirection=="RIGHT") : 
                            if passable:
                                instruction = "DOWN"
                            else : instruction = "UP"
                        elif dist == 0 and (playerdirection == "UP" or playerdirection=="DOWN") : 
                            if passable:
                                instruction = "LEFT"
                            else : instruction = "RIGHT"
                        self.on_AI_input(instruction)
                    else:
                        self.recenter(playerdirection)

                
                
    def recenter(self, playerdirection):
        cell_rect = self.cell_rect()
        if playerdirection == "DOWN" or playerdirection == "UP":
            if self.player.x >= cell_rect.centerx+5:
                self.on_AI_input("LEFT")
            elif self.player.x <= cell_rect.centerx-5:
                self.on_AI_input("RIGHT")

        elif playerdirection == "RIGHT" or playerdirection == "LEFT":
            if self.player.y >= cell_rect.centery+5:
                self.on_AI_input("UP")
            elif self.player.y <= cell_rect.centery-5:
                self.on_AI_input("DOWN")
    def cell_rect(self):
        tempcurrentCellrow, tempcurrentCellcol = self.maze.indices_from_coordinates(self.player.x, self.player.y)
        top = tempcurrentCellrow*self.maze.tile_size_y
        left = tempcurrentCellcol*self.maze.tile_size_x
        return pygame.Rect(left, top, self.maze.tile_size_x,self.maze.tile_size_y)
    def handle_monsters(self, perceptionList):
        if bool(perceptionList[3]) and self.monster_interact:
            monster = perceptionList[3][0]
            #print(f'there is a monsters nearby and the score is: {monster.mock_fight(self.player)}')
            self.call_genetic.monster = monster
            best_palyer_attributes = self.call_genetic.get_genetic()
            self.player.set_attributes(best_palyer_attributes)
            victoire, _ = monster.mock_fight(self.player) 
            if victoire >= 4:
                print(f'there is a monsters nearby and the score is: {monster.mock_fight(self.player)[0]}')
                self.call_genetic.flag = 0
                self.monster_interact = False
                self.Monster_row, self.Monster_col = self.maze.indices_from_coordinates(self.player.x, self.player.y)
    def on_execute(self):
        self.on_init()
        instruction = None
        index = 0
        maze = []
        with open(self.file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                maze.append(row)
        end_coords = [(i, j) for i, row in enumerate(maze) for j, value in enumerate(row) if value == 'E']
        mazeendrow, mazeendcol = end_coords[0]
        myTreasure = TreasureHunter.Treasures(self.file)
        myTreasure.readMaze()
        currentCellrow, currentCellcol = self.maze.indices_from_coordinates(self.player.get_rect().centerx, self.player.get_rect().centery)
        
        if self.do_treasures:
            if bool(myTreasure.treasure_coords):
                endrow, endcol = myTreasure.treasure_coords[index]
                MyAstar = PathFinder(self.file,currentCellrow,currentCellcol, endrow, endcol)
            else: MyAstar = PathFinder(self.file,currentCellrow,currentCellcol, mazeendrow, mazeendcol)
        else : MyAstar = PathFinder(self.file,currentCellrow,currentCellcol, mazeendrow, mazeendcol)
        MyAstar.A_Star()
        
        while self._running:
            self._clock.tick(GAME_CLOCK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.USEREVENT:
                    self.timer += 0.01
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            old_pos = self.player.get_rect()
            tempcurrentCellrow, tempcurrentCellcol = self.maze.indices_from_coordinates(self.player.get_rect().centerx, self.player.get_rect().centery)
            player_rect = self.player.get_rect()
            cell_rect = self.cell_rect()
            if cell_rect.contains(player_rect):
                currentCellrow = tempcurrentCellrow
                currentCellcol = tempcurrentCellcol
            
            if bool(myTreasure.treasure_coords):
                if myTreasure.treasure_coords[index] == myTreasure.treasure_coords[-1]:
                    MyAstar.currentcol = currentCellcol
                    MyAstar.currentrow = currentCellrow
                    MyAstar.endcol = mazeendcol
                    MyAstar.endrow = mazeendrow
                    MyAstar.A_Star()
                elif (currentCellrow,currentCellcol) == myTreasure.treasure_coords[index]:
                    index += 1
                    MyAstar.endrow, MyAstar.endcol = myTreasure.treasure_coords[index]
                    MyAstar.currentcol = currentCellcol
                    MyAstar.currentrow = currentCellrow
                    MyAstar.A_Star()
            

            perceptionList = self.maze.make_perception_list(self.player, self._display_surf)
            if bool(perceptionList[-1]):
                 instruction = self.handleDoor
                 self.on_AI_input(instruction)
            if abs(self.Monster_col - currentCellcol) == 2 or abs(self.Monster_row - currentCellrow) == 2:
                self.monster_interact = True
            self.handle_monsters(perceptionList)
            
            if (currentCellrow, currentCellcol) not in MyAstar.path:
                MyAstar.currentcol = currentCellcol
                MyAstar.currentrow = currentCellrow
                MyAstar.path = {}
                MyAstar.A_Star()
            NextCellRow, NextCellCol, instruction = MyAstar.NextMove(currentCellrow,currentCellcol)
            self.obstacle(perceptionList,currentCellrow, currentCellcol, NextCellRow, NextCellCol)

            tempcurrentCellrow, tempcurrentCellcol = self.maze.indices_from_coordinates(self.player.get_rect().centerx, self.player.get_rect().centery)
            player_rect = self.player.get_rect()
            cell_rect = self.cell_rect()
            if cell_rect.contains(player_rect):
                currentCellrow = tempcurrentCellrow
                currentCellcol = tempcurrentCellcol

            if (currentCellrow, currentCellcol) not in MyAstar.path:
                MyAstar.currentcol = currentCellcol
                MyAstar.currentrow = currentCellrow
                MyAstar.path = {}
                MyAstar.A_Star()

            nextRow, nextCol, instruction = MyAstar.NextMove(currentCellrow,currentCellcol)
            self.on_keyboard_input(keys)
            self.on_AI_input(instruction)
            
            new_pos = self.player.get_rect()
            playerdirection = self.find_direction(currentCellrow, currentCellcol, nextRow, nextCol)
            if old_pos == new_pos:
                if playerdirection == "UP" or playerdirection == "DOWN":
                    if maze[currentCellrow][currentCellcol+1] != "1":
                        MyAstar.path[(currentCellrow,currentCellcol)] = (currentCellrow, currentCellcol+1)
                    elif maze[currentCellrow][currentCellcol-1] != "1":
                        MyAstar.path[(currentCellrow,currentCellcol)] = (currentCellrow, currentCellcol-1)
                elif playerdirection == "RIGHT" or playerdirection == "LEFT":
                    if maze[currentCellrow-1][currentCellcol] != "1":
                        MyAstar.path[(currentCellrow,currentCellcol)] = (currentCellrow-1, currentCellcol)
                    elif maze[currentCellrow+1][currentCellcol] != "1":
                        MyAstar.path[(currentCellrow,currentCellcol)] = (currentCellrow+1, currentCellcol-1)
            
            if self.on_coin_collision():
                self.score += 1
            if self.on_treasure_collision():
                self.score += 10
            monster = self.on_monster_collision()
            if monster:
                if monster.fight(self.player):
                    self.maze.monsterList.remove(monster)
                    self.score += 50
                else:
                    self._running = False
                    self._dead = True
            if self.on_exit():
                self._running = False
                self._win = True
            self.on_render()

        while self._win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._win = False
            self.on_win_render()

        while self._dead:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._dead = False
            self.on_death_render()

        self.on_cleanup()

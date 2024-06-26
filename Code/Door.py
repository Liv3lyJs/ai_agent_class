import random


class Door:
    # STATES = [['gold', 'red', 'red', 'blue', 'yellow', '', ''],
    #           ['gold', 'blue', 'blue', 'yellow', '', '', ''],
    #           ['gold', 'red', 'white', 'blue', 'yellow', 'white', 'black'],
    #           ['silver', 'red', 'red', 'blue', 'yellow', '', ''],
    #           ['silver', 'yellow', 'red', 'blue', 'yellow', 'black', ''],
    #           ['silver', 'red', 'red', 'blue', '', '', ''],
    #           ['bronze', 'red', 'red', 'blue', 'yellow', '', ''],
    #           ['bronze', 'red', 'red', 'blue', 'yellow', 'black', ''],
    #           ['bronze', 'red', 'red', 'blue', 'blue', 'black', 'white'],
    #           ['bronze', 'yellow', 'white', 'blue', 'yellow', 'black', 'white']]

    # KEYS = ['first',
    #         'second',
    #         'fourth',
    #         'second',
    #         'first',
    #         'first',
    #         'first',
    #         'first',
    #         'third',
    #         'sixth']
    STATES = [['gold', 'yellow', 'blue', 'white', 'white', '', ''],
              ['gold', 'blue', 'blue', 'blue', '', '', ''],
              ['gold', 'blue', 'white', 'red', 'red', 'white', 'black'],
              ['silver', 'black', 'red', 'red', 'red', '', ''],
              ['gold', 'red', 'blue', 'red', 'blue', 'black', ''],
              ['silver', 'blue', 'red', 'yellow', '', '', ''],
              ['bronze', 'blue', 'blue', 'blue', 'blue', '', ''],
              ['bronze', 'white', 'black', 'black', 'blue', 'yellow', ''],
              ['bronze', 'blue', 'blue', 'red', 'yellow', 'black', 'white'],
              ['bronze', 'black', 'white', 'red', 'red', 'black', '']]

    KEYS = ['first',
            'second',
            'fourth',
            'fourth',
            'fourth',
            'first',
            'second',
            'first',
            'fourth',
            'first']
    def __init__(self, rect):
        self.rect = rect
        i = random.randrange(0, 10)
        self.state = self.STATES[i]
        self.key = self.KEYS[i]

    def check_door(self):
        return self.state

    def unlock_door(self, key):
        if key == self.key:
            return True
        else:
            i = random.randrange(0, 10)
            self.state = self.STATES[i]
            self.key = self.KEYS[i]
            return False

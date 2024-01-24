import search
import math
import utils

id=314096389
# link to chatGPT chat - https://chat.openai.com/share/40894136-64f7-4f5a-ab2c-9bae997c4a43

""" Rules """
RED = 20
BLUE = 30
YELLOW = 40
GREEN = 50
PACMAN = 77

class PacmanProblem(search.Problem):
    """This class implements a pacman problem"""
    def __init__(self, initial):
        """ Magic numbers for ghosts and Packman: 
        2 - red, 3 - blue, 4 - yellow, 5 - green and 7 - Packman.""" 

        self.locations = dict.fromkeys((7, 2, 3, 4, 5))
        self.dead_end = False

        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)

                
    def successor(self, state):
        """ Generates the successor state """
        utils.raiseNotDefined()

    def result(self, state, move):
        """given state and an action and return a new state"""

        utils.raiseNotDefined()
    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        '''note - code ouptputed by chatGPT after it was given context and promt of the required task, in this case goal_test'''
        # Flatten the 2D matrix 'state' into a 1D list using list comprehension
        flattened_state = [cell for row in state for cell in row]
         # Check if the value '11' (representing a pill) is not present in the flattened list
        return 11 not in flattened_state
        utils.raiseNotDefined()
        
    def h(self, node):
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate"""
        utils.raiseNotDefined()

def create_pacman_problem(game):
    print ("<<create_pacman_problem")
    """ Create a pacman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    return PacmanProblem(game)

game =()


create_pacman_problem(game)

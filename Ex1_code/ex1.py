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

    def calculate_new_position(self, state, entity, movement):
        """Calculates the new position for the given entity based on the movement"""

        # Find the current position of the entity in the state
        for i, row in enumerate(state):
            for j, cell in enumerate(row):
                if cell == entity:
                    current_position = (i, j)
                    break

        # Calculate the new position based on the movement
        new_position = (current_position[0] + movement[0], current_position[1] + movement[1])

        return new_position


    def is_valid_position(self, position, state):
        """Checks if the given position is within bounds and not a wall"""

        # Extract the row and column indices from the position tuple
        row, col = position

        # Check if the position is within the bounds of the state
        if 0 <= row < len(state) and 0 <= col < len(state[0]):
            return True;
            # Check if the position does not correspond to a wall (value 99)
            # return state[row][col] != 99

        return False

    # def successor (self, state):


    def successor(self, state):
        """Generates the successor state"""

        # Define possible movements for entities
        # movements = utils.orientations
        movements = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}

        # Initialize an empty list to store valid successor states
        valid_successors = []

        # Iterate over possible movements for Pacman
        for move_pacman in movements:
            # Calculate new position for Pacman
            new_pacman_position = self.calculate_new_position(state, PACMAN, movements[move_pacman])
            
            # Check if the new position is within bounds and not a wall
            if self.is_valid_position(new_pacman_position, state):
                
                # Initialize a list to store new positions for ghosts
                new_ghost_positions = []
                
                # Flag to track if all entities have valid movements
                all_entities_valid = True
                
                # Iterate over all ghost entities in the state
                for ghost_entity in [RED]:  # Add more ghosts as needed
                    # Initialize a list to store new positions for the current ghost
                    new_positions_for_ghost = []
                    
                    # Iterate over possible movements for the current ghost
                    for move_ghost in movements:
                        # Calculate new position for the current ghost
                        new_ghost_position = self.calculate_new_position(state, ghost_entity, movements[move_ghost])
                        
                        # Check if the new position is within bounds and not a wall
                        if self.is_valid_position(new_ghost_position, state):
                            new_positions_for_ghost.append(new_ghost_position)
                        else:
                            # If any entity has no valid movement, set the flag to False
                            all_entities_valid = False
                            break
                    
                    # If all entities are valid, append the list of new positions for the current ghost
                    if all_entities_valid:
                        new_ghost_positions.append(new_positions_for_ghost)
                    else:
                        all_entities_valid = True
                        break
                
                # If all entities have valid movements, append to valid_successors
                if all_entities_valid:
                    print('here')
                    valid_successors.append((new_pacman_position, *new_ghost_positions))

        return valid_successors

    # def successor(self, state):
        """Generates the successor state"""
        '''note - code ouptputed by chatGPT after it was given context and promt of the required task, in this case successor'''

        # Define possible movements for entities
        movements = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}

        # Initialize an empty list to store valid successor states
        valid_successors = []

        # Iterate over possible movements for Pacman
        for move_pacman in movements:
            # Calculate new position for Pacman
            new_pacman_position = self.calculate_new_position(state, PACMAN, movements[move_pacman])
            # Check if the new position is within bounds and not a wall
            if self.is_valid_position(new_pacman_position, state):
                
                # Initialize a list to store new positions for ghosts
                new_ghost_positions = []

                # Flag to track if all entities have valid movements
                all_entities_valid = True
                
                # Iterate over all ghost entities in the state
                for ghost_entity in [RED]:
                    # Calculate new position for each ghost
                    new_ghost_position = self.calculate_new_position(state, ghost_entity, movements[move_pacman])
                    
                    # Check if the new position is within bounds and not a wall
                    if self.is_valid_position(new_ghost_position, state):
                        new_ghost_positions.append(new_ghost_position)
                    
                # Append the valid successor states to the list
                valid_successors.append((new_pacman_position, *new_ghost_positions))

                print (valid_successors)
        return valid_successors

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

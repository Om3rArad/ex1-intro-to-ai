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
EATEN = 88
WALL = 99
G_R = 2
G_B = 3
G_Y = 4
G_G = 5
PAC = 7
EMPTY = 10
PILL = 11

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

    def idx(self, entity): 
        return int(entity/10)
    
    def get_location(self, state, entity):
        """Find location of the entity in the state"""
        current_position = self.locations[self.idx(entity)]

        if (not current_position):
            # Handle the case where locations is not initialized
            current_position = self.get_current_location(state, entity)
            self.locations[self.idx(entity)]

        return current_position
    
    def get_current_location(self, state, entity):
        """Find location of the entity that has moved in the state"""
        current_position = None
        for i, row in enumerate(state):
            for j, cell in enumerate(row):
                if self.idx(cell) == self.idx(entity):
                    current_position = (i, j)
                    break
        
        return current_position

    def calculate_new_position(self, state, entity, movement):
        """Calculates new position for the given entity based on the movement"""
        # Find location of the entity in the state
        current_position = self.get_current_location(state, entity)

        # Calculate the new position based on the movement
        if (current_position):
            new_position = (current_position[0] + movement[0], current_position[1] + movement[1])

            if (self.is_valid_position(new_position, state)):
                return new_position
        
        return None


    def is_valid_position(self, position, state):
        """Checks if given position is within bounds and not a wall"""
        if (position):
            # Extract the row and column indices from the position tuple
            row, col = position

            invalid_positions = [20,21,30,31,40,41,50,51,99]

            # Check if the position is within the bounds of the state
            if 0 <= row < len(state) and 0 <= col < len(state[0]):
                # Check if the position does not correspond to a wall (value 99)
                return state[row][col] not in invalid_positions

        return False
    
    def print_state(self, state):
        for row in state:
            print (row)
        print ()
    
    def old_update_state(self, state, new_position, entity):
        def update_row(row, position, value):
            return [value if idx == position else cell for idx, cell in enumerate(row)]

        result = []
        old_position = self.get_current_location(state, entity)
        for num_row, cells_row in enumerate(state):
            if num_row == old_position[0] and entity == PACMAN:
                cells_row = update_row(cells_row, old_position[1], EMPTY)
            if num_row == new_position[0]:
                if cells_row[new_position[1]] == 11:
                    print("PACMAN EAT")
                # self.locations[self.idx(entity)] = new_position
                cells_row = update_row(cells_row, new_position[1], PACMAN)
            result.append(cells_row)

        return tuple(result)
    
    def update_state(self, state, new_position, entity):
        def update_row(row, position, value):
            return tuple(value if idx == position else cell for idx, cell in enumerate(row))

        result = []
        old_position = self.get_current_location(state, entity)
        old_value = state[old_position[0]][old_position[1]]
        for num_row, cells_row in enumerate(state):
            # Ghost does not change slots previous value (X0 -> 10, X1 -> 11)
            if num_row == old_position[0]:
                # Pacman always leaves behind an emply slot (10)
                if entity == PACMAN or old_value%10 == 0:
                    cells_row = update_row(cells_row, old_position[1], EMPTY)
                else:
                    cells_row = update_row(cells_row, old_position[1], PILL)

            if num_row == new_position[0]:
                pill = 0
                if cells_row[new_position[1]] == PILL:
                    if entity == PACMAN:
                        # Pacman eats a pill
                        pill = 0
                        print("PACMAN EAT")
                    else:
                        # Ghost does not eat a pill (11 -> X1)
                        pill = 1
                elif cells_row[new_position[1]] == PACMAN: 
                    # Pacman gets eaten by a ghost (88)
                    cells_row = update_row(cells_row, new_position[1], EATEN)
                    result.append(cells_row)
                    self.dead_end = True
                    continue
                
                cells_row = update_row(cells_row, new_position[1], entity + pill)

            result.append(cells_row)

        return tuple(result)
    
    def manhattan_distance(self, position1, position2):
        """Calculate the Manhattan distance between two positions."""
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])
  
    def find_best_move(self, state, ghost_entity, pacman_position):
        """Find best movement direction for current ghost based on minimum Manhattan distance to Pacman"""
        best_move = None
        # Get locations of Pacman and the ghost
        pacman_position = self.get_current_location(state, PACMAN)
        ghost_position = self.get_current_location(state, ghost_entity)

        # Define possible movements for the ghost
        movements = utils.orientations
        movements = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # Calculate Manhattan distances for each possible movement
        distances = {}
        for move in movements:
            new_ghost_position = self.calculate_new_position(state, ghost_entity, move)
            if (new_ghost_position):
                distances[move] = self.manhattan_distance(new_ghost_position, pacman_position)

        if(distances):
            # Find the movement with the minimum distance (ties broken in the order: right, down, left, up)
            best_move = min(distances, key=lambda move: (distances[move], movements.index(move)))

        return best_move

    def successor(self, state):
        """Generates the successor state"""
        
        # Initialize an empty list to store valid successor states
        valid_successors = []
        
        # Define possible movements for entities
        movements = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}

        # Iterate over possible movements for Pacman
        for move_pacman in movements:
            # Calculate new state for Pacman movement
            new_state_tuple = self.result(state, (PACMAN, movements[move_pacman]))
            
            if (not new_state_tuple):
                continue
            else:
                new_state, new_position_pacman = new_state_tuple

            # Initialize a variable to store pacman's movement 
            movement = move_pacman
            print(movement)

            # Iterate over all ghost entities in the state
            for ghost_entity in [RED, BLUE, YELLOW, GREEN]:
                # Find the best movement direction for the current ghost
                best_move_ghost = self.find_best_move(new_state, ghost_entity, new_position_pacman)

                # Calculate new state for Ghost movement
                new_state = self.result(new_state, (ghost_entity, best_move_ghost))
                if (self.dead_end):
                    self.dead_end = False
                    break

            # Yield the tuple (action, state) for this round with new entities positions
            if (self.get_current_location(new_state, PACMAN)):
                valid_successors.append((movement, new_state))
            
            # yield (movement, new_state_ghost)
        self.print_state(state)
        # print(valid_successors)
        return valid_successors

    def result(self, state, move):
        """given state and an action and return a new state"""
        # Extract entity and orientation from the action
        entity, orientation = move

        # Check if the provided move is a valid orientation
        if orientation not in utils.orientations:
            # Unknown action, return the current state
            return state

        # Calculate the new position for the entity based on the orientation
        new_position = self.calculate_new_position(state, entity, orientation)

        # Check if the new position is within bounds and not a wall
        if (new_position):
            # Update the state based on the moved entity
            if entity == PACMAN:
                # Pacman leaves behind an emply slot ('10')
                new_state = (self.update_state(state, new_position, PACMAN), new_position)
            else:
                # Ghost does not change slots old value
                new_state = self.update_state(state, new_position, entity)

            return new_state
        else:
            # If the movement is not valid, return the current state
            if (entity == PACMAN):
                return None
            else:
                return state

        
    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state"""
        '''note - code ouptputed by chatGPT after it was given context and promt of the required task, in this case goal_test'''
        # Flatten the 2D matrix 'state' into a 1D list using list comprehension
        flattened_state = [cell % 10 for row in state for cell in row]
         # Check if the value '11' (representing a pill) is not present in the flattened list
        return 1 not in flattened_state
        
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

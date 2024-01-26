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
G_R = 2
G_B = 3
G_Y = 4
G_G = 5
PAC = 7

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
            for i, row in enumerate(state):
                for j, cell in enumerate(row):
                    if cell == entity:
                        current_position = (i, j)
                        self.locations[self.idx(entity)] = current_position
                        break
        
        return current_position

    def calculate_new_position(self, state, entity, movement):
        """Calculates new position for the given entity based on the movement"""
        # Find location of the entity in the state
        current_position = self.get_location(state, entity)

        # Calculate the new position based on the movement
        if (current_position):
            new_position = (current_position[0] + movement[0], current_position[1] + movement[1])

            return new_position
        
        return None


    def is_valid_position(self, position, state):
        """Checks if given position is within bounds and not a wall"""
        if (position):
            # Extract the row and column indices from the position tuple
            row, col = position

            # Check if the position is within the bounds of the state
            if 0 <= row < len(state) and 0 <= col < len(state[0]):
                return True;
                # Check if the position does not correspond to a wall (value 99)
                # return state[row][col] != 99

        return False
    
    def find_best_move(self, state, ghost_entity):
        """Find best movement direction for current ghost based on minimum Manhattan distance to Pacman"""

        # Get locations of Pacman and the ghost
        pacman_position = self.locations[PAC]
        ghost_position = self.get_location(state, ghost_entity)

        # Define possible movements for the ghost
        movements = utils.orientations

        # Calculate Manhattan distances for each possible movement
        distances = {}
        for move in movements:
            utils.raiseNotDefined()
            new_position = self.calculate_new_position(state, ghost_position, move)
            distances[move] = self.manhattan_distance(new_position, pacman_position)

        # Find the movement with the minimum distance (ties broken in the order: right, down, left, up)
        best_move = min(distances, key=lambda move: (distances[move], movements.keys().index(move)))

        return best_move


    def print_state(self, state):
        for row in state:
            print (row)
    
    def update_state(self, state, new_position, entity):
        def update_row(row, position, value):
            return [value if idx == position else cell for idx, cell in enumerate(row)]

        result = []
        old_position = self.get_location(state, entity)
        for num_row, cells_row in enumerate(state):
            if num_row == old_position[0] and entity == PACMAN:
                cells_row = update_row(cells_row, old_position[1], 10)
            if num_row == new_position[0]:
                if cells_row[new_position[1]] == 11:
                    print("PACMAN EAT")
                self.locations[self.idx(entity)] = new_position
                cells_row = update_row(cells_row, new_position[1], PACMAN)
            result.append(cells_row)

        return tuple(result)

    def successor(self, state):
        """Generates the successor state"""

        # Define possible movements for entities
        movements = utils.orientations
        # movements = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}

        # Initialize an empty list to store valid successor states
        valid_successors = []

        # Iterate over possible movements for Pacman
        for move_pacman in movements:
            # Calculate new position for Pacman
            new_pacman_position = self.calculate_new_position(state, PACMAN, move_pacman)
            
            # Check if the new position is within bounds and not a wall
            print('validating pacman with ', new_pacman_position)
            if self.is_valid_position(new_pacman_position, state):
                print('valid')
                # Iterate over all ghost entities in the state
                for ghost_entity in [RED]:  # Add more ghosts as needed
                    print('ghost ', ghost_entity)
                    # Iterate over possible movements for the current ghost
                    for move_ghost in movements:
                        # Calculate new position for the current ghost
                        new_ghost_position = self.calculate_new_position(state, ghost_entity, move_ghost)
                        
                        # Check if the new position is within bounds and not a wall
                        print(' validating ghost with ', new_ghost_position)
                        if self.is_valid_position(new_ghost_position, state):
                            print('valid')
                            valid_successors.append((new_pacman_position, new_ghost_position))
                
                
                        print("     valid_successors: ", valid_successors)


        return valid_successors
    
    def successor(self, state):
        """Generates the successor state"""

        # Define possible movements for entities
        movements = utils.orientations

        # Iterate over possible movements for Pacman
        for move_pacman in movements:

            # Calculate new state for Pacman movement
            new_state_pacman = self.result(state, (PACMAN, move_pacman))

            # Initialize a variable to store pacman's movement
            pacman_movement = move_pacman

            # Calculate new position for Pacman
            new_pacman_position = self.calculate_new_position(state, PACMAN, move_pacman)

            # Check if the new position is within bounds and not a wall
            if self.is_valid_position(new_pacman_position, state):
                # Iterate over all ghost entities in the state
                for ghost_entity in [RED]:  # Add more ghosts as needed
                    # Iterate over possible movements for the current ghost
                    for move_ghost in movements:
                        # Calculate new position for the current ghost
                        new_ghost_position = self.calculate_new_position(state, ghost_entity, move_ghost)

                        # Check if the new position is within bounds and not a wall
                        if self.is_valid_position(new_ghost_position, state):
                            # Yield the successor state as an (action, state) pair
                            yield (new_pacman_position, new_ghost_position)

    def successor(self, state):
        """Generates the successor state"""

        # Define possible movements for entities
        # movements = utils.orientations
        movements = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}

        # Iterate over possible movements for Pacman
        for move_pacman in movements:
            # Calculate new state for Pacman movement
            new_state_pacman = self.result(state, (PACMAN, movements[move_pacman]))
            
            if (not new_state_pacman):
                continue

            self.print_state(new_state_pacman);

            # Initialize a variable to store pacman's movement 
            movement = move_pacman

            # Iterate over all ghost entities in the state
            for ghost_entity in [RED]:
                # Find the best movement direction for the current ghost
                best_move_ghost = self.find_best_move(state, ghost_entity)

                # Calculate new state for Ghost movement
                new_state_ghost = self.result(new_state_pacman, (ghost_entity, best_move_ghost))

            # Yield the tuple (action, state) for this round with new entities positions
            yield (movement, new_state_ghost)


    def result(self, state, move):
        """given state and an action and return a new state"""
        # Extract entity and orientation from the action
        entity, orientation = move

        # Calculate the new position for the entity based on the orientation
        new_position = self.calculate_new_position(state, entity, orientation)

        # Check if the new position is within bounds and not a wall
        if self.is_valid_position(new_position, state):
            # Update the state based on the moved entity
            if entity == PACMAN:
                # Pacman leaves behind an emply slot ('10')
                new_state = self.update_state(state, new_position, PACMAN)
            else:
                # Ghost does not change slots old value
                new_state = tuple([cell if pos != new_position else cell for pos, cell in enumerate(state)])

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
        flattened_state = [cell for row in state for cell in row]
         # Check if the value '11' (representing a pill) is not present in the flattened list
        return 11 not in flattened_state
        
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

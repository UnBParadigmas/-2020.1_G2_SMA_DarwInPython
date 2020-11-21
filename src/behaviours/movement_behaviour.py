from random import randint
from pade.behaviours.protocols import TimedBehaviour
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message

from game.game_contants import GameConstants, GameActions
from game.board import Board
from behaviours.game_contract_communication import GameCommunicationInitiator, GameCommunicationParticipant
from game.exceptions import InvalidMovementTargetException, InvalidMovimentOriginException



import random
import math
from time import time
import pickle

class MovementBehaviour(GameCommunicationInitiator):

    def __init__(self, agent, message, movement_distance, food_type, reproduction_type):
        super(MovementBehaviour, self).__init__(agent=agent, message=message)

        self.movement_distance = movement_distance
        self.food_type = food_type
        self.reproduction_type = reproduction_type


    def get_response(self, message):

        game_data = pickle.loads(message.content)

        action = self.make_action(game_data['grid'])

        response = {
            'caller_type': self.agent.game_type,
            'orginal_position': self.agent.position,
            'target_position': action['position'],
            'action': action['action']
        }
        
        self.agent.position = action['position']
        display_message(self.agent.aid.name, f'ACTION {action["action"]}')

        return response

    def make_action(self, grid):
        size = (
            len(grid[0]),
            len(grid)
        )

        x, y = self.agent.position
        x_limits = (min(0, x - self.agent.vision_distance), min(size[0], x + self.agent.vision_distance))
        y_limits = (min(0, y - self.agent.vision_distance), min(size[1], y + self.agent.vision_distance))

        target = self.select_target()

        closest_target = self.get_closest_target(x, y, x_limits, y_limits, size, grid, target)

        action = None

        if closest_target is None:
            action = self.random_move(x, y, size)

        else:
            dist_x = closest_target[0] - x
            dist_y = closest_target[1] - y

            
            
            if target == self.reproduction_type and abs(dist_x) + abs(dist_y) == 2:
                display_message(self.agent.aid.name, f'Closest target: {closest_target}, {dist_x, dist_y}, {self.agent.position} ')
                action = self.reproduce(x, y)

            elif target == self.reproduction_type and abs(dist_x) + abs(dist_y) == 1:
                action = self.random_move(x, y, size)
                
            else:
                action = self.move(x, y, size, dist_x, dist_y)
                
        return action

    def select_target(self):
        if self.agent.hunger > self.agent.max_hunger:
            return self.food_type
        else:
            return self.reproduction_type

    def random_move(self, x, y, size):
        new_x = self.agent.position[0] + randint(-1, 1)
        new_y = self.agent.position[1] + randint(-1, 1)

        new_position = (
            new_x if 0 <= new_x < size[0] else x,
            new_y if 0 <= new_y < size[0] else y
        )

        return {
            'action': GameActions.MOVE,
            'position': new_position
        }

    def get_closest_target(self, x, y, x_limits, y_limits, size, grid, target):

        closest_distance, closest_target = None, None
        for current_x in range(x_limits[0], x_limits[1]):
            for current_y in range(y_limits[0], y_limits[1]):

                if current_x == x and current_y == y:
                    continue

                if current_x >= size[0] \
                        or current_x < 0 \
                        or current_y >= size[1]\
                        or current_y < 0:
                    continue

                if grid[current_x][current_y] == target:

                    distance = abs(
                        math.sqrt((x - current_x)**2 + (y - current_y)**2))

                    if closest_distance is None or distance < closest_distance:
                        closest_distance = distance
                        closest_target = (current_x, current_y)

        return closest_target

    def reproduce(self, x, y):
        
        self.agent.hunger += 30
        
        return {
            'action': GameActions.REPRODUCE,
            'position': (x,y)
        }

    def move(self, x, y, size, dist_x, dist_y):
        
        new_x = None
        new_y = None
        if abs(dist_x) < abs(dist_y) and dist_x != 0 or dist_y == 0:
            # move on x
            value = min(abs(dist_x), self.movement_distance)
            signal = 1 if dist_x >= 0 else -1
            new_x = x + (value * signal)
            new_y = y

        elif abs(dist_x) >= abs(dist_y) and dist_y != 0 or dist_x == 0:
            # move on y
            value = min(abs(dist_y), self.movement_distance)
            signal = 1 if dist_y >= 0 else -1
            new_y = y + (value * signal)
            new_x = x

        new_position = (
            new_x if 0 <= new_x < size[0] else 0,
            new_y if 0 <= new_y < size[1] else 0
        )

        return {
            'action': GameActions.MOVE,
            'position': new_position
        }
    
    def eat(self, old_grid):
        if old_grid == self.food_type:
            self.agent.hunger =  0

    def reset_event(self, message):
        data = pickle.loads(message.content)        
        self.agent.position = data['orginal_position']
 
        if 'alive' in data and data['alive'] is False:
            self.agent.alive = False

    def confirm_event(self, message):
        data = pickle.loads(message.content)
        self.eat(data['old_grid'])

class MovementProviderBehaviour(GameCommunicationParticipant):

    def get_cfp_content(self, message):
        content = pickle.loads(message.content)
        return {
            'grid': self.agent.board.grid,
            'position': content['position']
        }
    
    def create_inform_message(self, message):
        content = ''
        data = pickle.loads(message.content)

        if data['action'] == GameActions.REPRODUCE:
            self.agent.spawn_agent_close_to_position(
                data['caller_type'],
                data['orginal_position']
            )     

            content = {'msg': 'OK', 'old_grid': data['caller_type'], 'target_position': data['target_position'], 'position': data['orginal_position']}
        else:
            try:
                old_grid = self.agent.board.execute_move(
                    data['caller_type'],
                    data['orginal_position'],
                    data['target_position']
                )
                content = {'msg': 'OK', 'old_grid': old_grid, 'target_position': data['target_position'], 'position': data['target_position']}
            except InvalidMovimentOriginException:
                display_message(self.agent.aid.name, 'EXCEPTION: Invalid Movement Origin')
                
                content = {
                    'msg': 'ERROR',
                    'alive': False,
                    'orginal_position': data['orginal_position'],
                    'grid': self.agent.board.grid,
                    'position': data['orginal_position']
                }

            except InvalidMovementTargetException:
                display_message(self.agent.aid.name, 'EXCEPTION: Invalid Movement Target')
                content = {
                    'msg': 'ERROR',
                    'orginal_position': data['orginal_position'],
                    'grid': self.agent.board.grid,
                    'position': data['orginal_position']
                } 

        return content

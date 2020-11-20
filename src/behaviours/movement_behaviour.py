from random import randint
from pade.behaviours.protocols import TimedBehaviour
from pade.acl.messages import ACLMessage
from pade.misc.utility import display_message

from game.board import Board
from behaviours.game_contract_communication import GameCommunicationInitiator, GameCommunicationParticipant

import random
import math
from time import time

class MovementBehaviour(GameCommunicationInitiator):

    def __init__(self, agent, message, vision_distance, movement_distance, food_type, reproduction_type):
        super(MovementBehaviour, self).__init__(agent=agent, message=message)

        self.vision_distance = vision_distance
        self.movement_distance = movement_distance
        self.food_type = food_type
        self.reproduction_type = reproduction_type

        random.seed(self.agent.aid.port)

    def get_response(self, message):

        game_data = pickle.loads(message.content)

        new_position = self.movement(game_data['grid'])

        response = {
            'caller_type': self.agent.game_type,
            'orginal_position': self.agent.position,
            'target_position': new_position
        }
        
        self.agent.position = new_position
        display_message(self.agent.aid.name,
                        f'Moving from {response["orginal_position"]} to {new_position}')

        return response

    def movement(self, grid):

        size = (
            len(grid[0]),
            len(grid)
        )

        x, y = self.agent.position
        x_limits = (min(0, x - self.vision_distance), min(size[0], x + self.vision_distance))
        y_limits = (min(0, y - self.vision_distance), min(size[1], y + self.vision_distance))


        target = None
        if self.agent.hunger > 10:
            target = self.food_type
        else:
            target = self.reproduction_type

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

                    distance = abs(math.sqrt((x - current_x)**2 + (y - current_y)**2))

                    if closest_distance is None or distance < closest_distance:
                        closest_distance = distance
                        closest_target = (current_x, current_y)

        new_position = None
        if closest_target is None:
            display_message(self.agent.aid.name, f'Target is none')

            new_x = self.agent.position[0] + randint(-1, 1)
            new_y = self.agent.position[1] + randint(-1, 1)

            new_position = (
                new_x if 0 <= new_x < size[0] else x,
                new_y if 0 <= new_y < size[0] else y
            )

        else:

            dist_x = closest_target[0] - x
            dist_y = closest_target[1] - y

            display_message(self.agent.aid.name, f'Target: {target} -- Closest Target: {closest_target} -- dists: {[dist_x, dist_y]}')

            new_x = None
            new_y = None
            if abs(dist_x) < abs(dist_y) and dist_x != 0 or dist_y == 0:
                # move on x
                display_message(self.agent.aid.name, f'Move on X')
                value = min(abs(dist_x), self.movement_distance)
                signal = 1 if dist_x >= 0 else -1
                new_x = x + (value * signal)
                new_y = y
            elif abs(dist_x) >= abs(dist_y) and dist_y != 0 or dist_x == 0:
                # move on y
                display_message(self.agent.aid.name, f'Move on Y')
                value = min(abs(dist_y), self.movement_distance)
                signal = 1 if dist_y >= 0 else -1
                new_y = y + (value * signal)
                new_x = x

            new_position = (
                new_x if 0 <= new_x < size[0] else 0,
                new_y if 0 <= new_y < size[1] else 0
            )
            display_message(self.agent.aid.name, f'New position: X::{new_x} --- Y::{new_y}')

            max(0, min(size[0] -1, new_x))

        return new_position

    
    def reset_event(self, message):
        data = pickle.loads(message.content)
        self.agent.position = data['orginal_position']

    def confirm_event(self, message):
        data = pickle.loads(message.content)
        if data['old_grid'] == self.food_type:
            self.agent.hunger =  0

class MovementProviderBehaviour(GameCommunicationParticipant):

    def get_cfp_content(self, message):
        return {
            'grid': self.agent.board.grid,
        }
    
    def create_inform_message(self, message):

        content = ''
        data = pickle.loads(message.content)
        try:
            old_grid = self.agent.board.execute_move(
                data['caller_type'],
                data['orginal_position'],
                data['target_position']
            )
            content = {'msg': 'OK', 'old_grid': old_grid}
        except Exception as e:
            display_message(self.agent.aid.name,
                            'EXCEPTION: Invalid Movement')
            content = {
                'msg': 'ERROR',
                'orginal_position': data['orginal_position'],
                'grid': self.agent.board.grid
            } 

        return content
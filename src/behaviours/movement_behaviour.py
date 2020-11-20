from random import randint
from pade.behaviours.protocols import TimedBehaviour
from pade.acl.messages import ACLMessage
from pade.behaviours.protocols import FipaContractNetProtocol
from pade.misc.utility import display_message

from game.board import Board

import pickle
import random
import math
from time import time


class MovementBehaviour(FipaContractNetProtocol):

    def __init__(self, agent, message, vision_distance, movement_distance, food_type, reproduction_type):
        super(MovementBehaviour, self).__init__(
            agent=agent, message=message, is_initiator=True)

        self.replace_message(message)

        self.vision_distance = vision_distance
        self.movement_distance = movement_distance
        self.food_type = food_type
        self.reproduction_type = reproduction_type

    def replace_message(self, message):
        self.cfp = message
        self.message = message

    def handle_all_proposes(self, proposes):

        super(MovementBehaviour, self).handle_all_proposes(proposes)

        if len(proposes) < 1:
            display_message(self.agent.aid.name, 'No PROPOSE Received')

        game_data = pickle.loads(proposes[0].content)

        response = self.compute_next_position(game_data)
        self.send_movement_response(response, proposes[0].sender)
        
    def compute_next_position(self, game_data):
        
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

    def send_movement_response(self, response, sender):
        
        answer = ACLMessage(ACLMessage.ACCEPT_PROPOSAL)
        answer.set_protocol(ACLMessage.FIPA_CONTRACT_NET_PROTOCOL)
        answer.set_content(pickle.dumps(response))
        answer.add_receiver(sender)
        self.agent.send(answer)

    def movement(self, grid):

        size = (
            len(grid[0]),
            len(grid)
        )

        x, y = self.agent.position
        x_limits = (min(0, x - self.vision_distance), min(size[0], x + self.vision_distance))
        y_limits = (min(0, y - self.vision_distance), min(size[1], y + self.vision_distance))


        target = None
        if self.agent.hunger < 50:
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

            new_position = (
                self.agent.position[0] + 1 if 0 <= self.agent.position[0] + 1 < size[0] else 0,
                self.agent.position[1]
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

    def handle_inform(self, message):
        # TODO: Deal with error on position set
        super(MovementBehaviour, self).handle_inform(message)
        display_message(self.agent.aid.name, 'INFORM message received')

        data = pickle.loads(message.content)
        display_message(self.agent.aid.name, f'INFORM data: {data}')

        if data['msg'] != 'OK':
            self.agent.position = data['orginal_position']
            game_data = {
                'grid': data['grid']
            }

            response = self.compute_next_position(game_data)
            self.send_movement_response(response, message.sender)

    def handle_refuse(self, message):
        super(MovementBehaviour, self).handle_refuse(message)
        display_message(self.agent.aid.name, 'REFUSE message received')

    def handle_propose(self, message):
        super(MovementBehaviour, self).handle_propose(message)
        display_message(self.agent.aid.name, 'PROPOSE message received')

class MovementProviderBehaviour(FipaContractNetProtocol):

    def __init__(self, agent):
        super(MovementProviderBehaviour, self).__init__(
            agent=agent,
            message=None,
            is_initiator=False
        )

    def handle_cfp(self, message):
        display_message(self.agent.aid.name, 'handle CFP - call later')
        self.agent.call_later(1.0, self._handle_cfp, message)

    def _handle_cfp(self, message):
        super(MovementProviderBehaviour, self).handle_cfp(message)
        self.message = message

        display_message(self.agent.aid.name, 'CFP message received')

        answer = self.message.create_reply()
        answer.set_performative(ACLMessage.PROPOSE)

        data = {
            'grid': self.agent.board.grid,
        }

        answer.set_content(pickle.dumps(data))

        self.agent.send(answer)

    def handle_reject_propose(self, message):
        super(MovementProviderBehaviour, self).handle_reject_propose(message)
        display_message(self.agent.aid.name,
                        'REJECT_PROPOSAL message received')

    def handle_accept_propose(self, message):
        super(MovementProviderBehaviour, self).handle_accept_propose(message)
        display_message(self.agent.aid.name,
                        'ACCEPT_PROPOSE message received')

        content = ''
        data = pickle.loads(message.content)
        try:
            self.agent.board.execute_move(
                data['caller_type'],
                data['orginal_position'],
                data['target_position']
            )
            content = {'msg': 'OK'}
        except Exception as e:
            display_message(self.agent.aid.name,
                            'EXCEPTION: Invalid Movement')
            content = {
                'msg': 'ERROR',
                'orginal_position': data['orginal_position'],
                'grid': self.agent.board.grid
            } 

        answer = message.create_reply()
        answer.set_performative(ACLMessage.INFORM)
        answer.set_content(pickle.dumps(content))
        self.agent.send(answer)
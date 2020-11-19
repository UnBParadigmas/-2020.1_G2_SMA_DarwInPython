import pickle

class GameMessage:

    def __init__(self, board, x, y, action):
    
        self.board = board
        self.x = x
        self.y = y
        self.action = action
    
    def get_message(self):

        return {
            'board': self.board,
            'x': self.x,
            'y': self.y,
            'action': self.action
        }

    @staticmethod
    def from_message_content(message_content):
        data = pickle.loads(message_content)

        return GameMessage(**data)
    
class GameConstants:

    GRASS = 1
    RABBIT = 2
    CARROT = 3
    WOLF = 4

    COLORS = {
        GRASS: (0, 180, 50),
        RABBIT: (255, 255, 255),
        CARROT: (210, 61, 0),
        WOLF: (125, 125, 125)
    }

class GameActions:
    MOVE = 'move'
    REPRODUCE = 'reproduce'
    KILL = 'kill'
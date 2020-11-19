class GameConstants:

    GRASS = 1
    RABBIT = 2
    CARROT = 3

    COLORS = {
        GRASS: (0, 255, 0),
        RABBIT: (255, 255, 255),
        CARROT: (255, 92, 0)
    }

    class Actions:
        MOVE = 'move'
        EAT = 'eat'
        REPRODUCE = 'reproduce'
        INQUIRE = 'inquire'

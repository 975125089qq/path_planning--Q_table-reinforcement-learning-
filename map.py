import numpy as np


def generate_map(map_size, per, ENDX, ENDY):
    """generate a map the size of map_size * map_size"""
    """'per' part of the map is obstacle"""
    map = np.random.random((map_size, map_size))
    for i in range(map.shape[0]):
        for j in range(map.shape[0]):
            if map[i, j] < per:
                map[i, j] = 1  # an obstacle
            else:
                map[i, j] = 0
    map[ENDX, ENDY] = 0  # the goal shouldn't be an obstacle
    return map

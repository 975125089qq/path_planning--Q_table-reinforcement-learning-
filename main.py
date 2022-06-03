"""a small program to find the best route using Q table"""
"""the map, starting point, ending point can be customized"""
"""this program isn't perfect, when the map is big, it may fail"""
from robot import Robot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

MAP_SIZE = 6  # the size of a map
BEGINNING_POSITION_X = 0  # the starting point
BEGINNING_POSITION_Y = 0
ENDING_POSITION_X = MAP_SIZE - 1  # the goal
ENDING_POSITION_Y = MAP_SIZE - 1
EPISODES = 6000  # how many iterations to study
LEN_OB = 1000  # how often to show the movement visually
MOVEMENT = MAP_SIZE * 5  # number of movements in an iteration
MOVE_PENALTY = 1
OBSTACLE_PENALTY = 200
GOAL_REWARD = 500
epsilon = 0.9
DECAY = 0.998
# the color
picture = {"robot": (255, 0, 0), "goal": (0, 0, 255)}

"""parameters of the Q learning"""
LEARNING_RATE = 0.1
DISCOUNT = 0.95
"""initialize the q_table"""
q_table = {}
for i in range(MAP_SIZE):
    for j in range(MAP_SIZE):
        q_table[(i, j)] = [np.random.uniform(-8, 0) for i in range(8)]

episode_rewards = []
"""create the map"""
map = np.array([[0, 0, 0, 0, 0, 1], [0, 0, 1, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 1, 0], [0, 0, 0, 1, 0, 0],
                [1, 1, 1, 1, 0, 0]])
# map = generate_map(MAP_SIZE, 0.3, ENDING_POSITION_X, ENDING_POSITION_Y)


for episode in range(EPISODES):
    robot = Robot(BEGINNING_POSITION_X, BEGINNING_POSITION_Y, MAP_SIZE)
    episode_reward = 0
    PLOT = False
    if episode % LEN_OB == 0 and episode > 0:
        fig = plt.figure()
        ax = fig.add_subplot()
        PLOT = True
    for move in range(MOVEMENT):
        """take action"""
        position = (robot.x, robot.y)
        if np.random.random() > epsilon:
            action = np.argmax(q_table[position])
        else:
            action = np.random.randint(0, 8)
        robot.action(action)

        """if run into an obstacle or reach the goal"""
        if map[robot.x, robot.y] == 1:
            reward = -OBSTACLE_PENALTY
        elif robot.x == ENDING_POSITION_X and robot.y == ENDING_POSITION_Y:
            reward = GOAL_REWARD
        else:
            reward = -MOVE_PENALTY
        """draw the map"""
        if PLOT:
            fig.delaxes(ax)
            ax = fig.add_subplot()
            for i in range(MAP_SIZE):
                for j in range(MAP_SIZE):
                    if map[i, j] == 1:
                        ax.add_patch(patches.Rectangle(xy=(i, j), width=1, height=1, edgecolor="black", fill=True))
                    else:
                        ax.add_patch(patches.Rectangle(xy=(i, j), width=1, height=1, edgecolor="black", fill=False))
            ax.add_patch(
                patches.Rectangle(xy=(BEGINNING_POSITION_X, BEGINNING_POSITION_Y), width=1, height=1, edgecolor="black",
                                  fill=True, color="red"))
            ax.add_patch(
                patches.Rectangle(xy=(robot.x, robot.y), width=1, height=1, edgecolor="black", fill=True,
                                  color="yellow"))
            ax.add_patch(
                patches.Rectangle(xy=(ENDING_POSITION_X, ENDING_POSITION_Y), width=1, height=1, edgecolor="black",
                                  fill=True, color="red"))
            ax.autoscale()
            print(f"episode:{episode},move:{move},reward:{reward}")
            plt.pause(0.1)

        """calculate new q"""
        position_new = (robot.x, robot.y)
        max_future_q = np.max(q_table[position_new])
        q_current = q_table[position][action]

        if reward == GOAL_REWARD:
            q_new = GOAL_REWARD
        else:
            q_new = (1 - LEARNING_RATE) * q_current + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        q_table[position][action] = q_new
        """record reward"""
        episode_reward += reward
        if reward == GOAL_REWARD or reward == -OBSTACLE_PENALTY:
            break
    """update the epsilon"""
    episode_rewards.append(episode_reward)
    epsilon *= DECAY

    """close the figure"""
    if PLOT:
        plt.close(fig)

average_reward = np.convolve(episode_rewards, np.ones(LEN_OB), mode="valid") / LEN_OB
plt.plot([i for i in range(len(average_reward))], average_reward)
plt.xlabel("episode")
plt.ylabel("reward")
plt.show()

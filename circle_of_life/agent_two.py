from environment import Environment
from utils import pick_random
import random


# from visualize import visualize


def pick_neighbor(options):
    next_pos = -1
    if len(options[0]) != 0:
        options[0] = sorted(options[0], key=lambda x: (x[1], -x[2]))
        next_pos = pick_random(options[0])[0]
    elif len(options[1]) != 0:
        options[1] = sorted(options[1], key=lambda x: (x[1], -x[2]))
        next_pos = pick_random(options[1])[0]
    elif len(options[2]) != 0:
        options[2] = sorted(options[2], key=lambda x: (-x[2], x[1]))
        next_pos = pick_random(options[2])[0]
    elif len(options[3]) != 0:
        options[3] = sorted(options[3], key=lambda x: (-x[2], x[1]))
        next_pos = pick_random(options[3])[0]
    elif len(options[4]) != 0:
        next_pos = random.choice(options[4])[0]
    elif len(options[5]) != 0:
        next_pos = pick_random(options[5])[0]

    return next_pos


def move_agent(environment):
    next_pos = environment.agent_pos

    curr_distance_from_prey = environment.distance[environment.agent_pos][environment.prey_pos]
    curr_distance_from_predator = environment.distance[environment.agent_pos][environment.predator_pos]
    options = [[] for _ in range(6)]

    for neighbour in environment.graph.get(environment.agent_pos):
        neighbour_distance_from_prey = environment.distance[neighbour][environment.prey_pos]
        neighbour_distance_from_predator = environment.distance[neighbour][environment.predator_pos]

        if neighbour_distance_from_prey < curr_distance_from_prey and neighbour_distance_from_predator > curr_distance_from_predator:
            options[0].append((neighbour, neighbour_distance_from_prey, neighbour_distance_from_predator))
        elif neighbour_distance_from_prey < curr_distance_from_prey and neighbour_distance_from_predator == curr_distance_from_predator:
            options[1].append((neighbour, neighbour_distance_from_prey, neighbour_distance_from_predator))
        elif neighbour_distance_from_prey == curr_distance_from_prey and neighbour_distance_from_predator > curr_distance_from_predator:
            options[2].append((neighbour, neighbour_distance_from_prey, neighbour_distance_from_predator))
        elif neighbour_distance_from_predator > curr_distance_from_predator:
            options[3].append((neighbour, neighbour_distance_from_prey, neighbour_distance_from_predator))
        elif neighbour_distance_from_prey == curr_distance_from_prey and neighbour_distance_from_predator == curr_distance_from_predator:
            options[4].append((neighbour, neighbour_distance_from_prey, neighbour_distance_from_predator))
        elif neighbour_distance_from_predator == curr_distance_from_predator:
            options[5].append((neighbour, neighbour_distance_from_prey, neighbour_distance_from_predator))

    option = pick_neighbor(options)
    if option != -1:
        next_pos = option
    environment.agent_pos = next_pos


def agent_two(environment):
    steps = 1
    while steps <= 5000:
        steps += 1

        move_agent(environment)

        # check if agent caught prey
        if environment.agent_pos == environment.prey_pos:
            return 1

        environment.move_prey()

        # check if agent caught prey
        if environment.agent_pos == environment.prey_pos:
            return 1

        environment.move_predator()

        # check if agent is dead
        if not environment.check_agent_alive():
            return 0

    return -1


if __name__ == "__main__":

    # N - Number of Nodes, NG - Number of Graphs
    N, NG, runs = 50, 100, 30

    average_rate, metric = [0, 0, 0], []
    for num in range(NG):

        # Creating Environment
        env = Environment(N)

        # Add Edges
        env.add_edges(N)

        # Compute Distance matrix using Floyd Warshall
        env.floyd_warshall()

        rate = [0] * 3
        for run in range(runs):

            result = agent_two(env)

            if result == 1:
                rate[0] += 1
            elif result == 0:
                rate[1] += 1
            else:
                rate[2] += 1

            if run < runs - 1:
                # Resetting agent, prey and predator positions
                env.prey_pos, env.predator_pos = random.randint(1, N), random.randint(1, N)
                env.agent_pos = env.spawn_agent()

        metric.append(rate)
    for i in range(len(metric)):
        average_rate[0] += metric[i][0]
        average_rate[1] += metric[i][1]
        average_rate[2] += metric[i][2]
        print(metric[i][0], metric[i][1], metric[i][2])

    print('Avg(Agent Success Rate): ', average_rate[0] / runs, '%', '|', 'Avg(Agent Failure rate)',
          average_rate[1] / runs, '%' '|', 'Avg(Agent Timeout rate)', average_rate[2] / runs, '%')

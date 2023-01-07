import random

from environment import Environment
from utils import pick_highest_probability_node, pick_neighbor, update_belief


# from visualize import visualize


def update_belief_predator(environment, belief_predator):
    belief_predator_copy = []
    for belief in belief_predator:
        belief_predator_copy.append(belief)

    # Belief update for Predator
    for node in range(1, len(belief_predator)):
        neighbours = environment.graph.get(node)
        prob = 0
        for neighbour in neighbours:
            shortest_paths = environment.all_paths(environment.num_nodes + 1, neighbour, environment.agent_pos)
            count = 0
            for path in shortest_paths:
                if len(path) > 1 and (path[1] == node):
                    count += 1
            prob += belief_predator_copy[neighbour] * (0.4 / len(environment.graph[neighbour]))
            prob += (0.6 * belief_predator_copy[neighbour]) * (count / len(shortest_paths))
        belief_predator[node] = prob
    print("Sum of Belief: ", sum(belief_predator[1:]))


def move_agent(environment, predator_pos):
    next_pos = environment.agent_pos

    curr_distance_from_prey = environment.distance[environment.agent_pos][environment.prey_pos]
    curr_distance_from_predator = environment.distance[environment.agent_pos][predator_pos]
    options = [[] for _ in range(6)]

    for neighbour in environment.graph.get(environment.agent_pos):
        neighbour_distance_from_prey = environment.distance[neighbour][environment.prey_pos]
        neighbour_distance_from_predator = environment.distance[neighbour][predator_pos]

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


def move_distracted_predator(environment):
    options = sorted([(environment.distance[neighbour][environment.agent_pos], neighbour) for neighbour in
                      environment.graph.get(environment.predator_pos)])
    ideal_neighbours = [options[0][1]]

    for iteration in range(1, len(options)):
        if options[iteration][0] == options[0][0]:
            ideal_neighbours.append(options[iteration][1])
        else:
            break
    # implemented distracted behaviour with predator choosing ideal neighbour with 0.6 prob and 0.4 from the other neighbours
    rand = random.randint(1, 100)
    if rand <= 40:
        next_pos = random.choice(environment.graph.get(environment.predator_pos))
    else:
        next_pos = random.choice(ideal_neighbours)
    environment.predator_pos = next_pos


def survey(node, environment):
    return node == environment.predator_pos


def agent_six(environment):
    # Initialise belief vector
    belief_predator = [0.0] * (environment.num_nodes + 1)

    belief_predator[environment.predator_pos] = 1.0

    step, correct_survey = 1, 0
    while step <= 5000:

        highest_belief_node = pick_highest_probability_node(belief_predator)

        # Survey the highest probability node when uncertain
        found_predator = survey(highest_belief_node, environment)
        if found_predator:
            correct_survey += 1

        update_belief(belief_predator, highest_belief_node, found_predator)

        highest_belief_node = pick_highest_probability_node(belief_predator)

        move_agent(environment, highest_belief_node)

        if environment.agent_pos == environment.prey_pos:
            return 1, correct_survey, step

        # Update Belief vector
        update_belief(belief_predator, environment.agent_pos, False)

        environment.move_prey()

        if environment.agent_pos == environment.prey_pos:
            return 1, correct_survey, step

        # Predator moves to its neighbours uniformly at random
        move_distracted_predator(environment)

        if not environment.check_agent_alive():
            return 0, correct_survey, step

        # update belief vector after prey's movement
        update_belief_predator(environment, belief_predator)

        step += 1

    return -1, correct_survey, step


if __name__ == "__main__":

    # N - Number of Nodes, NG - Number of Graphs
    N, NG, runs = 50, 100, 30

    average_rate, metric = [0, 0, 0, 0, 0], []
    for num in range(NG):

        # Creating Environment
        env = Environment(N)

        # Add Edges
        env.add_edges(N)

        # Compute Distance matrix using Floyd Warshall
        env.floyd_warshall()

        rate = [0] * 5
        for run in range(runs):

            result, survey_counter, total_steps = agent_six(env)

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
            rate[3] += survey_counter
            rate[4] += total_steps

        metric.append(rate)
    for i in range(len(metric)):
        average_rate[0] += metric[i][0]
        average_rate[1] += metric[i][1]
        average_rate[2] += metric[i][2]
        average_rate[3] += metric[i][3]
        average_rate[4] += metric[i][4]
        print(metric[i][0], metric[i][1], metric[i][2])

    print('Avg(Agent Success Rate): ', average_rate[0] / runs, '%', '|', 'Avg(Agent Failure rate)',
          average_rate[1] / runs, '%' '|', 'Avg(Agent Timeout rate)', average_rate[2] / runs, '%' '|',
          'Avg(Agents Correct Survey)', (average_rate[3] * 100) / average_rate[4], '%')

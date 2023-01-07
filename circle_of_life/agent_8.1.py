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
            if count > 0:
                prob += (0.6 * belief_predator_copy[neighbour]) * (count / len(shortest_paths))
        belief_predator[node] = prob
    print("Sum of Belief: ", sum(belief_predator[1:]))


def update_belief_prey(environment, belief_prey):
    belief_prey_copy = []
    for belief in belief_prey:
        belief_prey_copy.append(belief)

    for node in range(1, len(belief_prey)):

        neighbors = environment.graph.get(node)

        belief_prey[node] = belief_prey_copy[node] * (1.0 / (len(neighbors) + 1))

        for neighbor in neighbors:
            belief_prey[node] += belief_prey_copy[neighbor] * (1.0 / (len(environment.graph.get(neighbor)) + 1))

    print("Sum of Belief after prey's movement: ", sum(belief_prey[1:]))


def update_belief_after_survey(belief, highest_belief_node, found):
    if found:
        belief[highest_belief_node] = 1.0
        for node in range(1, len(belief)):
            if node != highest_belief_node:
                belief[node] = 0.0
    else:
        prob_highest_belief_node = 1 - (0.9 * belief[highest_belief_node])
        belief[highest_belief_node] *= 0.1
        for node in range(1, len(belief)):
            belief[node] = belief[node] / prob_highest_belief_node
    print("Sum of Belief: ", sum(belief[1:]))


def move_agent(environment, predator_pos, prey_pos):
    next_pos = environment.agent_pos

    curr_distance_from_prey = environment.distance[environment.agent_pos][prey_pos]
    curr_distance_from_predator = environment.distance[environment.agent_pos][predator_pos]
    options = [[] for _ in range(6)]

    for neighbour in environment.graph.get(environment.agent_pos):
        neighbour_distance_from_prey = environment.distance[neighbour][prey_pos]
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
    if node == environment.predator_pos:
        rand = random.randint(1, 100)
        if 1 <= rand <= 90:
            return True
    return False


def survey_prey(node, environment):
    if node == environment.prey_pos:
        rand = random.randint(1, 100)
        if 1 <= rand <= 90:
            return True
    return False


def agent_eight(environment):
    # Initialise belief vector
    belief_predator = [0.0] * (environment.num_nodes + 1)
    belief_prey = [1 / (environment.num_nodes - 1)] * (environment.num_nodes + 1)

    belief_predator[environment.predator_pos] = 1.0

    belief_prey[environment.agent_pos] = 0.0

    step, correct_prey_survey, correct_predator_survey = 1, 0, 0
    while step <= 5000:

        highest_belief_node_predator = pick_highest_probability_node(belief_predator)

        highest_belief_node_prey = pick_highest_probability_node(belief_prey)

        if max(belief_predator) != 1.0 and belief_predator[highest_belief_node_predator] > belief_prey[highest_belief_node_prey]:
            found_predator = survey(highest_belief_node_predator, environment)
            if found_predator:
                correct_predator_survey += 1
            update_belief_after_survey(belief_predator, highest_belief_node_predator, found_predator)
            found_prey = survey_prey(highest_belief_node_predator, environment)
            if belief_prey[highest_belief_node_predator] != 1.0:
                update_belief_after_survey(belief_prey, highest_belief_node_predator, found_prey)
            highest_belief_node_predator = pick_highest_probability_node(belief_predator)

        else:
            found_prey = survey_prey(highest_belief_node_prey, environment)
            if found_prey:
                correct_prey_survey += 1
            update_belief_after_survey(belief_prey, highest_belief_node_prey, found_prey)
            found_predator = survey(highest_belief_node_prey, environment)
            if belief_predator[highest_belief_node_prey] != 1.0:
                update_belief_after_survey(belief_predator, highest_belief_node_prey, found_predator)
            highest_belief_node_prey = pick_highest_probability_node(belief_prey)

        move_agent(environment, highest_belief_node_predator, highest_belief_node_prey)

        if environment.agent_pos == environment.prey_pos:
            return 1, correct_prey_survey, correct_predator_survey, step

        # Update Belief vector
        predator_found = False
        if environment.agent_pos == environment.predator_pos:
            predator_found = True

        update_belief(belief_predator, environment.agent_pos, predator_found)
        update_belief(belief_prey, environment.agent_pos, False)

        environment.move_prey()

        if environment.agent_pos == environment.prey_pos:
            return 1, correct_prey_survey, correct_predator_survey, step

        # Predator moves to its neighbours uniformly at random
        move_distracted_predator(environment)

        if not environment.check_agent_alive():
            return 0, correct_prey_survey, correct_predator_survey, step

        # update belief vector after prey's movement
        update_belief_predator(environment, belief_predator)
        update_belief_prey(environment, belief_prey)

        step += 1

    return -1, correct_prey_survey, correct_predator_survey, step


if __name__ == "__main__":

    # N - Number of Nodes, NG - Number of Graphs
    N, NG, runs = 50, 100, 30

    average_rate, metric = [0, 0, 0, 0, 0, 0], []
    for num in range(NG):

        # Creating Environment
        env = Environment(N)

        # Add Edges
        env.add_edges(N)

        # Compute Distance matrix using Floyd Warshall
        env.floyd_warshall()

        rate = [0] * 6
        for run in range(runs):

            result, survey_prey_counter, survey_predator_counter, total_steps = agent_eight(env)

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
            rate[3] += survey_prey_counter
            rate[4] += survey_predator_counter
            rate[5] += total_steps

        metric.append(rate)
    for i in range(len(metric)):
        average_rate[0] += metric[i][0]
        average_rate[1] += metric[i][1]
        average_rate[2] += metric[i][2]
        average_rate[3] += metric[i][3]
        average_rate[4] += metric[i][4]
        average_rate[5] += metric[i][5]
        print(metric[i][0], metric[i][1], metric[i][2])

    print('Avg(Agent Success Rate): ', average_rate[0] / runs, '%', '|', 'Avg(Agent Failure rate)',
          average_rate[1] / runs, '%' '|', 'Avg(Agent Timeout rate)', average_rate[2] / runs, '%' '|',
          'Avg(Agents Correct Prey Survey)', (average_rate[3] * 100) / average_rate[5], '%', '|',
          'Avg(Agents Correct Predator Survey)', (average_rate[4] * 100) / average_rate[5], '%')

import random


def pick_random(options):
    # choosing random neighbours from options
    if len(options) == 2:
        if options[0][1] == options[1][1] and options[0][2] == options[1][2]:
            return random.choice(options)

    elif len(options) == 3:
        if options[0][1] == options[2][1] and options[0][2] == options[2][2]:
            return random.choice(options)
        elif options[0][1] == options[1][1] and options[0][2] == options[1][2]:
            return random.choice(options[:1])
    return options[0]


def pick_highest_probability_node(belief):
    # choosing neighbours randomly from the highest belief list
    max_prob, prob = max(belief[1:]), []

    for i in range(1, len(belief)):
        if belief[i] == max_prob:
            prob.append(i)

    return random.choice(prob)


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
        next_pos = random.choice(options[3])[0]
    elif len(options[4]) != 0:
        options[4] = sorted(options[4], key=lambda x: (-x[2], x[1]))
        next_pos = pick_random(options[4])[0]
    elif len(options[5]) != 0:
        next_pos = pick_random(options[5])[0]
    return next_pos


def survey(node, environment):
    return node == environment.prey_pos


def update_belief(belief_predator, survey_node, found_predator):
    # belief update for survey and agent movement
    if found_predator:
        belief_predator[survey_node] = 1.0
        for node in range(1, len(belief_predator)):
            if node != survey_node:
                belief_predator[node] = 0.0
    else:
        prob_survey_node = belief_predator[survey_node]
        belief_predator[survey_node] = 0.0
        for node in range(1, len(belief_predator)):
            belief_predator[node] = belief_predator[node] * (1.0 / (1 - prob_survey_node))
    print("Sum of Belief: ", sum(belief_predator[1:]))







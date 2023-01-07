import random
from collections import deque
from sys import maxsize


class Environment:
    def __init__(self, num_nodes):
        self.num_nodes, self.graph, self.path = num_nodes, dict(), []
        self.prey_pos, self.predator_pos = random.randint(1, num_nodes), random.randint(1, num_nodes)
        self.agent_pos = self.spawn_agent()
        self.distance = self.initialize_distance()

    def initialize_distance(self):
        # Initializing distance matrix to compute distance between all nodes
        distance = [[1000 for _ in range(self.num_nodes + 1)] for _ in range(self.num_nodes + 1)]
        for i in range(self.num_nodes + 1):
            distance[i][i] = 0
        return distance

    def spawn_agent(self):
        # Spawining agent at locations other than prey and predator
        curr_pos = random.randint(1, self.num_nodes)
        while curr_pos == self.prey_pos or curr_pos == self.predator_pos:
            curr_pos = random.randint(1, self.num_nodes)
        return curr_pos

    def add_edges(self, num_nodes):
        # Adding circular edges
        self.graph[1], self.graph[num_nodes] = [num_nodes, 2], [1, num_nodes - 1]
        for i in range(2, num_nodes):
            self.graph[i] = [(i + 1), (i - 1)]

        # Adding Random edges
        step = 4
        for i in range(1, num_nodes + 1):
            possible_neighbours = []
            for j in range(i + 1, i + step + 1):
                if j > num_nodes:
                    possible_neighbours.append(j%num_nodes)
                else:
                    possible_neighbours.append(j)

            if i - step < 1:
                back_iter = num_nodes + (i - step)
            else:
                back_iter = i - step

            for j in range(back_iter, back_iter + step):
                if j > num_nodes:
                    possible_neighbours.append(j % num_nodes)
                else:
                    possible_neighbours.append(j)


            while(len(possible_neighbours) > 0):
                choice = random.choice(possible_neighbours)

                # check if there's already an edge
                neighbours = self.graph.get(i)
                if len(neighbours) < 3 and len(self.graph[choice]) < 3 and choice not in neighbours:
                    self.graph[i].append(choice)
                    self.graph[choice].append(i)
                    break
                else:
                    possible_neighbours.remove(choice)


    def move_prey(self):
        # randomly choosing among neighbours and current position
        neighbours = [self.prey_pos]
        for neighbour in self.graph[self.prey_pos]:
            neighbours.append(neighbour)
        self.prey_pos = random.choice(neighbours)

    def move_predator(self):
        # randomly choosing among the neighbours that are shortest distance from agent
        options = sorted([(self.distance[neighbour][self.agent_pos], neighbour) for neighbour in self.graph.get(self.predator_pos)])
        neighbours = [options[0][1]]
        for iteration in range(1, len(options)):
            if options[iteration][0] == options[0][0]:
                neighbours.append(options[iteration][1])
        self.predator_pos = random.choice(neighbours)

    def check_agent_alive(self):
        # check if agent is alive
        return self.agent_pos != self.predator_pos

    def reconstruct_path(self, parent):
        # building shortest path from parent and child reference
        path = list()
        curr_pos = self.agent_pos
        path.append(curr_pos)
        while parent.get(curr_pos) != -1:
            path.append(parent.get(curr_pos))
            curr_pos = parent.get(curr_pos)
        return path[-1:]

    def add_distances(self):
        for i, j in self.graph.items():
            for node in j:
                self.distance[i][node] = 1

    def floyd_warshall(self):
        # computing distance matrix
        self.add_distances()
        for k in range(self.num_nodes + 1):
            for i in range(self.num_nodes + 1):
                for j in range(self.num_nodes + 1):
                    self.distance[i][j] = min(self.distance[i][j], self.distance[i][k] + self.distance[k][j])

    def find_paths(self, paths, path, parent, n, u):

        if (u == -1):
            paths.append(path.copy())
            return

        for par in parent[u]:
            path.append(u)
            self.find_paths(paths, path, parent, n, par)
            path.pop()


    def bfs(self, parent, n, start):
        # BFS to compute parent child reference
        dist = [maxsize for _ in range(n)]
        q = deque()
        q.append(start)
        parent[start] = [-1]
        dist[start] = 0

        while q:
            u = q[0]
            q.popleft()
            for v in self.graph[u]:
                if (dist[v] > dist[u] + 1):
                    dist[v] = dist[u] + 1
                    q.append(v)
                    parent[v].clear()
                    parent[v].append(u)

                elif (dist[v] == dist[u] + 1):
                    parent[v].append(u)


    def all_paths(self, n, start, end):
        # function to compute all shortest path from start to end
        paths, path, shortest_path = [], [], []
        parent = [[] for _ in range(n)]
        self.bfs(parent, n, start)
        self.find_paths(paths, path, parent, n, end)
        for v in paths:
            v = list(reversed(v))
            shortest_path.append(v)
        return shortest_path

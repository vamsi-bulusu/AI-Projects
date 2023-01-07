package com.agent.classes;

import com.agent.interfaces.AgentType;
import com.environment.classes.Environment;
import com.environment.classes.Pair;
import com.environment.interfaces.EnvironmentOperations;
import java.util.*;

public class AgentFour implements AgentType, EnvironmentOperations {


    static class Node {
        Pair cell;
        int g, f;
        Node(Pair cell, int g, int f){
            this.cell = cell;
            this.g = g;
            this.f = f;
        }
    }

    class CustomComparator implements Comparator<Node> {

        @Override
        public int compare(Node a, Node b) {
            Pair goal = new Pair(50, 50);
            double difference = euclideanDistance(a.cell, goal) - euclideanDistance(b.cell, goal);
            if(a.f < b.f) return -1;
            else if(a.f > b.f) return 1;
            else {
                if(difference < 0) return -1;
                else if(difference > 0) return 1;
                return 0;
            }
        }
    }

    double computeHeuristic(Pair current, Pair goal, Environment environment){
        double euclideanDistance = euclideanDistance(current, goal);
        int ghostIndex = getNearestGhost(environment, current);
        int distanceFromGhost  = manhattanDistance(current, environment.ghosts.get(ghostIndex));
        int[] penalty = {0, 9, 7, 5};
        return euclideanDistance + distanceFromGhost > 3 ? 0 : penalty[distanceFromGhost];
    }

    boolean startAgentFour(Environment environment, Pair start, Pair goal){

        // Directional Arrays
        int[] X = {0, 0, 1, -1};
        int[] Y = {1, -1, 0, 0};

        Node node = new Node(start, 0, (int)computeHeuristic(start, goal, environment));

        // To keep track of unexplored nodes
        PriorityQueue<Node> priorityQueue = new PriorityQueue<>(new CustomComparator());

        priorityQueue.add(node);

        // To keep track of explored nodes
        Set<Pair> visited = new HashSet<>();

        // To keep track of Nodes
        Map<Pair, Node> map = new HashMap<>();


        // To keep track of Path
        environment.parent.put(start, null);

        // To store distances
        map.put(start, node);


        while (!priorityQueue.isEmpty()){

            Node top = priorityQueue.poll();

            moveGhosts(environment);

            if(environment.ghosts.contains(top.cell)) return false;

            if(top.cell == goal) {
                reconstructPath(environment);
                return true;
            }

            // If already visited
            if(visited.contains(top.cell)) continue;

            // add node to the explored node
            visited.add(top.cell);

            // Visit neighbours or children
            for(int i = 0; i < 4; i++){
                int newX = X[i] + top.cell.first, newY = Y[i] + top.cell.second;
                if(checkBounds(newX, newY, environment.grid.length)){
                    Pair child = new Pair(newX, newY);
                    if(environment.grid[newX][newY] == '*') {
                        // F(x) = G(x) + H(x) { G(x) -> Distance from current to child, H(X) -> Distance from child to goal + penalty
                        int cost = top.g + 1 + (int)computeHeuristic(child, goal, environment);
                        if(visited.contains(child)) {
                            Node childNode = map.get(child);
                            if(childNode.f > cost){
                                priorityQueue.remove(childNode);
                                childNode.f = cost;
                                map.put(child, childNode);
                                priorityQueue.add(childNode);
                                environment.parent.put(child, top.cell);
                            }
                        }
                        else {
                            Node childNode = new Node(child, top.g + 1, cost);
                            priorityQueue.add(childNode);
                            map.put(child, childNode);
                            environment.parent.put(child, top.cell);
                        }
                    }
                }
            }
        }
        return false;
    }

    @Override
    public int simulate(Environment environment, Pair start) {
        Pair goal = new Pair(environment.grid.length - 1, environment.grid.length - 1);
        boolean reachedGoal = startAgentFour(environment, start, goal);
        if(reachedGoal) return 1;
        System.out.println("Agent Died *_*");
        return 0;
    }
}

package com.environment.interfaces;

import com.environment.classes.Environment;
import com.environment.classes.Pair;
import java.util.*;


public interface EnvironmentOperations {

    Random random = new Random();

    default void reconstructPath(Environment environment){

        Pair goal = new Pair(environment.grid.length - 1, environment.grid.length - 1);
        while(environment.parent.containsKey(goal)){
            environment.path.add(goal);
            goal = environment.parent.get(goal);
        }
        Collections.reverse(environment.path);
    }


    default boolean checkBounds(int row, int col, int gridSize){
        return row >= 0 && row < gridSize && col >= 0 && col < gridSize;
    }

    default boolean isWalledOffCondition(Environment environment, int row, int col){
        int gridSize = environment.grid.length;
        if(checkBounds(row, col + 1, gridSize) && environment.grid[row][col + 1] == '*') return false;
        else if(checkBounds(row, col - 1, gridSize) && environment.grid[row][col - 1] == '*') return false;
        else if(checkBounds(row + 1, col, gridSize) && environment.grid[row + 1][col] == '*') return false;
        else return !checkBounds(row - 1, col, gridSize) || environment.grid[row - 1][col] != '*';
    }

     default void spawnGhosts(Environment environment, int numOfGhosts){
        int bound = environment.grid.length;
        while(numOfGhosts > 0){
            int row = random.nextInt(0, bound);
            int col = random.nextInt(0, bound);
            if(!isWalledOffCondition(environment, row, col)) {
                environment.ghosts.add(new Pair(row, col));
                numOfGhosts--;
            }
        }
    }
    default int manhattanDistance(Pair a, Pair b){
        return Math.abs(a.first - b.first) + Math.abs(a.second - b.second);
    }

    default double euclideanDistance(Pair a, Pair b){
        int distance = (int)(Math.pow(Math.abs(a.first - b.first), 2) + Math.pow(Math.abs(a.second - b.second), 2));
        return Math.sqrt(distance);
    }

    default Pair moveAway(Environment environment, Pair current, Pair ghost){
        int[] X = {0, 0, 1, -1};
        int[] Y = {1, -1, 0, 0};
        int distance = 0;
        for(int i = 0; i < 4; i++){
            int newX = X[i] + current.first, newY = Y[i] + current.second;
            if(checkBounds(newX, newY, environment.grid.length) && (environment.grid[newX][newY]) == '*'){
                Pair newCurr = new Pair(newX, newY);
                int manDist = manhattanDistance(ghost, newCurr);
                if(distance < manDist){
                    distance = manDist;
                    current = newCurr;
                }
            }
        }
        return current;
    }


    default int getNearestGhost(Environment environment, Pair current){
        List<Pair> ghosts = environment.ghosts;
        int nearest = Integer.MAX_VALUE, index = -1;
        for (int i = 0; i < ghosts.size(); i++) {
            int manDist = manhattanDistance(ghosts.get(i), current);
            if(nearest > manDist) {
                nearest = manDist;
                index = i;
            }
        }
        return index;
    }
    default Pair moveAwayFromNearestGhost(Environment environment, Pair current){
        List<Pair> ghosts = environment.ghosts;
        int index = getNearestGhost(environment, current);
        return moveAway(environment, current, ghosts.get(index));
    }

    default Environment fillMaze(int gridSize, int numOfGhosts){
        Environment environment = new Environment(gridSize);
        for(int i = 0; i < environment.grid.length; i++){
            for(int j = 0; j < environment.grid.length; j++){
                if(random.nextInt(1, 100) <= 28) {
                    environment.grid[i][j] = 'X';
                }
                else environment.grid[i][j] = '*';
            }
        }

        // Spawn Ghosts
        spawnGhosts(environment, numOfGhosts);
        return environment;
    }

    /**
     * Function to generate valid maze
     * @return Environment
     */
    default Environment generateMaze(int gridSize, int numOfGhosts){
        Environment environment;
        Set<Pair> visited;
        do {
            visited = new HashSet<>();
            environment = fillMaze(gridSize, numOfGhosts);
        } while (!validMaze(environment.grid, visited, new Pair(0, 0)));
        return environment;
    }



    default Boolean validMaze(char[][] grid, Set<Pair> visited, Pair pair){
        if(!checkBounds(pair.first, pair.second, grid.length) || grid[pair.first][pair.second] == 'X') return false;

        if(visited.contains(pair)) return false;

        // Keeping track of visited nodes
        visited.add(pair);

        if(pair.first == grid.length - 1 && pair.second == grid.length - 1 && grid[pair.first][pair.second] == '*') return true;
        else if(grid[pair.first][pair.second] == '*') {
            return (validMaze(grid, visited, new Pair(pair.first, pair.second + 1)) || validMaze(grid, visited, new Pair(pair.first, pair.second - 1))
                    || validMaze(grid, visited, new Pair(pair.first + 1, pair.second)) || validMaze(grid, visited, new Pair(pair.first - 1, pair.second)));
        }
        else return false;
    }

    /**
     * The ghosts move according to simple rules: at every time step,
     * a ghost picks one of its neighbors (up/down/left/right);
     * if the picked neighbor is unblocked, the ghost moves to that cell;
     * if the picked neighbor is blocked, the ghost either
     * stays in place with probability 0.5, or moves into the blocked cell with probability 0.5.
     * (These rules apply even if the ghost is currently within a blocked cell.)
     */
    default void moveGhosts(Environment environment) {
        List<Pair> ghosts = environment.ghosts;

        int[] X = {0, 0, 1, -1};
        int[] Y = {1, -1, 0, 0};
        for (int i = 0; i < ghosts.size(); i++) {
            int dir = random.nextInt(0, 4);
            Pair pair = ghosts.get(i);
            int newX = X[dir] +  pair.first, newY = Y[dir] + pair.second;
            if (checkBounds(newX,newY,environment.grid.length)){
                if(environment.grid[newX][newY] =='*'){
                    ghosts.remove(pair);
                    ghosts.add(new Pair(newX, newY));
                }
                else {
                    if (random.nextInt(1, 100) < 50) {
                        ghosts.remove(pair);
                        ghosts.add(new Pair(newX, newY));
                    }
                }
            }
        }
    }

    default Pair moveAhead(Environment environment, Pair current){
        if(environment.path.indexOf(current) + 1 < environment.path.size()) {
            current = environment.path.get(environment.path.indexOf(current) + 1);
        }
        return current;
    }
    default void visitNeighbours(Environment environment, Set<Pair> visited, Pair pair, Queue<Pair> queue){
        int[] x = {0, 0, 1, -1};
        int[] y = {1, -1, 0, 0};

        for(int j = 0; j < 4; j++){

            int newX = pair.first + x[j], newY = pair.second + y[j];

            Pair p = new Pair(newX, newY);

            if(checkBounds(newX, newY, environment.grid.length)){
                if((!environment.ghosts.contains(p)) && (environment.grid[newX][newY] == '*') && (!visited.contains(p))){
                    queue.add(p);
                    environment.parent.put(p, pair);
                    visited.add(p);
                }
            }
        }
    }
}

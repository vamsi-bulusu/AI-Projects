package com.environment.classes;


import java.util.*;

public class Environment {

    public char[][] grid;

    public List<Pair> ghosts;

    public Map<Pair, Pair> parent;

    public List<Pair> path;



    public Environment(int gridSize){
        this.grid = new char[gridSize][gridSize];
        this.ghosts = new LinkedList<>();
        this.path = new LinkedList<>();
        this.parent = new HashMap<>();
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (char[] chars : grid) {
            for (char aChar : chars) {
                sb.append(aChar).append(' ');
            }
            sb.append('\n');
        }
        sb.append(path);
        return sb.toString();
    }
}



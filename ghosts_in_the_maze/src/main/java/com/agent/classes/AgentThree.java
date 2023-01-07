package com.agent.classes;

import com.agent.interfaces.AgentType;
import com.environment.classes.Environment;
import com.environment.classes.Pair;
import com.environment.interfaces.EnvironmentOperations;

import java.util.*;

public class AgentThree implements AgentType, EnvironmentOperations {

    AgentTwo agentTwo;

    AgentThree(){
        agentTwo = new AgentTwo();
    }

    public boolean startAgentThree(Environment environment, Pair current, Pair goal, Map<Pair, Integer> visited){
        // Run Simulation on Agent Two for 10 Times

        int currSuccess = Integer.MIN_VALUE;

        Pair strongCell = current;

        moveGhosts(environment);

        if (environment.ghosts.contains(current)) return false;

        if(current.equals(goal)) return true;

        Map<Pair, Integer> map = agentTwo.simulation(environment, current, 5);


        if(map.size() > 0){
            for (Map.Entry<Pair, Integer> mapElement : map.entrySet()) {
                Pair cell = mapElement.getKey();
                int success = mapElement.getValue();

                if(visited.containsKey(cell)){
                    success -= visited.get(cell);
                }

                if(success > currSuccess){
                    currSuccess = success;
                    strongCell = cell;
                }
                else if(success == currSuccess){
                    // Compute EuclideanDistance for tie-breaker
                    if(euclideanDistance(strongCell, goal) > euclideanDistance(cell, goal)){
                        System.out.println(cell + "->" + euclideanDistance(cell, goal));
                        System.out.println(strongCell + "->" + euclideanDistance(strongCell, goal));
                        strongCell = cell;
                    }
                }
            }
        }
        else strongCell = moveAwayFromNearestGhost(environment, strongCell);

        current = strongCell;
        if(visited.containsKey(current))  {
            visited.put(current, visited.get(current) + 1);
        } else {
            visited.put(current, 1);
        }

        System.out.println("Map: " + map );
        System.out.println("Agent Moved to: " + current);
        return startAgentThree(environment, current, goal, visited);
    }


    @Override
    public int simulate(Environment environment, Pair start) {
        Pair goal = new Pair(environment.grid.length - 1, environment.grid.length - 1);
        Map<Pair, Integer> visited = new HashMap<>();
        boolean reachedGoal = startAgentThree(environment, start, goal, visited);
        if(reachedGoal) return 1;
        System.out.println("Agent Died");
        return 0;
    }
}

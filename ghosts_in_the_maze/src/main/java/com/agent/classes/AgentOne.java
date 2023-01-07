package com.agent.classes;

import com.agent.interfaces.AgentType;
import com.environment.classes.Environment;
import com.environment.interfaces.EnvironmentOperations;
import com.environment.classes.Pair;


import java.util.*;

public class AgentOne implements AgentType, EnvironmentOperations {
    public boolean startAgentOne(Environment environment, Pair start, boolean moveGhost){
        Set<Pair> visited = new HashSet<>();
        Queue<Pair> queue = new LinkedList<>();
        queue.add(start); visited.add(start);
        environment.parent.put(start, null);
        while(!queue.isEmpty()) {
            for (int i = 0; i < queue.size(); i++) {
                Pair pair = queue.poll();

                // Move Ghost
                if(moveGhost) moveGhosts(environment);

                // Check if agent is alive
                if (moveGhost && environment.ghosts.contains(pair)){
                    return false;
                }

                visitNeighbours(environment, visited, pair, queue);
            }
        }
        //recomputePath(environment, goal);
        reconstructPath(environment);
        return true;
    }


    @Override
    public int simulate(Environment environment, Pair start) {
        if(startAgentOne(environment, start, true)) return 1;
        else {
            System.out.println("Agent Died *_*");
            return 0;
        }
    }
}

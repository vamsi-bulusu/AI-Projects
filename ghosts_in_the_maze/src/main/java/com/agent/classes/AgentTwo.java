package com.agent.classes;

import com.agent.interfaces.AgentType;
import com.environment.classes.Environment;
import com.environment.classes.Pair;
import com.environment.interfaces.EnvironmentOperations;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


public class AgentTwo implements AgentType, EnvironmentOperations {


    AgentOne agentOne;

    AgentTwo(){
        agentOne = new AgentOne();
    }

    public boolean startAgentTwo(Environment environment, Pair current, boolean pathExists){

        // Move Ghosts
        moveGhosts(environment);

        // check if agent is alive
        if(environment.ghosts.contains(current)) return false;


        // check if agent reached goal
        if(current.first == environment.grid.length - 1 && current.second == environment.grid.length - 1) return true;

        // check if ghost is in path
        for(Pair p : environment.path){
            if (environment.ghosts.contains(p)) {
                pathExists = false;
                break;
            }
        }

        // Choose next available shortest route
        if(!pathExists) {
            pathExists = agentOne.startAgentOne(environment, current, false);
        }
        current = pathExists ? moveAhead(environment, current) : moveAwayFromNearestGhost(environment, current);
        return startAgentTwo(environment, current, pathExists);
    }


    public Map<Pair, Integer> simulation(Environment environment, Pair start, int numSimulations){
        int[] X = {0, 0, 1, -1};
        int[] Y = {1, -1, 0, 0};
        Map<Pair, Integer> hashMap = new HashMap<>();
        List<Pair> ghosts = environment.ghosts;
        for(int i = 0; i < 4; i++){
            Pair pair = new Pair(start.first + X[i], start.second + Y[i]);
            if(checkBounds(pair.first, pair.second, environment.grid.length) && environment.grid[pair.first][pair.second] == '*'){
                for(int j = 1; j <= numSimulations; j++){
                    boolean reachedGoal = startAgentTwo(environment, pair, false);
                    if(reachedGoal){
                        if(hashMap.containsKey(pair)) {
                            hashMap.put(pair, hashMap.get(pair) + 1);
                        }
                        else {
                            hashMap.put(pair, 1);
                        }
                    }
                }
                environment.ghosts = ghosts;
            }
        }
        return hashMap;
    }
    @Override
    public int simulate(Environment environment, Pair start) {
        boolean pathExists = agentOne.startAgentOne(environment, start, false);
        boolean reachedGoal = startAgentTwo(environment, start, pathExists);
        if(reachedGoal) return 1;
        System.out.println("Agent Died *_*");
        return 0;
    }
}

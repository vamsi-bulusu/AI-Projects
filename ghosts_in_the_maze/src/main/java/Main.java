
import com.agent.classes.AgentFactory;
import com.agent.interfaces.AgentType;
import com.environment.classes.Environment;
import com.environment.classes.Pair;
import com.simulation.Simulation;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;



public class Main extends Simulation {

    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));

        System.out.print("Size of the Grid: ");
        int gridSize = Integer.parseInt(bufferedReader.readLine());

        System.out.print("Enter the agent type (ex: AGENT-1): ");

        String type = bufferedReader.readLine();
        AgentType agentType = AgentFactory.getInstance(type);

        System.out.print("Enter number of Ghosts: ");
        int numGhosts = Integer.parseInt(bufferedReader.readLine());


        System.out.print("Enter number of Simulations per Ghost: ");
        int numSimulations = Integer.parseInt(bufferedReader.readLine());

        Environment environment = null;
        int success;
        for(int i = 1; i <= numGhosts; i++){
            success = 0;
            for(int j = 1; j <= numSimulations; j++){
                environment = agentType.generateMaze(gridSize, i);
                success += agentType.simulate(environment, new Pair(0, 0));
            }
            // Subroutine To Write data into the Excel file
            writeToExcel(environment, type + ".xlsx", success, numSimulations);
        }
    }
}

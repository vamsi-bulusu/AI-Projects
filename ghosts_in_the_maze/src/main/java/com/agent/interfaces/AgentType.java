package com.agent.interfaces;

import com.environment.classes.Environment;
import com.environment.interfaces.EnvironmentOperations;
import com.environment.classes.Pair;

import java.io.IOException;

public interface AgentType extends EnvironmentOperations {
    int simulate(Environment environment, Pair start) throws IOException;

}

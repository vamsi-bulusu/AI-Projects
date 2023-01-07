package com.agent.classes;

import com.agent.interfaces.AgentType;

/**
 * Factory class to instantiate different agents
 */

public class AgentFactory {
    public static AgentType getInstance(String agentName) {
        return switch (agentName) {
            case "AGENT-1" -> new AgentOne();
            case "AGENT-2" -> new AgentTwo();
            case "AGENT-3" -> new AgentThree();
            case "AGENT-4" -> new AgentFour();
            default -> null;
        };
    }
}

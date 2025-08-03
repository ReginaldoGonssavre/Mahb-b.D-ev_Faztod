import sys
import os

# Add the framework directory to the Python path
# This allows us to import the agent module directly
framework_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'mahbub_agent_framework'))
sys.path.insert(0, framework_path)

from agent.agent import Agent

def main():
    """
    Main function to run the agent demonstration.
    """
    print("--- Starting Maḥbūb Agent Framework Demonstration ---")
    
    # Initialize an agent
    my_agent = Agent(agent_id="agent_007")
    
    print("\n--- First Execution ---")
    # Execute a task
    result1 = my_agent.execute("What is the capital of France?")
    print(f"\n[DEMO] Agent Response: {result1}\n")
    
    print("\n--- Second Execution (with memory) ---")
    # Execute another task, the agent should remember the previous one
    result2 = my_agent.execute("And what is its population?")
    print(f"\n[DEMO] Agent Response: {result2}\n")
    
    print("--- Maḥbūb Agent Framework Demonstration Finished ---")

if __name__ == "__main__":
    main()
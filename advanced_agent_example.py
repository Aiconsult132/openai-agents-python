"""
Advanced Agent Example - Demonstrates tools, handoffs, and multi-agent workflows
"""
import asyncio
import os
from datetime import datetime
from agents import Agent, Runner, function_tool

# Set your OpenAI API key as an environment variable
# You can set this in your system environment variables or create a .env file
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Define some useful tools
@function_tool
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@function_tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression safely."""
    try:
        # Simple calculator - only allow basic operations for safety
        allowed_chars = set('0123456789+-*/.()')
        if not all(c in allowed_chars or c.isspace() for c in expression):
            return "Error: Only basic mathematical operations are allowed"
        
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"

@function_tool
def get_weather(city: str) -> str:
    """Get weather information for a city (mock implementation)."""
    # This is a mock implementation - in real use, you'd call a weather API
    mock_weather = {
        "new york": "Sunny, 22°C",
        "london": "Cloudy, 15°C", 
        "tokyo": "Rainy, 18°C",
        "paris": "Partly cloudy, 19°C",
        "sydney": "Sunny, 25°C"
    }
    
    city_lower = city.lower()
    if city_lower in mock_weather:
        return f"Weather in {city}: {mock_weather[city_lower]}"
    else:
        return f"Weather data not available for {city} (this is a mock implementation)"

async def main():
    """Main function demonstrating advanced agent features."""
    
    # Create specialized agents
    math_agent = Agent(
        name="Math Specialist",
        instructions="""You are a mathematics expert. You help with calculations, 
        mathematical concepts, and problem-solving. Always show your work and use 
        the calculator tool for computations.""",
        tools=[calculate],
        handoff_description="Expert in mathematics and calculations"
    )
    
    weather_agent = Agent(
        name="Weather Specialist", 
        instructions="""You are a weather information specialist. You provide 
        weather updates and forecasts for different cities. Always use the 
        weather tool to get current information.""",
        tools=[get_weather],
        handoff_description="Expert in weather information and forecasts"
    )
    
    time_agent = Agent(
        name="Time Keeper",
        instructions="""You are a time and scheduling specialist. You help with 
        time-related queries, scheduling, and date calculations. Always use the 
        time tool to get current information.""",
        tools=[get_current_time],
        handoff_description="Expert in time, dates, and scheduling"
    )
    
    # Create a triage agent that can hand off to specialists
    triage_agent = Agent(
        name="Assistant Coordinator",
        instructions="""You are a helpful coordinator that routes user requests 
        to the appropriate specialist agent. Analyze the user's request and 
        determine which specialist would be best suited to help:
        
        - For math problems, calculations, or mathematical concepts: use Math Specialist
        - For weather information or forecasts: use Weather Specialist  
        - For time, date, or scheduling questions: use Time Keeper
        
        If the request doesn't fit these categories, handle it yourself with 
        general assistance.""",
        handoffs=[math_agent, weather_agent, time_agent]
    )
    
    # Test cases for different scenarios
    test_cases = [
        "What's the weather like in Tokyo?",
        "Calculate 15 * 23 + 45",
        "What time is it right now?",
        "What's the weather in Paris and can you calculate 100 / 4?",
        "Tell me a joke about programming",
        "What's 2^10 and what time is it?"
    ]
    
    print("🚀 Advanced Agent System Demo")
    print("=" * 60)
    print("This demo shows:")
    print("✅ Multiple specialized agents")
    print("✅ Function tools") 
    print("✅ Agent handoffs")
    print("✅ Intelligent routing")
    print("=" * 60)
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n🔍 Test Case {i}: {query}")
        print("-" * 40)
        
        try:
            result = await Runner.run(triage_agent, query)
            print(f"🤖 Response: {result.final_output}")
            
            # Show which agents were involved
            if hasattr(result, 'run_steps'):
                agents_used = set()
                for step in result.run_steps:
                    if hasattr(step, 'agent_name'):
                        agents_used.add(step.agent_name)
                if len(agents_used) > 1:
                    print(f"🔄 Agents involved: {', '.join(agents_used)}")
                    
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print()

if __name__ == "__main__":
    asyncio.run(main())

"""
My First Agent - A simple example to get started with OpenAI Agents SDK
"""
import asyncio
import os
from agents import Agent, Runner

# Set your OpenAI API key as an environment variable
# You can set this in your system environment variables or create a .env file
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

async def main():
    """Main function to run the agent."""
    
    # Create a simple agent
    agent = Agent(
        name="Personal Assistant",
        instructions="""You are a helpful personal assistant. 
        You provide clear, concise, and friendly responses to user questions.
        Always be polite and helpful."""
    )
    
    # Example questions to test
    questions = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms",
        "Write a short poem about coding",
        "What are some good programming practices?"
    ]
    
    print("🤖 Testing My First Agent!")
    print("=" * 50)
    
    for i, question in enumerate(questions, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 30)
        
        # Run the agent with the question
        result = await Runner.run(agent, question)
        print(f"🤖 Response: {result.final_output}")
        print()

if __name__ == "__main__":
    asyncio.run(main())

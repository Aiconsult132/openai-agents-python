"""
Streamlit UI for OpenAI Agents SDK
A simple and elegant web interface using Streamlit
"""
import asyncio
import os
from datetime import datetime
import streamlit as st

from agents import Agent, Runner, function_tool

# Set your OpenAI API key as an environment variable
# You can set this in your system environment variables or create a .env file
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Configure Streamlit page
st.set_page_config(
    page_title="OpenAI Agents UI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define tools
@function_tool
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# LinkedIn tools
@function_tool
def analyze_post_length(content: str) -> str:
    """Analyze the length of a LinkedIn post and provide recommendations."""
    length = len(content)
    
    if length < 300:
        return f"Post is {length} characters - TOO SHORT. LinkedIn posts should be 1300-3000 characters for optimal reach."
    elif length < 1300:
        return f"Post is {length} characters - SHORT. Consider expanding with more details, examples, or insights."
    elif length <= 3000:
        return f"Post is {length} characters - OPTIMAL LENGTH. Perfect for LinkedIn engagement!"
    else:
        return f"Post is {length} characters - TOO LONG. Consider breaking into multiple posts or cutting unnecessary content."

@function_tool
def suggest_hashtags(topic: str, industry: str = "general") -> str:
    """Suggest relevant hashtags based on topic and industry."""
    
    # General hashtags that work well
    general_hashtags = ["#LinkedIn", "#Professional", "#Career", "#Business", "#Growth"]
    
    # Industry-specific hashtags
    industry_hashtags = {
        "tech": ["#Technology", "#Innovation", "#AI", "#Software", "#TechTrends"],
        "marketing": ["#Marketing", "#DigitalMarketing", "#ContentMarketing", "#Branding", "#SocialMedia"],
        "leadership": ["#Leadership", "#Management", "#TeamBuilding", "#ExecutiveCoaching", "#WorkplaceCulture"],
        "entrepreneurship": ["#Entrepreneur", "#Startup", "#SmallBusiness", "#Innovation", "#BusinessGrowth"],
        "finance": ["#Finance", "#Investing", "#FinTech", "#Banking", "#Economics"],
        "sales": ["#Sales", "#B2B", "#CustomerSuccess", "#SalesStrategy", "#Networking"],
    }
    
    # Topic-based hashtags
    topic_lower = topic.lower()
    suggested = []
    
    if "learn" in topic_lower or "education" in topic_lower:
        suggested.extend(["#Learning", "#ProfessionalDevelopment", "#SkillBuilding"])
    if "success" in topic_lower or "achievement" in topic_lower:
        suggested.extend(["#Success", "#Achievement", "#Goals"])
    if "team" in topic_lower or "collaboration" in topic_lower:
        suggested.extend(["#Teamwork", "#Collaboration", "#TeamSuccess"])
    if "tip" in topic_lower or "advice" in topic_lower:
        suggested.extend(["#Tips", "#Advice", "#BestPractices"])
    
    # Combine hashtags
    final_hashtags = []
    final_hashtags.extend(industry_hashtags.get(industry.lower(), [])[:2])
    final_hashtags.extend(suggested[:2])
    final_hashtags.extend(general_hashtags[:1])
    
    # Remove duplicates and limit to 5
    final_hashtags = list(dict.fromkeys(final_hashtags))[:5]
    
    return f"Recommended hashtags: {' '.join(final_hashtags)}"

@function_tool
def check_engagement_potential(content: str) -> str:
    """Analyze content for engagement potential and provide a score."""
    score = 0
    feedback = []
    
    # Check for questions
    if "?" in content:
        score += 20
        feedback.append("✅ Contains questions (encourages comments)")
    else:
        feedback.append("❌ No questions found - add questions to encourage engagement")
    
    # Check for personal stories/experiences
    personal_indicators = ["I learned", "My experience", "When I", "I discovered", "I realized"]
    if any(indicator.lower() in content.lower() for indicator in personal_indicators):
        score += 25
        feedback.append("✅ Includes personal experience (builds connection)")
    else:
        feedback.append("⚠️ Consider adding personal experience or story")
    
    # Check for actionable content
    action_words = ["tip", "strategy", "how to", "step", "method", "technique"]
    if any(word in content.lower() for word in action_words):
        score += 20
        feedback.append("✅ Contains actionable content")
    else:
        feedback.append("⚠️ Consider adding actionable tips or insights")
    
    # Check for formatting
    if "\n\n" in content:
        score += 15
        feedback.append("✅ Good paragraph breaks")
    else:
        feedback.append("❌ Needs better paragraph formatting")
    
    # Check length
    length = len(content)
    if 1300 <= length <= 3000:
        score += 20
        feedback.append("✅ Optimal length")
    else:
        feedback.append("❌ Length needs adjustment")
    
    # Determine engagement level
    if score >= 80:
        level = "HIGH"
    elif score >= 60:
        level = "MEDIUM-HIGH" 
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"
    
    return f"Engagement Score: {score}/100 ({level})\n\nFeedback:\n" + "\n".join(feedback)

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

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agents" not in st.session_state:
    # Create agents
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

    linkedin_agent = Agent(
        name="LinkedIn Reformatter",
        instructions="""Role: You are a seasoned social media strategist with expertise in optimizing LinkedIn posts for maximum engagement, incorporating a touch of storytelling.

Objective: Reformat LinkedIn posts using a structured and engaging format that includes a hook, clear content, visuals, a call to action (CTA), and a postscript (PS). Keep posts below 2,500 characters!

WRITING STYLES TO CHOOSE FROM:

Marketing & Persuasion:
- AIDA (Attention, Interest, Desire, Action)
- PAS (Problem, Agitate, Solve) 
- BAB (Before, After, Bridge)
- PASTOR (Problem, Amplify, Solution, Testimonials, Offer, Response)
- FAB (Features, Advantages, Benefits)

Information & Analysis:
- 5W1H (Who, What, When, Where, Why, How)
- SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)
- Pyramid Principle
- KISS (Keep It Simple, Stupid)
- PEEL (Point, Explanation, Evidence, Link)

Storytelling & Professional:
- STAR (Situation, Task, Action, Result)
- SOAR (Situation, Obstacles, Actions, Results)
- Toulmin Model
- SCIPAB (Situation, Complication, Implication, Position, Action, Benefit)
- PREP (Point, Reason, Example, Point)

FORMATTING REQUIREMENTS:

Hook: Start with 1-2 lines that grab attention using a surprising fact, question, or short story.

Body - Core Principles:
- Single idea per line
- Break each complete thought into its own line
- Create visual breathing room between ideas
- Maximum one sentence per line

Line Break Strategies:
Opening Lines: Every single line gets its own space
- Break after questions
- Break after attention hooks
- Break after each part of a setup

Middle Content:
- Break after each key point
- Break before and after important revelations
- Break between items in a sequence

Closing Lines:
- Break before the call to action
- Break after emotional appeals
- Break final thoughts into digestible pieces

Emphasis Techniques:
- Use standalone "Why?" or "Picture this:" lines
- Create single-word lines for impact
- Place key phrases on their own lines
- Use ellipsis... on separate line for suspense

Visual Elements:
- Use bullet points (👉 or ✓) for lists
- Space out enumerated items
- Create white space between sections
- Break paragraphs into multiple lines

DO NOT use emojis in the main content! DO NOT add hashtags at the end!

Call to Action (CTA): End with a clear CTA encouraging readers to engage, such as asking them to comment, share, or posing a question to invite responses.

Postscript (PS): Add a PS section for extra prompts or insights, such as asking about the reader's biggest challenge on LinkedIn.

ALWAYS use the available tools to analyze and optimize the content. Choose the most appropriate writing style based on the content type and objective.""",
        
        tools=[analyze_post_length, suggest_hashtags, check_engagement_potential]
    )

    triage_agent = Agent(
        name="Assistant Coordinator",
        instructions="""You are a helpful coordinator that routes user requests 
        to the appropriate specialist agent. Analyze the user's request and 
        determine which specialist would be best suited to help:
        
        - For math problems, calculations, or mathematical concepts: use Math Specialist
        - For weather information or forecasts: use Weather Specialist  
        - For time, date, or scheduling questions: use Time Keeper
        - For LinkedIn content optimization or social media posts: use LinkedIn Reformatter
        
        If the request doesn't fit these categories, handle it yourself with 
        general assistance.""",
        handoffs=[math_agent, weather_agent, time_agent, linkedin_agent]
    )

    simple_agent = Agent(
        name="Personal Assistant",
        instructions="""You are a helpful personal assistant. 
        You provide clear, concise, and friendly responses to user questions.
        Always be polite and helpful."""
    )

    st.session_state.agents = {
        "Simple Assistant": simple_agent,
        "Multi-Agent System": triage_agent,
        "Math Specialist": math_agent,
        "Weather Specialist": weather_agent,
        "Time Keeper": time_agent,
        "LinkedIn Reformatter": linkedin_agent
    }

# Sidebar
with st.sidebar:
    st.title("🤖 Agent Settings")
    
    selected_agent_name = st.selectbox(
        "Choose an Agent:",
        options=list(st.session_state.agents.keys()),
        index=1  # Default to Multi-Agent System
    )
    
    selected_agent = st.session_state.agents[selected_agent_name]
    
    st.markdown("---")
    
    # Agent info
    st.subheader("📋 Agent Info")
    st.write(f"**Name:** {selected_agent.name}")
    
    with st.expander("View Instructions"):
        st.write(selected_agent.instructions)
    
    if hasattr(selected_agent, 'tools') and selected_agent.tools:
        with st.expander("Available Tools"):
            for tool in selected_agent.tools:
                st.write(f"• {tool.name}")
    
    if hasattr(selected_agent, 'handoffs') and selected_agent.handoffs:
        with st.expander("Can Hand Off To"):
            for agent in selected_agent.handoffs:
                st.write(f"• {agent.name}")
    
    st.markdown("---")
    
    # Clear conversation button
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()
    
    # Example prompts
    st.subheader("💡 Try These Examples")
    example_prompts = [
        "What's the weather in Tokyo?",
        "Calculate 15 * 23 + 45",
        "What time is it?",
        "Explain quantum computing",
        "Reformat for LinkedIn: I just finished a big project at work. It was challenging but we got it done.",
        "Optimize this LinkedIn post: Just read about AI. It's going to change everything.",
    ]
    
    for prompt in example_prompts:
        if st.button(prompt, key=f"example_{prompt}"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

# Main chat interface
st.title("💬 Chat with Your AI Agents")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "agent_name" in message:
                st.caption(f"🤖 {message['agent_name']}")
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner(f"🤔 {selected_agent.name} is thinking..."):
            try:
                # Run the selected agent
                result = asyncio.run(Runner.run(selected_agent, prompt))
                response = result.final_output
                
                # Display response
                st.caption(f"🤖 {selected_agent.name}")
                st.markdown(response)
                
                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "agent_name": selected_agent.name
                })
                
            except Exception as e:
                error_message = f"❌ Error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_message,
                    "agent_name": "System"
                })

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Built with ❤️ using OpenAI Agents SDK and Streamlit
    </div>
    """, 
    unsafe_allow_html=True
)

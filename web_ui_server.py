"""
Simple Web UI for OpenAI Agents SDK
A FastAPI-based web interface to interact with your agents
"""
import asyncio
import json
import os
from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from agents import Agent, Runner, function_tool

# Set your OpenAI API key as an environment variable
# You can set this in your system environment variables or create a .env file
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Define tools (same as in your advanced example)
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
        return f"Post is {length} characters - TOO SHORT. LinkedIn posts should be under 2,500 characters but with substantial content."
    elif length <= 2500:
        return f"Post is {length} characters - PERFECT LENGTH. Under the 2,500 character limit!"
    else:
        return f"Post is {length} characters - TOO LONG. Must be under 2,500 characters. Please shorten the content."

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
def format_linkedin_post_correctly(original_content: str) -> str:
    """Take any content and format it correctly with single ideas per line."""
    # This tool shows the agent exactly how to format
    lines = []
    sentences = original_content.replace('.', '.\n').replace('!', '!\n').replace('?', '?\n').split('\n')
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and len(sentence) > 15:
            # Break long sentences into shorter chunks
            words = sentence.split()
            current_line = []
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > 15:
                    if len(current_line) > 1:
                        lines.append(' '.join(current_line[:-1]))
                        current_line = [word]
                    else:
                        lines.append(word)
                        current_line = []
            if current_line:
                lines.append(' '.join(current_line))
        elif sentence:
            lines.append(sentence)
    
    # Add spacing every 2-3 lines
    formatted_lines = []
    for i, line in enumerate(lines):
        formatted_lines.append(line)
        if (i + 1) % 2 == 0 and i < len(lines) - 1:
            formatted_lines.append("")  # Empty line
    
    return f"CORRECTLY FORMATTED VERSION:\n\n" + "\n".join(formatted_lines)

@function_tool
def validate_linkedin_formatting(content: str) -> str:
    """Validate that the LinkedIn post follows the required formatting structure."""
    lines = content.split('\n')
    feedback = []
    score = 0
    
    # Check for proper line breaks (single ideas per line)
    long_lines = [line for line in lines if len(line) > 80 and line.strip()]
    if len(long_lines) > 2:  # Allow some flexibility
        feedback.append("❌ Too many long lines. Break thoughts into shorter lines (max 80 chars)")
    else:
        score += 20
        feedback.append("✅ Good line length - thoughts broken into digestible pieces")
    
    # Check for hook structure (first few lines should be short and impactful)
    if lines and len(lines[0]) < 60:
        score += 20
        feedback.append("✅ Strong hook - first line is concise and impactful")
    else:
        feedback.append("❌ Hook too long - first line should be under 60 characters")
    
    # Check for proper spacing (empty lines between sections)
    empty_lines = [i for i, line in enumerate(lines) if not line.strip()]
    if len(empty_lines) >= 2:
        score += 15
        feedback.append("✅ Good use of white space between sections")
    else:
        feedback.append("❌ Need more white space - add empty lines between sections")
    
    # Check for CTA structure (should have clear call to action)
    cta_indicators = ["?", "comment", "share", "thoughts", "experience", "story"]
    has_cta = any(indicator in content.lower() for indicator in cta_indicators)
    if has_cta:
        score += 20
        feedback.append("✅ Clear call-to-action present")
    else:
        feedback.append("❌ Missing call-to-action - add questions or engagement prompts")
    
    # Check for PS section
    if "PS:" in content or "P.S." in content:
        score += 15
        feedback.append("✅ PS section included")
    else:
        feedback.append("❌ Missing PS section - add postscript for extra engagement")
    
    # Check character limit
    if len(content) <= 2500:
        score += 10
        feedback.append("✅ Under 2,500 character limit")
    else:
        feedback.append("❌ Over 2,500 character limit - needs to be shortened")
    
    return f"Formatting Score: {score}/100\n\nFormatting Analysis:\n" + "\n".join(feedback)

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

# Create agents (same as in your advanced example)
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

# Create LinkedIn agent
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

CRITICAL FORMATTING EXAMPLE:
Original: "Success isn't about working harder every day and pushing yourself to exhaustion. It's about making smart choices and knowing when to take breaks."

MUST format as:
Success isn't about working harder every day.

It's not about pushing yourself to exhaustion.

It's about making smart choices.

And knowing when to take breaks.

ALWAYS use the available tools to analyze and optimize the content. Choose the most appropriate writing style based on the content type and objective.

MANDATORY FORMATTING RULES - FOLLOW EXACTLY:

1. NEVER write long sentences or paragraphs
2. MAXIMUM 15 words per line
3. Put each complete thought on its own line
4. Add empty line after every 2-3 lines
5. ALWAYS start with a short hook (under 10 words)
6. ALWAYS end with "What's your experience?" or similar question
7. ALWAYS include "PS:" section at the end

EXAMPLE OUTPUT FORMAT:
Ever felt overwhelmed by daily noise?

I walked into the forest yesterday.

Everything changed.

Before: rushing, thinking, worrying.

After: peace, clarity, presence.

The forest taught me something profound.

Slowing down isn't luxury.

It's necessity.

What's your favorite place to recharge?

PS: Share your peaceful spots below!

CRITICAL: Use this EXACT formatting style - short lines, empty spaces, no long paragraphs!

STEP-BY-STEP PROCESS:
1. First, use format_linkedin_post_correctly tool to see proper formatting
2. Then create your response using that exact format
3. Use validate_linkedin_formatting to check your work
4. NEVER output long paragraphs or sentences over 15 words""",
    
    tools=[format_linkedin_post_correctly, analyze_post_length, suggest_hashtags, check_engagement_potential, validate_linkedin_formatting],
    handoff_description="Expert in LinkedIn content optimization and social media best practices"
)

# Create a triage agent
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

# Simple agent for basic conversations
simple_agent = Agent(
    name="Personal Assistant",
    instructions="""You are a helpful personal assistant. 
    You provide clear, concise, and friendly responses to user questions.
    Always be polite and helpful."""
)

# Available agents
AGENTS = {
    "simple": simple_agent,
    "advanced": triage_agent,
    "math": math_agent,
    "weather": weather_agent,
    "time": time_agent,
    "linkedin": linkedin_agent
}

app = FastAPI(title="OpenAI Agents Web UI")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.conversation_history: Dict[str, List[Dict[str, Any]]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_message(self, websocket: WebSocket, message: dict):
        await websocket.send_text(json.dumps(message))

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def get_home():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenAI Agents Web UI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 1rem 2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            color: #333;
            font-size: 1.5rem;
            font-weight: 600;
        }
        
        .agent-selector {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .agent-selector label {
            color: #333;
            font-weight: 500;
        }
        
        .agent-selector select {
            padding: 0.5rem 1rem;
            border: 1px solid #ddd;
            border-radius: 6px;
            background: white;
            cursor: pointer;
        }
        
        .main {
            flex: 1;
            display: flex;
            flex-direction: column;
            padding: 2rem;
            max-width: 1000px;
            margin: 0 auto;
            width: 100%;
        }
        
        .chat-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 600px;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .message {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
        }
        
        .message.user {
            flex-direction: row-reverse;
        }
        
        .message-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            font-weight: bold;
            flex-shrink: 0;
        }
        
        .message.user .message-avatar {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .message.assistant .message-avatar {
            background: linear-gradient(135deg, #f093fb, #f5576c);
            color: white;
        }
        
        .message-content {
            background: white;
            padding: 1rem 1.25rem;
            border-radius: 18px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            max-width: 70%;
            word-wrap: break-word;
            line-height: 1.5;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .message-info {
            font-size: 0.8rem;
            color: #666;
            margin-top: 0.5rem;
            opacity: 0.7;
        }
        
        .chat-input {
            padding: 1.5rem;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.8);
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        
        .chat-input input {
            flex: 1;
            padding: 0.75rem 1rem;
            border: 1px solid #ddd;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.2s;
        }
        
        .chat-input input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .chat-input button {
            padding: 0.75rem 1.5rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 500;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .chat-input button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .chat-input button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }
        
        .status {
            text-align: center;
            padding: 1rem;
            color: #666;
            font-style: italic;
        }
        
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #666;
            font-style: italic;
        }
        
        .typing-dots {
            display: flex;
            gap: 3px;
        }
        
        .typing-dots span {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #667eea;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dots span:nth-child(2) { animation-delay: 0.2s; }
        .typing-dots span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }
        
        .connection-status {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .connection-status.connected {
            background: #d4edda;
            color: #155724;
        }
        
        .connection-status.disconnected {
            background: #f8d7da;
            color: #721c24;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 OpenAI Agents Web UI</h1>
        <div class="agent-selector">
            <label for="agentSelect">Agent:</label>
            <select id="agentSelect">
                <option value="simple">Simple Assistant</option>
                <option value="advanced" selected>Multi-Agent System</option>
                <option value="math">Math Specialist</option>
                <option value="weather">Weather Specialist</option>
                <option value="time">Time Keeper</option>
                <option value="linkedin">LinkedIn Reformatter</option>
            </select>
            <div id="connectionStatus" class="connection-status disconnected">Disconnected</div>
        </div>
    </div>
    
    <div class="main">
        <div class="chat-container">
            <div id="chatMessages" class="chat-messages">
                <div class="status">
                    Welcome! Connect to start chatting with your AI agents.
                </div>
            </div>
            <div class="chat-input">
                <input id="messageInput" type="text" placeholder="Type your message..." disabled>
                <button id="sendButton" disabled>Send</button>
            </div>
        </div>
    </div>

    <script>
        let ws = null;
        let isConnected = false;
        let sessionId = Math.random().toString(36).substring(7);
        
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const agentSelect = document.getElementById('agentSelect');
        const connectionStatus = document.getElementById('connectionStatus');
        
        function connect() {
            ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);
            
            ws.onopen = function() {
                isConnected = true;
                connectionStatus.textContent = 'Connected';
                connectionStatus.className = 'connection-status connected';
                messageInput.disabled = false;
                sendButton.disabled = false;
                
                // Clear welcome message
                chatMessages.innerHTML = '';
                addMessage('assistant', 'Hello! I\\'m ready to help you. What would you like to know?', 'System');
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                handleMessage(data);
            };
            
            ws.onclose = function() {
                isConnected = false;
                connectionStatus.textContent = 'Disconnected';
                connectionStatus.className = 'connection-status disconnected';
                messageInput.disabled = true;
                sendButton.disabled = true;
            };
            
            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
                addMessage('assistant', 'Connection error occurred. Please refresh the page.', 'System');
            };
        }
        
        function handleMessage(data) {
            if (data.type === 'response') {
                removeTypingIndicator();
                addMessage('assistant', data.message, data.agent_name || 'Assistant');
            } else if (data.type === 'error') {
                removeTypingIndicator();
                addMessage('assistant', `Error: ${data.message}`, 'System');
            } else if (data.type === 'thinking') {
                // Show typing indicator
                showTypingIndicator();
            }
        }
        
        function addMessage(sender, content, agentName = null) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.textContent = sender === 'user' ? 'U' : '🤖';
            
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.textContent = content;
            
            if (agentName && sender === 'assistant') {
                const messageInfo = document.createElement('div');
                messageInfo.className = 'message-info';
                messageInfo.textContent = `Agent: ${agentName}`;
                messageContent.appendChild(messageInfo);
            }
            
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(messageContent);
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function showTypingIndicator() {
            removeTypingIndicator(); // Remove any existing indicator
            
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message assistant';
            typingDiv.id = 'typingIndicator';
            
            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.textContent = '🤖';
            
            const typingContent = document.createElement('div');
            typingContent.className = 'message-content';
            
            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'typing-indicator';
            typingIndicator.innerHTML = `
                <span>Agent is thinking</span>
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            `;
            
            typingContent.appendChild(typingIndicator);
            typingDiv.appendChild(avatar);
            typingDiv.appendChild(typingContent);
            
            chatMessages.appendChild(typingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function removeTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            if (indicator) {
                indicator.remove();
            }
        }
        
        function sendMessage() {
            const message = messageInput.value.trim();
            if (!message || !isConnected) return;
            
            addMessage('user', message);
            showTypingIndicator();
            
            ws.send(JSON.stringify({
                type: 'message',
                content: message,
                agent: agentSelect.value
            }));
            
            messageInput.value = '';
        }
        
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        sendButton.addEventListener('click', sendMessage);
        
        // Connect automatically when page loads
        connect();
        
        // Handle agent selection change
        agentSelect.addEventListener('change', function() {
            if (isConnected) {
                addMessage('assistant', `Switched to ${this.options[this.selectedIndex].text}`, 'System');
            }
        });
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "message":
                content = message_data["content"]
                agent_type = message_data.get("agent", "simple")
                
                # Add user message to history
                manager.conversation_history[session_id].append({
                    "role": "user",
                    "content": content
                })
                
                # Send thinking indicator
                await manager.send_message(websocket, {
                    "type": "thinking"
                })
                
                try:
                    # Get the selected agent
                    agent = AGENTS.get(agent_type, simple_agent)
                    
                    # Run the agent
                    result = await Runner.run(agent, content)
                    response = result.final_output
                    
                    # Add assistant response to history
                    manager.conversation_history[session_id].append({
                        "role": "assistant", 
                        "content": response
                    })
                    
                    # Send response
                    await manager.send_message(websocket, {
                        "type": "response",
                        "message": response,
                        "agent_name": agent.name
                    })
                    
                except Exception as e:
                    await manager.send_message(websocket, {
                        "type": "error",
                        "message": str(e)
                    })
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting OpenAI Agents Web UI...")
    print("📱 Open your browser to: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

"""
Vercel-compatible OpenAI Agents API
Simplified version without WebSockets for serverless deployment
"""
import os
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from agents import Agent, Runner, function_tool

# Set your OpenAI API key as an environment variable
# You can set this in your system environment variables or create a .env file
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Define tools
@function_tool
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

# Create LinkedIn agent
linkedin_agent = Agent(
    name="LinkedIn Reformatter",
    instructions="""Role: You are a seasoned social media strategist with expertise in optimizing LinkedIn posts for maximum engagement, incorporating a touch of storytelling.

Objective: Reformat LinkedIn posts using a structured and engaging format that includes a hook, clear content, visuals, a call to action (CTA), and a postscript (PS). Keep posts below 2,500 characters!

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

CRITICAL: Use this EXACT formatting style - short lines, empty spaces, no long paragraphs!""",
    
    tools=[analyze_post_length, suggest_hashtags]
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
    "linkedin": linkedin_agent
}

app = FastAPI(title="OpenAI Agents API")

class ChatRequest(BaseModel):
    message: str
    agent: str = "simple"

class ChatResponse(BaseModel):
    response: str
    agent_name: str

@app.get("/", response_class=HTMLResponse)
async def get_home():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenAI Agents API</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 2rem;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            max-width: 800px;
            width: 100%;
        }
        
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .chat-form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        label {
            font-weight: 500;
            color: #333;
        }
        
        select, textarea, button {
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
        }
        
        textarea {
            min-height: 100px;
            resize: vertical;
        }
        
        button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            cursor: pointer;
            font-weight: 500;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        .response {
            margin-top: 2rem;
            padding: 1.5rem;
            background: #f8f9fa;
            border-radius: 8px;
            white-space: pre-wrap;
            display: none;
        }
        
        .loading {
            text-align: center;
            color: #666;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 OpenAI Agents API</h1>
        
        <form class="chat-form" onsubmit="sendMessage(event)">
            <div class="form-group">
                <label for="agent">Choose Agent:</label>
                <select id="agent" name="agent">
                    <option value="simple">Simple Assistant</option>
                    <option value="linkedin">LinkedIn Reformatter</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="message">Your Message:</label>
                <textarea id="message" name="message" placeholder="Type your message here..." required></textarea>
            </div>
            
            <button type="submit">Send Message</button>
        </form>
        
        <div id="response" class="response"></div>
    </div>

    <script>
        async function sendMessage(event) {
            event.preventDefault();
            
            const message = document.getElementById('message').value;
            const agent = document.getElementById('agent').value;
            const responseDiv = document.getElementById('response');
            
            responseDiv.style.display = 'block';
            responseDiv.innerHTML = '<div class="loading">🤔 Agent is thinking...</div>';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        agent: agent
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    responseDiv.innerHTML = `<strong>🤖 ${data.agent_name}:</strong>\\n\\n${data.response}`;
                } else {
                    responseDiv.innerHTML = `<strong>❌ Error:</strong>\\n${data.detail}`;
                }
            } catch (error) {
                responseDiv.innerHTML = `<strong>❌ Error:</strong>\\n${error.message}`;
            }
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """Chat with the selected agent."""
    try:
        # Get the selected agent
        agent = AGENTS.get(request.agent, simple_agent)
        
        # Run the agent
        result = await Runner.run(agent, request.message)
        response = result.final_output
        
        return ChatResponse(
            response=response,
            agent_name=agent.name
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "OpenAI Agents API is running"}

# For Vercel deployment
app_handler = app

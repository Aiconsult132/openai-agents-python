"""
LinkedIn Reformatter Agent - Specialized agent for optimizing LinkedIn posts
"""
import asyncio
import os
from typing import List
from pydantic import BaseModel

from agents import Agent, Runner, function_tool

# Set your OpenAI API key as an environment variable
# You can set this in your system environment variables or create a .env file
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# LinkedIn best practices data
LINKEDIN_BEST_PRACTICES = {
    "optimal_length": "1300-3000 characters",
    "hook_techniques": [
        "Start with a question",
        "Share a surprising statistic", 
        "Begin with a controversial statement",
        "Tell a personal story",
        "Use 'Here's what I learned...'"
    ],
    "engagement_tactics": [
        "Ask questions to encourage comments",
        "Use line breaks for readability",
        "Include relevant hashtags (3-5)",
        "Tag relevant people or companies",
        "Add a call-to-action"
    ],
    "formatting_tips": [
        "Use emojis strategically (not too many)",
        "Break text into short paragraphs",
        "Use bullet points or numbered lists",
        "Bold key phrases with **text**",
        "Include white space for readability"
    ]
}

class LinkedInPost(BaseModel):
    """Structure for a LinkedIn post"""
    hook: str
    main_content: str
    call_to_action: str
    hashtags: List[str]
    estimated_length: int
    engagement_score: str

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
        "hr": ["#HumanResources", "#Recruiting", "#TalentAcquisition", "#WorkplaceCulture", "#EmployeeEngagement"],
        "consulting": ["#Consulting", "#Strategy", "#BusinessConsulting", "#ProfessionalServices", "#Advisory"]
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

# Create the LinkedIn reformatter agent
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
    
    tools=[analyze_post_length, suggest_hashtags, check_engagement_potential],
    handoff_description="Expert in LinkedIn content optimization and social media best practices"
)

async def main():
    """Test the LinkedIn agent with sample content."""
    
    test_posts = [
        "I just finished a project at work. It was challenging but we got it done. The team worked really hard and I'm proud of the results.",
        
        "Just read an interesting article about AI. It's going to change everything. Companies need to adapt or they'll be left behind.",
        
        "Had a great meeting with a client today. They were happy with our proposal and we're moving forward with the project. Excited to get started!"
    ]
    
    print("🚀 LinkedIn Reformatter Agent Demo")
    print("=" * 60)
    
    for i, original_post in enumerate(test_posts, 1):
        print(f"\n📝 Original Post {i}:")
        print(f'"{original_post}"')
        print("\n" + "─" * 40)
        
        try:
            result = await Runner.run(
                linkedin_agent, 
                f"Please reformat this content for LinkedIn: {original_post}"
            )
            
            print("🔄 LinkedIn Optimized Version:")
            print(result.final_output)
            print("\n" + "=" * 60)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    # Interactive mode
    print("\n💬 Interactive Mode - Enter your content to optimize:")
    print("(Type 'quit' to exit)")
    
    while True:
        user_input = input("\nYour content: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if user_input:
            try:
                result = await Runner.run(linkedin_agent, f"Please reformat this content for LinkedIn: {user_input}")
                print("\n🔄 LinkedIn Optimized Version:")
                print(result.final_output)
            except Exception as e:
                print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())

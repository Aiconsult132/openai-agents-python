# My OpenAI Agents Examples

Welcome to your personal OpenAI Agents SDK examples! This directory contains examples to help you get started with building your own AI agents.

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or newer
- OpenAI API key (you need to set this as an environment variable)
- The OpenAI Agents SDK (already installed in this project)

### Setting up your OpenAI API Key

**Option 1: Environment Variable (Recommended)**
```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY = "your-api-key-here"

# Windows (Command Prompt) 
set OPENAI_API_KEY=your-api-key-here

# macOS/Linux
export OPENAI_API_KEY=your-api-key-here
```

**Option 2: In Code (Less Secure)**
Uncomment and modify this line in any of the example files:
```python
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

### Your Examples

#### 1. `my_first_agent.py` - Basic Agent
A simple example that demonstrates:
- Creating a basic agent with instructions
- Running multiple queries
- Getting responses from the agent

**Run it:**
```bash
python my_first_agent.py
```

#### 2. `advanced_agent_example.py` - Multi-Agent System
A more complex example showcasing:
- Multiple specialized agents (Math, Weather, Time)
- Function tools for calculations, weather, and time
- Agent handoffs and intelligent routing
- Triage agent that coordinates between specialists

**Run it:**
```bash
python advanced_agent_example.py
```

## 🛠️ Key Concepts Demonstrated

### Agents
- **Instructions**: Define how your agent behaves
- **Names**: Help identify agents in multi-agent workflows
- **Tools**: Functions that agents can call
- **Handoffs**: Transfer control between agents

### Tools
- **Function Tools**: Python functions that agents can call
- **@function_tool**: Decorator to make functions available to agents
- **Tool Descriptions**: Automatically generated from docstrings

### Multi-Agent Workflows
- **Triage Pattern**: One agent routes to specialists
- **Handoff Descriptions**: Help the routing agent understand when to use each specialist
- **Coordination**: Agents working together on complex tasks

## 🎯 Next Steps

1. **Modify the examples**: Change instructions, add new tools, create new agents
2. **Add your own tools**: Create functions for your specific use cases
3. **Experiment with handoffs**: Build more complex multi-agent workflows
4. **Add guardrails**: Implement safety checks for inputs and outputs
5. **Use sessions**: Add memory to maintain conversation history

## 📚 Resources

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [Examples Directory](examples/) - More examples in the main project
- [Quickstart Guide](docs/quickstart.md)
- [Agent Patterns](examples/agent_patterns/) - Common workflow patterns

## 🔧 Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your OpenAI API key is valid and has sufficient credits
2. **Import Error**: Ensure you're running with `python` in the project directory and that the agents package is installed
3. **Rate Limits**: If you hit rate limits, add delays between requests

### Getting Help

- Check the [documentation](https://openai.github.io/openai-agents-python/)
- Look at more [examples](examples/)
- Review the [tests](tests/) for usage patterns

Happy coding! 🎉

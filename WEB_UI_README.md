# 🌐 Web UI for OpenAI Agents

This directory contains two different web-based user interfaces for interacting with your OpenAI Agents:

1. **FastAPI + WebSocket UI** - Real-time chat interface
2. **Streamlit UI** - Simple and elegant interface

## 🚀 Quick Start

### Install Requirements

```bash
pip install -r ui_requirements.txt
```

## Option 1: FastAPI Web UI (Recommended)

### Features
- ✅ Real-time WebSocket communication
- ✅ Beautiful, modern interface
- ✅ Agent switching on the fly
- ✅ Typing indicators
- ✅ Connection status
- ✅ Conversation history

### Run the FastAPI UI

```bash
python web_ui_server.py
```

Then open your browser to: **http://localhost:8000**

### Screenshots
- Clean, modern chat interface
- Real-time responses with typing indicators
- Agent selection dropdown
- Connection status indicator

## Option 2: Streamlit UI (Easier to Customize)

### Features
- ✅ Simple setup and customization
- ✅ Sidebar with agent information
- ✅ Example prompts
- ✅ Clear conversation button
- ✅ Agent details and tools display

### Run the Streamlit UI

```bash
streamlit run streamlit_ui.py
```

Your browser will automatically open to the Streamlit app (usually http://localhost:8501)

## 🎯 Available Agents

Both UIs give you access to:

1. **Simple Assistant** - Basic conversational agent
2. **Multi-Agent System** - Intelligent routing to specialists
3. **Math Specialist** - Calculator and math problems
4. **Weather Specialist** - Weather information (mock data)
5. **Time Keeper** - Current time and date information

## 🛠️ Customization

### Adding New Agents

Edit either `web_ui_server.py` or `streamlit_ui.py`:

```python
# Create your new agent
my_agent = Agent(
    name="My Custom Agent",
    instructions="Your custom instructions here",
    tools=[your_tools_here]
)

# Add to the AGENTS dictionary
AGENTS["my_agent"] = my_agent
```

### Adding New Tools

```python
@function_tool
def my_custom_tool(parameter: str) -> str:
    """Description of what this tool does."""
    # Your tool logic here
    return "Tool result"
```

### Styling the FastAPI UI

The FastAPI UI includes embedded CSS that you can modify directly in `web_ui_server.py`. Look for the `<style>` section in the HTML template.

### Customizing Streamlit

Streamlit is highly customizable through its configuration and theming system. You can:
- Modify the sidebar content
- Add new widgets
- Change the layout
- Add custom CSS with `st.markdown()`

## 🔧 Technical Details

### FastAPI UI Architecture
- **Backend**: FastAPI with WebSocket support
- **Frontend**: Vanilla JavaScript with modern CSS
- **Communication**: Real-time WebSocket messages
- **Session Management**: In-memory conversation history

### Streamlit UI Architecture  
- **Framework**: Streamlit with session state
- **Async Support**: Uses `asyncio.run()` for agent execution
- **State Management**: Streamlit's built-in session state
- **UI Components**: Streamlit's native widgets

## 🎨 UI Comparison

| Feature | FastAPI UI | Streamlit UI |
|---------|------------|-------------|
| Real-time chat | ✅ | ❌ |
| Typing indicators | ✅ | ❌ |
| Agent switching | ✅ | ✅ |
| Conversation history | ✅ | ✅ |
| Easy customization | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Modern design | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Setup complexity | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   - FastAPI: Change port in `uvicorn.run(port=8001)`
   - Streamlit: Use `streamlit run streamlit_ui.py --server.port 8502`

2. **WebSocket connection fails**
   - Check if port 8000 is accessible
   - Ensure no firewall blocking the connection

3. **Agent responses are slow**
   - This is normal for complex multi-agent workflows
   - Consider using simpler agents for faster responses

4. **Streamlit app crashes**
   - Check that all dependencies are installed
   - Restart with `streamlit run streamlit_ui.py --server.runOnSave true`

### Performance Tips

- Use the Simple Assistant for fastest responses
- The Multi-Agent System is slower but more intelligent
- Consider caching responses for repeated queries

## 🚀 Next Steps

1. **Try both UIs** to see which you prefer
2. **Customize the agents** for your specific use cases
3. **Add new tools** that are relevant to your domain
4. **Experiment with different agent configurations**
5. **Deploy to the cloud** for remote access

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI Agents SDK Docs](https://openai.github.io/openai-agents-python/)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

Happy chatting! 🎉

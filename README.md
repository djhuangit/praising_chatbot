# Praising Chatbot - Your Supportive Chat Space

A supportive and encouraging chat application that provides positive, uplifting responses to help users feel good about themselves and their achievements. Built with a clean separation of frontend (Gradio) and backend (FastAPI) components.

## Features

- Real-time chat interface with Gradio
- RESTful API with FastAPI backend
- Supportive AI responses using GPT-4o-mini
- Cost and token usage tracking
- Modern, responsive UI
- Modular architecture with clear separation of concerns
- In-memory session tracking (no database required)

## Tech Stack

- **Python 3.13+**
- **uv** - Fast Python package manager
- **FastAPI** - Backend API framework
- **Gradio** - Frontend web interface
- **OpenAI API** - For AI responses (gpt-4o-mini)
- **Pydantic** - Data validation and settings management
- **Stateless architecture** - No persistent storage required

## Project Structure

```
praising_chatbot/
├── src/                            # Source code
│   ├── backend/                    # Backend components
│   │   ├── api/                    # FastAPI routes and app
│   │   │   ├── app.py              # FastAPI app factory
│   │   │   └── routes.py           # API endpoints
│   │   ├── models/                 # Data models (Pydantic)
│   │   │   └── chat.py             # Chat-related models
│   │   └── services/               # Business logic
│   │       ├── openai_service.py   # OpenAI API integration
│   │       └── stats_service.py    # Usage statistics tracking
│   ├── frontend/                   # Frontend components
│   │   └── components/             # UI components
│   │       └── chat_interface.py   # Gradio chat interface
│   └── config/                     # Configuration
│       └── settings.py             # Environment variables, constants
├── main.py                         # Application entry point
├── app.py                          # Original single-file version (legacy)
├── pyproject.toml                  # Project configuration
├── requirements.txt                # Python dependencies
└── .env                            # Environment variables (not in git)
```

### Why uv?

- ⚡ **10-100x faster** than pip for dependency installation
- 🔒 **Consistent** - Built-in lock file support
- 🎯 **Simple** - Run scripts directly with `uv run` (no separate install needed)
- 🔄 **Compatible** - Works with standard Python packaging (pip, PyPI)
- 📦 **Self-contained** - Dependencies declared inline using PEP 723

## Getting Started

### Prerequisites
- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- OpenAI API key

### Installation

#### Using uv (Recommended - Fast!)

1. Clone the repository:
```bash
git clone [repository-url]
cd praising_chatbot
```

2. Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Create a `.env` file in the root directory with your OpenAI API key:
```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

4. Sync dependencies and run the application:
```bash
uv sync
uv run main.py
```

The application will start on `http://localhost:7860`

**Endpoints:**
- Gradio UI: `http://localhost:7860/gradio`
- API docs: `http://localhost:7860/docs`
- Health check: `http://localhost:7860/health`
- Stats API: `http://localhost:7860/api/stats`

#### Using pip (Alternative)

1. Clone the repository and navigate to the directory
2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key
4. Run the application:
```bash
python main.py
```

## Usage

1. Open the application in your browser
2. Type your message in the text box
3. Click "Send" or press Enter
4. Receive supportive and encouraging responses
5. View usage statistics in the accordion section
6. Clear chat history anytime with the "Clear Chat" button

## Configuration

You can modify the chatbot's behavior by editing the `SYSTEM_PROMPT` in [src/config/settings.py](src/config/settings.py):

```python
SYSTEM_PROMPT = """You are a supportive and encouraging friend. Your role is to provide positive,
uplifting responses that make the user feel good about themselves and their achievements.
Always maintain a positive, humorous and fluffy tone and keep the responses within 50 words. No emoji."""
```

Other configuration options in [src/config/settings.py](src/config/settings.py):
- `OPENAI_MODEL`: Change the AI model (default: gpt-4o-mini)
- `HOST` and `PORT`: Server configuration
- `COST_PER_MILLION_TOKENS`: Adjust cost calculations

## Cost Tracking

The application tracks:
- Total tokens used
- Total cost incurred (based on GPT-4o-mini pricing: $0.15 per million tokens)

Note: Statistics are stored in-memory and reset when the server restarts.

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Architecture Benefits

The new modular structure provides:
- **Separation of Concerns**: Frontend and backend are clearly separated
- **Testability**: Each module can be tested independently
- **Scalability**: Easy to add new features or replace components
- **Maintainability**: Clear organization makes code easier to understand
- **Reusability**: Services can be reused across different interfaces

## Future Improvements

- Add conversation history (with user opt-in)
- Support for multiple AI models
- Customizable themes
- Export chat history
- Multi-language support
- Database integration for persistent storage
- User authentication and profiles

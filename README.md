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
│   │       ├── demo_service.py     # Demo/mock service (no API calls)
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

## Getting Started

### Prerequisites
- Python 3.13 or higher
- uv for dependency management [(docs including installation guide)]((https://docs.astral.sh/uv/))
- OpenAI API key (required only for production mode; app runs in demo mode by default)

### Quick Start
1. Clone the repository:
    ```bash
    git clone [repository-url]
    cd praising_chatbot
    ```
2. (Optional) Create a `.env` file in the root directory:

- **For demo/testing (default - no API key needed):**
    ```bash
    # No .env file needed! Demo mode is the default.
    # Or explicitly set:
    DEMO_MODE=true
    ```

- **For production (with OpenAI API):**
    ```bash
    OPENAI_API_KEY=your_openai_api_key_here
    DEMO_MODE=false
    ```

3. Sync dependencies and run the application:
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

## Usage

1. Open the application in your browser
2. Type your message in the text box
3. Click "Send" or press Enter
4. Receive supportive and encouraging responses
5. View usage statistics in the accordion section
6. Clear chat history anytime with the "Clear Chat" button

## Demo Mode

The application **runs in demo mode by default**, allowing you to test the interface without making actual OpenAI API calls. This is perfect for:
- Testing the application without an API key
- Development and debugging
- Demonstrations and presentations
- Avoiding API costs during testing

### How Demo Mode Works (Default)

- **No API calls**: Uses predefined encouraging responses instead of calling OpenAI
- **Mock tokens**: Simulates token usage for cost tracking (approximately 1 token per 4 characters)
- **Same interface**: The UI and API work identically to production mode
- **Clear indicators**: Console logs and UI banner clearly show when demo mode is active

### Switching to Production Mode

To use real OpenAI API responses, create a `.env` file with:

```bash
# In .env file
OPENAI_API_KEY=your_actual_api_key_here
DEMO_MODE=false
```

### Re-enabling Demo Mode

To switch back to demo mode:

```bash
# In .env file
DEMO_MODE=true
```

Or simply remove both `DEMO_MODE` and `OPENAI_API_KEY` from your `.env` file (demo is the default).

## Configuration

You can modify the chatbot's behavior by editing the `SYSTEM_PROMPT` in [src/config/settings.py](src/config/settings.py):

```python
SYSTEM_PROMPT = """You are a supportive and encouraging friend. Your role is to provide positive,
uplifting responses that make the user feel good about themselves and their achievements.
Always maintain a positive, humorous and fluffy tone and keep the responses within 50 words. No emoji."""
```

Other configuration options in [src/config/settings.py](src/config/settings.py):
- `DEMO_MODE`: Enable/disable demo mode (default: true)
- `OPENAI_MODEL`: Change the AI model (default: gpt-4o-mini)
- `HOST` and `PORT`: Server configuration
- `COST_PER_MILLION_TOKENS`: Adjust cost calculations

## Cost Tracking

The application tracks:
- Total tokens used
- Total cost incurred (based on GPT-4o-mini pricing: $0.15 per million tokens)

Note: Statistics are stored in-memory and reset when the server restarts.

## Deployment

### Heroku Deployment

This application is ready to deploy on Heroku. Follow these steps:

#### Prerequisites
- A [Heroku account](https://signup.heroku.com/)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed

#### Quick Deploy

1. **Login to Heroku:**
   ```bash
   heroku login
   ```

2. **Create a new Heroku app:**
   ```bash
   heroku create your-app-name
   ```

3. **Deploy to Heroku:**
   ```bash
   git push heroku main
   ```

4. **Open your application:**
   ```bash
   heroku open
   ```

   Your app will be available at `https://your-app-name.herokuapp.com/gradio`

#### Configuration

**Demo Mode (Default):**
The app deploys in demo mode by default - no API key required!

**Production Mode with OpenAI API:**
To enable real OpenAI responses, set your API key:

```bash
heroku config:set OPENAI_API_KEY=your_openai_api_key_here
heroku config:set DEMO_MODE=false
```

**Other Configuration Options:**
```bash
# Change the OpenAI model
heroku config:set OPENAI_MODEL=gpt-4

# Adjust logging level
heroku config:set LOG_LEVEL=debug
```

#### View Logs

```bash
heroku logs --tail
```

#### Important Notes

- **UV Support**: This project uses `uv` for dependency management. Heroku automatically detects `uv.lock` and uses native `uv` support for faster, more reliable builds.
- **Python Version**: Heroku uses Python 3.12 (specified in `runtime.txt`). The app is compatible with Python 3.12+.
- **Port Configuration**: Heroku automatically sets the `PORT` environment variable, which the app uses.
- **Persistent Storage**: The app uses in-memory storage, so stats reset on dyno restart.
- **Free Tier**: Heroku's free tier may cause the app to sleep after 30 minutes of inactivity.

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

# Praising Chatbot - Your Supportive Chat Space

A supportive and encouraging chat application that provides positive, uplifting responses to help users feel good about themselves and their achievements. Built with Gradio for simple deployment and a clean user interface.

## Features

- Real-time chat interface with Gradio
- Supportive AI responses using GPT-4o-mini
- Cost and token usage tracking
- Modern, responsive UI
- Single Python file - easy to deploy anywhere
- In-memory session tracking (no database required)

## Tech Stack

- **Python 3.8+**
- **uv** - Fast Python package manager
- **Gradio** - For the web interface
- **OpenAI API** - For AI responses (gpt-4o-mini)
- **Stateless architecture** - No persistent storage required

### Why uv?

- ⚡ **10-100x faster** than pip for dependency installation
- 🔒 **Consistent** - Built-in lock file support
- 🎯 **Simple** - Run scripts directly with `uv run` (no separate install needed)
- 🔄 **Compatible** - Works with standard Python packaging (pip, PyPI)
- 📦 **Self-contained** - Dependencies declared inline using PEP 723

## Getting Started

### Prerequisites
- Python 3.8 or higher
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

4. Run the application (uv automatically installs dependencies from inline metadata):
```bash
uv run app.py
```

The application will start on `http://localhost:7860`

**Note**: `app.py` includes inline script metadata (PEP 723), so `uv run` automatically handles all dependencies without needing a separate install step.

#### Using pip (Alternative)

1. Clone the repository and navigate to the directory
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key
4. Run the application:
```bash
python app.py
```

## Deployment

This application is incredibly easy to deploy thanks to its single-file architecture:

### Hugging Face Spaces (Recommended)
1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Select "Gradio" as the SDK
3. Upload `app.py` and `requirements.txt`
4. Add your `OPENAI_API_KEY` in the Space settings (Secrets)
5. Done! Your app is live

### Other Platforms
The app works on any platform that supports Python:
- **Render**: Deploy as a Web Service
- **Railway**: One-click deploy
- **PythonAnywhere**: Upload and run
- **Fly.io**: Simple Python deployment
- **Google Cloud Run**: Containerized deployment

### Docker (Optional)

Using uv for faster builds:
```dockerfile
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim
WORKDIR /app
COPY pyproject.toml .
COPY app.py .
COPY .env .
EXPOSE 7860
CMD ["uv", "run", "app.py"]
```

Or with pip:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY .env .
EXPOSE 7860
CMD ["python", "app.py"]
```

## Usage

1. Open the application in your browser
2. Type your message in the text box
3. Click "Send" or press Enter
4. Receive supportive and encouraging responses
5. View usage statistics in the accordion section
6. Clear chat history anytime with the "Clear Chat" button

## Configuration

You can modify the chatbot's behavior by editing the `SYSTEM_PROMPT` in `app.py`:

```python
SYSTEM_PROMPT = """You are a supportive and encouraging friend. Your role is to provide positive,
uplifting responses that make the user feel good about themselves and their achievements.
Always maintain a positive, humorous and fluffy tone and keep the responses within 50 words. No emoji."""
```

## Cost Tracking

The application tracks:
- Total tokens used
- Total cost incurred (based on GPT-4o-mini pricing: $0.15 per million tokens)

Note: Statistics are stored in-memory and reset when the server restarts.

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Future Improvements

- Add conversation history (with user opt-in)
- Support for multiple AI models
- Customizable themes
- Export chat history
- Multi-language support

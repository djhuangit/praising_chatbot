# Praising Chatbot - Your Supportive Chat Space

A supportive and encouraging chat application that provides positive, uplifting responses to help users feel good about themselves and their achievements. Now powered by **Gradio** for a simple, intuitive interface!

## Features

- 🎨 Beautiful Gradio chat interface
- 🤗 Supportive AI responses using GPT-4o-mini
- 💾 Session-based conversations with database persistence
- 💰 Real-time cost and token usage tracking
- 🚀 Easy to run - just one command!
- 📊 Usage statistics displayed in the UI

## Tech Stack

- **Frontend**: Gradio 4.44.0 (Python-based UI)
- **Backend**: FastAPI (legacy, still available in `/backend`)
- **Database**: PostgreSQL/SQLite (async with SQLAlchemy)
- **AI**: OpenAI API (GPT-4o-mini)
- **Language**: Python 3.x

## Getting Started

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- PostgreSQL (for production) or SQLite (for development)

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd praising_chatbot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:
```
OPENAI_API_KEY=your-openai-api-key-here
DATABASE_URL=sqlite+aiosqlite:///./chat.db  # Or your PostgreSQL URL
```

### Running the Application

Simply run:
```bash
python app.py
```

The application will be available at:
- **Local**: http://localhost:7860
- **Network**: http://0.0.0.0:7860

## Usage

1. Open the application in your browser
2. Type your message in the text box
3. Click "Send" or press Enter
4. Receive supportive and encouraging responses!
5. Track your API usage in real-time at the top of the page

## Project Structure

```
praising_chatbot/
├── app.py              # Main Gradio application
├── backend/            # Legacy FastAPI backend (kept for reference)
│   ├── main.py
│   ├── database.py
│   └── models.py
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md
```

## Configuration

### Database Options

**SQLite** (Default - Easy for development):
```
DATABASE_URL=sqlite+aiosqlite:///./chat.db
```

**PostgreSQL** (Production):
```
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
```

### OpenAI Model

Currently using `gpt-4o-mini` at $0.15 per 1M tokens. To change the model, edit `app.py` line 76.

## Features in Detail

### 💬 Chat Interface
- Clean, modern Gradio interface
- Real-time message display
- Avatar support for AI responses

### 💾 Persistence
- All messages saved to database
- Unique session ID per user
- Chat history maintained across sessions

### 💰 Cost Tracking
- Real-time token usage display
- Total cost calculation
- Persistent cost tracking across app restarts

## Deployment

The Gradio app can be deployed to:
- **Hugging Face Spaces** (Recommended for Gradio apps)
- **Render** (Python web service)
- **Railway** (Easy deployment)
- Any platform supporting Python applications

## Migration Notes

This version represents **Branch 1** of a major overhaul:
- ✅ Migrated from React + TypeScript to Gradio
- 🔄 Database still in use (will be removed in Branch 2)
- 🔄 Architecture restructuring pending (Branch 3)
- 🔄 File-based token storage pending (Branch 4)

## Future Improvements

- [ ] Remove database dependency (use JSON files)
- [ ] Restructure codebase with proper `src/` architecture
- [ ] Add conversation history to AI context
- [ ] Support multiple chat sessions
- [ ] Export chat history feature
- [ ] More customization options

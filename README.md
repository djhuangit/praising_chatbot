# Praising Chatbot - Your Supportive Chat Space

A supportive and encouraging chat application that provides positive, uplifting responses to help users feel good about themselves and their achievements. The application is built with a modern tech stack and features a clean, user-friendly interface.

🌐 Live Demo: [https://djpraisingchat.netlify.app/](https://djpraisingchat.netlify.app/)

## Features

- Real-time chat interface
- Supportive AI responses using GPT-4
- Session-based conversations
- Cost and token usage tracking
- Modern, responsive UI
- Cross-platform compatibility

## Tech Stack

### Frontend
- React 18
- TypeScript
- Vite
- Emotion (Styled Components)
- Axios for API communication

### Backend
- FastAPI
- OpenAI API
- Stateless architecture (no persistent storage)
- Python 3.x

## Getting Started

### Prerequisites
- Node.js (v18 or higher)
- Python 3.x

### Environment Setup

1. Clone the repository:
```bash
git clone [repository-url]
cd praising_chatbot
```

2. Backend Setup:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the backend directory with:
```
OPENAI_API_KEY=your_openai_api_key
```

Note: This application runs in stateless mode - chat history is not persisted. Cost tracking is maintained in-memory during the current session only.

3. Frontend Setup:
```bash
cd frontend
npm install
```

Create a `.env` file in the frontend directory with:
```
VITE_API_URL=http://localhost:8000
```

### Running the Application

1. Start the backend:
```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend:
```bash
cd frontend
npm run dev
```

## Deployment

The application uses a stateless architecture and can be deployed to any platform:
- Frontend: Netlify
- Backend: Compatible with Heroku, Render, PythonAnywhere, Railway, Fly.io, or any platform supporting Python
- Storage: No persistent storage required - works with ephemeral filesystems!

## Future Improvements

- Add more features to the chatbot
- Add more tests
- Add more documentation

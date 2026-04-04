# MindMate

MindMate is a local Flask-based mental wellness companion for emotional check-ins, supportive conversation, and mood/stress tracking.

It runs fully on your machine and serves a browser UI at localhost.

## What It Does
- Provides supportive chat responses based on detected emotional context
- Detects potential crisis language and returns immediate support messaging
- Classifies stress level from message content
- Stores mood entries in a local SQLite database
- Supports multiple chat sessions in the sidebar (create/switch/reset)

## Tech Stack
- Backend: Flask
- NLP/ML: Hugging Face Transformers + Torch
- Storage: SQLite
- Frontend: HTML/CSS/JS (Jinja templates + static assets)

## Project Structure
- [app.py](app.py): Main local server entrypoint and API routes
- [emotion_model.py](emotion_model.py): Emotion model setup/inference
- [stress_classifier.py](stress_classifier.py): Stress-level classification logic
- [crisis_detector.py](crisis_detector.py): Crisis phrase detection and support resources
- [response_generator.py](response_generator.py): Conversational and coping response generation
- [database.py](database.py): SQLite database wrapper
- [templates/local_home.html](templates/local_home.html): Home page template
- [templates/local_index.html](templates/local_index.html): Chat page template
- [static/local_style.css](static/local_style.css): Styles
- [static/local_app.js](static/local_app.js): Frontend chat/session behavior
- [requirements.txt](requirements.txt): Python dependencies

## Prerequisites
- Python 3.10+
- A virtual environment is recommended
- Internet access on first run (for model download)

## Setup
1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate it (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Run The App
```bash
python app.py
```

Open:
- http://127.0.0.1:5000 (Home)
- http://127.0.0.1:5000/chat (Chat)

## How To Use
1. Open Home and click Start a session.
2. In Chat, type a message and send.
3. Use + New Session to create a new chat thread.
4. Click any session in the sidebar to switch to it.

## API Endpoints
- `GET /`: Home page
- `GET /chat`: Chat page
- `POST /api/message`: Send a message
- `POST /api/new-session`: Create a new session
- `POST /api/switch-session`: Switch active session
- `POST /api/reset`: Clear current session messages

## Data Storage
- Chat session state is kept in browser session cookies/server session object.
- Mood entries are stored in local SQLite:
   - [mood_tracker.db](mood_tracker.db)

## Troubleshooting
- Port already in use:
   - Stop the existing Python process or change port in [app.py](app.py).
- First emotional message is slow:
   - The model may be downloading/loading for the first time.
- App does not start from `python app.py`:
   - Confirm venv is active and dependencies are installed.

## Important Note
MindMate is a supportive tool, not a substitute for licensed professional care. If someone is in immediate danger, contact local emergency services or crisis support right away.


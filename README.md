# MindMate

MindMate is a Streamlit-based AI mental wellness companion that supports emotional check-ins, mood tracking, and stress insights.

## Features
- Guided emotional chat with supportive responses
- Crisis signal detection and safety-oriented alerts
- Mood/stress tracking stored in a local database
- Dashboard and analytics (stress trend + emotion distribution)

## Project Structure
- `app.py` – Streamlit app entry point and UI
- `emotion_model.py` – emotion detection setup
- `stress_classifier.py` – stress level classification
- `crisis_detector.py` – crisis signal checks
- `response_generator.py` – response generation utilities
- `database.py` – local persistence layer
- `requirements.txt` – dependencies

## Run Locally
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```

## Deploy (Streamlit Community Cloud)
1. Push this folder to a GitHub repository.
2. In Streamlit Community Cloud, create a new app from that repo.
3. Set the main file path to `app.py`.
4. Deploy.

## Notes
- `mood_tracker.db` is local runtime data and excluded from git via `.gitignore`.
- For production-grade deployments, consider moving persistence to a managed database and pinning dependency versions.

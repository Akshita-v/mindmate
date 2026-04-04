import logging
import os
import random
import uuid
from datetime import datetime
from functools import lru_cache

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from crisis_detector import CrisisDetector
from database import MoodDatabase
from emotion_model import initialize_emotion_detector
from response_generator import ConversationClassifier, ResponseGenerator
from stress_classifier import StressClassifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "mindmate-local-dev-secret")


def _normalize_level(level: str) -> str:
    if not level:
        return "Low"
    value = str(level).strip().lower()
    if value in {"moderate", "medium"}:
        return "Moderate"
    if value == "high":
        return "High"
    return "Low"


@lru_cache(maxsize=1)
def get_emotion_detector():
    return initialize_emotion_detector()


@lru_cache(maxsize=1)
def get_stress_classifier():
    return StressClassifier()


@lru_cache(maxsize=1)
def get_response_generator():
    return ResponseGenerator()


@lru_cache(maxsize=1)
def get_crisis_detector():
    return CrisisDetector()


@lru_cache(maxsize=1)
def get_database():
    return MoodDatabase()


def is_simple_greeting(user_text):
    text = user_text.lower().strip()
    greetings = {
        "hey", "hi", "hello", "hiya", "heya", "sup", "yo", "hii", "hiii",
        "hey there", "hi there", "hello there", "good morning", "good evening",
        "good afternoon", "howdy", "greetings",
    }
    cleaned = text.replace("!", "").replace(".", "").replace("?", "")
    return text in greetings or cleaned in greetings


def generate_greeting_response():
    responses = [
        "Hi, I am here with you. How are you feeling today?",
        "Good to hear from you. What has your day felt like so far?",
        "I am listening. Share anything that is on your mind.",
        "Thanks for checking in. What feels heaviest right now?",
    ]
    return random.choice(responses)


def generate_boundary_response():
    responses = [
        "I am focused on emotional support, stress, and wellbeing. If you want, tell me how you are feeling and I can help from there.",
        "I cannot help with technical tasks here, but I can absolutely support you emotionally. What has been on your mind?",
        "I am here for your feelings and stress support. Share what you are going through and we can work through it together.",
    ]
    return random.choice(responses)


def _fallback_emotion_result(text: str):
    """Fallback emotion classification when model inference is unavailable."""
    text_lower = (text or "").lower()

    stress_words = {"stress", "stressed", "overwhelmed", "burnout", "pressure"}
    anxiety_words = {"anxious", "anxiety", "panic", "worried", "nervous"}
    sadness_words = {"sad", "depressed", "hopeless", "lonely", "empty"}
    anger_words = {"angry", "furious", "frustrated", "annoyed", "mad"}
    joy_words = {"happy", "joy", "grateful", "excited", "great"}

    if any(word in text_lower for word in stress_words):
        emotion = "stress"
        sentiment = "negative"
    elif any(word in text_lower for word in anxiety_words):
        emotion = "anxiety"
        sentiment = "negative"
    elif any(word in text_lower for word in sadness_words):
        emotion = "sadness"
        sentiment = "negative"
    elif any(word in text_lower for word in anger_words):
        emotion = "anger"
        sentiment = "negative"
    elif any(word in text_lower for word in joy_words):
        emotion = "joy"
        sentiment = "positive"
    else:
        emotion = "neutral"
        sentiment = "neutral"

    return {
        "emotion": emotion,
        "confidence": 0.55,
        "sentiment": sentiment,
        "all_scores": [],
    }


def process_message(user_text: str):
    try:
        cleaned_text = (user_text or "").strip()
        if not cleaned_text:
            return {
                "conversation_type": "empty",
                "crisis": {"is_crisis": False},
                "emotion": {"emotion": "neutral", "confidence": 1.0, "sentiment": "neutral"},
                "stress": {"level": "Low", "score": 0},
                "response": "I am here whenever you are ready to share.",
                "coping": None,
            }

        if is_simple_greeting(cleaned_text):
            return {
                "conversation_type": "casual",
                "crisis": {"is_crisis": False},
                "emotion": {"emotion": "neutral", "confidence": 0.95, "sentiment": "positive"},
                "stress": {"level": "Low", "score": 10},
                "response": generate_greeting_response(),
                "coping": None,
            }

        conversation_type = ConversationClassifier.classify_conversation(cleaned_text)
        if conversation_type == "informational":
            return {
                "conversation_type": "informational",
                "crisis": {"is_crisis": False},
                "emotion": {"emotion": "neutral", "confidence": 0.8, "sentiment": "neutral"},
                "stress": {"level": "Low", "score": 20},
                "response": generate_boundary_response(),
                "coping": None,
            }

        if conversation_type == "casual":
            return {
                "conversation_type": "casual",
                "crisis": {"is_crisis": False},
                "emotion": {"emotion": "neutral", "confidence": 0.9, "sentiment": "positive"},
                "stress": {"level": "Low", "score": 15},
                "response": ConversationClassifier.get_casual_response(),
                "coping": None,
            }

        stress_classifier = get_stress_classifier()
        crisis_detector = get_crisis_detector()
        response_generator = get_response_generator()
        mood_db = get_database()

        crisis_result = crisis_detector.detect_crisis(cleaned_text)

        try:
            emotion_result = get_emotion_detector().detect_emotion(cleaned_text)
        except Exception:
            logger.exception("Emotion model unavailable. Using keyword fallback.")
            emotion_result = _fallback_emotion_result(cleaned_text)

        emotion = emotion_result.get("emotion", "neutral")
        confidence = emotion_result.get("confidence", 0.0)
        sentiment = emotion_result.get("sentiment", "neutral")

        stress_result = stress_classifier.classify_stress(emotion, confidence, cleaned_text)
        stress_result["level"] = _normalize_level(stress_result.get("level"))

        mood_db.add_mood_entry(
            user_input=cleaned_text,
            emotion=emotion,
            emotion_confidence=confidence,
            stress_level=stress_result.get("level"),
            stress_score=stress_result.get("score"),
            sentiment=sentiment,
        )

        if crisis_result.get("is_crisis"):
            crisis_message = crisis_result.get("support_message", "")
            crisis_result = {**crisis_result, "message": crisis_message}
            return {
                "conversation_type": "crisis",
                "crisis": crisis_result,
                "emotion": emotion_result,
                "stress": stress_result,
                "response": crisis_message,
                "coping": None,
            }

        response_text = response_generator.generate_response(
            emotion,
            confidence,
            stress_result.get("level"),
            user_text=cleaned_text,
        )
        coping = response_generator.get_coping_strategy(emotion, stress_result.get("level"))

        return {
            "conversation_type": conversation_type,
            "crisis": {"is_crisis": False},
            "emotion": emotion_result,
            "stress": stress_result,
            "response": response_text,
            "coping": coping,
        }

    except Exception:
        logger.exception("Error processing user message")
        return {
            "conversation_type": "error",
            "crisis": {"is_crisis": False},
            "emotion": {"emotion": "neutral", "confidence": 0.5, "sentiment": "neutral"},
            "stress": {"level": "Moderate", "score": 50},
            "response": "I am here with you. I had trouble processing that message, but you can try again and I will keep listening.",
            "coping": {
                "technique_name": "Grounding Pause",
                "instructions": "Take a slow breath in for 4 counts and out for 6 counts. Repeat 3 times.",
                "affirmation": "I can take this one step at a time.",
                "tip": "Short pauses help your nervous system settle.",
            },
        }


def _get_history():
    sessions, chat_sessions, current_session_id = _ensure_session_store()
    _ = sessions  # Keep for readability; sessions are ensured for sidebar rendering.
    history = chat_sessions.get(current_session_id, [])
    if not isinstance(history, list):
        return []
    return history


def _ensure_session_store():
    """Ensure session metadata and per-session chat history exist."""
    sessions = session.get("sessions")
    chat_sessions = session.get("chat_sessions")
    current_session_id = session.get("current_session_id")

    if not isinstance(sessions, list):
        sessions = []

    if not isinstance(chat_sessions, dict):
        chat_sessions = {}

    session_ids = {item.get("id") for item in sessions if isinstance(item, dict)}
    if not current_session_id or current_session_id not in session_ids:
        new_id = uuid.uuid4().hex
        sessions.append(
            {
                "id": new_id,
                "title": f"Session {len(sessions) + 1}",
                "date": datetime.now().strftime("%b %d, %Y"),
            }
        )
        chat_sessions[new_id] = []
        current_session_id = new_id

    # Ensure all session IDs have a history bucket.
    for item in sessions:
        sid = item.get("id")
        if sid and sid not in chat_sessions:
            chat_sessions[sid] = []

    session["sessions"] = sessions
    session["chat_sessions"] = chat_sessions
    session["current_session_id"] = current_session_id

    return sessions, chat_sessions, current_session_id


@app.get("/")
def index():
    return render_template("local_home.html")


@app.get("/chat")
def chat():
    sessions, _, current_session_id = _ensure_session_store()
    return render_template(
        "local_index.html",
        chat_history=_get_history(),
        sessions=sessions,
        current_session_id=current_session_id,
    )


@app.get("/home")
def home_redirect():
    return redirect(url_for("index"))


@app.post("/api/message")
def api_message():
    payload = request.get_json(silent=True) or {}
    user_text = (payload.get("message") or "").strip()
    if not user_text:
        return jsonify({"error": "Message is required"}), 400

    try:
        result = process_message(user_text)
        entry = {
            "timestamp": datetime.now().strftime("%H:%M"),
            "user": user_text,
            "result": result,
        }

        sessions, chat_sessions, current_session_id = _ensure_session_store()
        _ = sessions
        history = chat_sessions.get(current_session_id, [])
        history.append(entry)
        chat_sessions[current_session_id] = history[-30:]
        session["chat_sessions"] = chat_sessions

        return jsonify(entry)

    except Exception:
        logger.exception("Unhandled API error")
        return jsonify({"error": "Internal server error"}), 500


@app.post("/api/reset")
def api_reset():
    _, chat_sessions, current_session_id = _ensure_session_store()
    chat_sessions[current_session_id] = []
    session["chat_sessions"] = chat_sessions
    return jsonify({"ok": True})


@app.post("/api/new-session")
def api_new_session():
    sessions, chat_sessions, _ = _ensure_session_store()

    new_id = uuid.uuid4().hex
    sessions.append(
        {
            "id": new_id,
            "title": f"Session {len(sessions) + 1}",
            "date": datetime.now().strftime("%b %d, %Y"),
        }
    )
    chat_sessions[new_id] = []

    session["sessions"] = sessions
    session["chat_sessions"] = chat_sessions
    session["current_session_id"] = new_id

    return jsonify({"ok": True, "session_id": new_id})


@app.post("/api/switch-session")
def api_switch_session():
    payload = request.get_json(silent=True) or {}
    session_id = (payload.get("session_id") or "").strip()
    if not session_id:
        return jsonify({"error": "session_id is required"}), 400

    sessions, _, _ = _ensure_session_store()
    valid_ids = {item.get("id") for item in sessions if isinstance(item, dict)}
    if session_id not in valid_ids:
        return jsonify({"error": "session not found"}), 404

    session["current_session_id"] = session_id
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

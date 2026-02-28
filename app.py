import logging
import random
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from crisis_detector import CrisisDetector
from database import MoodDatabase
from emotion_model import initialize_emotion_detector
from response_generator import ResponseGenerator, ConversationClassifier
from stress_classifier import StressClassifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="MindMate - AI Mental Health Companion",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_modern_css():
    """Apply complete premium frontend redesign."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

        * {
            font-family: 'Manrope', sans-serif;
        }

        :root {
            --bg-0: #060b1a;
            --bg-1: #0f172a;
            --bg-2: #1e293b;
            --text-main: #f8fafc;
            --text-soft: #cbd5e1;
            --line: rgba(148, 163, 184, 0.25);
            --brand: #60a5fa;
            --brand-2: #22d3ee;
            --ok: #34d399;
            --warn: #fb923c;
            --danger: #fb7185;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp {
            color: var(--text-main);
            background:
                radial-gradient(1200px 600px at 8% -5%, rgba(56, 189, 248, 0.15), transparent 45%),
                radial-gradient(1000px 500px at 105% 5%, rgba(99, 102, 241, 0.13), transparent 42%),
                linear-gradient(160deg, var(--bg-0) 0%, var(--bg-1) 45%, #111c36 100%);
        }

        .main .block-container {
            max-width: 1080px;
            padding: 1.4rem 2rem 2rem 2rem;
        }

        h1, h2, h3, h4 {
            color: var(--text-main);
            letter-spacing: -0.02em;
        }

        p, li, label {
            color: var(--text-soft);
        }

        .glass-panel {
            background: linear-gradient(160deg, rgba(30, 41, 59, 0.72) 0%, rgba(15, 23, 42, 0.78) 100%);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 20px;
            box-shadow: 0 18px 40px rgba(2, 6, 23, 0.55);
            backdrop-filter: blur(6px);
            padding: 1.4rem;
        }

        .hero-title {
            font-size: 3.3rem;
            font-weight: 800;
            line-height: 1.05;
            margin: 0.35rem 0;
        }

        .hero-sub {
            color: #dbeafe;
            font-size: 1.07rem;
            margin: 0.2rem 0 0 0;
        }

        .pill {
            display: inline-block;
            border: 1px solid rgba(96, 165, 250, 0.45);
            background: rgba(96, 165, 250, 0.12);
            color: #bfdbfe;
            border-radius: 999px;
            padding: 0.3rem 0.8rem;
            font-size: 0.75rem;
            font-weight: 500;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }

        .stButton > button {
            border: 1px solid rgba(148, 163, 184, 0.25);
            background: linear-gradient(130deg, #3b82f6 0%, #06b6d4 100%);
            color: #eff6ff;
            border-radius: 14px;
            padding: 0.65rem 1rem;
            font-weight: 700;
            font-size: 0.95rem;
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.33);
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(14, 165, 233, 0.42);
            border-color: rgba(125, 211, 252, 0.65);
        }

        .stTextArea textarea {
            background: rgba(15, 23, 42, 0.6);
            color: var(--text-main);
            border: 1px solid rgba(96, 165, 250, 0.58);
            border-radius: 200px;
            padding: 0.5rem 0.75rem;
            font-size: 0.93rem;
            resize: none;
            min-height: 68px !important;
            max-height: 100px !important;
        }

        .stTextArea textarea:focus {
            border-color: rgba(96, 165, 250, 0.6);
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.12);
            outline: none;
        }

        .stTextArea textarea::placeholder {
            color: #64748b;
        }

        /* Chat input styling */
        .stTextInput input {
            background-color: rgba(71, 85, 105, 0.8) !important;
            border: 1px solid rgba(100, 116, 139, 0.6) !important;
            border-radius: 50px !important;
            color: #ffffff !important;
            height: 60px !important;
            padding: 12px 70px 12px 20px !important;
            font-size: 1rem !important;
        }

        .stTextInput input:focus {
            border-color: rgba(96, 165, 250, 0.8) !important;
            box-shadow: 0 0 0 1px rgba(96, 165, 250, 0.3) !important;
        }

        .stTextInput input::placeholder {
            color: #94a3b8 !important;
        }

        /* Button inside pill */
        .chat-inline-row {
            position: relative !important;
        }

        [data-testid="column"]:last-child {
            position: absolute !important;
            right: 10px !important;
            top: 50% !important;
            transform: translateY(-50%) !important;
        }

        /* Send button styling - Normal size */
        .stFormSubmitButton button {
            background: linear-gradient(135deg, #60a5fa 0%, #22d3ee 100%) !important;
            border: none !important;
            color: white !important;
            border-radius: 50% !important;
            width: 48px !important;
            height: 48px !important;
            padding: 0 !important;
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.2s ease !important;
        }

        .stFormSubmitButton button:hover {
            box-shadow: 0 8px 30px rgba(34, 211, 238, 0.7) !important;
            transform: scale(1.1) !important;
        }

        .stFormSubmitButton button:active {
            transform: scale(0.95) !important;
        }

        .kpi-card {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.82) 0%, rgba(30, 41, 59, 0.78) 100%);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 18px;
            padding: 1.05rem;
            min-height: 130px;
            box-shadow: 0 12px 28px rgba(2, 6, 23, 0.42);
        }

        .kpi-title { color: #cbd5e1; font-size: 0.84rem; margin-top: 0.4rem; }
        .kpi-value { color: #f8fafc; font-size: 2rem; font-weight: 800; margin: 0; line-height: 1.1; }

        .section-title {
            margin: 0 0 0.8rem 0;
            font-size: 1.15rem;
            color: #e2e8f0;
            font-weight: 700;
        }

        .user-msg {
            display: flex;
            justify-content: flex-end;
            margin: 0.8rem 0;
        }

        .user-msg-bubble {
            max-width: 76%;
            border-radius: 18px 18px 6px 18px;
            background: linear-gradient(130deg, #0ea5e9 0%, #3b82f6 100%);
            color: #ecfeff;
            padding: 0.85rem 1rem;
            box-shadow: 0 10px 22px rgba(14, 165, 233, 0.34);
            font-weight: 600;
        }

        .bot-msg {
            display: flex;
            justify-content: flex-start;
            margin: 0.8rem 0;
        }

        .bot-msg-bubble {
            max-width: 78%;
            border-radius: 18px 18px 18px 6px;
            background: rgba(30, 41, 59, 0.84);
            border: 1px solid rgba(148, 163, 184, 0.26);
            color: #e2e8f0;
            padding: 0.9rem 1rem;
            box-shadow: 0 10px 24px rgba(2, 6, 23, 0.48);
        }

        .msg-info {
            color: #94a3b8;
            font-size: 0.72rem;
            margin-top: 0.32rem;
        }

        .crisis-alert {
            background: rgba(251, 113, 133, 0.15);
            border: 1px solid rgba(251, 113, 133, 0.5);
            border-radius: 14px;
            padding: 1rem;
            margin: 1rem 0;
            color: #fecdd3;
        }

        .coping-strategy {
            background: rgba(52, 211, 153, 0.11);
            border: 1px solid rgba(52, 211, 153, 0.42);
            border-radius: 14px;
            padding: 1rem;
            margin: 0.9rem 0 1.2rem 0;
            color: #d1fae5;
        }

        .muted-note {
            color: #94a3b8;
            text-align: center;
            font-size: 0.84rem;
            margin-top: 0.8rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b1224 0%, #111f3d 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.2);
        }

        [data-testid="stSidebar"] .stButton > button {
            background: rgba(30, 41, 59, 0.7);
            color: #bfdbfe;
            border: 1px solid rgba(125, 211, 252, 0.25);
            border-radius: 12px;
            box-shadow: none;
            text-align: left;
            justify-content: flex-start;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            transform: none;
            background: rgba(37, 99, 235, 0.32);
            border-color: rgba(125, 211, 252, 0.5);
            box-shadow: inset 0 0 0 1px rgba(125, 211, 252, 0.2);
        }

        hr {
            border: none;
            border-top: 1px solid rgba(148, 163, 184, 0.24);
            margin: 1.1rem 0;
        }

        @media (max-width: 900px) {
            .main .block-container {
                padding: 1rem 1rem 1.5rem 1rem;
            }
            .hero-title { font-size: 2.5rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# CACHED RESOURCE GETTERS
# ==========================================
@st.cache_resource
def get_emotion_detector():
    """Get or initialize emotion detection model."""
    return initialize_emotion_detector()


@st.cache_resource
def get_stress_classifier():
    """Get or initialize stress classifier."""
    return StressClassifier()


@st.cache_resource
def get_response_generator():
    """Get or initialize response generator."""
    return ResponseGenerator()


@st.cache_resource
def get_crisis_detector():
    """Get or initialize crisis detector."""
    return CrisisDetector()


def get_database():
    """Get or initialize mood database (session-scoped)."""
    if "mood_db" not in st.session_state:
        st.session_state["mood_db"] = MoodDatabase()
    return st.session_state["mood_db"]


def is_simple_greeting(user_text):
    """Detect if the user is just saying hello/greeting."""
    text = user_text.lower().strip()
    greetings = [
        "hey", "hi", "hello", "hiya", "heya", "sup", "yo", "hii", "hiii", 
        "hey there", "hi there", "hello there", "good morning", "good evening", 
        "good afternoon", "howdy", "greetings"
    ]
    return text in greetings or text.replace("!", "").replace(".", "").replace("?", "") in greetings


def generate_greeting_response():
    """Generate a warm welcoming response for simple greetings."""
    responses = [
        "Hey there! 👋 I'm MindMate, your emotional support companion. I'm here to listen without judgment. How are you feeling today? Is there something on your mind?",
        
        "Hi! 😊 I'm really glad you're here. I'm MindMate, and I'm here to support you emotionally. What's going on with you today? Want to talk about how you're feeling?",
        
        "Hello! 💙 Thanks for reaching out. I'm MindMate, and I'm here to listen and support you through whatever you're experiencing. How can I help you today? What's on your mind?",
        
        "Hey! 🤗 I'm MindMate. I'm here for you whenever you need to talk about your feelings, stress, or anything weighing on your heart. How are you doing today?",
        
        "Hi there! ✨ I'm MindMate, your mental wellness companion. I'm here to listen, understand, and support you. What's been going on? How are you feeling right now?",
        
        "Hey! 😊 Good to see you here. I'm MindMate, and I'm all about helping you process emotions and feel supported. What would you like to talk about today?",
    ]
    return random.choice(responses)


def generate_boundary_response():
    """Generate a warm but clear boundary-setting response for off-topic requests."""
    # MindMate's identity: warm, emotionally intelligent companion (not medical/technical)
    responses = [
        "Hey, I appreciate you thinking of me, but I'm specifically here to support you emotionally. I can't help with links, technical stuff, or general questions—but I'm all ears if you want to talk about how you're feeling. 💙",
        
        "I hear you, but that's outside my wheelhouse! I'm your emotional companion—think of me as someone to talk to about feelings, stress, anxiety, or whatever's weighing on you. I can't do websites or tech stuff, but I can definitely listen. What's on your mind emotionally?",
        
        "I wish I could help with that, but I'm really designed to be here for your emotions and mental well-being. Links, features, and technical stuff aren't my thing—but talking through feelings, stress, or tough days? That's where I shine. Want to share what's really going on?",
        
        "Ah, I can't help with that kind of request—I'm your emotional support companion, not a search engine or tech assistant. But if something's bothering you, stressing you out, or you just need someone to listen... I'm right here for that. 🤗",
        
        "I'm here for the emotional stuff—feelings, stress, anxiety, whatever's heavy on your heart. I can't do links or technical tasks, but I can absolutely be here to listen and support you through what you're going through. What's really going on?",
        
        "Just so you know—I'm MindMate, your mental health companion. I focus on emotions, stress, and feelings. I don't do diagnoses, links, or tech stuff. But if you need someone to listen? I'm here, and I care. What's weighing on you?",
    ]
    return random.choice(responses)


def process_message(user_text):
    """Run the full MindMate pipeline on user text."""
    try:
        cleaned_text = user_text.strip()
        if not cleaned_text:
            return {
                "conversation_type": "empty",
                "crisis": {"is_crisis": False},
                "emotion": {"emotion": "neutral", "confidence": 1.0, "sentiment": "neutral"},
                "stress": {"level": "low", "score": 0},
                "response": "I'm here with you. Share anything that's on your mind whenever you're ready.",
                "coping": None,
            }

        if is_simple_greeting(cleaned_text):
            return {
                "conversation_type": "casual",
                "crisis": {"is_crisis": False},
                "emotion": {"emotion": "neutral", "confidence": 0.95, "sentiment": "positive"},
                "stress": {"level": "low", "score": 10},
                "response": generate_greeting_response(),
                "coping": None,
            }

        conversation_type = ConversationClassifier.classify_conversation(cleaned_text)
        
        if conversation_type == "informational":
            return {
                "conversation_type": "informational",
                "crisis": {"is_crisis": False},
                "emotion": {"emotion": "neutral", "confidence": 0.8, "sentiment": "neutral"},
                "stress": {"level": "low", "score": 20},
                "response": generate_boundary_response(),
                "coping": None,
            }
        
        if conversation_type == "casual":
            return {
                "conversation_type": "casual",
                "crisis": {"is_crisis": False},
                "emotion": {"emotion": "neutral", "confidence": 0.9, "sentiment": "positive"},
                "stress": {"level": "low", "score": 15},
                "response": ConversationClassifier.get_casual_response(),
                "coping": None,
            }
        
        # Full pipeline for emotional/crisis conversation
        emotion_detector = get_emotion_detector()
        stress_classifier = get_stress_classifier()
        crisis_detector = get_crisis_detector()
        response_generator = get_response_generator()
        mood_db = get_database()
        
        # Run analysis
        crisis_result = crisis_detector.detect_crisis(user_text)
        emotion_result = emotion_detector.detect_emotion(user_text)
        emotion = emotion_result.get("emotion", "neutral")
        confidence = emotion_result.get("confidence", 0.0)
        sentiment = emotion_result.get("sentiment", "neutral")
        
        stress_result = stress_classifier.classify_stress(emotion, confidence, cleaned_text)
        
        # Store in database
        mood_db.add_mood_entry(
            user_input=cleaned_text,
            emotion=emotion,
            emotion_confidence=confidence,
            stress_level=stress_result.get("level"),
            stress_score=stress_result.get("score"),
            sentiment=sentiment,
        )
        
        # Generate response
        response_text = response_generator.generate_response(
            emotion, confidence, stress_result.get("level"), user_text=cleaned_text
        )
        coping = response_generator.get_coping_strategy(emotion, stress_result.get("level"))
        
        return {
            "conversation_type": conversation_type,
            "crisis": crisis_result,
            "emotion": emotion_result,
            "stress": stress_result,
            "response": response_text,
            "coping": coping,
        }
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        return {
            "conversation_type": "error",
            "crisis": {"is_crisis": False},
            "emotion": {"emotion": "neutral", "confidence": 0.5, "sentiment": "neutral"},
            "stress": {"level": "low", "score": 25},
            "response": "I'm here to listen. Thank you for sharing with me.",
            "coping": "Take a moment to breathe deeply.\nReflect on your thoughts.\nReach out to someone you trust.",
        }


def get_emotion_badge(stress_level):
    """Return badge HTML based on stress level."""
    stress = str(stress_level).lower() if stress_level else "low"
    
    if "low" in stress:
        return '<span class="badge-success">😊 Low Stress</span>'
    elif "moderate" in stress or "medium" in stress:
        return '<span class="badge-warning">😐 Moderate Stress</span>'
    else:
        return '<span class="badge-danger">😰 High Stress</span>'


def get_emotion_icon(emotion):
    """Return emoji for emotion."""
    emotion_map = {
        "joy": "😊",
        "happy": "😊",
        "sadness": "😢",
        "sad": "😔",
        "anger": "😠",
        "angry": "😡",
        "fear": "😨",
        "anxious": "😰",
        "anxiety": "😰",
        "neutral": "😐",
        "surprise": "😲",
    }
    return emotion_map.get(emotion.lower(), "🙂")


# ==========================================
# SCREEN 1: WELCOME SCREEN
# ==========================================
def show_welcome_screen():
    """Display redesigned welcome screen."""
    left, right = st.columns([1.2, 1], gap="large")

    with left:
        st.markdown("<span class='pill'>AI Wellness Space</span>", unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>Meet MindMate</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p class='hero-sub'>A calm, private place to talk through emotions, reduce stress, and build healthier mental habits.</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class='glass-panel' style='margin-top: 1rem;'>
                <p style='margin: 0; line-height: 1.75;'>
                    I respond with empathy, practical grounding steps, and emotional clarity.
                    No pressure, no judgment, no noise.<br><br>
                    <strong style='color:#bfdbfe;'>You can start with one line:</strong> “I had a hard day.”
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)
        if st.button("Start With MindMate →", use_container_width=True, key="welcome_btn"):
            st.session_state["current_screen"] = "dashboard"
            st.rerun()

    with right:
        st.markdown(
            """
            <div class='glass-panel' style='text-align:center; min-height: 360px; display:flex; flex-direction:column; justify-content:center;'>
                <div style='font-size: 4.2rem;'>🧠</div>
                <h3 style='margin: 0.4rem 0 0 0; color:#dbeafe;'>Your Emotional Companion</h3>
                <p style='margin: 0.8rem 0 0 0; color:#cbd5e1;'>Track mood • Understand patterns • Feel supported</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==========================================
# SCREEN 2: HOME DASHBOARD
# ==========================================
def show_dashboard():
    """Display redesigned home dashboard."""
    mood_db = get_database()

    st.markdown("<span class='pill'>Dashboard</span>", unsafe_allow_html=True)
    st.markdown("## Your Emotional Snapshot")
    st.markdown("<p style='margin-top:-0.45rem;'>See where you are today and how your week is trending.</p>", unsafe_allow_html=True)

    # Get latest mood entry
    recent_entries = mood_db.get_recent_entries(days=1)
    
    if recent_entries:
        latest = recent_entries[0]
        emotion = latest.get("emotion", "neutral").capitalize()
        stress = latest.get("stress_level", "low").capitalize()
        confidence = latest.get("emotion_confidence", 0)

        st.markdown("<p class='section-title'>Latest Check-in</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"<div class='kpi-card'><p style='font-size:2rem; margin:0;'>{get_emotion_icon(emotion.lower())}</p><p class='kpi-value' style='font-size:1.5rem; margin-top:0.55rem;'>{emotion}</p><p class='kpi-title'>Detected Emotion</p></div>", unsafe_allow_html=True)

        with col2:
            stress_color = "#93c5fd" if stress == "Low" else "#fb923c" if stress == "Moderate" else "#fb7185"
            st.markdown(f"<div class='kpi-card'><p class='kpi-value' style='font-size:1.5rem; color:{stress_color};'>{stress}</p><p class='kpi-title'>Stress Level</p></div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='kpi-card'><p class='kpi-value' style='color:#34d399;'>{int(confidence * 100)}%</p><p class='kpi-title'>Confidence</p></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-panel'><p style='margin:0;'>No mood entries yet. Start a chat and your dashboard will fill automatically.</p></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.7rem;'></div>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>This Week's Stress Trend</p>", unsafe_allow_html=True)
    trends = mood_db.get_stress_trends(days=7)

    if trends:
        trend_df = pd.DataFrame(trends)
        trend_df["date"] = pd.to_datetime(trend_df["date"])
        trend_df = trend_df.sort_values("date")

        fig, ax = plt.subplots(figsize=(10, 3.6), facecolor="#0b1224")
        ax.set_facecolor("#111c35")
        ax.plot(trend_df["date"], trend_df["avg_stress"], color="#60a5fa", linewidth=2.7, marker="o", markersize=5)
        ax.fill_between(trend_df["date"], trend_df["avg_stress"], alpha=0.22, color="#22d3ee")
        ax.set_xlabel("Date", color="#cbd5e1", fontsize=9)
        ax.set_ylabel("Avg Stress", color="#cbd5e1", fontsize=9)
        ax.tick_params(colors="#cbd5e1", labelsize=8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color("#334155")
        ax.spines['bottom'].set_color("#334155")
        ax.grid(True, alpha=0.12, color="#60a5fa")
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.markdown("<div class='glass-panel'><p style='margin:0;'>No trend data yet. Keep checking in to unlock insights.</p></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)
    if st.button("Open Chat Session", use_container_width=True):
        st.session_state["current_screen"] = "chat"
        st.rerun()


# ==========================================
# SCREEN 3: CHAT INTERFACE
# ==========================================
def show_chat_interface():
    """Display ChatGPT-style chat interface with history, suggestions, and coping strategies."""

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    st.markdown("<span class='pill'>Conversation</span>", unsafe_allow_html=True)
    st.markdown("## Talk Freely")
    st.markdown("<p style='margin-top:-0.4rem;'>Type what you're feeling. MindMate listens and responds gently.</p>", unsafe_allow_html=True)

    # Chat history area
    if st.session_state["chat_history"]:
        st.markdown("<div style='max-height: 480px; overflow-y: auto;'>", unsafe_allow_html=True)
        for chat in st.session_state["chat_history"]:
            result = chat.get("result", {})

            if result.get("crisis", {}).get("is_crisis"):
                st.markdown('<div class="crisis-alert">', unsafe_allow_html=True)
                st.markdown("### ⚠️ Crisis Support Alert")
                st.markdown(result["crisis"]["message"])
                st.markdown('</div>', unsafe_allow_html=True)

            # User message
            st.markdown(
                f'<div class="user-msg">'
                f'<div class="user-msg-bubble">{chat["user"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Bot response
            emotion = result.get("emotion", {})
            stress = result.get("stress", {})
            emotion_name = emotion.get("emotion", "neutral").capitalize()
            stress_level = stress.get("level", "low").capitalize()
            conversation_type = result.get("conversation_type", "emotional")
            bot_text = result.get("response", "")

            if conversation_type == "emotional":
                metadata = f'<span style="font-size: 0.75rem; color: #93c5fd; opacity: 0.8;">Emotion: {emotion_name} • Stress: {stress_level}</span><br><br>'
            else:
                metadata = ""

            st.markdown(
                f'<div class="bot-msg">'
                f'<div class="bot-msg-bubble">'
                f'<strong style="color: #7dd3fc;">MindMate</strong> ✓<br>'
                f'{metadata}'
                f'{bot_text}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Coping strategies
            if result.get("coping"):
                st.markdown('<div class="coping-strategy">', unsafe_allow_html=True)
                coping = result["coping"]

                if isinstance(coping, dict):
                    st.markdown(f"### 💡 {coping.get('technique_name', 'Coping Strategy')}")
                    st.markdown(coping.get('instructions', ''))
                    if coping.get('affirmation'):
                        st.markdown(f"*{coping['affirmation']}*")
                    if coping.get('tip'):
                        st.markdown(coping['tip'])
                else:
                    st.markdown("### 💡 Suggestions")
                    st.markdown(str(coping))

                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Suggestion buttons only on first load
        st.markdown(
            "<p style='font-size: 0.86rem; text-transform: uppercase; letter-spacing: 0.09em; color:#93c5fd; text-align:center; margin-bottom:0.8rem;'>Try a prompt</p>",
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2, gap="small")
        with col1:
            if st.button("💭 How are you feeling today?", key="sug1", use_container_width=True):
                st.session_state["suggested_input"] = "I want to talk about how I'm feeling today"
                st.session_state["auto_submit_message"] = "I want to talk about how I'm feeling today"
                st.rerun()

            if st.button("😰 I'm feeling stressed", key="sug2", use_container_width=True):
                st.session_state["suggested_input"] = "I'm feeling really stressed and overwhelmed"
                st.session_state["auto_submit_message"] = "I'm feeling really stressed and overwhelmed"
                st.rerun()

        with col2:
            if st.button("😔 I'm feeling sad", key="sug3", use_container_width=True):
                st.session_state["suggested_input"] = "I've been feeling sad lately"
                st.session_state["auto_submit_message"] = "I've been feeling sad lately"
                st.rerun()

            if st.button("😊 Something positive to share", key="sug4", use_container_width=True):
                st.session_state["suggested_input"] = "I want to share something good that happened"
                st.session_state["auto_submit_message"] = "I want to share something good that happened"
                st.rerun()

    # Check if we should auto-submit a suggestion
    auto_submit_message = None
    if "auto_submit_message" in st.session_state and st.session_state["auto_submit_message"]:
        auto_submit_message = st.session_state.pop("auto_submit_message")

    # Compact input area at bottom
    st.markdown(
        """
        <style>
            .chat-input-wrapper {
                margin-top: 1.2rem;
                padding-top: 0.8rem;
                border-top: 1px solid rgba(148, 163, 184, 0.2);
            }
        </style>
        <div class='chat-input-wrapper'></div>
        """,
        unsafe_allow_html=True,
    )

    with st.form(key="chat_form", clear_on_submit=True):
        default_value = st.session_state.pop("suggested_input", "")

        st.markdown("<div class='chat-inline-row'>", unsafe_allow_html=True)
        col_input, col_send = st.columns([30, 1], gap="small")

        with col_input:
            user_input = st.text_input(
                "Message",
                value=default_value,
                placeholder="Tell me what's on your mind...",
                label_visibility="collapsed",
            )

        with col_send:
            send_clicked = st.form_submit_button("➤", use_container_width=False, help="Send message")

        st.markdown("</div>", unsafe_allow_html=True)

    # Process auto-submitted suggestion
    if auto_submit_message:
        with st.spinner("🧠 MindMate is thinking..."):
            try:
                result = process_message(auto_submit_message)
                st.session_state["chat_history"].append({
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "user": auto_submit_message,
                    "result": result,
                })
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
                logger.error(f"Chat error: {str(e)}")

    user_message = user_input.strip()
    if send_clicked and user_message:
        with st.spinner("🧠 MindMate is thinking..."):
            try:
                result = process_message(user_message)
                st.session_state["chat_history"].append({
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "user": user_message,
                    "result": result,
                })
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
                logger.error(f"Chat error: {str(e)}")


# ==========================================
# SCREEN 4: MOOD ANALYTICS
# ==========================================
def show_analytics():
    """Display redesigned mood analytics."""
    mood_db = get_database()

    st.markdown("<span class='pill'>Insights</span>", unsafe_allow_html=True)
    st.markdown("## Pattern Analytics")
    st.markdown("<p style='margin-top:-0.4rem;'>A clearer picture of mood and stress over the past 7 days.</p>", unsafe_allow_html=True)

    # Summary Stats
    summary = mood_db.get_stress_summary(days=7)
    
    if summary:
        st.markdown("<p class='section-title'>Weekly Stats</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class='kpi-card'>
                <p class='kpi-value' style='color:#93c5fd;'>{summary.get("entry_count", 0)}</p>
                <p class='kpi-title'>Check-ins</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='kpi-card'>
                <p class='kpi-value' style='color:#fdba74;'>{summary.get("average_stress", 0):.0f}</p>
                <p class='kpi-title'>Avg Stress</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class='kpi-card'>
                <p class='kpi-value' style='color:#fda4af;'>{summary.get("peak_stress", 0):.0f}</p>
                <p class='kpi-title'>Peak Stress</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.7rem;'></div>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>Stress Trend</p>", unsafe_allow_html=True)
    trends = mood_db.get_stress_trends(days=7)
    if trends:
        trend_df = pd.DataFrame(trends)
        trend_df["date"] = pd.to_datetime(trend_df["date"])
        trend_df = trend_df.sort_values("date")

        fig, ax = plt.subplots(figsize=(10, 4), facecolor="#0b1224")
        ax.set_facecolor("#111c35")
        ax.fill_between(trend_df["date"], trend_df["avg_stress"], alpha=0.26, color="#60a5fa")
        ax.plot(trend_df["date"], trend_df["avg_stress"], color="#22d3ee", linewidth=2.8, marker="o", markersize=7)

        ax.set_xlabel("Date", color="#cbd5e1", fontsize=10)
        ax.set_ylabel("Stress Level", color="#cbd5e1", fontsize=10)
        ax.tick_params(colors="#cbd5e1")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#334155')
        ax.spines['bottom'].set_color('#334155')
        ax.grid(True, alpha=0.14, color='#60a5fa')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.markdown("<div class='glass-panel'><p style='margin:0;'>No data yet. Start chatting to unlock your trend report.</p></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.7rem;'></div>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>Emotion Distribution</p>", unsafe_allow_html=True)
    distribution = mood_db.get_emotion_distribution(days=7)
    if distribution:
        fig, ax = plt.subplots(figsize=(8, 5), facecolor="#0b1224")
        ax.set_facecolor("#111c35")

        labels = list(distribution.keys())
        sizes = list(distribution.values())
        colors = ['#60a5fa', '#34d399', '#fda4af', '#fdba74', '#a78bfa', '#22d3ee']

        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                           colors=colors[:len(labels)], startangle=90)

        for text in texts:
            text.set_color('#dbeafe')
            text.set_fontsize(10)

        for autotext in autotexts:
            autotext.set_color('#0f172a')
            autotext.set_fontweight('bold')

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.markdown("<div class='glass-panel'><p style='margin:0;'>No emotion data yet.</p></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:0.7rem;'></div>", unsafe_allow_html=True)
    if summary:
        st.markdown("<p class='section-title'>This Week's Summary</p>", unsafe_allow_html=True)

        if summary.get('average_stress', 0) < 30:
            status = "<div class='glass-panel' style='border-color: rgba(52, 211, 153, 0.5);'><p style='color:#86efac; margin:0; font-weight:700;'>Great work. Your average stress is in a healthy zone.</p></div>"
        elif summary.get('average_stress', 0) < 60:
            status = "<div class='glass-panel' style='border-color: rgba(251, 146, 60, 0.55);'><p style='color:#fdba74; margin:0; font-weight:700;'>Stress is moderate. Small daily recovery rituals can help.</p></div>"
        else:
            status = "<div class='glass-panel' style='border-color: rgba(251, 113, 133, 0.55);'><p style='color:#fda4af; margin:0; font-weight:700;'>Stress is elevated. Prioritize rest and reach out for support if needed.</p></div>"

        st.markdown(status, unsafe_allow_html=True)


# ==========================================
# NAVIGATION BAR
# ==========================================
def show_navigation():
    """Display vertical navigation sidebar."""
    with st.sidebar:
        current_screen = st.session_state.get("current_screen", "dashboard")

        st.markdown(
            """
            <div style='text-align: center; padding: 0.8rem 0 1rem 0;'>
                <div style='font-size: 2.6rem;'>🧠</div>
                <h2 style='margin: 0.3rem 0 0 0; color: #bfdbfe; font-size: 1.35rem;'>MindMate</h2>
                <p style='margin: 0.3rem 0 0 0; font-size: 0.78rem; color: #94a3b8;'>Mental Wellness Companion</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<p style='font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; color:#93c5fd; margin:0.6rem 0 0.4rem 0;'>Navigate</p>", unsafe_allow_html=True)

        # Navigation menu
        nav_items = [
            ("🏠 Home", "dashboard"),
            ("💬 Chat", "chat"),
            ("📊 Stats", "analytics"),
        ]
        
        for label, screen_id in nav_items:
            is_active = current_screen == screen_id
            button_label = f"{label} •" if is_active else label
            
            if st.button(button_label, use_container_width=True, key=f"nav_{screen_id}"):
                st.session_state["current_screen"] = screen_id
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style='text-align: center; padding: 0.5rem 0; color: #94a3b8; font-size: 0.74rem;'>
                <p style='margin: 0;'>Always here, always listening.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==========================================
# MAIN APP LOGIC
# ==========================================
def main():
    """Main application entry point."""
    load_modern_css()
    
    # Initialize session state
    if "current_screen" not in st.session_state:
        st.session_state["current_screen"] = "welcome"
    
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    
    # Route to appropriate screen
    current_screen = st.session_state["current_screen"]
    
    if current_screen == "welcome":
        show_welcome_screen()
    else:
        # Show navigation for all other screens
        show_navigation()
        
        if current_screen == "dashboard":
            show_dashboard()
        elif current_screen == "chat":
            show_chat_interface()
        elif current_screen == "analytics":
            show_analytics()


if __name__ == "__main__":
    main()

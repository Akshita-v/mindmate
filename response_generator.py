"""
Response Generator and Coping Strategy Engine

Generates empathetic, emotion-appropriate responses and coping strategies
based on detected emotion and stress level.
"""

import random
import logging

logger = logging.getLogger(__name__)


# ==========================================
# CONVERSATION TYPE CLASSIFIER
# ==========================================

class ConversationClassifier:
    """Classifies the type of conversation before emotion detection."""
    
    # Casual/small talk patterns
    CASUAL_PATTERNS = [
        "hi", "hey", "hello", "good morning", "good evening", "good night",
        "how are you", "how ru", "how r u", "wassup", "what's up", "whats up",
        "sup", "how's it going", "hows it going", "how do you do",
        "nice to meet you", "thanks", "thank you", "bye", "goodbye", "see you",
        "ok", "okay", "cool", "nice", "great", "awesome",
    ]
    
    # Emotional/therapy indicators
    EMOTIONAL_PATTERNS = [
        "feel", "feeling", "felt", "emotion", "mood", "sad", "happy", "angry",
        "anxious", "anxiety", "stress", "stressed", "worry", "worried", "scared",
        "afraid", "fear", "depressed", "depression", "lonely", "alone", "hurt",
        "pain", "suffering", "struggling", "difficult", "hard time", "overwhelm",
        "exhausted", "tired", "burnout", "frustrated", "upset", "crying", "cry",
        "hate myself", "worthless", "hopeless", "helpless", "lost", "confused",
        "broken", "empty", "numb", "panic", "nervous", "tense", "guilt", "shame",
        "regret", "disappointed", "grief", "miss", "love", "heartbreak", "rejected",
    ]
    
    # Crisis keywords (highest priority)
    CRISIS_PATTERNS = [
        "kill myself", "suicide", "want to die", "end it all", "ending my life",
        "don't want to live", "better off dead", "hurt myself", "self harm",
        "cut myself", "cutting", "overdose", "jump off", "gun", "pills",
    ]
    
    # Informational request patterns
    INFORMATIONAL_PATTERNS = [
        "link", "website", "url", "search", "google", "find me", "look up",
        "what is", "who is", "when did", "where is", "define", "meaning of",
        "how to", "can you add", "add feature", "implement", "build",
        "weather", "news", "time", "date", "calculate", "math",
        "translate", "buy", "purchase", "order", "shop",
    ]
    
    @staticmethod
    def classify_conversation(user_text: str) -> str:
        """
        Classify the conversation type.
        
        Args:
            user_text: User's input message
            
        Returns:
            str: "crisis" | "emotional" | "casual" | "informational"
        """
        if not user_text or len(user_text.strip()) < 2:
            return "casual"
        
        text = user_text.lower().strip()
        
        # 1. Crisis check (highest priority)
        if any(pattern in text for pattern in ConversationClassifier.CRISIS_PATTERNS):
            return "crisis"
        
        # 2. Informational request check
        # Only flag as informational if no emotional context
        has_emotional_words = any(pattern in text for pattern in ConversationClassifier.EMOTIONAL_PATTERNS)
        if not has_emotional_words and any(pattern in text for pattern in ConversationClassifier.INFORMATIONAL_PATTERNS):
            return "informational"
        
        # 3. Emotional/therapy mode check
        if any(pattern in text for pattern in ConversationClassifier.EMOTIONAL_PATTERNS):
            return "emotional"
        
        # 4. Casual/small talk check
        if any(pattern in text for pattern in ConversationClassifier.CASUAL_PATTERNS):
            # But if message is long or has depth, might still be emotional
            if len(text) > 50 and not any(casual in text for casual in ["how are you", "how ru", "hi", "hey", "hello"]):
                return "emotional"  # Long message likely has substance
            return "casual"
        
        # 5. Default: if uncertain, treat as emotional (safer for mental health app)
        return "emotional"
    
    @staticmethod
    def get_casual_response() -> str:
        """Generate casual, friendly responses for small talk."""
        responses = [
            "Hey there! I'm doing well, thanks for asking. How about you—how's your day going? 😊",
            "Hi! Good to hear from you. I'm here and ready to listen. What's on your mind today?",
            "Hello! I'm doing great, thanks! More importantly, how are you feeling? What brings you here?",
            "Hey! Thanks for checking in. I'm good! But I'm curious—how are *you* really doing?",
            "Hi there! I'm here and happy to chat. How's everything going in your world?",
            "Hello! I appreciate you reaching out. I'm well! What's going on with you today?",
        ]
        return random.choice(responses)


class ResponseGenerator:
    """
    Generates emotion-appropriate therapeutic responses with deep empathy.
    Uses evidence-based therapeutic techniques and active listening.
    """
    
    # MindMate's Core Personality & Identity
    PERSONALITY = """
    You are MindMate, a warm, emotionally intelligent mental health companion.
    You speak gently, calmly, and empathetically.
    You do NOT give medical diagnoses.
    You focus on listening and emotional support.
    You respond like a kind therapist who's also a friend.
    You set boundaries kindly when asked about non-emotional topics.
    """
    
    # Conversational starters to make responses feel natural and human
    STARTERS = [
        "I hear you. ",
        "Oh, I see... ",
        "Thanks for sharing that with me. ",
        "That sounds like a lot to carry. ",
        "I'm listening. ",
        "I'm right here with you. ",
        "Okay, let me sit with this for a moment... ",
        "I really appreciate you opening up. ",
        "You know what? ",
        "Hey, first off—",
        "I want you to know something. ",
        "Can I be honest with you? ",
        "Here's what I'm picking up on... ",
        "Let me tell you what I'm sensing. ",
    ]
    
    # Friend-like follow-up questions that feel conversational
    FRIEND_FOLLOW_UPS = [
        "What's the hardest part of this right now?",
        "Do you feel like you've been carrying this for a while?",
        "If you could change one small thing about today, what would it be?",
        "I'm here for as long as you need to vent. What else is on your mind?",
        "Has this been building up, or did something specific happen?",
        "What would make today feel just a little bit easier?",
        "How long have you been feeling this way?",
        "Is there something you've been wanting to say but haven't been able to?",
        "What's the first thing that comes to mind when you think about this?",
        "If you could tell someone exactly how you feel, what would you say?",
        "What do you need most right now—someone to listen, or advice, or just space?",
        "When's the last time you felt okay? Like, truly okay?",
    ]
    
    # Empathetic, therapeutic responses for each emotion
    EMOTION_RESPONSES = {
        'sadness': [
            "I hear you, and I want you to know that what you're feeling is completely valid. Sadness is your heart's honest response to something that matters to you. 💙",
            "Thank you for trusting me with this. It takes real courage to sit with sadness instead of running from it. That's actually a sign of emotional strength.",
            "I can sense the weight you're carrying right now. Please know that these feelings, as painful as they are, are temporary and you don't have to feel this way alone.",
            "Sadness often tells us something important—that we care deeply about something or someone. Your sadness reflects your capacity for love and connection.",
            "I'm here with you in this moment. Your feelings matter, and there's no timeline for healing. What you're going through is real, and so is your resilience.",
        ],
        'anxiety': [
            "What you're experiencing makes sense. Anxiety is your mind trying to protect you, even when the threat isn't real. That shows how much you care and how aware you are. Let's work through this together. 🌿",
            "Your anxiety is telling you something matters to you. Instead of fighting it, let's understand what it's trying to say. You're safe, and we can navigate this.",
            "I want you to know that the thoughts anxiety brings aren't predictions—they're just possibilities your mind is considering. You're more capable than anxiety tells you.",
            "Many people feel what you're feeling right now. You're not broken or weak—you're human. Your nervous system is just working overtime, and we can help calm it.",
            "Anxiety loves certainty, but life is uncertain—and guess what? You've handled uncertainty before. You have more strength than you realize.",
        ],
        'anger': [
            "Your anger is real, and it's important. It's telling you that a boundary has been crossed or something unfair has happened. Let's listen to what it's trying to say. 💪",
            "I respect your feelings right now. Anger, when understood, can be a powerful force for positive change. Let's channel this energy constructively.",
            "It sounds like you've reached your limit, and that's okay. Sometimes anger is the only appropriate response. The question is: what do you need right now?",
            "Behind anger is often pain, disappointment, or feeling unheard. I'm listening now. What would help you feel understood and respected?",
            "You have every right to feel frustrated. Rather than judge your anger, let's explore what it's protecting—what matters so much that this crossed the line?",
        ],
        'fear': [
            "Fear is your mind trying to protect you, and I honor that. But I also want you to know you're stronger than your fears. Let's face this together. 🤝",
            "What you're afraid of feels very real right now, and that's significant. Fear can feel overwhelming, but it always passes. You've survived every difficult moment so far.",
            "I want to help you build confidence in your ability to handle whatever comes. Fear often diminishes when we stop running from it and start understanding it.",
            "Your fear is telling you that something matters deeply to you. That's not weakness—that's proof of how much you care. We can work with that.",
            "Many people feel afraid of what you're facing. You're not alone, and there are ways to move through this that honor both your concerns and your courage.",
        ],
        'stress': [
            "I can sense how much you're carrying right now. You don't have to do it all at once, and you don't have to do it alone. Let's find what needs your attention first. 🌿",
            "Stress is a sign you care about things and people. While that's beautiful, it also means you might benefit from slowing down and being gentler with yourself.",
            "Your nervous system is working hard to keep up. Let's give it some relief. Small actions can create big shifts in how you feel.",
            "Sometimes stress is a signal that something needs to change—your boundaries, your priorities, or your approach. What would give you the most relief right now?",
            "You're doing better than you think you are. Stress can cloud our perception. Let's focus on what you're actually managing and what support would help.",
        ],
        'joy': [
            "This is beautiful! You deserve to feel this good. Joy is a gift—savor it and let it fill you completely. ✨",
            "Your happiness brightens not just your own world, but the world around you. Never underestimate the power of your joy.",
            "I'm genuinely happy for you. This moment of joy is proof of your capacity for happiness and resilience. Hold onto this feeling.",
            "What you're experiencing right now is important. These moments of joy are reminders of what's possible and what you're capable of creating.",
            "Your positive energy is inspiring. Keep trusting that good things happen, because clearly, they do!",
        ],
        'disgust': [
            "Your reaction makes sense. Disgust is often your values or boundaries signaling that something isn't right. What's crossing the line for you?",
            "You have good instincts. That feeling of disgust is your integrity speaking. It's worth listening to and understanding.",
            "It sounds like something has violated your sense of what's right or acceptable. That matters. Let's understand what boundary needs protecting.",
        ],
        'surprise': [
            "That's quite unexpected! Give yourself a moment to process. Surprises can shift our world, and it takes time to adjust. How are you really feeling about this?",
            "Unexpected things can feel unsettling. Take your time processing this. Your feelings about it are completely valid, whatever they are.",
            "That's a lot to take in. Surprise often leaves us feeling a bit off-balance. What would help you feel grounded again?",
        ],
        'neutral': [
            "Hey! I'm doing well, thanks for asking. More importantly though—how are *you* doing? Like, really doing?",
            "I appreciate you checking in! I'm here and ready to listen. But let's talk about you—what's going on in your world today?",
            "You know, I'm just here doing what I do—being present. But I'm way more interested in how you're feeling. What's on your mind?",
            "Thanks for asking! I'm good. But I want to hear about you—what brings you here? How's your day treating you?",
            "I'm here and listening. More importantly, how are you holding up? What's the real story behind that question?",
            "That's sweet of you to ask! I'm alright. But seriously, how are *you*? What's been on your heart lately?",
        ]
    }
    
    # Grounding and breathing techniques
    COPING_STRATEGIES = {
        'anxiety': {
            'technique_name': '4-7-8 Calming Breath (Proven Anxiety Relief)',
            'instructions': """
            **Why this works:** This ancient breathing technique signals your nervous system that you're safe.
            
            **4-7-8 Breathing (2-3 minutes)**:
            1. Exhale completely through your mouth
            2. Close your mouth, inhale through nose for 4 counts
            3. Hold your breath for 7 counts
            4. Exhale completely through mouth for 8 counts (audible exhale helps)
            5. Repeat 4-5 times
            
            Notice how your body feels more relaxed with each cycle.
            """,
            'affirmation': "I am safe in this moment. My breath is my anchor. I choose calm over worry. 🌬️",
            'tip': "Practice this 2-3 times daily, even when you're not anxious, so it becomes a tool you trust."
        },
        'anger': {
            'technique_name': 'Compassionate Anger Release (Transform Anger)',
            'instructions': """
            **Why this works:** Anger needs expression and understanding, not suppression.
            
            **Releasing Anger Constructively (5-10 minutes)**:
            1. Sit somewhere private where you can express yourself
            2. Journal or write out: "I'm angry because..." - let it all out without filtering
            3. Identify the deeper need: What boundary was crossed? What's unfair?
            4. Ask: "What does my anger want me to protect?" 
            5. Write one thing you can do to honor that need
            6. Practice compassion: Even those who angered us have struggles
            
            This transforms anger from destruction into power for positive change.
            """,
            'affirmation': "My anger is valid. I use it wisely. I choose to respond, not react. 💪",
            'tip': "Anger is information. Instead of judging it, ask what it's trying to protect."
        },
        'sadness': {
            'technique_name': '5-4-3-2-1 Grounding Exercise (Return to Present)',
            'instructions': """
            **Why this works:** Sadness often shows us memories. This brings you back to safety now.
            
            **Grounding Through Your Senses (3-5 minutes)**:
            1. Notice 5 things you can SEE - describe colors, shapes, details
            2. Notice 4 things you can TOUCH - textures, temperatures, sensations
            3. Notice 3 things you can HEAR - sounds near and far
            4. Notice 2 things you can SMELL - or pause to appreciate the scent of your surroundings
            5. Notice 1 thing you can TASTE - or savor a flavor
            
            Each sense brings you into THIS moment, which is safe.
            """,
            'affirmation': "This pain is temporary. I am safe here, now. I will feel better. 💙",
            'tip': "Use this whenever sadness feels overwhelming. Grounding works when everything else feels too much."
        },
        'fear': {
            'technique_name': 'Progressive Muscle Relaxation (Build Courage)',
            'instructions': """
            **Why this works:** Fear creates tension. Relaxing your body relaxes your mind.
            
            **Full Body Relaxation (5-7 minutes)**:
            1. Tense your toes and feet for 3 seconds, then release - notice the relief
            2. Move to calves, thighs, then your whole legs
            3. Clench your stomach, then soften - feel it relax
            4. Make fists, tense arms, then release
            5. Shrug shoulders to your ears, then drop them - ahhhh
            6. Make a face (squint, purse lips), then relax - smile gently
            
            Your body learning to relax teaches your mind it's safe.
            """,
            'affirmation': "I have handled difficulty before. I am more capable than my fears. I am safe. 🌿",
            'tip': "Do this at night to sleep better, or whenever fear tightens your chest."
        },
        'stress': {
            'technique_name': 'Mindfulness Reset (Reduce Overwhelm)',
            'instructions': """
            **Why this works:** Stress pulls you into future worries. Mindfulness anchors you in now.
            
            **Mindful Breathing & Presence (5-10 minutes)**:
            1. Sit somewhere comfortable, no distractions
            2. Close your eyes or soften your gaze
            3. Breathe naturally: in through nose, out through mouth
            4. Focus on one word: "in" (inhale), "out" (exhale)
            5. When your mind wanders (it will!), gently return to breath - no judgment
            6. Practice this daily, even just 5 minutes
            
            This trains your brain to focus on what you can control (your breath) not what you can't.
            """,
            'affirmation': "I am present. I am whole. I am doing enough. This moment is enough. 🧘",
            'tip': "Start with 2 minutes if 5 feels hard. The practice compounds over days."
        },
        'default': {
            'technique_name': 'Compassionate Self-Soothing (For Whenever You Need It)',
            'instructions': """
            **Why this works:** Self-compassion is powerful medicine for emotional pain.
            
            **Self-Soothing Technique (3-5 minutes)**:
            1. Place your hand on your heart - feel it beating (you're alive!)
            2. Speak to yourself like you'd speak to a dear friend in pain
            3. Say: "This is really hard right now. And I'm doing the best I can."
            4. Say: "Others feel this way too. I'm not alone in this."
            5. Say: "May I be kind to myself. May I be patient with myself."
            6. Take three deep, comforting breaths
            
            You deserve your own kindness most, especially in hard moments.
            """,
            'affirmation': "I am worthy of my own compassion. I am doing better than I think. You've got this. ✨",
            'tip': "This works for any emotion—it's a universal practice of self-compassion."
        }
    }
    
    # Study/productivity advice based on stress
    PRODUCTIVITY_TIPS = [
        "Take a 5-10 minute break from studying. Walk around, stretch, get some water.",
        "Try the Pomodoro technique: 25 min focus + 5 min break. Repeat 4 times, then take longer break.",
        "Switch your study location. Sometimes a change of scenery helps reset your mind.",
        "Break your work into smaller chunks. Small wins build momentum!",
        "Make sure you're hydrated and have eaten something healthy. Your brain works better.",
        "Step outside for 5 minutes. Fresh air and sunlight boost mood and focus.",
        "Put your phone in another room. Reduce distractions to improve focus.",
        "Talk to someone about what's stressing you. Sometimes just sharing helps.",
    ]
    
    def __init__(self):
        """Initialize the response generator."""
        self.logger = logging.getLogger(__name__)
    
    def _normalize_stress_level(self, stress_level):
        if not stress_level:
            return ""
        normalized = str(stress_level).strip().lower()
        if normalized == "medium":
            return "moderate"
        return normalized

    def _extract_context_hint(self, user_text):
        """Extract context clues for more personalized responses."""
        if not user_text:
            return ""

        text = user_text.lower()
        
        # Academic/work stress - more conversational
        if any(word in text for word in ["exam", "test", "study", "school", "class", "homework", "assignment"]):
            return "Academic pressure is real, and I can tell it's weighing on you. Just so you know? Your grades don't define who you are or what you're capable of."
        
        if any(word in text for word in ["work", "job", "boss", "deadline", "office", "meeting", "coworker"]):
            return "Work stress can feel all-consuming, especially when you're juggling a lot. But your job—however important—doesn't determine your worth as a person."
        
        # Relationships - friend-like tone
        if any(word in text for word in ["family", "parents", "mom", "dad", "sibling", "home"]):
            return "Family stuff is complicated. Like, really complicated. The people closest to us can stir up the deepest emotions. What you're feeling makes total sense."
        
        if any(word in text for word in ["relationship", "partner", "boyfriend", "girlfriend", "dating", "breakup", "love", "divorce"]):
            return "Relationship issues hit different, don't they? They touch the heart in ways that are hard to put into words. These feelings are big, and they're real."
        
        # Health/body - conversational empathy
        if any(word in text for word in ["health", "sick", "pain", "disease", "illness", "doctor", "hospital", "mental health"]):
            return "Health worries are heavy. They affect everything—your body, your mind, your whole life. What you're feeling is completely valid."
        
        if any(word in text for word in ["sleep", "tired", "insomnia", "exhausted", "fatigue", "rest"]):
            return "Sleep deprivation makes everything ten times harder. Your exhaustion is real, and it's your body telling you something needs to shift."
        
        # Financial - warm but real
        if any(word in text for word in ["money", "rent", "bills", "debt", "financial", "afford", "poor"]):
            return "Money stress is one of those deep, gut-level worries that affects everything. What you're dealing with is real, and it's heavy."
        
        # Loss and grief - gentle and present
        if any(word in text for word in ["loss", "lost", "died", "death", "grief", "miss you", "gone", "goodbye"]):
            return "I'm so sorry. Grief is love with nowhere to go. Your pain is real, and it's a reflection of how much that person meant to you."
        
        # Self-doubt - direct but compassionate
        if any(word in text for word in ["useless", "failure", "stupid", "dumb", "pathetic", "worthless", "loser"]):
            return "Hey, you're being really hard on yourself right now. Those harsh words? That's pain talking, not truth. You're not what your inner critic says you are."
        
        # Loneliness - validating and normalizing
        if any(word in text for word in ["alone", "lonely", "isolated", "nobody", "no one understands", "invisible"]):
            return "Loneliness is one of the hardest things to sit with. It's more common than you'd think, and it's also one of the most valid feelings. Your need for connection is deeply human."
        
        # Pressure/overwhelm - gentle reality check
        if any(word in text for word in ["pressure", "overwhelm", "too much", "can't handle", "breaking", "collapse"]):
            return "You're sensing you're at your limit—and that awareness? That's actually important. You need support, and reaching out like this is a strong first step."

        return ""

    def _follow_up_question(self, emotion):
        """Generate therapeutic follow-up questions using active listening."""
        questions = {
            "sadness": "It sounds like your heart is carrying something heavy. What's the deepest part of what you're feeling right now?",
            "anxiety": "Your mind seems to be jumping ahead. What's the worst thing you're worried might happen? Let's look at that together.",
            "anger": "Beneath the anger, I sense something important. What boundary of yours was crossed? What do you need to happen?",
            "fear": "Fear tries to keep us small. Looking back at your life, what's a time you felt scared but got through it anyway?",
            "stress": "You're carrying a lot. If you could put down just one thing right now, what would give you the most relief?",
            "joy": "This is beautiful. What would help you hold onto this feeling? How can we protect this space of joy?",
            "disgust": "Your gut is telling you something. What value or boundary feels violated here?",
            "surprise": "That's unexpected. How does this shift things for you? What do you need to process this?",
            "neutral": "Sometimes neutral is where we pause. What brought you here today? What's underneath?",
        }
        return questions.get(emotion, questions["neutral"])

    def generate_response(self, emotion, confidence, stress_level, user_text=""):
        """
        Generate a detailed, personalized response based on emotion.
        Uses active listening, validation, and therapeutic principles.
        Now with conversational, friend-like tone.
        
        Args:
            emotion (str): Detected emotion label
            confidence (float): Confidence score (0-1)
            stress_level (str): Low, Moderate, or High
            user_text (str): Original user message
        
        Returns:
            str: Empathetic therapeutic response message
        """
        try:
            # 1. Pick a conversational starter to sound human
            prefix = random.choice(self.STARTERS)
            
            # 2. Get the core empathetic message
            responses = self.EMOTION_RESPONSES.get(emotion, self.EMOTION_RESPONSES["neutral"])
            base_response = random.choice(responses)

            stress = self._normalize_stress_level(stress_level)
            context_hint = self._extract_context_hint(user_text)
            
            # Build the response conversationally
            lines = [
                f"{prefix}{base_response}",
                ""  # Spacing
            ]

            # Add context-specific insights (conversational tone)
            if context_hint:
                lines.append(context_hint)
                lines.append("")

            # Validation and psychoeducation (friend-like)
            if emotion in ['anxiety', 'fear']:
                lines.append("Your brain's just trying to protect you, you know? It's doing its job—maybe a bit too well. That's not a flaw. We just need to help it calm down a bit.")
            elif emotion == 'anger':
                lines.append("Anger gets a bad rap, but honestly? It's telling you something important. Something you value is being threatened. That's worth paying attention to.")
            elif emotion == 'sadness':
                lines.append("Sadness isn't weakness—it's proof you care deeply about something. That's actually beautiful, even though it hurts right now.")
            elif emotion == 'stress':
                lines.append("Stress usually means you're trying to do too much because you care about everything. That's admirable, but you can't pour from an empty cup, you know?")

            lines.append("")

            # Address confidence if low (more conversational)
            if confidence is not None and confidence < 0.5:
                lines.append("*Just so you know—I might be reading this wrong. If I'm off base, please tell me. Your truth is what matters here.*")
                lines.append("")

            # Stress-specific guidance (friend-like tone)
            if stress in ["high", "moderate", "medium"]:
                lines.append("Listen, you don't have to solve everything today. Or even this week. One small step—that's all you need right now. That's more than enough.")
                lines.append("")

            if stress == "high":
                lines.append("Real talk? When stress is this high, your brain literally can't think straight. So give yourself permission to just... pause. Rest isn't giving up. It's resetting.")
                lines.append("")

            # 3. Add friend-like follow-up question as natural suffix
            friend_question = random.choice(self.FRIEND_FOLLOW_UPS)
            lines.append(friend_question)
            lines.append("")

            # Supportive closure - more conversational
            if confidence is not None and confidence > 0.8:
                if stress in ["high", "moderate"]:
                    lines.append("And hey—if you feel like you need to talk to someone face-to-face, there's no shame in that. A friend, a counselor, someone who gets it... sometimes that's exactly what we need. You're worth that support.")
                else:
                    lines.append("I see you showing up for yourself right now, and that takes strength. Keep going. 💙")

            return "\n".join(lines)
        
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return "I'm here to listen and understand. Your feelings matter. What's on your heart right now?"
    
    def get_coping_strategy(self, emotion, stress_level):
        """
        Get a therapeutic coping strategy based on emotion and stress.
        Includes evidence-based techniques and empowering affirmations.
        
        Args:
            emotion (str): Detected emotion
            stress_level (str): Low, Moderate, or High
        
        Returns:
            dict: {
                'technique_name': str,
                'instructions': str,
                'affirmation': str,
                'tip': str
            }
        """
        try:
            # Select strategy based on emotion
            if emotion in ['anxiety', 'fear']:
                strategy = self.COPING_STRATEGIES.get('anxiety')
            elif emotion == 'anger':
                strategy = self.COPING_STRATEGIES.get('anger')
            elif emotion == 'sadness':
                strategy = self.COPING_STRATEGIES.get('sadness')
            elif emotion == 'stress':
                strategy = self.COPING_STRATEGIES.get('stress')
            else:
                strategy = self.COPING_STRATEGIES.get('default')
            
            # Add stress-level specific advice
            stress_tips = {
                'High': "\n\n**Priority Right Now:** Focus on one thing only. Everything else can wait. Your nervous system needs a reset above all else.",
                'Moderate': "\n\n**Consider:** Building these practices into your daily routine will prevent stress from escalating further.",
                'Low': "\n\n**Pro Tip:** Using these techniques now will make them feel natural when you really need them in tough moments."
            }
            
            normalized_stress = self._normalize_stress_level(stress_level)
            if normalized_stress == 'high':
                stress_label = 'High'
            elif normalized_stress == 'moderate':
                stress_label = 'Moderate'
            else:
                stress_label = 'Low'
            tip = strategy.get('tip', '') + stress_tips.get(stress_label, '')
            
            return {
                'technique_name': strategy['technique_name'],
                'instructions': strategy['instructions'],
                'affirmation': strategy.get('affirmation', 'You are stronger than you know. 💙'),
                'tip': tip
            }
        
        except Exception as e:
            self.logger.error(f"Error getting coping strategy: {e}")
            return {
                'technique_name': 'Compassionate Self-Support',
                'instructions': 'You don\'t have to be perfect. Right now, what would make you feel even 1% better? That\'s enough.',
                'affirmation': 'You are worthy. You are enough. You matter. 💙',
                'tip': 'When overwhelmed, the smallest act of self-kindness counts.'
            }
    
    def get_affirmation(self, emotion):
        """
        Get evidence-based affirmations for emotional resilience.
        
        Args:
            emotion (str): Detected emotion
        
        Returns:
            str: Empowering affirmation message
        """
        affirmations = {
            'sadness': [
                "Your pain is valid and temporary. Healing comes with time, support, and self-compassion.",
                "You've survived every difficult day so far. Your resilience is deeper than you know.",
                "Crying is a sign of strength, not weakness. Let yourself feel what needs to be felt.",
                "This darkness won't last. You will see light again. You will laugh again.",
                "Your sadness shows how much you love. That's a profound strength.",
            ],
            'anxiety': [
                "You are in control. You've faced difficult moments before and you're still here.",
                "This anxious thought is not a prediction—it's your mind offering options. You choose what's true.",
                "Your anxiety doesn't define you. You are capable, strong, and more resilient than you believe.",
                "This feeling will pass. You've dealt with uncertainty before. You'll handle this too.",
                "Your worries show you care. But you deserve peace more than you deserve worry.",
            ],
            'anger': [
                "Your boundaries matter. Your needs are valid. Stand firm in what's right for you.",
                "Anger is power. Use it to create change, to speak truth, to protect what matters.",
                "You have the right to feel upset. You also have choices about what comes next.",
                "Transform this fire into fuel for positive change. You have that power.",
                "Your anger is feedback. Listen to it, learn from it, then choose your response.",
            ],
            'fear': [
                "Courage isn't the absence of fear. It's moving forward anyway. You are brave.",
                "You are stronger than your fears. You've overcome scary things before.",
                "Fear means something matters to you. That's not weakness; that's human.",
                "This fear will pass, and you'll look back and see how capable you were.",
                "You are safe. Even if it doesn't feel like it, you have gotten through hard moments.",
            ],
            'joy': [
                "You deserve this happiness. Celebrate yourself fully. You've earned this good feeling.",
                "Your joy brightens the world. Never apologize for being happy.",
                "This moment is evidence that good things are possible for you. Believe in more.",
                "Hold this feeling close. Remember it when times get hard. You can feel this way again.",
                "You are worthy of happiness, peace, and good things. Always.",
            ],
            'stress': [
                "You are doing better than you think. Stress distorts how you see yourself.",
                "One step at a time. Progress over perfection. You don't have to see the whole path.",
                "Your needs matter as much as everyone else's. Taking care of yourself isn't selfish.",
                "Stress is temporary. You will feel lighter. You will find balance again.",
                "You're carrying a lot with grace. You're doing better than you're giving yourself credit for.",
            ],
            'default': [
                "You matter. Your life has value. Never forget that.",
                "One step at a time. You've got this, even if it doesn't feel like it right now.",
                "Be as kind to yourself as you would be to someone you love. You deserve that.",
                "This is temporary. You will feel better. You are not broken.",
                "You are stronger than you know. Stronger than your doubts. Trust yourself.",
            ]
        }
        
        aff_list = affirmations.get(emotion, affirmations['default'])
        return random.choice(aff_list)


def generate_emotion_response(emotion, confidence, stress_level, user_text=""):
    """Convenience function."""
    generator = ResponseGenerator()
    return generator.generate_response(emotion, confidence, stress_level, user_text=user_text)


def get_coping_strategy(emotion, stress_level):
    """Convenience function."""
    generator = ResponseGenerator()
    return generator.get_coping_strategy(emotion, stress_level)

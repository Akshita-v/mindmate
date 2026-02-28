"""
Emotion Detection Module

Uses HuggingFace Transformers to detect emotions and sentiment from user text.
Loads a pre-trained emotion classification model with confidence scores.
"""

from transformers import pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmotionDetector:
    """
    Detects emotions and sentiment from text using a pre-trained transformer model.
    
    Model: j-hartmann/emotion-english-distilroberta-base
    Emotions: anger, disgust, fear, joy, neutral, sadness, surprise
    """
    
    def __init__(self):
        """Initialize the emotion detection pipeline."""
        try:
            self.classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base"
            )
            logger.info("Emotion model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading emotion model: {e}")
            raise
    
    def detect_emotion(self, text):
        """
        Detect emotion from input text.
        
        Args:
            text (str): User input text to analyze
        
        Returns:
            dict: {
                'emotion': str - primary emotion label,
                'confidence': float - confidence score (0-1),
                'sentiment': str - positive/neutral/negative,
                'all_scores': list - all emotion scores
            }
        """
        if not text or not text.strip():
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'sentiment': 'neutral',
                'all_scores': []
            }
        
        try:
            # Get emotion predictions
            predictions = self.classifier(text)
            
            if not predictions:
                return {
                    'emotion': 'neutral',
                    'confidence': 0.0,
                    'sentiment': 'neutral',
                    'all_scores': []
                }
            
            # Extract top emotion
            top_emotion = predictions[0]
            emotion_label = self._map_emotion_label(top_emotion['label'], text)
            confidence = top_emotion['score']
            
            # Determine sentiment based on emotion
            sentiment = self._get_sentiment(emotion_label)
            
            return {
                'emotion': emotion_label,
                'confidence': round(confidence, 3),
                'sentiment': sentiment,
                'all_scores': predictions
            }
        
        except Exception as e:
            logger.error(f"Error detecting emotion: {e}")
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'sentiment': 'neutral',
                'all_scores': []
            }
    
    @staticmethod
    def _get_sentiment(emotion_label):
        """
        Map emotion to sentiment category.
        
        Args:
            emotion_label (str): Detected emotion
        
        Returns:
            str: positive, neutral, or negative
        """
        positive_emotions = ['joy', 'surprise']
        negative_emotions = ['sadness', 'anger', 'fear', 'disgust', 'anxiety', 'stress']
        
        if emotion_label in positive_emotions:
            return 'positive'
        elif emotion_label in negative_emotions:
            return 'negative'
        else:
            return 'neutral'

    @staticmethod
    def _map_emotion_label(raw_label, text):
        """
        Map model labels to app-friendly labels like anxiety or stress.

        Args:
            raw_label (str): Model emotion label
            text (str): User input text

        Returns:
            str: Normalized emotion label
        """
        if not text:
            return raw_label

        text_lower = text.lower()
        anxiety_keywords = [
            'anxious', 'anxiety', 'panic', 'nervous', 'worried', 'overthinking'
        ]
        stress_keywords = [
            'stress', 'stressed', 'overwhelmed', 'burnout', 'burned out', 'pressure'
        ]

        if any(keyword in text_lower for keyword in stress_keywords):
            return 'stress'

        if raw_label == 'fear' and any(keyword in text_lower for keyword in anxiety_keywords):
            return 'anxiety'

        return raw_label
    
    def get_emotion_description(self, emotion):
        """
        Get a therapeutic description of the detected emotion.
        
        Args:
            emotion (str): Emotion label
            
        Returns:
            str: Therapeutic understanding of the emotion
        """
        descriptions = {
            'joy': 'You seem happy and positive. This is a moment to celebrate and hold close. 🌟',
            'sadness': 'You\'re experiencing sadness—your heart responding to something meaningful. This is how we process deep emotions. 💙',
            'anger': 'You\'re feeling angry—which means something important has been crossed. Your boundaries matter. 💪',
            'fear': 'You\'re feeling fearful—your mind is alerting you to something that feels uncertain. That\'s actually a sign of awareness. 🌿',
            'disgust': 'You\'re experiencing disgust—your values or integrity are signaling that something isn\'t right. 🛑',
            'surprise': 'You\'re surprised—the expected has been disrupted. Give yourself time to process this shift. 🔄',
            'neutral': 'Your emotions feel balanced right now. That\'s a good place to be. 🧘',
            'anxiety': 'You\'re experiencing anxiety—your mind is working hard to protect you, even when the threat might not be real. Understanding this helps. 🫂',
            'stress': 'You\'re feeling stressed—your system is stretched. This is important information that something needs to change. 📌'
        }
        return descriptions.get(emotion, 'Your emotions are valid and important. Give yourself space to feel what you feel.')


def initialize_emotion_detector():
    """
    Convenience function to initialize the emotion detector.
    
    Returns:
        EmotionDetector: Initialized detector instance
    """
    return EmotionDetector()

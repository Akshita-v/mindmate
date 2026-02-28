"""
Stress Level Classification Module

Calculates stress level based on emotion type, confidence score, and negative keywords.
Outputs: Low, Moderate, High
"""

import logging

logger = logging.getLogger(__name__)


class StressClassifier:
    """
    Classifies stress level from emotion data and text content.
    """
    
    # Keywords that increase stress score
    STRESS_KEYWORDS = {
        'critical': ['urgent', 'emergency', 'crisis', 'critical', 'severe', 'extreme'],
        'high': ['struggle', 'difficulty', 'overwhelm', 'stressed', 'anxious', 'worried', 
                 'terrible', 'horrible', 'awful', 'exhausted', 'burnt out', 'burnout'],
        'moderate': ['tired', 'frustrated', 'concerned', 'problem', 'issue', 'challenge',
                    'difficult', 'stressful', 'pressure']
    }
    
    # Base stress scores for emotions
    EMOTION_STRESS_SCORES = {
        'anger': 75,
        'fear': 80,
        'sadness': 70,
        'disgust': 65,
        'neutral': 20,
        'surprise': 35,
        'joy': 10
    }
    
    def __init__(self):
        """Initialize the stress classifier."""
        self.logger = logging.getLogger(__name__)
    
    def classify_stress(self, emotion_label, confidence, text):
        """
        Classify stress level as Low, Moderate, or High.
        
        Args:
            emotion_label (str): Detected emotion label
            confidence (float): Confidence score of emotion detection (0-1)
            text (str): User input text
        
        Returns:
            dict: {
                'level': 'Low'|'Moderate'|'High',
                'score': float (0-100),
                'reasoning': str - explanation of stress level
            }
        """
        try:
            # Calculate base stress from emotion
            emotion_score = self.EMOTION_STRESS_SCORES.get(emotion_label, 50)
            
            # Boost score by confidence
            confidence_multiplier = 1 + (confidence * 0.5)
            stress_score = emotion_score * confidence_multiplier
            
            # Add keyword-based stress
            keyword_boost = self._calculate_keyword_boost(text)
            stress_score += keyword_boost
            
            # Normalize to 0-100 scale
            stress_score = min(100, max(0, stress_score))
            
            # Classify into level
            level, reasoning = self._get_stress_level(stress_score, emotion_label, keyword_boost > 0)
            
            return {
                'level': level,
                'score': round(stress_score, 1),
                'reasoning': reasoning
            }
        
        except Exception as e:
            self.logger.error(f"Error classifying stress: {e}")
            return {
                'level': 'Moderate',
                'score': 50.0,
                'reasoning': 'Unable to calculate stress level'
            }
    
    def _calculate_keyword_boost(self, text):
        """
        Calculate stress boost based on negative keywords in text.
        
        Args:
            text (str): User input text
        
        Returns:
            float: Stress boost value
        """
        text_lower = text.lower()
        boost = 0
        
        # Check critical keywords (+20)
        for keyword in self.STRESS_KEYWORDS['critical']:
            if keyword in text_lower:
                boost += 20
        
        # Check high keywords (+15)
        for keyword in self.STRESS_KEYWORDS['high']:
            if keyword in text_lower:
                boost += 10
        
        # Check moderate keywords (+5)
        for keyword in self.STRESS_KEYWORDS['moderate']:
            if keyword in text_lower:
                boost += 3
        
        return min(30, boost)  # Cap at 30 points
    
    def _get_stress_level(self, score, emotion, has_stress_keywords):
        """
        Determine stress level with therapeutic guidance.
        
        Args:
            score (float): Calculated stress score (0-100)
            emotion (str): Emotion label
            has_stress_keywords (bool): Whether stress keywords detected
        
        Returns:
            tuple: (level_string, reasoning_string)
        """
        if score < 35:
            reasoning = (
                "Your stress level is manageable right now—that's good news! "
                "Use this as an opportunity to strengthen your coping skills so they're second nature when stress increases."
            )
            return 'Low', reasoning
        
        elif score < 65:
            reasoning = (
                f"Your stress is moderate, compounded by {emotion} emotions. "
                "This is your mind's way of telling you that something needs attention or adjustment. "
                "This is the perfect time to practice coping strategies and make small changes before stress escalates. "
                "You have more control than you think."
            )
            if has_stress_keywords:
                reasoning += (
                    " The language you're using suggests you're emotionally activated right now—"
                    "that's important information about what you really need."
                )
            return 'Moderate', reasoning
        
        else:
            reasoning = (
                f"Your stress is elevated right now, combined with {emotion} emotions. "
                "This is a red flag that your system is stretched. You need support and relief—not judgment. "
                "**What matters now:** prioritize REST, set boundaries, reach out for help, and know this is temporary but requires action. "
                "Consider talking to a trusted friend, family member, or mental health professional—not because anything is wrong with you, "
                "but because you deserve support when carrying this much weight."
            )
            return 'High', reasoning


def classify_stress_level(emotion_label, confidence, text):
    """
    Convenience function to classify stress level.
    
    Args:
        emotion_label (str): Detected emotion
        confidence (float): Confidence score
        text (str): User input
    
    Returns:
        dict: Stress classification result
    """
    classifier = StressClassifier()
    return classifier.classify_stress(emotion_label, confidence, text)

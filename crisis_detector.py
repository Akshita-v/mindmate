"""
Crisis Detection Module

Detects high-risk phrases indicating suicidal ideation or severe distress.
Provides emergency support resources and professional help information.
"""

import logging
import re

logger = logging.getLogger(__name__)


class CrisisDetector:
    """
    Detects crisis indicators in user messages.
    Provides appropriate emergency support messaging.
    """
    
    # High-risk phrases indicating suicidal ideation
    CRISIS_KEYWORDS = [
        # Suicidal ideation
        "want to die",
        "want to kill myself",
        "i want to end",
        "take my own life",
        "i can't live",
        "don't want to exist",
        "give up on life",
        "i will end it",
        "kill myself",
        "commit suicide",
        "suicide",
        "want to give up",
        "feel hopeless",
        "can't continue",
        "no point in living",
        "better off dead",
        "everyone would be better without me",
        "worthless",
        "nobody cares",
        "alone forever",
        "nobody understands",
        "too much pain",
    ]
    
    # High-harm but non-suicidal keywords
    HARM_KEYWORDS = [
        "self harm",
        "hurt myself",
        "cut myself",
        "harm myself",
        "don't deserve",
        "hate myself"
    ]
    
    # Crisis support resources
    CRISIS_RESOURCES = {
        'US': {
            'name': '988 Suicide & Crisis Lifeline',
            'number': '988',
            'text': 'Text "HOME" to 741741',
            'link': 'https://988lifeline.org'
        },
        'UK': {
            'name': 'Samaritans',
            'number': '116 123',
            'link': 'https://www.samaritans.org.uk/'
        },
        'INTERNATIONAL': {
            'name': 'International Association for Suicide Prevention',
            'link': 'https://www.iasp.info/resources/Crisis_Centres/'
        }
    }
    
    def __init__(self):
        """Initialize the crisis detector."""
        self.logger = logging.getLogger(__name__)
    
    def detect_crisis(self, text):
        """
        Detect crisis indicators in user text.
        
        Args:
            text (str): User input text
        
        Returns:
            dict: {
                'is_crisis': bool,
                'severity': 'low'|'medium'|'high',
                'matched_phrase': str or None,
                'support_message': str,
                'resources': dict
            }
        """
        if not text or not text.strip():
            return {
                'is_crisis': False,
                'severity': 'low',
                'matched_phrase': None,
                'support_message': '',
                'resources': {}
            }
        
        text_lower = text.lower()
        
        try:
            # Check for crisis keywords (more serious)
            crisis_match = self._check_keywords(text_lower, self.CRISIS_KEYWORDS)
            if crisis_match:
                return {
                    'is_crisis': True,
                    'severity': 'high',
                    'matched_phrase': crisis_match,
                    'support_message': self._get_crisis_support_message(),
                    'resources': self.CRISIS_RESOURCES
                }
            
            # Check for harm keywords (less serious but concerning)
            harm_match = self._check_keywords(text_lower, self.HARM_KEYWORDS)
            if harm_match:
                return {
                    'is_crisis': True,
                    'severity': 'medium',
                    'matched_phrase': harm_match,
                    'support_message': self._get_harm_support_message(),
                    'resources': self.CRISIS_RESOURCES
                }
            
            # No crisis detected
            return {
                'is_crisis': False,
                'severity': 'low',
                'matched_phrase': None,
                'support_message': '',
                'resources': {}
            }
        
        except Exception as e:
            self.logger.error(f"Error in crisis detection: {e}")
            return {
                'is_crisis': False,
                'severity': 'low',
                'matched_phrase': None,
                'support_message': '',
                'resources': {}
            }
    
    @staticmethod
    def _check_keywords(text, keywords):
        """
        Check if any keywords match in text.
        
        Args:
            text (str): Lowercased text to check
            keywords (list): List of keywords to search for
        
        Returns:
            str: Matched keyword or None
        """
        for keyword in keywords:
            # Use word boundaries for more accurate matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text):
                return keyword
        return None
    
    @staticmethod
    def _get_crisis_support_message():
        """Get compassionate crisis support message for suicidal ideation."""
        return """
        ⚠️ **IMPORTANT: I CARE ABOUT YOUR WELLBEING**

        I hear pain in what you've shared, and I want you to know: **your life has immense value**, 
        even if it doesn't feel that way right now. What you're feeling is temporary—but your life is permanent.
        
        **The pain you feel is real. But suicide isn't the answer—it's pain speaking, not truth.**

        **Please reach out for immediate human support:**
        
        🆘 **United States:**
        - Call or text **988** (Suicide & Crisis Lifeline) - FREE, 24/7, confidential
        - Text "HOME" to **741741** (Crisis Text Line)
        - **Call 911** or go to your nearest Emergency Room if in immediate danger
        
        🌍 **International:**
        - UK: Call **116 123** (Samaritans)
        - Canada: Call **1-833-456-4566** (Canada Suicide Prevention Service)
        - Australia: Call **13 11 14** (Lifeline)
        - Find your country: https://findahelpline.com

        **Why reach out?**
        ✓ Trained counselors understand what you're going through
        ✓ They've helped people in your exact situation find reasons to stay
        ✓ Suicidal thoughts are treatable—like any other mental health condition
        ✓ This crisis is temporary, but the relief from professional help is lasting
        ✓ You don't have to figure this out alone

        **You matter. Your story isn't over. It can get better—not immediately, but it absolutely can.**
        
        Please reach out to someone today. You deserve to feel better, and people want to help. ❤️
        """
    
    @staticmethod
    def _get_harm_support_message():
        """Get compassionate support message for self-harm indicators."""
        return """
        ⚠️ **I'M CONCERNED ABOUT YOU, AND I WANT TO HELP**

        Self-harm is a sign that the pain inside feels too big to contain. I understand why you might 
        do this—but I want you to know: **there are better ways to feel relief**, and **you deserve healing, not harm**.
        
        **What you're feeling is valid. Your way of coping shows you're trying to survive. 
        But there are healthier paths forward.**

        **Please reach out for professional support:**
        
        🆘 **Immediate Help:**
        - Call or text **988** (Suicide & Crisis Lifeline) - 24/7, confidential
        - Text "HOME" to **741741** (Crisis Text Line)
        - Go to your nearest Emergency Room if you're in immediate danger
        - Tell a trusted adult: parent, teacher, counselor, friend

        **Speaking with a therapist can help because:**
        ✓ They understand self-harm and never shame you for it
        ✓ They teach better coping skills that actually work
        ✓ They help with the underlying pain, not just the behavior
        ✓ They provide the real, lasting relief you deserve
        ✓ Many people recover fully and never feel the urge again

        **In this moment, try:**
        - Hold ice cubes in your hand (provides sensation without injury)
        - Take a very hot or very cold shower
        - Squeeze a pillow or punch a mattress
        - Draw on your skin with red marker instead of cutting
        - Call someone: crisis line, friend, or family

        **You're stronger than you know. The fact that you reached out shows incredible courage.
        Please keep reaching out until you get the support you need. You deserve it. ❤️**
        """
    
    def get_emergency_disclaimer(self):
        """
        Get the standard disclaimer about this system's limitations.
        
        Returns:
            str: Disclaimer text
        """
        return """
        **⚠️ IMPORTANT DISCLAIMER:**
        
        MindMate is an AI tool designed to provide supportive resources and mood tracking. 
        It is **NOT a substitute for professional mental health care**.
        
        **If you are in crisis:**
        - Call 988 (US) | Text "HOME" to 741741
        - Visit emergency services
        - Call your local emergency number
        
        Please reach out to a qualified mental health professional, school counselor, 
        or trusted person in your life. You deserve real support from trained professionals.
        """


def detect_crisis_indicators(text):
    """
    Convenience function to detect crisis indicators.
    
    Args:
        text (str): User input text
    
    Returns:
        dict: Crisis detection result
    """
    detector = CrisisDetector()
    return detector.detect_crisis(text)

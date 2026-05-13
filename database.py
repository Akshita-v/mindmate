"""
Database Module for Mood Tracking

Uses SQLite to store and retrieve mood data including:
- Date/Time
- User input text
- Detected emotion
- Stress level
- Confidence score
"""

import sqlite3
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class MoodDatabase:
    """
    Manages SQLite database for mood tracking and historical analysis.
    """
    
    def __init__(self, db_path='mood_tracker.db'):
        """
        Initialize the database connection.
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.initialize_database()
    
    def initialize_database(self):
        """Create tables if they don't exist."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = self.conn.cursor()
            
            # Create mood_entries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mood_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_input TEXT NOT NULL,
                    emotion TEXT NOT NULL,
                    emotion_confidence REAL,
                    stress_level TEXT,
                    stress_score REAL,
                    sentiment TEXT,
                    notes TEXT
                )
            ''')
            
            # Create index for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON mood_entries(timestamp)
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    session_id TEXT,
                    user_input TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    conversation_type TEXT,
                    emotion TEXT,
                    emotion_confidence REAL,
                    stress_level TEXT,
                    stress_score REAL,
                    sentiment TEXT,
                    tip TEXT,
                    coping_json TEXT
                )
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_conversation_timestamp
                ON conversation_entries(timestamp)
            ''')
            
            self.conn.commit()
            logger.info(f"Database initialized at {self.db_path}")
        
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def add_mood_entry(self, user_input, emotion, emotion_confidence, 
                       stress_level, stress_score, sentiment='neutral', notes=''):
        """
        Add a new mood entry to the database.
        
        Args:
            user_input (str): User's original input text
            emotion (str): Detected emotion label
            emotion_confidence (float): Emotion detection confidence (0-1)
            stress_level (str): Low, Moderate, or High
            stress_score (float): Calculated stress score (0-100)
            sentiment (str): positive, neutral, or negative
            notes (str): Optional additional notes
        
        Returns:
            int: ID of the inserted record
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO mood_entries 
                (user_input, emotion, emotion_confidence, stress_level, 
                 stress_score, sentiment, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_input, emotion, emotion_confidence, stress_level, 
                  stress_score, sentiment, notes))
            
            self.conn.commit()
            entry_id = cursor.lastrowid
            logger.info(f"Mood entry added with ID: {entry_id}")
            return entry_id
        
        except Exception as e:
            logger.error(f"Error adding mood entry: {e}")
            return None

    def add_conversation_entry(
        self,
        session_id,
        user_input,
        bot_response,
        conversation_type,
        emotion,
        emotion_confidence,
        stress_level,
        stress_score,
        sentiment='neutral',
        tip='',
        coping=None,
    ):
        """Store a full conversational turn for dashboard history."""
        try:
            cursor = self.conn.cursor()
            coping_json = json.dumps(coping) if isinstance(coping, dict) else None
            cursor.execute('''
                INSERT INTO conversation_entries
                (session_id, user_input, bot_response, conversation_type, emotion,
                 emotion_confidence, stress_level, stress_score, sentiment, tip, coping_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session_id,
                user_input,
                bot_response,
                conversation_type,
                emotion,
                emotion_confidence,
                stress_level,
                stress_score,
                sentiment,
                tip,
                coping_json,
            ))

            self.conn.commit()
            return cursor.lastrowid

        except Exception as e:
            logger.error(f"Error adding conversation entry: {e}")
            return None
    
    def get_recent_entries(self, days=7):
        """
        Fetch mood entries from the last N days.
        
        Args:
            days (int): Number of days to retrieve (default: 7)
        
        Returns:
            list: List of mood entry dictionaries
        """
        try:
            cursor = self.conn.cursor()
            cutoff_date = datetime.now() - timedelta(days=days)
            
            cursor.execute('''
                SELECT id, timestamp, user_input, emotion, emotion_confidence,
                       stress_level, stress_score, sentiment
                FROM mood_entries
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
            ''', (cutoff_date,))
            
            columns = ['id', 'timestamp', 'user_input', 'emotion', 
                      'emotion_confidence', 'stress_level', 'stress_score', 'sentiment']
            
            rows = cursor.fetchall()
            entries = [dict(zip(columns, row)) for row in rows]
            
            logger.info(f"Retrieved {len(entries)} entries from last {days} days")
            return entries
        
        except Exception as e:
            logger.error(f"Error retrieving recent entries: {e}")
            return []
    
    def get_emotion_distribution(self, days=7):
        """
        Get distribution of emotions over the past N days.
        
        Args:
            days (int): Number of days to analyze
        
        Returns:
            dict: {emotion: count}
        """
        try:
            cursor = self.conn.cursor()
            cutoff_date = datetime.now() - timedelta(days=days)
            
            cursor.execute('''
                SELECT emotion, COUNT(*) as count
                FROM mood_entries
                WHERE timestamp >= ?
                GROUP BY emotion
                ORDER BY count DESC
            ''', (cutoff_date,))
            
            distribution = {row[0]: row[1] for row in cursor.fetchall()}
            logger.info(f"Emotion distribution calculated: {distribution}")
            return distribution
        
        except Exception as e:
            logger.error(f"Error calculating emotion distribution: {e}")
            return {}

    def get_recent_conversations(self, limit=8):
        """Fetch the latest stored conversation turns for dashboard display."""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, timestamp, session_id, user_input, bot_response,
                       conversation_type, emotion, emotion_confidence,
                       stress_level, stress_score, sentiment, tip, coping_json
                FROM conversation_entries
                ORDER BY timestamp DESC, id DESC
                LIMIT ?
            ''', (limit,))

            columns = [
                'id', 'timestamp', 'session_id', 'user_input', 'bot_response',
                'conversation_type', 'emotion', 'emotion_confidence',
                'stress_level', 'stress_score', 'sentiment', 'tip', 'coping_json'
            ]
            rows = cursor.fetchall()
            conversations = []
            for row in rows:
                item = dict(zip(columns, row))
                coping_json = item.get('coping_json')
                if coping_json:
                    try:
                        item['coping'] = json.loads(coping_json)
                    except Exception:
                        item['coping'] = None
                else:
                    item['coping'] = None
                conversations.append(item)

            return conversations

        except Exception as e:
            logger.error(f"Error retrieving recent conversations: {e}")
            return []
    
    def get_stress_trends(self, days=7):
        """
        Get daily stress level trends for visualization.
        
        Args:
            days (int): Number of days to analyze
        
        Returns:
            list: List of dicts with date and average stress score
        """
        try:
            cursor = self.conn.cursor()
            cutoff_date = datetime.now() - timedelta(days=days)
            
            cursor.execute('''
                SELECT DATE(timestamp) as date, 
                       AVG(stress_score) as avg_stress,
                       COUNT(*) as entry_count
                FROM mood_entries
                WHERE timestamp >= ?
                GROUP BY DATE(timestamp)
                ORDER BY date ASC
            ''', (cutoff_date,))
            
            trends = []
            for row in cursor.fetchall():
                trends.append({
                    'date': row[0],
                    'avg_stress': round(row[1], 1),
                    'entry_count': row[2]
                })
            
            logger.info(f"Stress trends calculated for {len(trends)} days")
            return trends
        
        except Exception as e:
            logger.error(f"Error calculating stress trends: {e}")
            return []
    
    def get_stress_summary(self, days=7):
        """
        Get a summary of stress stats over N days.
        
        Args:
            days (int): Number of days to analyze (default: 7)
        
        Returns:
            dict: Stress summary statistics
        """
        try:
            cursor = self.conn.cursor()
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Average stress
            cursor.execute('''
                SELECT AVG(stress_score) FROM mood_entries
                WHERE timestamp >= ?
            ''', (cutoff_date,))
            avg_stress = cursor.fetchone()[0] or 0
            
            # Peak stress
            cursor.execute('''
                SELECT MAX(stress_score) FROM mood_entries
                WHERE timestamp >= ?
            ''', (cutoff_date,))
            peak_stress = cursor.fetchone()[0] or 0
            
            # Entry count
            cursor.execute('''
                SELECT COUNT(*) FROM mood_entries
                WHERE timestamp >= ?
            ''', (cutoff_date,))
            entry_count = cursor.fetchone()[0]
            
            summary = {
                'average_stress': round(avg_stress, 1),
                'peak_stress': round(peak_stress, 1),
                'entry_count': entry_count
            }
            
            logger.info(f"Stress summary calculated: {summary}")
            return summary
        
        except Exception as e:
            logger.error(f"Error calculating stress summary: {e}")
            return {'average_stress': 0, 'peak_stress': 0, 'entry_count': 0}
    
    def get_weekly_summary(self):
        """
        Get a comprehensive summary of the past 7 days.
        
        Returns:
            dict: Summary statistics
        """
        try:
            cursor = self.conn.cursor()
            cutoff_date = datetime.now() - timedelta(days=7)
            
            # Total entries
            cursor.execute('''
                SELECT COUNT(*) FROM mood_entries
                WHERE timestamp >= ?
            ''', (cutoff_date,))
            total_entries = cursor.fetchone()[0]
            
            # Average stress
            cursor.execute('''
                SELECT AVG(stress_score) FROM mood_entries
                WHERE timestamp >= ?
            ''', (cutoff_date,))
            avg_stress = cursor.fetchone()[0] or 0
            
            # Most common emotion
            cursor.execute('''
                SELECT emotion, COUNT(*) as count FROM mood_entries
                WHERE timestamp >= ?
                GROUP BY emotion
                ORDER BY count DESC
                LIMIT 1
            ''', (cutoff_date,))
            
            emotion_result = cursor.fetchone()
            most_common_emotion = emotion_result[0] if emotion_result else 'N/A'
            
            # Sentiment breakdown
            cursor.execute('''
                SELECT sentiment, COUNT(*) as count FROM mood_entries
                WHERE timestamp >= ?
                GROUP BY sentiment
            ''', (cutoff_date,))
            
            sentiment_counts = {row[0]: row[1] for row in cursor.fetchall()}
            
            summary = {
                'period': 'Last 7 days',
                'total_entries': total_entries,
                'average_stress': round(avg_stress, 1),
                'most_common_emotion': most_common_emotion,
                'sentiment_breakdown': sentiment_counts,
                'date_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            logger.info(f"Weekly summary generated: {summary}")
            return summary
        
        except Exception as e:
            logger.error(f"Error generating weekly summary: {e}")
            return {}
    
    def get_all_entries(self):
        """
        Retrieve all mood entries (for data export or advanced analysis).
        
        Returns:
            list: All mood entries
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, timestamp, user_input, emotion, emotion_confidence,
                       stress_level, stress_score, sentiment
                FROM mood_entries
                ORDER BY timestamp DESC
            ''')
            
            columns = ['id', 'timestamp', 'user_input', 'emotion', 
                      'emotion_confidence', 'stress_level', 'stress_score', 'sentiment']
            
            rows = cursor.fetchall()
            entries = [dict(zip(columns, row)) for row in rows]
            
            return entries
        
        except Exception as e:
            logger.error(f"Error retrieving all entries: {e}")
            return []
    
    def delete_old_entries(self, days=90):
        """
        Delete mood entries older than N days (data cleanup).
        
        Args:
            days (int): Keep entries from last N days
        
        Returns:
            int: Number of deleted entries
        """
        try:
            cursor = self.conn.cursor()
            cutoff_date = datetime.now() - timedelta(days=days)
            
            cursor.execute('''
                DELETE FROM mood_entries
                WHERE timestamp < ?
            ''', (cutoff_date,))
            
            self.conn.commit()
            deleted_count = cursor.rowcount
            logger.info(f"Deleted {deleted_count} entries older than {days} days")
            return deleted_count
        
        except Exception as e:
            logger.error(f"Error deleting old entries: {e}")
            return 0
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def __del__(self):
        """Ensure connection is closed when object is destroyed."""
        self.close()


def get_mood_database(db_path='mood_tracker.db'):
    """Convenience function to get database instance."""
    return MoodDatabase(db_path)

"""
Meeting History Manager

This module provides functionality to store, retrieve, and manage meeting data
for the Meeting Summarizer application. It includes features for:
- Storing meeting transcripts and analysis results
- Retrieving historical meeting data
- Searching across past meetings
- Tracking team performance over time
- Generating trend reports

Author: GitHub Copilot
Date: October 2025
"""

import json
import os
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class MeetingRecord:
    """Data class representing a meeting record"""
    id: str
    title: str
    date: datetime
    participants: List[str]
    transcript: str
    summary: Dict[str, Any]
    sentiment_analysis: Dict[str, Any]
    coach_feedback: Dict[str, Any]
    duration_minutes: Optional[int] = None
    meeting_type: Optional[str] = None
    tags: Optional[List[str]] = None

class MeetingHistoryManager:
    """
    Manages storage and retrieval of meeting data with SQLite backend
    """
    
    def __init__(self, db_path: str = "meetings.db"):
        """
        Initialize the Meeting History Manager
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize the SQLite database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create meetings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS meetings (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    date TEXT NOT NULL,
                    participants TEXT NOT NULL,
                    transcript TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    sentiment_analysis TEXT NOT NULL,
                    coach_feedback TEXT NOT NULL,
                    duration_minutes INTEGER,
                    meeting_type TEXT,
                    tags TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            
            # Create search index for full-text search
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS meetings_fts USING fts5(
                    id, title, transcript, summary_text, tags,
                    content='meetings'
                )
            """)
            
            conn.commit()
    
    def store_meeting(self, meeting_record: MeetingRecord) -> bool:
        """
        Store a meeting record in the database
        
        Args:
            meeting_record: MeetingRecord object to store
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Convert complex fields to JSON strings
                participants_json = json.dumps(meeting_record.participants)
                summary_json = json.dumps(meeting_record.summary)
                sentiment_json = json.dumps(meeting_record.sentiment_analysis)
                coach_json = json.dumps(meeting_record.coach_feedback)
                tags_json = json.dumps(meeting_record.tags or [])
                
                cursor.execute("""
                    INSERT OR REPLACE INTO meetings (
                        id, title, date, participants, transcript, summary,
                        sentiment_analysis, coach_feedback, duration_minutes,
                        meeting_type, tags, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    meeting_record.id,
                    meeting_record.title,
                    meeting_record.date.isoformat(),
                    participants_json,
                    meeting_record.transcript,
                    summary_json,
                    sentiment_json,
                    coach_json,
                    meeting_record.duration_minutes,
                    meeting_record.meeting_type,
                    tags_json,
                    datetime.now().isoformat()
                ))
                
                # Update FTS index
                summary_text = self._extract_summary_text(meeting_record.summary)
                cursor.execute("""
                    INSERT OR REPLACE INTO meetings_fts (
                        id, title, transcript, summary_text, tags
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    meeting_record.id,
                    meeting_record.title,
                    meeting_record.transcript,
                    summary_text,
                    " ".join(meeting_record.tags or [])
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error storing meeting: {e}")
            return False
    
    def get_meeting(self, meeting_id: str) -> Optional[MeetingRecord]:
        """
        Retrieve a specific meeting by ID
        
        Args:
            meeting_id: Unique identifier for the meeting
            
        Returns:
            MeetingRecord object or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM meetings WHERE id = ?", (meeting_id,))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_meeting_record(row)
                return None
                
        except Exception as e:
            print(f"Error retrieving meeting: {e}")
            return None
    
    def get_recent_meetings(self, limit: int = 10) -> List[MeetingRecord]:
        """
        Get the most recent meetings
        
        Args:
            limit: Maximum number of meetings to return
            
        Returns:
            List of MeetingRecord objects
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM meetings 
                    ORDER BY date DESC 
                    LIMIT ?
                """, (limit,))
                
                return [self._row_to_meeting_record(row) for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"Error retrieving recent meetings: {e}")
            return []
    
    def search_meetings(self, query: str, limit: int = 20) -> List[MeetingRecord]:
        """
        Search meetings using full-text search
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching MeetingRecord objects
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Use FTS for search
                cursor.execute("""
                    SELECT m.* FROM meetings m
                    JOIN meetings_fts fts ON m.id = fts.id
                    WHERE meetings_fts MATCH ?
                    ORDER BY rank
                    LIMIT ?
                """, (query, limit))
                
                return [self._row_to_meeting_record(row) for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"Error searching meetings: {e}")
            return []
    
    def get_meetings_by_date_range(self, start_date: datetime, end_date: datetime) -> List[MeetingRecord]:
        """
        Get meetings within a date range
        
        Args:
            start_date: Start of date range
            end_date: End of date range
            
        Returns:
            List of MeetingRecord objects
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM meetings 
                    WHERE date BETWEEN ? AND ?
                    ORDER BY date DESC
                """, (start_date.isoformat(), end_date.isoformat()))
                
                return [self._row_to_meeting_record(row) for row in cursor.fetchall()]
                
        except Exception as e:
            print(f"Error retrieving meetings by date range: {e}")
            return []
    
    def get_team_sentiment_trends(self, days: int = 30) -> Dict[str, Any]:
        """
        Analyze sentiment trends over time for team performance insights
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary containing sentiment trend analysis
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            meetings = self.get_meetings_by_date_range(start_date, end_date)
            
            if not meetings:
                return {"error": "No meetings found in the specified time range"}
            
            sentiment_scores = []
            dates = []
            
            for meeting in meetings:
                sentiment_data = meeting.sentiment_analysis
                if isinstance(sentiment_data, dict) and 'overall_score' in sentiment_data:
                    sentiment_scores.append(sentiment_data['overall_score'])
                    dates.append(meeting.date.strftime('%Y-%m-%d'))
            
            if not sentiment_scores:
                return {"error": "No sentiment data available"}
            
            # Calculate trends
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            trend = "improving" if len(sentiment_scores) > 1 and sentiment_scores[-1] > sentiment_scores[0] else "declining"
            
            return {
                "period_days": days,
                "meetings_analyzed": len(meetings),
                "average_sentiment": round(avg_sentiment, 2),
                "trend": trend,
                "sentiment_timeline": list(zip(dates, sentiment_scores)),
                "highest_sentiment": max(sentiment_scores),
                "lowest_sentiment": min(sentiment_scores)
            }
            
        except Exception as e:
            print(f"Error analyzing sentiment trends: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def generate_team_performance_report(self, days: int = 30) -> Dict[str, Any]:
        """
        Generate a comprehensive team performance report
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary containing performance metrics and insights
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            meetings = self.get_meetings_by_date_range(start_date, end_date)
            
            if not meetings:
                return {"error": "No meetings found in the specified time range"}
            
            # Aggregate statistics
            total_meetings = len(meetings)
            total_action_items = 0
            completed_decisions = 0
            average_effectiveness = 0
            
            participant_frequency = {}
            meeting_types = {}
            
            for meeting in meetings:
                # Count action items
                if 'action_items' in meeting.summary:
                    total_action_items += len(meeting.summary['action_items'])
                
                # Count decisions
                if 'decisions' in meeting.summary:
                    completed_decisions += len(meeting.summary['decisions'])
                
                # Track effectiveness scores
                if 'effectiveness_score' in meeting.coach_feedback:
                    average_effectiveness += meeting.coach_feedback['effectiveness_score']
                
                # Track participant frequency
                for participant in meeting.participants:
                    participant_frequency[participant] = participant_frequency.get(participant, 0) + 1
                
                # Track meeting types
                if meeting.meeting_type:
                    meeting_types[meeting.meeting_type] = meeting_types.get(meeting.meeting_type, 0) + 1
            
            if total_meetings > 0:
                average_effectiveness /= total_meetings
            
            return {
                "report_period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
                "total_meetings": total_meetings,
                "total_action_items": total_action_items,
                "total_decisions": completed_decisions,
                "average_effectiveness_score": round(average_effectiveness, 2),
                "action_items_per_meeting": round(total_action_items / total_meetings, 1) if total_meetings > 0 else 0,
                "decisions_per_meeting": round(completed_decisions / total_meetings, 1) if total_meetings > 0 else 0,
                "most_active_participants": sorted(participant_frequency.items(), key=lambda x: x[1], reverse=True)[:5],
                "meeting_types_distribution": meeting_types,
                "sentiment_trends": self.get_team_sentiment_trends(days)
            }
            
        except Exception as e:
            print(f"Error generating performance report: {e}")
            return {"error": f"Report generation failed: {str(e)}"}
    
    def delete_meeting(self, meeting_id: str) -> bool:
        """
        Delete a meeting record
        
        Args:
            meeting_id: ID of the meeting to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM meetings WHERE id = ?", (meeting_id,))
                cursor.execute("DELETE FROM meetings_fts WHERE id = ?", (meeting_id,))
                conn.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Error deleting meeting: {e}")
            return False
    
    def _row_to_meeting_record(self, row: Tuple) -> MeetingRecord:
        """Convert database row to MeetingRecord object"""
        return MeetingRecord(
            id=row[0],
            title=row[1],
            date=datetime.fromisoformat(row[2]),
            participants=json.loads(row[3]),
            transcript=row[4],
            summary=json.loads(row[5]),
            sentiment_analysis=json.loads(row[6]),
            coach_feedback=json.loads(row[7]),
            duration_minutes=row[8],
            meeting_type=row[9],
            tags=json.loads(row[10]) if row[10] else []
        )
    
    def _extract_summary_text(self, summary: Dict[str, Any]) -> str:
        """Extract searchable text from summary data"""
        text_parts = []
        
        if 'key_points' in summary:
            text_parts.extend([point.get('point', '') for point in summary['key_points']])
        
        if 'action_items' in summary:
            text_parts.extend([item.get('task', '') for item in summary['action_items']])
            text_parts.extend([item.get('assignee', '') for item in summary['action_items']])
        
        if 'decisions' in summary:
            text_parts.extend([decision.get('decision', '') for decision in summary['decisions']])
        
        return ' '.join(text_parts)
    
    @staticmethod
    def generate_meeting_id(transcript: str, date: datetime) -> str:
        """Generate a unique meeting ID based on content and date"""
        content = f"{transcript[:100]}{date.isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]


# Utility functions for easy integration
def create_meeting_from_analysis(
    title: str,
    transcript: str,
    participants: List[str],
    summary: Dict[str, Any],
    sentiment_analysis: Dict[str, Any],
    coach_feedback: Dict[str, Any],
    meeting_type: str = None,
    tags: List[str] = None
) -> MeetingRecord:
    """
    Helper function to create a MeetingRecord from analysis results
    
    Args:
        title: Meeting title
        transcript: Meeting transcript
        participants: List of participant names
        summary: Summary analysis results
        sentiment_analysis: Sentiment analysis results
        coach_feedback: Coach feedback results
        meeting_type: Type of meeting (optional)
        tags: List of tags (optional)
        
    Returns:
        MeetingRecord object ready to be stored
    """
    meeting_date = datetime.now()
    meeting_id = MeetingHistoryManager.generate_meeting_id(transcript, meeting_date)
    
    return MeetingRecord(
        id=meeting_id,
        title=title,
        date=meeting_date,
        participants=participants,
        transcript=transcript,
        summary=summary,
        sentiment_analysis=sentiment_analysis,
        coach_feedback=coach_feedback,
        meeting_type=meeting_type,
        tags=tags
    )

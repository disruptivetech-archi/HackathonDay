import os
import openai
from typing import Dict, List, Any

openai.api_key = os.getenv("OPENAI_API_KEY", "sk-demo-key123456789")

def generate_summary(transcript: str) -> Dict[str, Any]:
    """
    Generate a structured summary of a meeting transcript
    
    Args:
        transcript: The meeting transcript text
        
    Returns:
        Dictionary containing key points, action items, and decisions
    """
    prompt = f"""
    You are an AI assistant specialized in summarizing meeting transcripts.
    Please analyze the following meeting transcript and provide:
    1. Key Discussion Points: Extract the main topics discussed
    2. Action Items: List tasks that were assigned, including who is responsible
    3. Decisions Made: Identify decisions that were finalized during the meeting
    
    Meeting Transcript:
    {transcript}
    
    Format your response as JSON with the following structure:
    {{
        "key_points": [
            {{"point": "Description of key point 1"}},
            {{"point": "Description of key point 2"}}
        ],
        "action_items": [
            {{"task": "Task description", "assignee": "Person name"}},
            {{"task": "Task description", "assignee": "Person name"}}
        ],
        "decisions": [
            {{"decision": "Description of decision 1"}},
            {{"decision": "Description of decision 2"}}
        ]
    }}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use appropriate model based on availability
            messages=[
                {"role": "system", "content": "You are a meeting summarization assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent outputs
            max_tokens=1000
        )
        
        summary = response.choices[0].message.content
        
        
        return {
            "summary": summary,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

def analyze_sentiment(transcript: str) -> Dict[str, Any]:
    """
    Analyze the sentiment and emotional tone of a meeting transcript
    
    Args:
        transcript: The meeting transcript text
        
    Returns:
        Dictionary containing sentiment analysis results
    """
    prompt = f"""
    You are an AI assistant specialized in analyzing the emotional tone of meetings.
    Please analyze the following meeting transcript and provide:
    1. Overall Sentiment: The general emotional tone of the meeting (positive, negative, neutral)
    2. Sentiment Trends: How the emotional tone changed throughout the meeting
    3. Tension Points: Identify moments where there might have been disagreement or tension
    4. Team Morale Indicators: Signs of team engagement, enthusiasm, or disengagement
    
    Meeting Transcript:
    {transcript}
    
    Format your response as JSON with the following structure:
    {{
        "overall_sentiment": "positive/negative/neutral",
        "sentiment_score": 0.75, # 0 to 1 scale, higher is more positive
        "sentiment_trends": [
            {{"segment": "Beginning", "tone": "Description", "score": 0.8}},
            {{"segment": "Middle", "tone": "Description", "score": 0.6}},
            {{"segment": "End", "tone": "Description", "score": 0.7}}
        ],
        "tension_points": [
            {{"topic": "Topic where tension occurred", "description": "Description of the tension"}}
        ],
        "morale_indicators": [
            {{"indicator": "Description of morale indicator", "type": "positive/negative"}}
        ]
    }}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use appropriate model based on availability
            messages=[
                {"role": "system", "content": "You are a meeting sentiment analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        sentiment_analysis = response.choices[0].message.content
        
        return {
            "sentiment_analysis": sentiment_analysis,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

def generate_coach_feedback(transcript: str) -> Dict[str, Any]:
    """
    Generate coaching feedback on meeting effectiveness
    
    Args:
        transcript: The meeting transcript text
        
    Returns:
        Dictionary containing coaching feedback
    """
    prompt = f"""
    You are an AI meeting coach specialized in improving meeting effectiveness.
    Please analyze the following meeting transcript and provide:
    1. Meeting Effectiveness Score: Rate the meeting's effectiveness on a scale of 1-10
    2. Strengths: What went well in this meeting
    3. Areas for Improvement: What could be improved in future meetings
    4. Specific Recommendations: Actionable suggestions for better meetings
    5. Participation Balance: Analysis of speaking time distribution
    
    Meeting Transcript:
    {transcript}
    
    Format your response as JSON with the following structure:
    {{
        "effectiveness_score": 7,
        "strengths": [
            {{"strength": "Description of what went well"}},
            {{"strength": "Description of what went well"}}
        ],
        "improvement_areas": [
            {{"area": "Description of improvement area"}},
            {{"area": "Description of improvement area"}}
        ],
        "recommendations": [
            {{"recommendation": "Actionable suggestion"}},
            {{"recommendation": "Actionable suggestion"}}
        ],
        "participation_balance": {{
            "balanced": true/false,
            "description": "Description of speaking time distribution",
            "dominant_speakers": ["Name1", "Name2"]
        }}
    }}
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use appropriate model based on availability
            messages=[
                {"role": "system", "content": "You are a meeting effectiveness coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        coaching_feedback = response.choices[0].message.content
        
        return {
            "coaching_feedback": coaching_feedback,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

def handle_chat(transcript: str, question: str, chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Handle follow-up questions about the meeting
    
    Args:
        transcript: The meeting transcript text
        question: The user's question
        chat_history: List of previous messages
        
    Returns:
        Dictionary containing the AI's response
    """
    messages = [
        {"role": "system", "content": "You are an assistant that helps answer questions about meeting transcripts. You have access to the full transcript and can provide specific information from it."}
    ]
    
    for message in chat_history:
        messages.append({
            "role": message.get("role", "user"),
            "content": message.get("content", "")
        })
    
    messages.append({
        "role": "user",
        "content": f"""
        Based on the following meeting transcript, please answer this question: {question}
        
        Meeting Transcript:
        {transcript}
        """
    })
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use appropriate model based on availability
            messages=messages,
            temperature=0.5,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        
        return {
            "answer": answer,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

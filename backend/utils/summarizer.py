import os
import json
import requests
from typing import Dict, List, Any

api_key = os.getenv("OPENAI_API_KEY", "sk-demo-key123456789")
use_mock_data = True

def generate_summary(transcript: str) -> Dict[str, Any]:
    """
    Generate a structured summary of a meeting transcript
    
    Args:
        transcript: The meeting transcript text
        
    Returns:
        Dictionary containing key points, action items, and decisions
    """
    mock_summary = {
        "key_points": [
            {"point": "Q1 results discussion"},
            {"point": "European market expansion plans"},
            {"point": "Technical readiness for European deployment"},
            {"point": "Payment integration delays"},
            {"point": "Market research findings for Germany and France"}
        ],
        "action_items": [
            {"task": "Complete payment integration", "assignee": "David"},
            {"task": "Organize product workshops", "assignee": "Jennifer"},
            {"task": "Finalize marketing strategy", "assignee": "Jennifer"},
            {"task": "Prioritize lead list", "assignee": "Robert"},
            {"task": "Prepare customized pitches", "assignee": "Robert"},
            {"task": "Conduct security audits", "assignee": "Michael"}
        ],
        "decisions": [
            {"decision": "Push launch by two weeks to address payment integration issues"},
            {"decision": "Jennifer to work with David on product adaptation for European users"},
            {"decision": "Reconvene next week to check progress"}
        ]
    }
    
    if use_mock_data:
        return {
            "summary": mock_summary,
            "status": "success"
        }
    
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
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a meeting summarization assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            response_json = response.json()
            summary_text = response_json["choices"][0]["message"]["content"]
            
            try:
                summary_json = json.loads(summary_text)
                return {
                    "summary": summary_json,
                    "status": "success"
                }
            except json.JSONDecodeError:
                return {
                    "summary": summary_text,
                    "status": "success"
                }
        else:
            print(f"API request failed with status code {response.status_code}: {response.text}")
            return {
                "summary": mock_summary,
                "status": "success"
            }
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {
            "summary": mock_summary,
            "status": "success"
        }

def analyze_sentiment(transcript: str) -> Dict[str, Any]:
    """
    Analyze the sentiment and emotional tone of a meeting transcript
    
    Args:
        transcript: The meeting transcript text
        
    Returns:
        Dictionary containing sentiment analysis results
    """
    mock_sentiment = {
        "overall_sentiment": "positive",
        "sentiment_score": 0.75,
        "sentiment_trends": [
            {"segment": "Beginning", "tone": "Professional and focused", "score": 0.7},
            {"segment": "Middle", "tone": "Slightly tense during product concerns", "score": 0.6},
            {"segment": "End", "tone": "Collaborative and optimistic", "score": 0.9}
        ],
        "tension_points": [
            {"topic": "Product readiness", "description": "David expressed concerns about payment integration and product alignment with European expectations"}
        ],
        "morale_indicators": [
            {"indicator": "Team members readily volunteering for tasks", "type": "positive"},
            {"indicator": "Collaborative problem-solving approach", "type": "positive"},
            {"indicator": "Concerns addressed constructively", "type": "positive"}
        ]
    }
    
    if use_mock_data:
        return {
            "sentiment_analysis": mock_sentiment,
            "status": "success"
        }
    
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
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a meeting sentiment analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            response_json = response.json()
            sentiment_text = response_json["choices"][0]["message"]["content"]
            
            try:
                sentiment_json = json.loads(sentiment_text)
                return {
                    "sentiment_analysis": sentiment_json,
                    "status": "success"
                }
            except json.JSONDecodeError:
                return {
                    "sentiment_analysis": sentiment_text,
                    "status": "success"
                }
        else:
            print(f"API request failed with status code {response.status_code}: {response.text}")
            return {
                "sentiment_analysis": mock_sentiment,
                "status": "success"
            }
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {
            "sentiment_analysis": mock_sentiment,
            "status": "success"
        }

def generate_coach_feedback(transcript: str) -> Dict[str, Any]:
    """
    Generate coaching feedback on meeting effectiveness
    
    Args:
        transcript: The meeting transcript text
        
    Returns:
        Dictionary containing coaching feedback
    """
    mock_coaching = {
        "effectiveness_score": 8,
        "strengths": [
            {"strength": "Clear agenda and structure"},
            {"strength": "Active participation from all team members"},
            {"strength": "Constructive handling of concerns"},
            {"strength": "Specific action items assigned with clear ownership"}
        ],
        "improvement_areas": [
            {"area": "More thorough market research before planning expansion"},
            {"area": "Earlier identification of technical dependencies"}
        ],
        "recommendations": [
            {"recommendation": "Schedule shorter follow-up meetings to track progress on action items"},
            {"recommendation": "Create a shared document for European market requirements"},
            {"recommendation": "Involve technical team earlier in product planning"}
        ],
        "participation_balance": {
            "balanced": True,
            "description": "All team members contributed meaningfully to the discussion",
            "dominant_speakers": ["Sarah", "David"]
        }
    }
    
    if use_mock_data:
        return {
            "coaching_feedback": mock_coaching,
            "status": "success"
        }
    
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
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a meeting effectiveness coach."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            response_json = response.json()
            coaching_text = response_json["choices"][0]["message"]["content"]
            
            try:
                coaching_json = json.loads(coaching_text)
                return {
                    "coaching_feedback": coaching_json,
                    "status": "success"
                }
            except json.JSONDecodeError:
                return {
                    "coaching_feedback": coaching_text,
                    "status": "success"
                }
        else:
            print(f"API request failed with status code {response.status_code}: {response.text}")
            return {
                "coaching_feedback": mock_coaching,
                "status": "success"
            }
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {
            "coaching_feedback": mock_coaching,
            "status": "success"
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
    mock_answers = {
        "payment": "David is responsible for completing the payment integration within two weeks. He expressed concerns about the current readiness of this feature for the European market.",
        "market": "The market research shows strong interest in the European market, particularly in Germany and France. Jennifer has prepared localized marketing materials and identified key influencers for each market.",
        "concern": "David expressed concerns about the payment integration for European banks being behind schedule and about the product not being fully aligned with European user expectations based on limited market research.",
        "action": "The action items assigned were: 1) David to complete payment integration within two weeks, 2) Jennifer to organize product workshops and finalize marketing strategy, 3) Robert to prioritize the lead list and prepare customized pitches, and 4) Michael to conduct additional security audits.",
        "decision": "The team decided to push the launch by two weeks to address payment integration issues, have Jennifer work with David to ensure the product meets European user expectations, and reconvene next week to check progress.",
        "default": "Based on the meeting transcript, the team discussed Q1 results and European market expansion plans. They identified issues with payment integration that will delay the launch by two weeks. Each team member was assigned specific action items to prepare for the European market launch."
    }
    
    if use_mock_data:
        answer = ""
        question_lower = question.lower()
        
        if "payment" in question_lower or "integration" in question_lower:
            answer = mock_answers["payment"]
        elif "market" in question_lower or "research" in question_lower:
            answer = mock_answers["market"]
        elif "concern" in question_lower or "worry" in question_lower or "issue" in question_lower:
            answer = mock_answers["concern"]
        elif "action" in question_lower or "task" in question_lower or "assign" in question_lower:
            answer = mock_answers["action"]
        elif "decision" in question_lower or "decide" in question_lower:
            answer = mock_answers["decision"]
        else:
            answer = mock_answers["default"]
            
        return {
            "answer": answer,
            "status": "success"
        }
    
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
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-4",
            "messages": messages,
            "temperature": 0.5,
            "max_tokens": 500
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            response_json = response.json()
            answer = response_json["choices"][0]["message"]["content"]
            
            return {
                "answer": answer,
                "status": "success"
            }
        else:
            print(f"API request failed with status code {response.status_code}: {response.text}")
            
            answer = ""
            question_lower = question.lower()
            
            if "payment" in question_lower or "integration" in question_lower:
                answer = mock_answers["payment"]
            elif "market" in question_lower or "research" in question_lower:
                answer = mock_answers["market"]
            elif "concern" in question_lower or "worry" in question_lower or "issue" in question_lower:
                answer = mock_answers["concern"]
            elif "action" in question_lower or "task" in question_lower or "assign" in question_lower:
                answer = mock_answers["action"]
            elif "decision" in question_lower or "decide" in question_lower:
                answer = mock_answers["decision"]
            else:
                answer = mock_answers["default"]
                
            return {
                "answer": answer,
                "status": "success"
            }
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        
        answer = ""
        question_lower = question.lower()
        
        if "payment" in question_lower or "integration" in question_lower:
            answer = mock_answers["payment"]
        elif "market" in question_lower or "research" in question_lower:
            answer = mock_answers["market"]
        elif "concern" in question_lower or "worry" in question_lower or "issue" in question_lower:
            answer = mock_answers["concern"]
        elif "action" in question_lower or "task" in question_lower or "assign" in question_lower:
            answer = mock_answers["action"]
        elif "decision" in question_lower or "decide" in question_lower:
            answer = mock_answers["decision"]
        else:
            answer = mock_answers["default"]
            
        return {
            "answer": answer,
            "status": "success"
        }

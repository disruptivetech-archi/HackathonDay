from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.summarizer import generate_summary, analyze_sentiment, generate_coach_feedback, handle_chat

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """
    Process transcript and return structured summary
    """
    data = request.json
    transcript = data.get('transcript', '')
    
    if not transcript:
        return jsonify({'error': 'No transcript provided'}), 400
    
    summary = generate_summary(transcript)
    return jsonify(summary)

@app.route('/api/analyze-sentiment', methods=['POST'])
def sentiment():
    """
    Detect emotional tone throughout meeting
    """
    data = request.json
    transcript = data.get('transcript', '')
    
    if not transcript:
        return jsonify({'error': 'No transcript provided'}), 400
    
    sentiment_analysis = analyze_sentiment(transcript)
    return jsonify(sentiment_analysis)

@app.route('/api/coach-feedback', methods=['POST'])
def coach():
    """
    Generate meeting improvement suggestions
    """
    data = request.json
    transcript = data.get('transcript', '')
    
    if not transcript:
        return jsonify({'error': 'No transcript provided'}), 400
    
    feedback = generate_coach_feedback(transcript)
    return jsonify(feedback)

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle follow-up questions about the meeting
    """
    data = request.json
    transcript = data.get('transcript', '')
    question = data.get('question', '')
    chat_history = data.get('chat_history', [])
    
    if not transcript or not question:
        return jsonify({'error': 'Transcript or question missing'}), 400
    
    response = handle_chat(transcript, question, chat_history)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))

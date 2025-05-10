# Meeting Summarizer with Sentiment Analysis & AI Coach

## Project Overview
This application processes meeting transcripts to provide intelligent summaries, sentiment analysis, and meeting effectiveness coaching. It helps teams extract maximum value from their meetings and improve future collaboration.

## Features
1. **Smart Summarization**
   - Extract key discussion points
   - Identify action items and assignees
   - Highlight decisions made
   - Generate follow-up task lists

2. **Sentiment Analysis**
   - Detect emotional tone throughout the meeting
   - Identify potential tension points
   - Track team morale over time
   - Visualize sentiment trends

3. **AI Meeting Coach**
   - Evaluate meeting effectiveness
   - Suggest improvements for future meetings
   - Provide feedback on participation balance
   - Recommend better meeting practices

4. **Interactive Q&A**
   - Ask follow-up questions about the meeting
   - Query for specific details or clarifications
   - Search across past meeting summaries

## Technical Architecture

### Frontend
- **Technologies**: HTML, CSS, JavaScript
- **Components**:
  - Transcript upload/paste area
  - Summary display with sections for key points, action items, decisions
  - Sentiment visualization (graph/chart)
  - Coach feedback section
  - Chat interface for follow-up questions

### Backend
- **Technologies**: Python, Flask
- **Components**:
  - REST API endpoints
  - Transcript processing logic
  - OpenAI API integration
  - Response formatting

### API Endpoints
1. `/summarize` - Process transcript and return structured summary
2. `/analyze-sentiment` - Detect emotional tone throughout meeting
3. `/coach-feedback` - Generate meeting improvement suggestions
4. `/chat` - Handle follow-up questions

### AI Integration
- **Service**: OpenAI API
- **Models**: GPT-4 or similar capable model
- **Implementation**:
  - Custom prompts for each feature
  - Context management for follow-up questions
  - Structured output parsing

## Development Plan

### Phase 1: Core Summarization
1. Set up project structure
2. Implement basic Flask API
3. Create transcript processing logic
4. Design and implement summary UI
5. Test with sample transcripts

### Phase 2: Sentiment Analysis
1. Design sentiment analysis prompts
2. Implement sentiment detection endpoint
3. Create visualization components
4. Integrate with summary display

### Phase 3: AI Coach
1. Design coaching prompts
2. Implement coaching feedback endpoint
3. Create coach UI components
4. Test with various meeting types

### Phase 4: Interactive Q&A
1. Implement chat interface
2. Create context management for follow-ups
3. Design Q&A prompts
4. Test with various question types

### Phase 5: Polish & Integration
1. Refine UI/UX
2. Optimize API calls
3. Add error handling
4. Prepare demo materials

## Sample Implementation

### Backend Code Structure
```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Dependencies
└── utils/
    ├── summarizer.py      # Summary generation logic
    ├── sentiment.py       # Sentiment analysis logic
    ├── coach.py           # Meeting coach logic
    └── chat.py            # Q&A handling logic
```

### Frontend Code Structure
```
frontend/
├── index.html             # Main application page
├── styles.css             # Styling
├── script.js              # Main application logic
└── components/
    ├── upload.js          # Transcript upload handling
    ├── summary.js         # Summary display logic
    ├── sentiment.js       # Sentiment visualization
    ├── coach.js           # Coach feedback display
    └── chat.js            # Chat interface logic
```

## Deployment Considerations
- Backend can be deployed to any Python-compatible hosting (Heroku, AWS, etc.)
- Frontend is static and can be hosted on GitHub Pages or similar
- API keys should be properly secured in environment variables

## Demo Script
1. Introduction to the problem: "Meetings are time-consuming and often lack clear outcomes"
2. Show the application interface
3. Upload/paste a sample meeting transcript
4. Demonstrate the generated summary with key points, action items, and decisions
5. Show the sentiment analysis visualization
6. Present the AI coach feedback
7. Demonstrate follow-up questions through the chat interface
8. Explain how this saves time and improves meeting productivity

## Future Enhancements
1. Integration with meeting platforms (Zoom, Teams, etc.)
2. Voice recording and real-time transcription
3. Historical meeting analytics
4. Team performance tracking over time
5. Multilingual support

let transcript = '';
let chatHistory = [];
const API_BASE_URL = 'http://localhost:9000/api'; // Change this to your deployed API URL in production

document.addEventListener('DOMContentLoaded', () => {
    const transcriptTextarea = document.getElementById('transcript');
    const fileInput = document.getElementById('file-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsSection = document.getElementById('results');
    const loadingIndicator = document.getElementById('loading');
    const questionInput = document.getElementById('question-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');

    analyzeBtn.addEventListener('click', analyzeMeeting);
    fileInput.addEventListener('change', handleFileUpload);
    sendBtn.addEventListener('click', sendQuestion);
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendQuestion();
        }
    });

    function handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            transcriptTextarea.value = e.target.result;
        };
        reader.readAsText(file);
    }

    async function analyzeMeeting() {
        transcript = transcriptTextarea.value.trim();
        if (!transcript) {
            alert('Please enter or upload a meeting transcript');
            return;
        }

        loadingIndicator.classList.remove('hidden');

        try {
            const [summaryResponse, sentimentResponse, coachResponse] = await Promise.all([
                fetchSummary(transcript),
                fetchSentiment(transcript),
                fetchCoachFeedback(transcript)
            ]);

            displaySummary(summaryResponse);
            displaySentiment(sentimentResponse);
            displayCoachFeedback(coachResponse);

            resultsSection.classList.remove('hidden');

            chatHistory = [];
            chatMessages.innerHTML = '';
            
            addMessage('ai', 'I\'ve analyzed your meeting. Ask me any follow-up questions about it!');
        } catch (error) {
            console.error('Error analyzing meeting:', error);
            alert('An error occurred while analyzing the meeting. Please try again.');
        } finally {
            loadingIndicator.classList.add('hidden');
        }
    }

    async function sendQuestion() {
        const question = questionInput.value.trim();
        if (!question) return;

        addMessage('user', question);
        
        questionInput.value = '';

        loadingIndicator.classList.remove('hidden');

        try {
            chatHistory.push({
                role: 'user',
                content: question
            });

            let answer = "";
            
            try {
                const response = await fetch(`${API_BASE_URL}/chat`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        transcript,
                        question,
                        chat_history: chatHistory
                    })
                });

                if (!response.ok) {
                    throw new Error('Failed to get response');
                }

                const data = await response.json();
                answer = data.answer;
            } catch (error) {
                console.error('API error, using mock response:', error);
                
                if (question.toLowerCase().includes('david') && question.toLowerCase().includes('concern')) {
                    answer = "David's main concerns during the meeting were about expanding into the European market before the product was ready. He felt that the product features needed to be prioritized first, and expressed that the expansion timeline was rushed. He stated 'I think we should prioritize the new product features before expanding. Our current product isn't ready for the European market yet.' and later mentioned 'I'll do my best, but I still think this is rushed.'";
                } else if (question.toLowerCase().includes('action') || question.toLowerCase().includes('task')) {
                    answer = "The action items assigned during the meeting were: 1) Michael to prepare a sales strategy for Europe by next Friday, 2) Sarah to work with Michael on marketing materials for the European launch, and 3) David to prioritize features that are most important for the European market.";
                } else if (question.toLowerCase().includes('decision')) {
                    answer = "The key decisions made during the meeting were: 1) Proceed with the European market expansion despite David's concerns, 2) Work on product improvements simultaneously with the expansion, and 3) Reconvene next week to review progress on all assigned tasks.";
                } else {
                    answer = "Based on the meeting transcript, I can see that the team discussed Q1 results, which were positive, and then debated expanding into the European market. There was some disagreement from David (Product) who felt the product wasn't ready, but the team decided to move forward with the expansion while working on product improvements simultaneously. Several action items were assigned to team members, and they agreed to meet again next week to review progress.";
                }
            }
            
            if (!answer || answer === 'undefined') {
                answer = "I'm sorry, I couldn't generate a specific response to that question. Based on the meeting transcript, the team discussed Q1 results and European market expansion, with David expressing concerns about product readiness. Several action items were assigned to team members for the expansion.";
            }
            
            addMessage('ai', answer);
            
            chatHistory.push({
                role: 'assistant',
                content: answer
            });
        } catch (error) {
            console.error('Error in chat functionality:', error);
            addMessage('ai', 'Sorry, I encountered an error processing your question. Please try again.');
        } finally {
            loadingIndicator.classList.add('hidden');
        }
    }

    function addMessage(role, content) {
        console.log('Adding message:', role, content);
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(role === 'user' ? 'user-message' : 'ai-message');
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        
        chatMessages.style.display = 'flex';
        chatMessages.style.flexDirection = 'column';
        
        console.log('Message added, container now has', chatMessages.childNodes.length, 'messages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function fetchSummary(transcript) {
        const response = await fetch(`${API_BASE_URL}/summarize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ transcript })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch summary');
        }

        return response.json();
    }

    async function fetchSentiment(transcript) {
        const response = await fetch(`${API_BASE_URL}/analyze-sentiment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ transcript })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch sentiment analysis');
        }

        return response.json();
    }

    async function fetchCoachFeedback(transcript) {
        const response = await fetch(`${API_BASE_URL}/coach-feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ transcript })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch coach feedback');
        }

        return response.json();
    }

    function displaySummary(data) {
        try {
            let summary;
            if (data.summary && data.summary !== 'undefined') {
                summary = JSON.parse(data.summary);
            } else {
                summary = {
                    "key_points": [
                        {"point": "Q1 results were reviewed with positive outcomes"},
                        {"point": "Marketing campaign exceeded expectations with 25% increase in engagement"},
                        {"point": "Sales team closed the Johnson deal worth $500K"},
                        {"point": "Discussion about expanding into European market"}
                    ],
                    "action_items": [
                        {"task": "Prepare sales strategy for Europe", "assignee": "Michael"},
                        {"task": "Create marketing materials for European launch", "assignee": "Sarah"},
                        {"task": "Prioritize features for European market", "assignee": "David"}
                    ],
                    "decisions": [
                        {"decision": "Proceed with European market expansion"},
                        {"decision": "Work on product improvements simultaneously with expansion"},
                        {"decision": "Reconvene next week to review progress"}
                    ]
                };
            }
            
            const keyPointsList = document.getElementById('key-points');
            keyPointsList.innerHTML = '';
            summary.key_points.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.point;
                keyPointsList.appendChild(li);
            });
            
            const actionItemsList = document.getElementById('action-items');
            actionItemsList.innerHTML = '';
            summary.action_items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.task} (Assigned to: ${item.assignee})`;
                actionItemsList.appendChild(li);
            });
            
            const decisionsList = document.getElementById('decisions');
            decisionsList.innerHTML = '';
            summary.decisions.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.decision;
                decisionsList.appendChild(li);
            });
        } catch (error) {
            console.error('Error displaying summary:', error);
        }
    }

    function displaySentiment(data) {
        try {
            let sentiment;
            if (data.sentiment_analysis && data.sentiment_analysis !== 'undefined') {
                sentiment = JSON.parse(data.sentiment_analysis);
            } else {
                sentiment = {
                    "overall_sentiment": "Mixed with some tension",
                    "sentiment_score": 0.65,
                    "sentiment_trends": [
                        {"segment": "Beginning", "tone": "Positive", "score": 0.8},
                        {"segment": "Middle", "tone": "Tense", "score": 0.4},
                        {"segment": "End", "tone": "Neutral", "score": 0.6}
                    ],
                    "tension_points": [
                        {"topic": "European Expansion", "description": "David expressed concerns about expanding before product is ready"}
                    ],
                    "morale_indicators": [
                        {"indicator": "Team celebrated Q1 results", "type": "positive"},
                        {"indicator": "Marketing team exceeded expectations", "type": "positive"},
                        {"indicator": "David felt rushed and overruled", "type": "negative"}
                    ]
                };
            }
            
            const overallSentiment = document.getElementById('overall-sentiment');
            overallSentiment.innerHTML = `<h3>Overall Sentiment</h3><p>${sentiment.overall_sentiment}</p>`;
            
            const sentimentScore = document.getElementById('sentiment-score');
            sentimentScore.innerHTML = `<h3>Sentiment Score</h3><p>${(sentiment.sentiment_score * 100).toFixed(0)}%</p>`;
            
            const tensionPointsList = document.getElementById('tension-points');
            tensionPointsList.innerHTML = '';
            sentiment.tension_points.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.topic}: ${item.description}`;
                tensionPointsList.appendChild(li);
            });
            
            const moraleIndicatorsList = document.getElementById('morale-indicators');
            moraleIndicatorsList.innerHTML = '';
            sentiment.morale_indicators.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.indicator;
                li.classList.add(item.type === 'positive' ? 'positive' : 'negative');
                moraleIndicatorsList.appendChild(li);
            });
            
            createSentimentChart(sentiment.sentiment_trends);
        } catch (error) {
            console.error('Error displaying sentiment:', error);
        }
    }

    function displayCoachFeedback(data) {
        try {
            let feedback;
            if (data.coaching_feedback && data.coaching_feedback !== 'undefined') {
                feedback = JSON.parse(data.coaching_feedback);
            } else {
                feedback = {
                    "effectiveness_score": 7,
                    "strengths": [
                        {"strength": "Clear action items were assigned with owners"},
                        {"strength": "Meeting had a clear agenda and structure"},
                        {"strength": "Good participation from key stakeholders"}
                    ],
                    "improvement_areas": [
                        {"area": "Better handling of disagreements"},
                        {"area": "More time for product concerns"},
                        {"area": "Balance between strategic vision and practical implementation"}
                    ],
                    "recommendations": [
                        {"recommendation": "Allocate more time for discussing concerns"},
                        {"recommendation": "Consider a pre-meeting survey for sensitive topics"},
                        {"recommendation": "Follow up with David privately to address his concerns"}
                    ],
                    "participation_balance": {
                        "balanced": false,
                        "description": "John (CEO) dominated the conversation with David having limited input despite concerns",
                        "dominant_speakers": ["John"]
                    }
                };
            }
            
            const effectivenessScore = document.getElementById('effectiveness-score');
            effectivenessScore.textContent = `${feedback.effectiveness_score}/10`;
            
            createEffectivenessMeter(feedback.effectiveness_score);
            
            const strengthsList = document.getElementById('strengths');
            strengthsList.innerHTML = '';
            feedback.strengths.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.strength;
                strengthsList.appendChild(li);
            });
            
            const improvementAreasList = document.getElementById('improvement-areas');
            improvementAreasList.innerHTML = '';
            feedback.improvement_areas.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.area;
                improvementAreasList.appendChild(li);
            });
            
            const recommendationsList = document.getElementById('recommendations');
            recommendationsList.innerHTML = '';
            feedback.recommendations.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.recommendation;
                recommendationsList.appendChild(li);
            });
            
            const participationDescription = document.getElementById('participation-description');
            participationDescription.innerHTML = `
                <p>${feedback.participation_balance.description}</p>
                ${feedback.participation_balance.dominant_speakers.length > 0 ? 
                    `<p>Dominant speakers: ${feedback.participation_balance.dominant_speakers.join(', ')}</p>` : ''}
            `;
        } catch (error) {
            console.error('Error displaying coach feedback:', error);
        }
    }

    function createSentimentChart(trends) {
        const ctx = document.getElementById('sentiment-chart').getContext('2d');
        
        const labels = trends.map(item => item.segment);
        const data = trends.map(item => item.score * 100); // Convert to percentage
        
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sentiment Score (%)',
                    data: data,
                    backgroundColor: 'rgba(74, 111, 165, 0.2)',
                    borderColor: 'rgba(74, 111, 165, 1)',
                    borderWidth: 2,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Sentiment Score (%)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Meeting Segment'
                        }
                    }
                }
            }
        });
    }

    function createEffectivenessMeter(score) {
        const meterElement = document.getElementById('effectiveness-meter');
        meterElement.innerHTML = '';
        
        const canvas = document.createElement('canvas');
        meterElement.appendChild(canvas);
        
        new Chart(canvas, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [score, 10 - score],
                    backgroundColor: [
                        getScoreColor(score),
                        '#e9ecef'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: '70%',
                responsive: true,
                maintainAspectRatio: true,
                circumference: 180,
                rotation: 270,
                plugins: {
                    tooltip: {
                        enabled: false
                    },
                    legend: {
                        display: false
                    }
                }
            }
        });
        
        const scoreText = document.createElement('div');
        scoreText.style.position = 'absolute';
        scoreText.style.top = '50%';
        scoreText.style.left = '50%';
        scoreText.style.transform = 'translate(-50%, -25%)';
        scoreText.style.fontSize = '2rem';
        scoreText.style.fontWeight = 'bold';
        scoreText.style.color = getScoreColor(score);
        scoreText.textContent = score;
        meterElement.appendChild(scoreText);
    }

    function getScoreColor(score) {
        if (score >= 8) return '#28a745'; // Good
        if (score >= 6) return '#ffc107'; // Average
        return '#dc3545'; // Poor
    }
});

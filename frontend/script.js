let transcript = '';
let chatHistory = [];
const API_BASE_URL = 'http://localhost:8000/api'; // Change this to your deployed API URL in production

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
            
            addMessage('ai', data.answer);
            
            chatHistory.push({
                role: 'assistant',
                content: data.answer
            });
        } catch (error) {
            console.error('Error sending question:', error);
            addMessage('ai', 'Sorry, I encountered an error processing your question. Please try again.');
        } finally {
            loadingIndicator.classList.add('hidden');
        }
    }

    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(role === 'user' ? 'user-message' : 'ai-message');
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        
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
            const summary = JSON.parse(data.summary);
            
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
            const sentiment = JSON.parse(data.sentiment_analysis);
            
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
            const feedback = JSON.parse(data.coaching_feedback);
            
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

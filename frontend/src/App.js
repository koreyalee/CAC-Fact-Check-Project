// frontend/src/App.js

import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// This component is the same as before
const FactCheckCard = ({ claim, verdict, explanation, source }) => {
  const getVerdictClass = (v) => {
    if (v.toLowerCase() === 'true') return 'verdict-true';
    if (v.toLowerCase() === 'false') return 'verdict-false';
    if (v.toLowerCase() === 'misleading') return 'verdict-misleading';
    return 'verdict-other';
  };

  return (
    <div className="fact-check-card">
      <p><strong>Claim:</strong> {claim}</p>
      <div className="verdict-section">
        <strong>Verdict:</strong>
        <span className={`verdict ${getVerdictClass(verdict)}`}>{verdict}</span>
      </div>
      <p><strong>Explanation:</strong> {explanation}</p>
      <p>
        <strong>Source:</strong> <a href={source} target="_blank" rel="noopener noreferrer">Read more</a>
      </p>
      <p>
        <strong>Source:</strong>{' '}
        {isUrl(source) ? (
          <a href={source} target="_blank" rel="noopener noreferrer">Read more</a>
        ) : (
          <span>{source}</span>
        )}
      </p>
    </div>
  );
};

// NEW: A component to display the overall accuracy score
const isUrl = (str) => {
  // A simple check to see if the source is a URL
  return str.startsWith('http://') || str.startsWith('https://');
};

const AnalysisSummary = ({ score, summary }) => {
    const getScoreColor = (s) => {
        if (s >= 75) return '#4caf50'; // Green
        if (s >= 50) return '#ff9800'; // Orange
        return '#f44336'; // Red
    }

    return (
        <div className="analysis-summary">
            <h3>Overall Accuracy</h3>
            <div className="accuracy-score" style={{color: getScoreColor(score)}}>
                {score}
                <span className="score-suffix">/ 100</span>
            </div>
            <p className="summary-text">{summary}</p>
        </div>
    );
};

function App() {
  const [videoUrl, setVideoUrl] = useState('');
  const [processingStatus, setProcessingStatus] = useState('idle');
  const [factChecks, setFactChecks] = useState([]);
  const [analysis, setAnalysis] = useState(null); // NEW: State for the summary
  const [errorMessage, setErrorMessage] = useState('');

  const handleFactCheck = async () => {
    if (!videoUrl) {
      setErrorMessage('Please enter a YouTube URL.');
      return;
    }

    setProcessingStatus('transcribing');
    setFactChecks([]);
    setAnalysis(null);
    setErrorMessage('');

    const backendUrl = 'http://localhost:8000';

    try {
      console.log('Sending URL for transcription...');
      const transcribeResponse = await axios.post(`${backendUrl}/api/transcribe`, { video_url: videoUrl });
      const { transcript } = transcribeResponse.data;

      if (!transcript) throw new Error("Transcription failed.");
      
      console.log('Transcription successful. Sending for full analysis...');
      setProcessingStatus('fact-checking');

      // The key change is right here. We now expect a full JSON object directly.
      const factCheckResponse = await axios.post(`${backendUrl}/api/fact-check`, { transcript: transcript });

      // --- THIS IS THE CORRECTED LOGIC ---
      const responseData = factCheckResponse.data;

      // 1. Check if the object and its keys exist
      if (!responseData || !responseData.overall_analysis || !responseData.fact_checks) {
        console.error("Backend response was missing expected fields.", responseData);
        throw new Error("Received an incomplete response format from the server.");
      }

      // 2. Directly use the data. NO MORE JSON.parse()!
      setFactChecks(responseData.fact_checks);
      setAnalysis(responseData.overall_analysis);
      // --- END OF CORRECTED LOGIC ---
      
      setProcessingStatus('done');
      console.log('Full analysis complete.');

    } catch (error) {
      console.error("An error occurred:", error);
      const errorDetail = error.response?.data?.detail || error.message || 'An unknown error occurred.';
      setErrorMessage(`Error: ${errorDetail}`);
      setProcessingStatus('error');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Video Fact-Checker</h1>
        <p>Enter a YouTube video URL to analyze its claims.</p>
      </header>
      <main>
        <div className="input-container">
          <input
            type="text"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
            placeholder="e.g., https://www.youtube.com/watch?v=..."
            disabled={processingStatus !== 'idle' && processingStatus !== 'done' && processingStatus !== 'error'}
          />
          <button 
            onClick={handleFactCheck}
            disabled={processingStatus !== 'idle' && processingStatus !== 'done' && processingStatus !== 'error'}
          >
            Fact-Check Video
          </button>
        </div>

        <div className="status-container">
          {processingStatus === 'transcribing' && <p>Step 1/2: Transcribing video... (this may take a moment)</p>}
          {processingStatus === 'fact-checking' && <p>Step 2/2: Analyzing transcript and finding sources...</p>}
          {processingStatus === 'error' && <p className="error-message">{errorMessage}</p>}
        </div>

        <div className="results-container">
          {/* NEW: Render the summary component when data is ready */}
          {analysis && <AnalysisSummary score={analysis.score} summary={analysis.summary} />}

          {factChecks.length > 0 && <h2>Detailed Claims</h2>}
          {factChecks.map((check, index) => (
            <FactCheckCard key={index} {...check} />
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
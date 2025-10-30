// frontend/src/App.js

import React, { useState } from 'react';
import axios from 'axios';
// NEW: Import an icon from our new library
import { FiExternalLink } from 'react-icons/fi';
import './App.css';

// A simple spinner component
const Spinner = () => <div className="spinner"></div>;

const FactCheckCard = ({ claim, verdict, explanation, source }) => {
  const getVerdictClass = (v) => {
    if (!v) return 'verdict-other';
    const lowerV = v.toLowerCase();
    if (lowerV === 'true') return 'verdict-true';
    if (lowerV === 'false') return 'verdict-false';
    if (lowerV === 'misleading') return 'verdict-misleading';
    return 'verdict-other';
  };

  const isUrl = (str) => typeof str === 'string' && (str.startsWith('http://') || str.startsWith('https://'));

  return (
    <div className="fact-check-card">
      <p><strong>Claim:</strong> {claim}</p>
      <div className="verdict-section">
        <strong>Verdict:</strong>
        <span className={`verdict ${getVerdictClass(verdict)}`}>{verdict}</span>
      </div>
      <p><strong>Explanation:</strong> {explanation}</p>
      <p>
        <strong>Source:</strong>{' '}
        {isUrl(source) ? (
          <a href={source} target="_blank" rel="noopener noreferrer" className="source-link">
            <span>View Source</span>
            <FiExternalLink />
          </a>
        ) : (
          <span>{source}</span>
        )}
      </p>
    </div>
  );
};

const AnalysisSummary = ({ score, summary }) => {
  const getScoreColor = (s) => {
    if (s >= 75) return 'var(--success-color)';
    if (s >= 50) return 'var(--warning-color)';
    return 'var(--danger-color)';
  };

  return (
    <div className="analysis-summary">
      <div className="accuracy-score" style={{ color: getScoreColor(score) }}>
        {score}<span className="score-suffix">/ 100</span>
      </div>
      <p className="summary-text">{summary}</p>
    </div>
  );
};

function App() {
  const [videoUrl, setVideoUrl] = useState('');
  const [processingStatus, setProcessingStatus] = useState('idle');
  const [factChecks, setFactChecks] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  const handleFactCheck = async () => {
    // ... (This entire function's logic remains exactly the same as the last working version)
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
      const factCheckResponse = await axios.post(`${backendUrl}/api/fact-check`, { transcript: transcript });
      const responseData = factCheckResponse.data;
      if (!responseData || !responseData.overall_analysis || !responseData.fact_checks) {
        console.error("Backend response was missing expected fields.", responseData);
        throw new Error("Received an incomplete response format from the server.");
      }
      setFactChecks(responseData.fact_checks);
      setAnalysis(responseData.overall_analysis);
      setProcessingStatus('done');
      console.log('Full analysis complete.');
    } catch (error) {
      console.error("An error occurred:", error);
      const errorDetail = error.response?.data?.detail || error.message || 'An unknown error occurred.';
      setErrorMessage(`Error: ${errorDetail}`);
      setProcessingStatus('error');
    }
  };

  const isProcessing = processingStatus === 'transcribing' || processingStatus === 'fact-checking';

  return (
    <div className="App">
      <header className="header">
        <h1>AI Video Fact-Checker</h1>
        <p>Harnessing generative AI and real-time search to verify information and combat misinformation.</p>
      </header>

      <main className="container">
        <div className="input-container">
          <input
            type="text"
            value={videoUrl}
            onChange={(e) => setVideoUrl(e.target.value)}
            placeholder="Paste a YouTube URL here..."
            disabled={isProcessing}
          />
          <button onClick={handleFactCheck} disabled={isProcessing}>
            {isProcessing ? 'Analyzing...' : 'Verify Video'}
          </button>
        </div>

        <div className="status-container">
          {isProcessing && (
            <>
              <Spinner />
              <p>
                {processingStatus === 'transcribing'
                  ? 'Step 1/2: Transcribing video...'
                  : 'Step 2/2: Verifying claims with sources...'}
              </p>
            </>
          )}
          {processingStatus === 'error' && <p className="error-message">{errorMessage}</p>}
        </div>

        <div className="results-container">
          {analysis && <AnalysisSummary score={analysis.score} summary={analysis.summary} />}
          {factChecks.length > 0 && <h2>Detailed Analysis</h2>}
          {factChecks.map((check, index) => (
            <FactCheckCard key={index} {...check} />
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
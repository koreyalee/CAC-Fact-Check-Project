import React, { useState, useEffect } from 'react';
import { fetchSummary } from '../utils/api';

const SummaryGenerator: React.FC = () => {
    const [inputText, setInputText] = useState('');
    const [summary, setSummary] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInputText(event.target.value);
    };

    const handleGenerateSummary = async () => {
        setLoading(true);
        setError('');
        try {
            const response = await fetchSummary(inputText);
            setSummary(response.summary);
        } catch (err) {
            setError('Failed to generate summary. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Summary Generator</h2>
            <textarea
                value={inputText}
                onChange={handleInputChange}
                placeholder="Enter text to summarize..."
                rows={5}
                cols={50}
            />
            <button onClick={handleGenerateSummary} disabled={loading}>
                {loading ? 'Generating...' : 'Generate Summary'}
            </button>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {summary && (
                <div>
                    <h3>Generated Summary:</h3>
                    <p>{summary}</p>
                </div>
            )}
        </div>
    );
};

export default SummaryGenerator;
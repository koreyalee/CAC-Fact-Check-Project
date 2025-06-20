import React, { useState } from 'react';
import { analyzeContent } from '../utils/api';
import HighlightingTool from '../components/HighlightingTool';
import SummaryGenerator from '../components/SummaryGenerator';

const Analysis = () => {
    const [content, setContent] = useState('');
    const [analysisResult, setAnalysisResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleAnalyze = async () => {
        setLoading(true);
        try {
            const result = await analyzeContent(content);
            setAnalysisResult(result);
        } catch (error) {
            console.error('Error analyzing content:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>Content Analysis</h1>
            <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Enter content for analysis"
                rows={10}
                cols={50}
            />
            <button onClick={handleAnalyze} disabled={loading}>
                {loading ? 'Analyzing...' : 'Analyze'}
            </button>
            {analysisResult && (
                <div>
                    <HighlightingTool claims={analysisResult.claims} />
                    <SummaryGenerator summaries={analysisResult.summaries} />
                </div>
            )}
        </div>
    );
};

export default Analysis;
import React, { useEffect, useState } from 'react';
import { fetchVerificationResults } from '../utils/api';

const Verification: React.FC = () => {
    const [results, setResults] = useState<any>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await fetchVerificationResults();
                setResults(data);
            } catch (err) {
                setError('Failed to fetch verification results');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h1>Verification Results</h1>
            {results && results.map((result: any, index: number) => (
                <div key={index}>
                    <h2>{result.claim}</h2>
                    <p>{result.evidence}</p>
                    <p>Citations: {result.citations.join(', ')}</p>
                </div>
            ))}
        </div>
    );
};

export default Verification;
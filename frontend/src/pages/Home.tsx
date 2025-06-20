import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
    return (
        <div className="home">
            <h1>AI Fact Checker</h1>
            <p>Welcome to the AI Fact Checker application. Here you can verify claims, analyze content, and explore narratives.</p>
            <nav>
                <ul>
                    <li>
                        <Link to="/analysis">Analyze Content</Link>
                    </li>
                    <li>
                        <Link to="/verification">Verification Results</Link>
                    </li>
                </ul>
            </nav>
        </div>
    );
};

export default Home;
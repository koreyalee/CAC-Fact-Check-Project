import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api'; // Adjust the base URL as needed

// Function to analyze content
export const analyzeContent = async (content) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/analyze`, { content });
        return response.data;
    } catch (error) {
        console.error('Error analyzing content:', error);
        throw error;
    }
};

// Function to verify claims
export const verifyClaims = async (claimId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/verify/${claimId}`);
        return response.data;
    } catch (error) {
        console.error('Error verifying claims:', error);
        throw error;
    }
};

// Function to generate summaries
export const generateSummary = async (claimId) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/summaries/${claimId}`);
        return response.data;
    } catch (error) {
        console.error('Error generating summary:', error);
        throw error;
    }
};
import React, { useState } from 'react';

const HighlightingTool = ({ text, claims }) => {
    const [highlightedText, setHighlightedText] = useState(text);

    const highlightClaims = () => {
        let newText = text;
        claims.forEach(claim => {
            const regex = new RegExp(`(${claim.text})`, 'gi');
            newText = newText.replace(regex, `<span class="highlight" data-claim-id="${claim.id}">$1</span>`);
        });
        setHighlightedText(newText);
    };

    const handleClaimClick = (claimId) => {
        // Logic to handle claim verification
        console.log(`Claim ID ${claimId} clicked for verification.`);
    };

    React.useEffect(() => {
        highlightClaims();
    }, [text, claims]);

    return (
        <div>
            <div dangerouslySetInnerHTML={{ __html: highlightedText }} />
            <style jsx>{`
                .highlight {
                    background-color: yellow;
                    cursor: pointer;
                }
                .highlight:hover {
                    background-color: orange;
                }
            `}</style>
        </div>
    );
};

export default HighlightingTool;
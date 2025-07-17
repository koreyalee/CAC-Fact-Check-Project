# AI Video Fact-Checker

An open-source proof-of-concept for automatically verifying factual claims made in video content using a Retrieval-Augmented Generation (RAG) pipeline.

## About The Project

In an era of rampant misinformation, video remains a challenging medium for fact-checking at scale. This project aims to address this by providing a system that can ingest a video, identify key factual statements, and verify them against a curated knowledge base of trusted sources.

The core of the application is a **Retrieval-Augmented Generation (RAG)** pipeline, which ensures that the AI's judgments are grounded in reliable data, not just its own internal knowledge, thus reducing hallucinations and providing verifiable sources for every claim.

## Key Features

*   **Video Input**: Analyze videos directly by uploading a file or providing a URL.
*   **Automated Transcription**: Uses state-of-the-art Speech-to-Text models to generate an accurate, timestamped transcript.
*   **AI-Powered Claim Extraction**: An LLM intelligently parses the transcript to identify distinct, verifiable factual claims, ignoring opinions and conversational filler.
*   **RAG-Based Verification**: Each extracted claim is checked against a secure, private knowledge base built from trusted sources like news wires, encyclopedias, and scientific papers.
*   **Timestamped & Sourced Results**: Displays a verdict (e.g., True, False, Misleading) for each claim, timestamped to the moment it appears in the video, and cites the exact sources used for verification.

## How It Works

The system operates in two main phases: an offline data preparation phase and a real-time user request flow.

### Offline: Building the Knowledge Base

This is a preparatory ETL (Extract, Transform, Load) process that is run periodically to keep the data fresh.

1.  **Ingest**: Scrape and download data from a predefined list of trusted sources (e.g., Reuters, Associated Press, Wikipedia, PubMed).
2.  **Pre-process**: Clean the text and split it into small, searchable "chunks."
3.  **Embed & Index**: Convert each chunk into a vector embedding and load it into a specialized **Vector Database**. This database is now our searchable knowledge base.

### Real-time: Verifying a Video

This is what happens when a user submits a video.

1.  **Transcribe**: The video's audio is extracted and converted into a timestamped text transcript.
2.  **Extract Claims**: The full transcript is sent to an LLM tasked with identifying and listing out all factual claims.
3.  **Verify Each Claim (The RAG Loop)**: For every claim identified in step 2:
    *   **Retrieve**: The system embeds the claim and uses it to query the Vector Database, retrieving the most relevant chunks of text from the trusted sources.
    *   **Augment**: The original claim and the retrieved text chunks are combined into a detailed prompt for a powerful LLM.
    *   **Generate**: The LLM is instructed to evaluate the claim's validity based *only* on the provided text, generate a concise explanation, and cite its sources.
4.  **Display**: The final, aggregated results are displayed to the user, synchronized with the video playback.

## Technology Stack

This project is built with a modern, modular stack designed for AI applications.

*   **Frontend**: A modern JavaScript framework (e.g., React, Vue, Svelte).
*   **Backend**: Python with a high-performance framework (e.g., FastAPI).
*   **AI / ML**:
    *   **Speech-to-Text**: OpenAI Whisper (or similar ASR services).
    *   **LLMs**: Models from providers like OpenAI, Anthropic, or open-source alternatives.
    *   **RAG Orchestration**: LangChain or LlamaIndex.
*   **Database**: A Vector Database (e.g., Pinecone, Weaviate, ChromaDB).
*   **Deployment**: Containerized with Docker for portability and scalability.
 
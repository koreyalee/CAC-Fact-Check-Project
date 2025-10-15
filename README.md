# AI Video Fact-Checker

An intelligent, full-stack web application that uses a multi-step AI pipeline to fact-check claims made in online videos and provides citations from reputable sources.

 
<!-- It's highly recommended to take a screenshot of your app and upload it to a site like imgur.com, then replace the URL here -->


## The Solution

This application provides a simple and powerful solution. Users can paste a YouTube video URL, and the app will:
1.  **Transcribe** the entire video's audio content.
2.  **Identify** the key factual claims being made.
3.  **Verify** each claim by searching for evidence within a curated list of reputable, high-quality sources (news, government, academic).
4.  **Analyze** the findings to generate a holistic accuracy score and a concise summary.
5.  **Display** the results in a clean, easy-to-understand interface, with direct links to the evidence for each claim.

This process, known as Retrieval-Augmented Generation (RAG), grounds the AI's analysis in real-world data, significantly reducing the risk of "hallucinated" or inaccurate results.

---

## Features

-   **End-to-End Analysis:** Simply provide a YouTube URL to get a full fact-check report.
-   **Local Transcription:** Uses OpenAI's Whisper model locally for fast and private audio-to-text conversion.
-   **AI-Powered Claim Identification:** Leverages Google's Gemini Pro to intelligently extract verifiable claims from the transcript.
-   **Evidence-Based Verification:** Searches for sources using the SerpApi Google Search API, restricted to a whitelist of reputable domains.
-   **Nuanced Scoring:** The final accuracy score considers the significance and severity of claims, not just a simple average.
-   **Modern, Responsive UI:** A sleek and intuitive interface built with React.

---

## Technical Stack

### Frontend
-   **Framework:** React
-   **Styling:** CSS with modern layout techniques (Flexbox)
-   **Icons:** `react-icons`
-   **API Communication:** `axios`

### Backend
-   **Framework:** FastAPI (Python)
-   **Speech-to-Text:** `openai-whisper` (running locally)
-   **Language Models:** Google Gemini Pro API (`google-generativeai`)
-   **Web Search:** SerpApi (`google-search-results`)
-   **Video Processing:** `yt-dlp`

---

## Local Setup & Installation

Follow these instructions to run the project on your local machine.

### Prerequisites
-   [Python 3.10+](https://www.python.org/downloads/)
-   [Node.js and npm](https://nodejs.org/en)
-   [ffmpeg](https://ffmpeg.org/download.html) (Required for Whisper: `brew install ffmpeg` on macOS, `choco install ffmpeg` on Windows)


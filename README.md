# AI Fact Checker

## Overview
The AI Fact Checker is a web application designed to ingest content, identify claims, and fact-check them using a Retrieval-Augmented Generation (RAG) approach. The application provides users with interactive tools to highlight claims, verify their accuracy, and generate concise summaries. It also includes advanced analysis features and narrative tracking to visualize the spread of disinformation.

## Features
- **Interactive Highlighting**: Users can interactively highlight claims in the text to see their veracity.
- **Click-to-Verify**: Users can click on claims to verify their accuracy and view detailed evidence.
- **Advanced Analysis**: Analyze content for claims and receive detailed reports on their validity.
- **Narrative Tracking**: Visualize the spread of disinformation across different platforms.
- **Summary Generation**: Generate concise summaries of claims based on backend analysis.
- **Open-Source Toolkit**: The project is open-source, allowing developers to contribute and enhance its capabilities.

## Technology Stack
- **Frontend**: React
- **Backend**: FastAPI
- **Databases**: Weaviate, PostgreSQL
- **AI and Data Processing Tools**: Various tools for implementing RAG and data management.

## Project Structure
```
ai-fact-checker
├── frontend
│   ├── src
│   ├── public
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
├── backend
│   ├── app
│   ├── requirements.txt
│   └── README.md
├── database
│   ├── migrations
│   ├── weaviate
│   └── README.md
└── README.md
```

## Setup Instructions
1. **Clone the Repository**: 
   ```
   git clone <repository-url>
   cd ai-fact-checker
   ```

2. **Frontend Setup**:
   - Navigate to the `frontend` directory.
   - Install dependencies:
     ```
     npm install
     ```
   - Start the development server:
     ```
     npm start
     ```

3. **Backend Setup**:
   - Navigate to the `backend` directory.
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Run the FastAPI application:
     ```
     uvicorn app.main:app --reload
     ```

4. **Database Setup**:
   - Initialize the PostgreSQL database using the SQL commands in `database/migrations/init.sql`.
   - Set up the Weaviate schema defined in `database/weaviate/schema.json`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
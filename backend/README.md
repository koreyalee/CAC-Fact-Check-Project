# AI Fact Checker Backend

This is the backend component of the AI Fact Checker web application. It is built using FastAPI and is responsible for handling requests related to claims, fact-checking, and generating summaries.

## Features

- **Claims Ingestion and Identification**: The backend can ingest content and identify claims for further analysis.
- **Fact-Checking Process**: Utilizes a Retrieval-Augmented Generation (RAG) pipeline to fact-check claims against a knowledge base.
- **Summary Generation**: Generates concise summaries of claims based on the analysis results.

## Technology Stack

- **FastAPI**: A modern web framework for building APIs with Python.
- **PostgreSQL**: A relational database for storing application data.
- **Weaviate**: A vector database for managing and retrieving data related to claims and fact-checking.

## Directory Structure

- **app**: Contains the main application code.
  - **main.py**: Entry point for the FastAPI application.
  - **routers**: Contains route handlers for claims, fact-checking, and summaries.
  - **services**: Contains business logic and interactions with databases.
  - **models**: Contains data models and schemas.
- **requirements.txt**: Lists the Python dependencies required for the backend.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ai-fact-checker/backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the FastAPI application:
   ```
   uvicorn app.main:app --reload
   ```

5. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is open-source and available under the MIT License.
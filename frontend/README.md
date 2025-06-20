# AI Fact Checker Frontend

This is the frontend part of the AI Fact Checker project, built using React and TypeScript. The application is designed to help users identify and verify claims made in various content, providing tools for interactive highlighting, narrative tracking, and summary generation.

## Features

- **Interactive Highlighting**: Users can highlight claims in the text to see their veracity.
- **Narrative Tracking**: Visualizes the spread of disinformation across different platforms.
- **Summary Generation**: Generates concise summaries of claims based on backend analysis.
- **Click-to-Verify**: Users can click on claims to verify their accuracy and view supporting evidence.
- **Advanced Analysis**: Provides detailed analysis of claims and their sources.
- **Open-Source Toolkit**: The project is open-source, allowing contributions and improvements from the community.

## Project Structure

- `src/components`: Contains reusable React components.
  - `HighlightingTool.tsx`: Component for interactive claim highlighting.
  - `NarrativeTracker.tsx`: Component for visualizing narrative flow.
  - `SummaryGenerator.tsx`: Component for generating summaries of claims.
  
- `src/pages`: Contains main application pages.
  - `Home.tsx`: Landing page with an overview of features.
  - `Analysis.tsx`: Page for inputting content for analysis.
  - `Verification.tsx`: Page displaying detailed verification results.

- `src/utils`: Contains utility functions for API calls.
  - `api.ts`: Functions for handling requests and responses to the backend.

- `App.tsx`: Main application component that sets up routing.

## Getting Started

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd ai-fact-checker/frontend
   ```

2. **Install dependencies**:
   ```
   npm install
   ```

3. **Run the application**:
   ```
   npm start
   ```

The application will be available at `http://localhost:3000`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
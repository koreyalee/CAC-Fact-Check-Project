# AI Fact Checker Database Documentation

This directory contains the necessary files and documentation for setting up and managing the database components of the AI Fact Checker project.

## Directory Structure

- **migrations/**: Contains SQL migration files for initializing and updating the PostgreSQL database schema.
  - **init.sql**: SQL commands to set up the initial database schema.

- **weaviate/**: Contains files related to the Weaviate vector database.
  - **schema.json**: Defines the schema for the Weaviate database, specifying the structure of the data to be stored.

## Database Setup

To set up the database for the AI Fact Checker project, follow these steps:

1. **PostgreSQL Setup**:
   - Ensure that PostgreSQL is installed and running on your machine.
   - Create a new database for the AI Fact Checker project.

2. **Run Migrations**:
   - Execute the SQL commands in `migrations/init.sql` to initialize the database schema.

3. **Weaviate Setup**:
   - Follow the Weaviate documentation to set up the Weaviate vector database.
   - Use the `weaviate/schema.json` file to configure the schema in your Weaviate instance.

## Usage

This database will be used to store claims, fact-checking results, and other relevant data for the AI Fact Checker application. Ensure that the database connections are properly configured in the backend application to interact with both PostgreSQL and Weaviate.

For further details on the database schema and usage, refer to the individual files within the migrations and weaviate directories.
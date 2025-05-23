Scrap Articles Application
Overview
The Scrap Articles application is a Python-based web scraping tool designed to extract, summarize, and store articles from various websites. It provides both CLI and API interfaces for interacting with the application, making it versatile for different use cases. The application is built using modern Python libraries and frameworks, ensuring scalability and maintainability.

Features
Web Scraping:
Scrapes articles from websites like quotes.toscrape.com, news.ycombinator.com, and other generic websites.
Extracts titles, authors, and content dynamically.
Summarization:
Summarizes scraped content using external APIs (e.g., Google Gemini API).
Database Integration:
Stores scraped articles in an SQLite database for persistence.
CLI Interface:
Provides commands for scraping, listing, summarizing, and deleting articles.
API Interface:
Exposes RESTful endpoints for interacting with the application programmatically.
Docker Support:
Fully containerized for consistent deployment across environments.
Tech Stack
Backend Framework: FastAPI
Web Scraping: BeautifulSoup, Requests
Database: SQLite (via SQLAlchemy ORM)
CLI: Click
Containerization: Docker, Docker Compose
Environment Management: Python-dotenv
Summarization API: Google Gemini API
Future Enhancements: LangChain, LangGraph, LangSmith, Pinecone for vector embeddings and QA agents.
Installation
1. Clone the Repository
2. Set Up the Environment
Using Virtual Environment:
Using Docker:
Configuration
The application uses a .env file for configuration. Create a .env file in the root directory with the following content:

Usage
1. CLI Commands
The application provides a set of CLI commands for interacting with the scraper and database.

Command	Description	Example
init-database	Initialize the database and create tables.	python cli.py init-database
scrape	Scrape articles from a given URL.	python cli.py scrape --url "https://quotes.toscrape.com" --limit 5
list-articles	List all stored articles.	python cli.py list-articles --limit 10
get-summary	Retrieve the summary of a specific article.	python cli.py get-summary --id 1
delete-article	Delete a single article by its ID.	python cli.py delete-article --id 1
delete-articles	Delete multiple articles by their IDs.	python cli.py delete-articles --ids 1 2 3
test-gemini	Test the connection to the Gemini API.	python cli.py test-gemini
2. API Endpoints
The application exposes RESTful endpoints for programmatic interaction.

Endpoint	Method	Description	Example
/api/v1/scrape-and-summarize	POST	Scrape and summarize articles from a URL.	curl -X POST -d '{"url": "https://quotes.toscrape.com", "limit": 5}'
/api/v1/articles	GET	List all stored articles.	curl -X GET "http://localhost:8000/api/v1/articles?skip=0&limit=10"
/api/v1/get-summary/{id}	GET	Retrieve the summary of a specific article.	curl -X GET "http://localhost:8000/api/v1/get-summary/1"
/api/v1/articles/{id}	DELETE	Delete a specific article by its ID.	curl -X DELETE "http://localhost:8000/api/v1/articles/1"
/health	GET	Check the health of the application.	curl -X GET "http://localhost:8000/health"
How to Run
1. Using CLI
Initialize the database:
Scrape articles:
List articles:
2. Using Docker
Build and run the application:
Access the API:
API Root: http://localhost:8000/
API Documentation: http://localhost:8000/docs
Future Enhancements
1. LangChain Integration
Goal: Use LangChain to create a Question-Answering (QA) agent that can answer questions based on the scraped articles.
Progress: Researching LangChain's document loaders and chain models for integration.
2. LangGraph
Goal: Build a graph-based representation of the scraped articles for better contextual understanding.
Progress: Exploring LangGraph's capabilities for knowledge graph generation.
3. LangSmith
Goal: Use LangSmith for debugging and monitoring the QA agent's performance.
Progress: Setting up LangSmith's observability tools.
4. Vector Embeddings with Pinecone
Goal: Store vector embeddings of articles in Pinecone for semantic search and retrieval.
Progress: Experimenting with embedding models and Pinecone's vector database.
Key Benefits of the Application
Versatility:

Use the CLI for quick local operations.
Use the API for programmatic interaction and integration with other systems.
Scalability:

Easily deployable using Docker for consistent environments.
Future-ready with planned integrations for advanced NLP and vector search.
Persistence:

Articles are stored in an SQLite database, ensuring data is not lost between sessions.
Extensibility:

The modular design allows for easy addition of new scraping logic or API endpoints.
Contributing
If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Let me know if you need further adjustments or additional sections!
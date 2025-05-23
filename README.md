# 📰 Scrap Articles

A Python-based web scraping tool designed to **extract**, **summarize**, and **store** articles from various websites. Scrap Articles provides both **CLI** and **RESTful API** interfaces, supporting flexible usage across different environments.

---

##  Features

| Feature             | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| Web Scraping        | Extracts titles, authors, and content from websites using BeautifulSoup.     |
| Summarization       | Summarizes content using the Google Gemini API.                             |
| Database Integration| Stores articles in SQLite via SQLAlchemy ORM.                               |
| CLI Interface       | Command-line access to all major functionalities using Click.               |
| API Interface       | FastAPI-powered REST endpoints for programmatic access.                     |
| Docker Support      | Containerized deployment using Docker and Docker Compose.                   |

---

##  Tech Stack

| Component          | Technology           |
|--------------------|----------------------|
| Backend Framework  | FastAPI              |
| Scraping Library   | BeautifulSoup, Requests |
| Database           | SQLite + SQLAlchemy  |
| CLI Tool           | Click                |
| Summarization API  | Google Gemini API    |
| Containerization   | Docker, Docker Compose |
| Env Management     | Python-dotenv        |

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/happyrao78/scrap-articles.git
cd scrap-articles
````

### 2. Set Up the Environment

#### Using Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Using Docker

```bash
docker-compose up --build
```

---

## ⚙️ Configuration

Create a `.env` file in the root directory with the following content or check out .env.example:

```env
DATABASE_URL=sqlite:///./articles.db
GEMINI_API_KEY=your_google_gemini_api_key
```

---

## 🖥 Usage

### 1. CLI Commands

| Command           | Description                      | Example                                                              |
| ----------------- | -------------------------------- | -------------------------------------------------------------------- |
| `init-database`   | Initialize the database          | `python cli.py init-database`                                        |
| `scrape`          | Scrape articles from a given URL | `python cli.py scrape --url "https://quotes.toscrape.com" --limit 5` |
| `list-articles`   | List all stored articles         | `python cli.py list-articles --limit 10`                             |
| `get-summary`     | Get the summary of an article    | `python cli.py get-summary --id 1`                                   |
| `delete-article`  | Delete a single article          | `python cli.py delete-article --id 1`                                |
| `delete-articles` | Delete multiple articles         | `python cli.py delete-articles --ids 1 2 3`                          |
| `test-gemini`     | Test Gemini API integration      | `python cli.py test-gemini`                                          |

### 2. API Endpoints

| Endpoint                       | Method | Description                       | Example                                                                                                                                                      |
| ------------------------------ | ------ | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/api/v1/scrape-and-summarize` | POST   | Scrape and summarize from a URL   | `curl -X POST -H "Content-Type: application/json" -d '{"url": "https://quotes.toscrape.com", "limit": 5}' http://localhost:8000/api/v1/scrape-and-summarize` |
| `/api/v1/articles`             | GET    | List all stored articles          | `curl -X GET http://localhost:8000/api/v1/articles?skip=0&limit=10`                                                                                          |
| `/api/v1/get-summary/{id}`     | GET    | Get summary of a specific article | `curl -X GET http://localhost:8000/api/v1/get-summary/1`                                                                                                     |
| `/api/v1/articles/{id}`        | DELETE | Delete an article by ID           | `curl -X DELETE http://localhost:8000/api/v1/articles/1`                                                                                                     |
| `/health`                      | GET    | Check application health          | `curl -X GET http://localhost:8000/health`                                                                                                                   |

---

##  How to Run

### Using CLI

```bash
python cli.py init-database
python cli.py scrape --url "https://quotes.toscrape.com" --limit 5
python cli.py list-articles
```

### Using Docker

```bash
docker-compose up --build
```

* API Root: `http://localhost:8000/`
* API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔮 Future Enhancements

| Feature       | Goal                                                     | Status            |
| ------------- | -------------------------------------------------------- | ----------------- |
| **LangChain** | Build QA agent for scraped articles                      | Research ongoing  |
| **LangGraph** | Graph-based contextual representation of articles        | Exploring options |
| **LangSmith** | Debugging and monitoring the QA agents                   | Tool integration  |
| **Pinecone**  | Store and retrieve vector embeddings for semantic search | In progress       |

---

##  Key Benefits

* **Versatile**: Use CLI locally or API for integrations.
* **Scalable**: Dockerized setup for consistent deployment.
* **Persistent**: SQLite ensures articles are stored across sessions.
* **Extensible**: Modular design supports feature additions.

---

For major features or bugs, [open an issue](https://github.com/happyrao78/scrap-articles/issues) first to discuss.



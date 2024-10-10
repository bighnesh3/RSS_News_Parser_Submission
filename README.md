# RSS Feed Parser and Categorizer

This application parses news articles from various RSS feeds, stores them in a MySQL database, and categorizes them into predefined categories based on their content.

## Features

- **RSS Feed Parsing:** Retrieves news articles from multiple RSS feeds.
- **Database Storage:** Stores article details such as title, content, published date, and source URL in a MySQL database.
- **Article Categorization:** Classifies articles into one of the following categories:
  - Terrorism / Protest / Political Unrest / Riot
  - Positive / Uplifting
  - Natural Disasters
  - Others
- **Logging:** Logs all important events and errors.

## Tech Stack

- **Programming Language:** Python
- **Libraries Used:**
  - `feedparser`: For parsing RSS feeds.
  - `SQLAlchemy`: For interacting with the MySQL database.
  - `Celery`: For task queue management (intended, but not fully implemented).
  - `pymysql`: MySQL connector for SQLAlchemy.
  - `logging`: For logging important events.
- **Database:** MySQL

## Requirements

The `requirements.txt` file lists all the Python libraries needed for the project. You can install them using:
```
pip install -r requirements.txt
```

## MySQL Setup

1. Create a MySQL database:
   - The SQL script for database setup is included in the `create_database.sql` file.
   - To set up the database, execute the SQL script in your MySQL instance.

2. Update your MySQL credentials in the `rss_parser.py` file:
   ```python
   DATABASE_URL = "mysql+pymysql://your_username:your_password@localhost/news_db"
   ```

## How to Run

1. Clone the repository:
   ```
   git clone <repository_url>
   ```

2. Set up the Python environment (if not already done):
   ```
   python -m venv venv
   source venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the Python script:
   ```
   python rss_parser.py
   ```

This will parse the RSS feeds, save articles to the MySQL database, and categorize them.

## Issues Faced with Redis/Celery Setup

While developing the application, there were challenges in setting up Redis and Celery due to environment issues related to the Virtual Machine Platform on Windows. Specifically, Docker could not be successfully configured despite multiple attempts to enable the necessary platform features.

Due to these issues, the task queue functionality (using Celery) for asynchronous article processing could not be fully implemented. This part of the project, intended to improve efficiency, remains incomplete.

As a result, this submission focuses on the core features of:
- Parsing RSS feeds.
- Storing articles in the MySQL database.
- Categorizing articles into predefined categories.

Future work could involve revisiting the Redis/Celery setup once the environment issues are resolved.

---

This structure clearly explains the project, how to set it up, run it, and the challenges faced with the Redis/Celery setup.

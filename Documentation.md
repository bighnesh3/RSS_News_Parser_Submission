### Problem Statement

The goal of thsi project is to build an application that collects news articles from various RSS feeds, stores them in a MySQL database, and categorizes them into predefined categories such as:
- Terrorism/Protest/Political Unrest/Riot
- Positive/Uplifting
- Natural Disasters
- Others

The program addresses the challenge of efficiently fetching news articles, storing them without duplicates, and categorizing the articles automatically.

---

### Approach

#### 1. **RSS Feed Parsing**
   - The program uses the `feedparser` library to fetch and parse RSS feeds. 
   - Feeds are provided in a list, and each feed is processed one by one. Each articles title, content, publication date, and link are extracted.
   - Error handling is included to ensure that netwokr issues or feed errors are logged but do not crash the program.

#### 2. **Database Design**
   - The data is stored in a MySQL database, with a table designed to store articles. The table schema includes fields like `title`, `content`, `published date`, `link` (which is unique), and `category`.
   - The SQLAlchemy ORM is used to define the table schema and handle the interaction between the Python application and the MySQL database.

#### 3. **Article Classification**
   - Articles are categorized based on keywords using a basic classification approach. Depending on the presence of specific keywords (e.g., "protest," "uplifting," "earthquake"), an article is assigned to one of the predefined categories.
   - A function (`classify_article`) is used to assign categories to each article.

#### 4. **Error Handling and Logging**
   - Logging is implemented to keep track of events like successful article processing, duplicate detection, and errors (e.g., issues in fetching feeds).
   - The program ensures that duplicate articles (articles with the same URL) are not stored multiple times in the database.

#### 5. **Celery and Redis Integration (Planned but Not Fully Implemented)**
   - The application is designed to use Celery for asynchronous task management and Redis as the message broker to handle large amounts of data and process each article independently.
   - Due to environment issues related to setting up Redis and Celery, this part could not be fully implemented, but the placeholder code is included for reference.
   - The logic is designed such that each article would be processed asynchronously to classify the content after it's saved in the database.

---

### Design Choices

#### 1. **Libraries and Tools**
   - **Feedparser**: Chosen for its simplicity and efficiency in parsing RSS feeds.
   - **SQLAlchemy**: Used to interact with the MySQL database using ORM, simplifying database operations.
   - **MySQL**: A relational database was chosen for structured storage and efficient querying of news articles.
   - **Celery and Redis**: While not fully implemented, these tools were chosen for their ability to handle asynchronous tasks efficiently.

---

### Next Steps and Further Improvements

If more time were available or the environment allowed, the following improvements would be made:
   - Complete the Celery and Redis integration to handle task processing asynchronously.
   - Implement more advanced NLP-based categorization techniques using libraries like spaCy or NLTK to improve the classification accuracy.

--- 

### How to Run the Application

#### Prerequisites
- Python 3.x
- MySQL installed
- Install the required Python packages via `requirements.txt`:
  ```
  pip install -r requirements.txt
  ```

#### Setup MySQL
- Run the SQL script `create_database.sql` to create the necessary database and tables.

#### Modify `rss_parser.py`
- Update the `DATABASE_URL` in the script to use your MySQL username and password:
  ```python
  DATABASE_URL = "mysql+pymysql://your_username:your_password@localhost/news_db"
  ```

#### Running the Script
- Simply run the script to start fetching and processing the RSS feeds:
  ```
  python rss_parser.py
  ```

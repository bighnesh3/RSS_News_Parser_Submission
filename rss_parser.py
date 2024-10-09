import feedparser
import logging
from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from celery import Celery

# Configure the Celery app using Redis
app = Celery('tasks', broker='redis://localhost:6379/0')

logging.basicConfig(filename='rss_app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# List of given RSS feeds
rss_feeds = [
    'http://rss.cnn.com/rss/cnn_topstories.rss',
    'http://qz.com/feed',
    'http://feeds.foxnews.com/foxnews/politics',
    'http://feeds.reuters.com/reuters/businessNews',
    'http://feeds.feedburner.com/NewshourWorld',
    'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
]

# Database setup
DATABASE_URL = "mysql+pymysql://bigh:bigh123@localhost/news_db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Define the Article model
class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    published = Column(DateTime)
    link = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=True)

# Create the articles table
Base.metadata.create_all(engine)

def parse_rss_feed(feed_url):
    """Parsing the RSS feed and returning a list of articles."""
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        # Convert published date to datetime object
        published_date = None
        if 'published' in entry:
            try:
                published_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z')
            except Exception as e:
                logging.error(f"Error parsing date for article: {entry.title}, Error: {e}")
                published_date = None
        
        article = {
            'title': entry.title,
            'content': entry.summary if 'summary' in entry else entry.description,
            'published': published_date,
            'link': entry.link
        }
        articles.append(article)
    return articles

def fetch_all_feeds(feed_urls):
    """Fetching and parsing multiple RSS feeds."""
    all_articles = []
    for url in feed_urls:
        try:
            articles = parse_rss_feed(url)
            all_articles.extend(articles)
            logging.info(f"Fetched {len(articles)} articles from {url}")
        except Exception as e:
            logging.error(f"Failed to parse feed {url}: {e}")
    return all_articles

def save_article(session, article_data):
    """Saving article to the database if not a duplicate."""
    existing_article = session.query(Article).filter_by(link=article_data['link']).first()
    if not existing_article:
        new_article = Article(
            title=article_data['title'],
            content=article_data['content'],
            published=article_data['published'],
            link=article_data['link'],
            category=None  # Initially no category
        )
        try:
            session.add(new_article)
            session.commit()
            logging.info(f"Saved article: {article_data['title']}")
        except Exception as e:
            logging.error(f"Error saving article: {article_data['title']}, Error: {e}")
            session.rollback()
    else:
        logging.info(f"Duplicate article found: {article_data['title']}")

@app.task
def process_article(article_id):
    """Processing and classifying article content."""
    article = session.query(Article).filter_by(id=article_id).first()
    if article:
        # Call the classification function
        category = classify_article(article.content)
        article.category = category
        session.commit()

def classify_article(content):
    """Classifying the article content into predefined categories."""
    content = content.lower()
    if any(word in content for word in ['terrorism', 'protest', 'riot', 'political unrest']):
        return 'Terrorism/Protest/Political Unrest/Riot'
    elif any(word in content for word in ['uplifting', 'inspiring', 'positive']):
        return 'Positive/Uplifting'
    elif any(word in content for word in ['earthquake', 'flood', 'hurricane', 'natural disaster']):
        return 'Natural Disasters'
    else:
        return 'Others'

def process_all_articles():
    """Fetching articles, saving to DB, and classifying them using Celery."""
    articles = fetch_all_feeds(rss_feeds)
    for article_data in articles:
        save_article(session, article_data)

        # Retrieve the saved article ID
        saved_article = session.query(Article).filter_by(link=article_data['link']).first()
        # Send the article to Celery for processing
        process_article.delay(saved_article.id)

if __name__ == "__main__":
    process_all_articles()

import requests
from bs4 import BeautifulSoup
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from gtts import gTTS
import os
import platform

# Download required NLTK data files (if not already available).
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

def get_bing_news_articles(company_name, num_articles=10):
    """
    Scrapes Bing News search results for a given company name.
    Returns a list of articles with metadata: title, summary, URL, and source.
    """
    query = company_name.replace(" ", "+")
    url = f"https://www.bing.com/news/search?q={query}&FORM=HDRSC6"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    news_cards = soup.find_all("div", class_="news-card")
    for card in news_cards:
        title_tag = card.find("a", class_="title")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        article_url = title_tag.get("href")
        snippet_tag = card.find("div", class_="snippet")
        snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
        source_tag = card.find("div", class_="source")
        source = source_tag.get_text(strip=True) if source_tag else ""
        articles.append({
            "title": title,
            "summary": snippet,
            "url": article_url,
            "source": source
        })
        if len(articles) >= num_articles:
            break
    return articles

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text using NLTK's VADER.
    Returns:
        sentiment (str): "Positive", "Negative", or "Neutral"
        scores (dict): The full set of polarity scores.
    """
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return sentiment, scores

def extract_topics(text):
    """
    Extracts topics from the input text using basic noun extraction.
    Tokenizes the text, removes stopwords and punctuation, and returns a list of unique nouns.
    """
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    filtered = [word for word in tokens if word.isalpha() and word not in stop_words]
    tagged = nltk.pos_tag(filtered)
    nouns = [word for word, pos in tagged if pos in ["NN", "NNS", "NNP", "NNPS"]]
    return list(set(nouns))

def comparative_analysis(articles):
    """
    Performs comparative analysis across articles.
    Returns a dictionary with:
      - Sentiment Distribution: Count of articles per sentiment.
      - Coverage Differences: Insights based on keyword presence.
      - Topic Overlap: Common topics and unique topics per article.
    """
    sentiment_distribution = {"Positive": 0, "Negative": 0, "Neutral": 0}
    sales_keywords = {"sales", "growth", "record", "profit"}
    regulatory_keywords = {"regulation", "regulatory", "scrutiny", "lawsuit", "legal", "compliance"}
    sales_count = 0
    reg_count = 0
    all_topics = []
    for article in articles:
        sentiment = article.get("sentiment", "Neutral")
        sentiment_distribution[sentiment] += 1
        combined_text = f"{article['title']} {article['summary']}".lower()
        if any(keyword in combined_text for keyword in sales_keywords):
            sales_count += 1
        if any(keyword in combined_text for keyword in regulatory_keywords):
            reg_count += 1
        topics = extract_topics(combined_text)
        article["topics"] = topics
        all_topics.extend(topics)
    if sales_count > reg_count:
        coverage_insight = (f"More articles ({sales_count}) emphasize sales and financial growth compared to regulatory concerns ({reg_count}).")
    elif reg_count > sales_count:
        coverage_insight = (f"More articles ({reg_count}) focus on regulatory or legal challenges compared to sales aspects ({sales_count}).")
    else:
        coverage_insight = (f"An equal number of articles emphasize sales/growth and regulatory issues ({sales_count} each).")
    topic_counter = Counter(all_topics)
    common_topics = [topic for topic, count in topic_counter.items() if count > 1]
    unique_topics = {}
    for i, article in enumerate(articles, start=1):
        unique = [topic for topic in article.get("topics", []) if topic_counter[topic] == 1]
        unique_topics[f"Article {i}"] = unique
    analysis = {
        "Sentiment Distribution": sentiment_distribution,
        "Coverage Differences": coverage_insight,
        "Topic Overlap": {
            "Common Topics": common_topics,
            "Unique Topics": unique_topics
        }
    }
    return analysis

def convert_text_to_hindi_tts(text, output_file="output.mp3"):
    """
    Converts the input text into Hindi speech using gTTS and saves it as an MP3 file.
    """
    tts = gTTS(text=text, lang='hi', slow=False)
    tts.save(output_file)
    return output_file

def play_audio(file_path):
    """
    Plays an audio file using the system's default media player.
    """
    if platform.system() == "Windows":
        os.startfile(file_path)
    elif platform.system() == "Darwin":
        os.system(f"open {file_path}")
    else:
        os.system(f"mpg123 {file_path}")

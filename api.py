from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import time
from utils import (
    get_bing_news_articles,
    analyze_sentiment,
    extract_topics,
    comparative_analysis,
    convert_text_to_hindi_tts,
)

app = FastAPI(title="News Summarization & TTS API")

@app.get("/news")
def get_news(company: str, num_articles: int = 10):
    articles = get_bing_news_articles(company, num_articles=num_articles)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found.")
    for article in articles:
        combined_text = article["title"]
        if article["summary"]:
            combined_text += ". " + article["summary"]
        sentiment, scores = analyze_sentiment(combined_text)
        article["sentiment"] = sentiment
        article["sentiment_scores"] = scores
        article["topics"] = extract_topics(combined_text)
        time.sleep(0.5)
    analysis = comparative_analysis(articles)
    return {"articles": articles, "analysis": analysis}

@app.get("/tts")
def get_tts(text: str):
    output_file = "output.mp3"
    convert_text_to_hindi_tts(text, output_file=output_file)
    return FileResponse(output_file, media_type="audio/mpeg", filename=output_file)

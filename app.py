import streamlit as st
import time
from utils import (
    get_bing_news_articles,
    analyze_sentiment,
    extract_topics,
    comparative_analysis,
    convert_text_to_hindi_tts,
)
from collections import Counter
from googletrans import Translator

# Initialize the translator.
translator = Translator()

st.title("News Summarization & Sentiment Analysis with Automatic Hindi Translation & TTS")
st.write("Enter a company name to fetch news articles, analyze sentiment, and generate a final summary automatically converted to Hindi.")

company = st.text_input("Company Name", "Tesla")

if st.button("Generate Report"):
    with st.spinner("Fetching news articles..."):
        articles = get_bing_news_articles(company, num_articles=10)
    
    if not articles:
        st.error("No articles found or there was an error fetching the articles.")
    else:
        # Process each article: perform sentiment analysis.
        for article in articles:
            combined_text = article["title"]
            if article["summary"]:
                combined_text += ". " + article["summary"]
            sentiment, scores = analyze_sentiment(combined_text)
            article["sentiment"] = sentiment
            article["sentiment_scores"] = scores
            # Topics are extracted for internal analysis but not used in the final summary.
            article["topics"] = extract_topics(combined_text)
            time.sleep(0.5)
        
        # Display extracted articles.
        st.subheader("Extracted Articles")
        for idx, article in enumerate(articles, start=1):
            st.markdown(f"**Article {idx}:**")
            st.write("Title:", article["title"])
            st.write("Summary:", article["summary"])
            st.write("Source:", article["source"])
            st.write("URL:", article["url"])
            st.write("Sentiment:", article["sentiment"])
            st.markdown("---")
        
        # Perform comparative analysis for internal metrics.
        analysis = comparative_analysis(articles)
        st.subheader("Comparative Analysis")
        st.write("**Sentiment Distribution:**", analysis["Sentiment Distribution"])
        st.write("**Coverage Differences:**", analysis["Coverage Differences"])
        
        # Create a final summary report in English.
        total_articles = len(articles)
        dist = analysis["Sentiment Distribution"]
        final_summary_en = (
            f"Out of a total of {total_articles} articles, {dist.get('Positive', 0)} articles are positive, "
            f"{dist.get('Negative', 0)} are negative, and {dist.get('Neutral', 0)} are neutral. "
            "Many articles emphasize sales growth and financial development, while some discuss regulatory challenges and legal issues. "
            "Overall, the news coverage of the company is predominantly positive, suggesting potential market growth."
        )
        
        # Automatically translate the final summary to Hindi.
        translation = translator.translate(final_summary_en, dest='hi')
        final_summary_hi = translation.text
        
        st.subheader("Final Summary Report (Hindi)")
        st.markdown(final_summary_hi)
        
        # Convert the Hindi summary into speech.
        with st.spinner("Generating Hindi TTS audio..."):
            audio_file = convert_text_to_hindi_tts(final_summary_hi, output_file="summary_hi.mp3")
        
        st.success("Audio summary generated!")
        st.audio(audio_file)

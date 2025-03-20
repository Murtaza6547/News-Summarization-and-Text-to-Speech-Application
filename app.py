import nltk
nltk.download('punkt')
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

st.title("News Summarization & Sentiment Analysis with Hindi TTS")
st.write("Enter a company name to fetch news articles, analyze sentiment, and generate a Hindi summary.")

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
            # Topics are still extracted but not used in the final summary.
            article["topics"] = extract_topics(combined_text)
            time.sleep(0.5)
        
        # Display individual article details.
        st.subheader("Extracted Articles")
        for idx, article in enumerate(articles, start=1):
            st.markdown(f"**Article {idx}:**")
            st.write("Title:", article["title"])
            st.write("Summary:", article["summary"])
            st.write("Source:", article["source"])
            st.write("URL:", article["url"])
            st.write("Sentiment:", article["sentiment"])
            st.markdown("---")
        
        # Perform comparative analysis for internal metrics (sentiment distribution, coverage insights)
        analysis = comparative_analysis(articles)
        st.subheader("Comparative Analysis")
        st.write("**Sentiment Distribution:**", analysis["Sentiment Distribution"])
        st.write("**Coverage Differences:**", analysis["Coverage Differences"])
        
        # Create a final Hindi summary report that aggregates all the articles.
        total_articles = len(articles)
        dist = analysis["Sentiment Distribution"]
        final_summary = (
            f"कुल {total_articles} लेखों में से, {dist.get('Positive', 0)} लेख सकारात्मक, "
            f"{dist.get('Negative', 0)} लेख नकारात्मक, और {dist.get('Neutral', 0)} लेख तटस्थ हैं।\n"
            "कई लेखों में विक्रय में वृद्धि और आर्थिक विकास पर जोर दिया गया है, जबकि कुछ लेखों में नियामकीय चुनौतियाँ और कानूनी मुद्दों पर चर्चा की गई है।\n"
            "संपूर्ण रूप से, यह रिपोर्ट दर्शाती है कि कंपनी का समाचार कवरेज मुख्य रूप से सकारात्मक है, "
            "जो संभावित आर्थिक विकास के संकेत देता है।"
        )
        
        st.subheader("Final Summary Report")
        st.markdown(final_summary)
        
        # Convert the final summary into Hindi speech.
        with st.spinner("Generating Hindi TTS audio..."):
            audio_file = convert_text_to_hindi_tts(final_summary, output_file="tesla_summary_hi.mp3")
        
        st.success("Audio summary generated!")
        st.audio(audio_file)

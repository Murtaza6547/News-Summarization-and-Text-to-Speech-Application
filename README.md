# README

## Sentiment Analysis Dashboard

This project implements a sentiment analysis dashboard that processes news articles about a selected company, summarizes the content, determines sentiment (positive, negative, or neutral), and provides a Hindi summary with text-to-speech (TTS) output. The application is built using Streamlit and deployed on Hugging Face Spaces.

---

## Features

1. **News Extraction:**
   - Fetches the latest news articles related to the selected company using web scraping.
   - Extracts the article title, content, and metadata.

2. **Summarization:**
   - Summarizes each article to a concise text using the Hugging Face Transformer model.

3. **Sentiment Analysis:**
   - Analyzes the sentiment of the summarized content (positive, negative, or neutral).

4. **Text-to-Speech (TTS):**
   - Converts the summarized Hindi text into speech using the `gTTS` library.

5. **Interactive Dashboard:**
   - Provides a user-friendly interface using Streamlit for input and output visualization.

6. **Customization:**
   - Allows users to select companies from a dropdown and adjust sentiment thresholds.

7. **Deployment:**
   - Hosted on Hugging Face Spaces for accessibility and testing.

---

## Dependencies

Below are the required Python libraries:

- **Main Libraries:**
  - `streamlit`
  - `streamlit-lottie`
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  - `nltk`
  - `transformers`
  - `gTTS`

---

## File Structure

```
project/
├── app.py            # Main script
├── utils.py          # Utility functions
├── api.py            # Development
├── requirements.txt  # Required Python libraries
├── README.md         # Documentation
└── assets/           # Folder for Lottie animations or additional assets
```
---

## Acknowledgments

- **Streamlit:** For providing an easy-to-use Python framework for building dashboards.
- **Hugging Face:** For the Transformer models used in summarization.
- **NLTK:** For text processing and tokenization.
- **gTTS:** For enabling text-to-speech functionality in Hindi.


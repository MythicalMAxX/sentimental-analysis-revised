import json
import os

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from flask import Flask, jsonify, request, send_file, send_from_directory
from random import choice
from bs4 import BeautifulSoup
import requests

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class WebScraper:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.4; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/115.0",
        ]

    def scrape_data(self, url):
        headers = {"User-Agent": choice(self.user_agents)}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        content = ""
        for paragraph in paragraphs:
            content += paragraph.text
        return content

    def process_data(self, content):
        splitter = CharacterTextSplitter()
        texts = splitter.split_text(content)
        return texts

    def analyze_sentiment(self, texts):
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = []
        for text in texts:
            score = sia.polarity_scores(text)
            sentiment_scores.append(score)
        return sentiment_scores



os.environ["GOOGLE_API_KEY"] = "TODO"; 

app = Flask(__name__)


@app.route("/")
def index():
    return send_file('web/index.html')


@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        if os.environ["GOOGLE_API_KEY"] == 'TODO':
            return jsonify({ "error": '''
                To get started, get an API key at
                https://g.co/ai/idxGetGeminiKey and enter it in
                main.py
                '''.replace('\n', '') })
        try:
            req_body = request.get_json()
            content = req_body.get("contents")
            model = ChatGoogleGenerativeAI(model=req_body.get("model"))
            message = HumanMessage(
                content=content
            )
            response = model.stream([message])
            def stream():
                for chunk in response:
                    yield 'data: %s\n\n' % json.dumps({ "text": chunk.content })

            return stream(), {'Content-Type': 'text/event-stream'}

        except Exception as e:
            return jsonify({ "error": str(e) })


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)


if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))

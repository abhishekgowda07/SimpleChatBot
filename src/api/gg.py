from flask import Flask, request, jsonify
from contextlib import nullcontext
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.probability import FreqDist
from nltk import ne_chunk

# Set up the lemmatizer
lemmatizer = WordNetLemmatizer()

# Define some sample user queries
user_queries = [
    "Hello",
    "What is your name?",
    "How are you?",
    "What are your hobbies?",
    "Where are you from?",
    "Goodbye",
    "thank you"
]

# Define the chatbot's responses
bot_responses = [
    "Hello there, How can I help you today?",
    "My name is ChatBot.",
    "I'm doing well, thank you!",
    "I enjoy helping people.",
    "I am an AI chatbot, so I don't have a physical location.",
    "Goodbye! It was nice chatting with you.",
    "Your most welcome!!"
]

preprocessed_queries = []


def scrape_website(url, user_input):
    response = requests.get(url)
    html_content = response.text
    if response.status_code == 200:
        soup = BeautifulSoup(html_content, 'html.parser')
        target_text = user_input
        paragraphs = soup.find_all("p")
        for paragraph in paragraphs:
            if target_text.lower() in paragraph.get_text().lower():
                # print(paragraph.get_text())
                break
    else:
        return None

    return paragraph.get_text()


for query in user_queries:
    tokens = nltk.word_tokenize(query.lower())
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    preprocessed_queries.append(' '.join(lemmatized_tokens))

# Create the TF-IDF vectorizer and compute the document-term matrix
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(preprocessed_queries)


while True:
    user_input = input()
    similarity_threshold = 0.4

    preprocessed_input = lemmatizer.lemmatize(user_input.lower())

    # Calculate the cosine similarity between the input and each query
    input_vector = vectorizer.transform([preprocessed_input])
    similarities = cosine_similarity(input_vector, X)

    # Find the most similar query
    most_similar_index = np.argmax(similarities)

    most_similar_index = np.argmax(similarities)
    highest_similarity_score = similarities[0][most_similar_index]

    if highest_similarity_score < similarity_threshold:
        # No match found, trigger the fallback mechanism
        information = scrape_website("https://en.wikipedia.org/wiki/{0}".format(user_input), user_input)
        if information is not None:
            # Process the retrieved information
            response = information
        else:
            # print(highest_similarity_score)
            response = "I'm sorry, I couldn't find any relevant information."
    else:
        response = bot_responses[most_similar_index]

    # Check if user wants to end the conversation
    if preprocessed_input == "goodbye":
        print("bye")
        break

    print(response)


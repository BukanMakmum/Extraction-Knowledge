import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import mysql.connector

nltk.download('punkt')
nltk.download('stopwords')

def process_text(text):
    # Tokenization
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    
    # Stopword Removal
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.casefold() not in stop_words]
    
    # Stemming
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    
    processed_text = ' '.join(words)
    return processed_text

def save_to_database(text, processed_text, category):
    conn = mysql.connector.connect(
            host="localhost",
            user="imam",
            password="Aceh2033",
            database="project_uas"
    )
    cursor = conn.cursor()
    query = "INSERT INTO knowledge (text, processed_text, category) VALUES (%s, %s, %s)"
    values = (text, processed_text, category)
    cursor.execute(query, values)
    conn.commit()
    conn.close()

def get_category(processed_text):
    # Category classification logic here
    # Example: classify the text into "technology" category if it contains the word "technology"
    if 'technology' in processed_text:
        return 'Technology'
    else:
        return 'Other'

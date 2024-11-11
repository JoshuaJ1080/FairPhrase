import subprocess
import sys

# This code is to ensure that the required sentence-transformers python libararies are installed
# If the libraries are not installed, theyll be installed by this snippet of code
 
def install_sentence_transformers():
    try:
        import sentence_transformers
    except ImportError:
        subprocess.call(['pip', 'install', 'sentence-transformers'])

install_sentence_transformers()

# This code is to ensure that the required pandas python libararies are installed
# If the libraries are not installed, theyll be installed by this snippet of code

def install_pandas():
    try:
        import pandas
    except ImportError:
        subprocess.call(['pip', 'install', 'pandas'])

install_pandas()

# This code is to ensure that the required scipy python libararies are installed
# If the libraries are not installed, theyll be installed by this snippet of code

def install_scipy():
    try:
        import scipy
    except ImportError:
        subprocess.call(['pip', 'install', 'scipy'])

install_scipy()

# This code is to ensure that the required TextBlob python libraries are installed
# If the libraries are not installed, they'll be installed by this snippet of code

def install_textblob():
    try:
        import textblob
    except ImportError:
        subprocess.call(['pip', 'install', 'textblob'])

install_textblob()

# Main Program

import pandas as pd
import re
from textblob import TextBlob
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
 
# Load keywords from CSV
def load_keywords(csv_file):
    df = pd.read_csv(csv_file)
    keyword_mapping = {}
    for _, row in df.iterrows():
        for gender in ['Neutral', 'Male', 'Female']:
            if pd.notna(row[gender]):
                keyword_mapping[row[gender].lower()] = {
                    'Male': row['Male'].lower() if pd.notna(row['Male']) else row['Neutral'].lower(),
                    'Female': row['Female'].lower() if pd.notna(row['Female']) else row['Neutral'].lower(),
                    'Neutral': row['Neutral'].lower()
                }
    return keyword_mapping

# Pronoun mapping
pronoun_mapping = {
    'he': {'Male': 'he', 'Female': 'she', 'Neutral': 'they'},
    'him': {'Male': 'him', 'Female': 'her', 'Neutral': 'them'},
    'his': {'Male': 'his', 'Female': 'her', 'Neutral': 'their'},
    'himself': {'Male': 'himself', 'Female': 'herself', 'Neutral': 'themselves'}
}

# Preprocess the sentence: Lowercase and extract words
def preprocess_text(paragraph):
    # Split the paragraph into sentences using regex
    sentences = re.split(r'(?<=[.!?]) +', paragraph)
    words = [re.findall(r'\b\w+\b', sentence) for sentence in sentences]
    return sentences, words

# Replace keywords based on target gender
def replace_gender_words(words, keyword_mapping, target_gender):
    replaced_words = []
    for sentence in words:
        sentence_replaced = []
        for word in sentence:
            lower_word = word.lower()
            if lower_word in keyword_mapping:
                target_word = keyword_mapping[lower_word][target_gender]
                sentence_replaced.append(target_word.capitalize() if word[0].isupper() else target_word)
            elif lower_word in pronoun_mapping:
                target_word = pronoun_mapping[lower_word][target_gender]
                sentence_replaced.append(target_word.capitalize() if word[0].isupper() else target_word)
            else:
                sentence_replaced.append(word)
        replaced_words.append(sentence_replaced)
    return replaced_words

# Grammar correction using TextBlob
def correct_grammar_with_textblob(modified_text):
    blob = TextBlob(modified_text)
    corrected_text = str(blob.correct())
    return corrected_text

# VInitialize the SentenceTransformer model globally
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Main function
def change_gender(paragraph, csv_file, target_gender):
    keyword_mapping = load_keywords(csv_file)
    sentences, words = preprocess_text(paragraph)
    replaced_words = replace_gender_words(words, keyword_mapping, target_gender)

    new_sentences = [' '.join(sentence) for sentence in replaced_words]
    new_paragraph = '. '.join(new_sentences) + '.'

    corrected_paragraph = correct_grammar_with_textblob(new_paragraph)
    return corrected_paragraph

# This function will be called from app.py
def process_text(paragraph, csv_file, target_gender):
    return change_gender(paragraph, csv_file, target_gender)
import subprocess
import sys
 
# This code is to ensure that the required pandas python libararies are installed
# If the libraries are not installed, theyll be installed by this snippet of code

def install_pandas(): 
    try:
        import pandas
    except ImportError: 
        subprocess.call(['pip', 'install', 'pandas'])

install_pandas()

# This code is to ensure that the required re python libararies are installed
# If the libraries are not installed, theyll be installed by this snippet of code

def install_re():
    try:
        import re
    except ImportError:
        subprocess.call(['pip', 'install', 'regex'])

install_re()

# This code is to ensure that the required collections python libararies are installed
# If the libraries are not installed, theyll be installed by this snippet of code

def install_collections():
    try:
        import collections
    except ImportError:
        subprocess.call(['pip', 'install', 'collections'])

install_collections()

# Main Program

import pandas as pd
import re
from collections import Counter

def load_keywords(csv_file):
    df = pd.read_csv(csv_file)
    keywords = {
        'Neutral': set(df['Neutral'].dropna().str.lower()),
        'Male': set(df['Male'].dropna().str.lower()),
        'Female': set(df['Female'].dropna().str.lower())
    }
    return keywords

def preprocess_text(paragraph):
    return re.findall(r'\b[\w\'-]+\b', paragraph.lower())

def count_gender_keywords(words, keywords):
    gender_counts = Counter()
    for word in words:
        for gender, gender_keywords in keywords.items():
            if word in gender_keywords:
                gender_counts[gender] += 1
    return gender_counts

def calculate_percentages(gender_counts):
    total = sum(gender_counts.values())
    percentages = {
        'Male': round((gender_counts.get('Male', 0) / total) * 100, 2) if total > 0 else 0.00,
        'Female': round((gender_counts.get('Female', 0) / total) * 100, 2) if total > 0 else 0.00,
        'Neutral': round((gender_counts.get('Neutral', 0) / total) * 100, 2) if total > 0 else 0.00
    }
    return percentages

def analyze_gender(paragraph, csv_file):
    keywords = load_keywords(csv_file)
    words = preprocess_text(paragraph)
    gender_counts = count_gender_keywords(words, keywords)
    return calculate_percentages(gender_counts)  # Return only percentages

# End of Detection Program
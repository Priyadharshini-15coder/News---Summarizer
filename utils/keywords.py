import re
from collections import Counter
from nltk.corpus import stopwords

# Load stopwords
stop_words = set(stopwords.words('english'))

def extract_keywords(text, n=10):
    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Split words
    words = text.split()

    # Remove stopwords + short words
    filtered_words = [
        word for word in words
        if word not in stop_words and len(word) > 3
    ]

    # Count frequency
    common = Counter(filtered_words).most_common(n)

    return common